from functools import reduce
from typing import List

from beanie import PydanticObjectId
from beanie.operators import NE, And, Eq, In, Or, RegEx
from fastapi import Depends
from fastapi_restful.cbv import cbv
from fastapi_restful.inferring_router import InferringRouter

from ....database import (
    PathologicalEmbeddedEntity,
    PathologicalEntity,
    PatientEntity,
    ProvinceEntity,
    UserEntity,
)
from ....exceptions.bad_request import BadRequest
from ....exceptions.not_found import NotFound
from ....utils.bad_request_response import bad_request_response
from ....utils.not_found_response import not_found_response
from ..auth import get_current_active_user
from ..schemas import (
    PathologicalSchema,
    PatientGetSchema,
    PatientPostSchema,
    PatientPutSchema,
)

router = InferringRouter(tags=["Patients"])


@cbv(router)
class PatientsController:
    current_user: UserEntity = Depends(get_current_active_user)

    @router.get("/patients/search/{query}")
    async def get_patients(self, query: str) -> List[PatientGetSchema]:
        provinces = await ProvinceEntity.find_all().to_list()
        municipalities = {
            municipality.id: (municipality.name, province.name)
            for province in provinces
            for municipality in province.municipalities
        }
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
        pathologicals_id = list(
            {
                model.pathological
                for item in result
                for model in item.personal_pathological_history
                + item.family_pathological_history
            }
        )
        pathologicals = await PathologicalEntity.find(
            In(PathologicalEntity.id, pathologicals_id)
        ).to_list()
        pathologicals_dict = {item.id: item.name for item in pathologicals}
        return [
            PatientGetSchema(
                **item.dict(
                    exclude={
                        "municipality",
                        "personal_pathological_history",
                        "family_pathological_history",
                    }
                ),
                municipality=municipalities[item.municipality][0],
                province=municipalities[item.municipality][1],
                personal_pathological_history=[
                    PathologicalSchema(
                        name=pathologicals_dict[p.pathological],
                        treatments=p.treatments,
                    )
                    for p in item.personal_pathological_history
                ],
                family_pathological_history=[
                    PathologicalSchema(
                        name=pathologicals_dict[p.pathological],
                        treatments=p.treatments,
                    )
                    for p in item.family_pathological_history
                ],
            )
            for item in result
        ]

    @router.get(
        "/patients/{patientId}",
        responses={
            404: not_found_response,
        },
    )
    async def get_patient(self, patientId: PydanticObjectId):
        patient = await PatientEntity.get_or_404(patientId)
        provinces = await ProvinceEntity.find_all().to_list()
        municipalities = {
            municipality.id: (municipality.name, province.name)
            for province in provinces
            for municipality in province.municipalities
        }
        pathologicals = await PathologicalEntity.find_all().to_list()
        pathologicals_dict = {item.id: item.name for item in pathologicals}
        return PatientGetSchema(
            **patient.dict(
                exclude={
                    "municipality",
                    "personal_pathological_history",
                    "family_pathological_history",
                }
            ),
            municipality=municipalities[patient.municipality][0],
            province=municipalities[patient.municipality][1],
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
        province = next(
            (
                p
                for p in await ProvinceEntity.find_all().to_list()
                if any((p.id == schema.municipality for p in p.municipalities))
            ),
            None,
        )
        municipality = (
            next(
                (m for m in province.municipalities if m.id == schema.municipality),
                None,
            )
            if province
            else None
        )
        if not province or not municipality:
            raise NotFound("Municipality")
        ps_input = list(
            {
                p.name.lower()
                for p in schema.personal_pathological_history
                + schema.family_pathological_history
            }
        )
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
        patient = PatientEntity(
            **schema.dict(
                exclude={"personal_pathological_history", "family_pathological_history"}
            ),
            personal_pathological_history=[
                PathologicalEmbeddedEntity(
                    pathological=ps_dict[p.name].id,
                    treatments=p.treatments,
                )
                for p in schema.personal_pathological_history
            ],
            family_pathological_history=[
                PathologicalEmbeddedEntity(
                    pathological=ps_dict[p.name].id,
                    treatments=p.treatments,
                )
                for p in schema.family_pathological_history
            ],
        )
        await patient.save()
        return PatientGetSchema(
            **schema.dict(exclude={"municipality"}),
            municipality=municipality.name,
            province=province.name,
            id=patient.id,
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
    ) -> PatientGetSchema:
        actual_patient = await PatientEntity.get_or_404(patientId)
        old_patient = await PatientEntity.find_one(
            And(Eq(PatientEntity.ci, schema.ci), NE(PatientEntity.id, patientId))
        )
        if old_patient:
            raise BadRequest("Already exists a patient with same CI")
        municipality_id = (
            schema.municipality if schema.municipality else actual_patient.municipality
        )
        province = next(
            (
                p
                for p in await ProvinceEntity.find_all().to_list()
                if any((p.id == municipality_id for p in p.municipalities))
            ),
            None,
        )
        municipality = (
            next(
                (m for m in province.municipalities if m.id == municipality_id),
                None,
            )
            if province
            else None
        )
        if not province or not municipality:
            raise NotFound("Municipality")
        if (
            schema.personal_pathological_history is not None
            or schema.family_pathological_history is not None
        ):
            inputs = (
                schema.personal_pathological_history
                if schema.personal_pathological_history
                else []
            )
            inputs += (
                schema.family_pathological_history
                if schema.family_pathological_history
                else []
            )
            ps_input = list({p.name.lower() for p in inputs})
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
            if schema.personal_pathological_history is not None:
                actual_patient.personal_pathological_history = [
                    PathologicalEmbeddedEntity(
                        pathological=ps_dict[p.name].id,
                        treatments=p.treatments,
                    )
                    for p in schema.personal_pathological_history
                ]
            if schema.family_pathological_history is not None:
                actual_patient.family_pathological_history = [
                    PathologicalEmbeddedEntity(
                        pathological=ps_dict[p.name].id,
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
        pathologicals = await PathologicalEntity.find_all().to_list()
        pathologicals_dict = {item.id: item.name for item in pathologicals}
        return PatientGetSchema(
            **updated_patient.dict(
                exclude={
                    "municipality",
                    "personal_pathological_history",
                    "family_pathological_history",
                }
            ),
            municipality=municipality.name,
            province=province.name,
            personal_pathological_history=[
                PathologicalSchema(
                    name=pathologicals_dict[p.pathological],
                    treatments=p.treatments,
                )
                for p in updated_patient.personal_pathological_history
            ],
            family_pathological_history=[
                PathologicalSchema(
                    name=pathologicals_dict[p.pathological],
                    treatments=p.treatments,
                )
                for p in updated_patient.family_pathological_history
            ],
        )
