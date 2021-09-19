from functools import reduce
from typing import Dict, List, Optional, cast

from beanie import PydanticObjectId
from beanie.operators import NE, And, Eq, In, Or, RegEx
from fastapi import Depends
from fastapi_restful.cbv import cbv
from fastapi_restful.inferring_router import InferringRouter

from ....database import (
    PathologicalEmbeddedEntity,
    PathologicalEntity,
    PatientEntity,
    SymptomEntity,
    UserEntity,
)
from ....exceptions.bad_request import BadRequest
from ....exceptions.not_found import NotFound
from ....services.province_service import ProvinceService
from ....utils.bad_request_response import bad_request_response
from ....utils.not_found_response import not_found_response
from ..auth import get_current_active_user
from ..schemas import (
    DischargeOfPositiveCasesOfCovid19Schema,
    PathologicalSchema,
    PatientGetDetailSchema,
    PatientGetSchema,
    PatientPostSchema,
    PatientPutSchema,
)

router = InferringRouter(tags=["Patients"])


@cbv(router)
class PatientsController:
    current_user: UserEntity = Depends(get_current_active_user)
    province_service: ProvinceService = Depends()

    @router.get("/patients/search/{query}")
    async def get_patients(self, query: str) -> List[PatientGetSchema]:
        words = query.strip().lower().split(" ")
        ors = reduce(
            lambda acc, item: Or(acc, item),
            map(
                lambda x: Or(
                    Or(
                        RegEx(PatientEntity.firstname, x, options="i"),
                        RegEx(PatientEntity.lastname, x, options="i"),
                    ),
                    RegEx(PatientEntity.ci, x, options="i"),
                ),
                words,
            ),
        )
        result = await PatientEntity.find(ors).to_list()
        pathologicals = await PathologicalEntity.find_all().to_list()
        return [
            await self._get_patient_schema(
                item,
                cache_pathologicals=pathologicals,
            )
            for item in result
        ]

    @router.get("/patients/{patientId}", responses={404: not_found_response})
    async def get_patient(self, patientId: PydanticObjectId) -> PatientGetDetailSchema:
        patient = await PatientEntity.get_or_404(patientId)
        return await self._get_patient_detail_schema(patient)

    @router.post(
        "/patients",
        responses={
            400: bad_request_response,
            404: not_found_response,
        },
    )
    async def post_patient(self, schema: PatientPostSchema) -> PatientGetSchema:
        old_patient = await PatientEntity.find_one(PatientEntity.ci == schema.ci)
        if old_patient:
            raise BadRequest("Already exists a patient with same CI")
        if not self.province_service.get_municipality(schema.municipality_code):
            raise NotFound("Municipality")
        pathologicals = await self._get_pathologicals_entities_from_schemas(
            schema.family_pathological_history + schema.personal_pathological_history
        )
        patient = PatientEntity(
            **schema.dict(
                exclude={"personal_pathological_history", "family_pathological_history"}
            ),
            personal_pathological_history=[
                PathologicalEmbeddedEntity(
                    pathological=pathologicals[p.name.lower()].id,
                    treatments=p.treatments,
                )
                for p in schema.personal_pathological_history
            ],
            family_pathological_history=[
                PathologicalEmbeddedEntity(
                    pathological=pathologicals[p.name.lower()].id,
                    treatments=p.treatments,
                )
                for p in schema.family_pathological_history
            ],
        )
        await patient.save()
        return await self._get_patient_schema(
            patient,
            cache_pathologicals=list(pathologicals.values()),
        )

    @router.put(
        "/patients/{patientId}",
        responses={
            400: bad_request_response,
            404: not_found_response,
        },
    )
    async def put_patient(
        self,
        patientId: PydanticObjectId,
        schema: PatientPutSchema,
    ) -> PatientGetDetailSchema:
        actual_patient = await PatientEntity.get_or_404(patientId)
        old_patient = await PatientEntity.find_one(
            And(Eq(PatientEntity.ci, schema.ci), NE(PatientEntity.id, patientId))
        )
        if old_patient:
            raise BadRequest("Already exists a patient with same CI")
        municipality_code = (
            schema.municipality_code
            if schema.municipality_code
            else actual_patient.municipality_code
        )
        if not self.province_service.get_municipality(municipality_code):
            raise NotFound("Municipality")
        pathologicals: Optional[Dict[str, PathologicalEntity]] = None
        if (
            schema.personal_pathological_history is not None
            or schema.family_pathological_history is not None
        ):
            pathologicals = await self._get_pathologicals_entities_from_schemas(
                (
                    schema.personal_pathological_history
                    if schema.personal_pathological_history
                    else []
                )
                + (
                    schema.family_pathological_history
                    if schema.family_pathological_history
                    else []
                )
            )
            if schema.personal_pathological_history is not None:
                actual_patient.personal_pathological_history = [
                    PathologicalEmbeddedEntity(
                        pathological=pathologicals[p.name].id,
                        treatments=p.treatments,
                    )
                    for p in schema.personal_pathological_history
                ]
            if schema.family_pathological_history is not None:
                actual_patient.family_pathological_history = [
                    PathologicalEmbeddedEntity(
                        pathological=pathologicals[p.name].id,
                        treatments=p.treatments,
                    )
                    for p in schema.family_pathological_history
                ]
        updated_patient = actual_patient.copy(
            update=schema.dict(
                exclude_unset=True,
                exclude={
                    "personal_pathological_history",
                    "family_pathological_history",
                },
            ),
        )
        await updated_patient.save()
        return await self._get_patient_detail_schema(
            updated_patient,
            cache_pathologicals=list(pathologicals.values()) if pathologicals else None,
        )

    @router.put(
        "/patients/{patientId}/egreso",
        responses={
            400: bad_request_response,
            404: not_found_response,
        },
    )
    async def put_patient_egreso(
        self,
        patientId: PydanticObjectId,
        schema: DischargeOfPositiveCasesOfCovid19Schema,
    ) -> PatientGetDetailSchema:
        actual_patient = await PatientEntity.get_or_404(patientId)
        if schema.symptoms is not None:
            symptoms = await self._get_symptoms_entities_from_schemas(schema.symptoms)
            actual_patient.discharge_of_positive_cases_of_covid_19.symptoms = [
                cast(PydanticObjectId, symptoms[s.lower()].id)
                for s in schema.symptoms
                if s in symptoms
            ]
        actual_patient.discharge_of_positive_cases_of_covid_19 = (
            actual_patient.discharge_of_positive_cases_of_covid_19.copy(
                update=schema.dict(
                    exclude_unset=True,
                    exclude={"symptoms"},
                )
            )
        )
        await actual_patient.save()
        return await self._get_patient_detail_schema(actual_patient)

    async def _get_patient_schema(
        self,
        patient: PatientEntity,
        cache_pathologicals: Optional[List[PathologicalEntity]] = None,
    ) -> PatientGetSchema:
        municipality = self.province_service.get_municipality(patient.municipality_code)
        if not municipality:
            raise NotFound("Municipality")
        pathologicals = (
            cache_pathologicals
            if cache_pathologicals
            else await PathologicalEntity.find_all().to_list()
        )
        pathologicals_dict = {item.id: item.name for item in pathologicals}
        return PatientGetSchema(
            **patient.dict(
                exclude={
                    "personal_pathological_history",
                    "family_pathological_history",
                    "discharge_of_positive_cases_of_covid_19",
                }
            ),
            municipality=municipality.name,
            province=municipality.province.name,
            personal_pathological_history=[
                PathologicalSchema(
                    name=pathologicals_dict[p.pathological],
                    treatments=p.treatments,
                )
                for p in patient.personal_pathological_history
            ],
            family_pathological_history=[
                PathologicalSchema(
                    name=pathologicals_dict[p.pathological],
                    treatments=p.treatments,
                )
                for p in patient.family_pathological_history
            ],
        )

    async def _get_patient_detail_schema(
        self,
        patient: PatientEntity,
        cache_pathologicals: Optional[List[PathologicalEntity]] = None,
    ) -> PatientGetDetailSchema:
        schema = await self._get_patient_schema(
            patient,
            cache_pathologicals,
        )
        symptoms = await SymptomEntity.find_all().to_list()
        symptoms_dict = {item.id: item.name for item in symptoms}
        return PatientGetDetailSchema(
            **schema.dict(),
            discharge_of_positive_cases_of_covid_19=DischargeOfPositiveCasesOfCovid19Schema(  # noqa: E501
                **patient.discharge_of_positive_cases_of_covid_19.dict(
                    exclude={"symptoms"},
                ),
                symptoms=[
                    symptoms_dict[s]
                    for s in patient.discharge_of_positive_cases_of_covid_19.symptoms
                    if s in symptoms_dict
                ],
            ),
        )

    async def _get_pathologicals_entities_from_schemas(
        self,
        pathologicals: List[PathologicalSchema],
    ) -> Dict[str, PathologicalEntity]:
        ps_input = list({p.name.lower() for p in pathologicals})
        ps_in_db = await PathologicalEntity.find(
            In(PathologicalEntity.name.lower(), ps_input)
        ).to_list()
        ps_dict = {p.name.lower(): p for p in ps_in_db}
        new_ps = [PathologicalEntity(name=p) for p in ps_input if p not in ps_dict]
        if new_ps:
            result = await PathologicalEntity.insert_many(new_ps)
            for id, item in zip(result.inserted_ids, new_ps):
                item.id = id
        ps_dict.update({p.name: p for p in new_ps})
        return ps_dict

    async def _get_symptoms_entities_from_schemas(
        self,
        symptoms: List[str],
    ) -> Dict[str, SymptomEntity]:
        symptoms_input = list({p for p in symptoms})
        symptoms_in_db = await SymptomEntity.find(
            In(SymptomEntity.name.lower(), symptoms_input)
        ).to_list()
        symptoms_dict = {p.name.lower(): p for p in symptoms_in_db}
        new_symptoms = [
            SymptomEntity(name=p) for p in symptoms_input if p not in symptoms_dict
        ]
        if new_symptoms:
            result = await SymptomEntity.insert_many(new_symptoms)
            for id, item in zip(result.inserted_ids, new_symptoms):
                item.id = id
        symptoms_dict.update({p.name: p for p in new_symptoms})
        return symptoms_dict
