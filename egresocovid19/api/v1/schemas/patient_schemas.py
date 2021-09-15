from typing import List, Optional

from beanie import PydanticObjectId
from fastapi_restful.api_model import APIModel

from ....enums import BloodTypeEnum, SexEnum, SkinColorEnum


class PathologicalSchema(APIModel):
    name: str
    treatments: str


class PatientBaseSchema(APIModel):
    firstname: str
    lastname: str
    ci: str
    age: int
    sex: SexEnum
    skin_color: SkinColorEnum
    blood_type: Optional[BloodTypeEnum]
    address: str
    polyclinic: str
    surgery: str
    popular_council: str
    neighborhood: str
    block_number: int
    personal_pathological_history: List[PathologicalSchema]
    family_pathological_history: List[PathologicalSchema]
    # discharge_of_positive_cases_of_covid_19: Optional[
    #     DischargeOfPositiveCasesOfCovid19EmbeddedEntity
    # ]


class PatientGetSchema(PatientBaseSchema):
    id: PydanticObjectId
    province: str
    municipality: str


class PatientPostSchema(PatientBaseSchema):
    municipality: PydanticObjectId
