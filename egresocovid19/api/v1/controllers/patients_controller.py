from beanie.operators import In
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
from ..schemas.patient_schemas import PatientGetSchema, PatientPostSchema

router = InferringRouter(tags=["Patients"])


@cbv(router)
class PatientsController:
    current_user: UserEntity = Depends(get_current_active_user)

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
        ps_input = [
            p.name
            for p in schema.personal_pathological_history
            + schema.family_pathological_history
        ]
        ps_in_db = await PathologicalEntity.find(
            In(PathologicalEntity.name, ps_input)
        ).to_list()
        ps_dict = {p.name: p for p in ps_in_db}
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
