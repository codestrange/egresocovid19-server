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


class PatientGetSchema(PatientBaseSchema):
    id: PydanticObjectId
    province: str
    municipality: str
    discharge_of_positive_cases_of_covid_19: Optional[
        DischargeOfPositiveCasesOfCovid19Schema
    ]


class PatientPostSchema(PatientBaseSchema):
    municipality: PydanticObjectId


class PatientPutSchema(APIModel):
    firstname: Optional[str]
    lastname: Optional[str]
    ci: Optional[str]
    age: Optional[int]
    sex: Optional[SexEnum]
    skin_color: Optional[SkinColorEnum]
    blood_type: Optional[Optional[BloodTypeEnum]]
    address: Optional[str]
    polyclinic: Optional[str]
    surgery: Optional[str]
    popular_council: Optional[str]
    neighborhood: Optional[str]
    block_number: Optional[int]
    personal_pathological_history: Optional[List[PathologicalSchema]]
    family_pathological_history: Optional[List[PathologicalSchema]]
    municipality: Optional[PydanticObjectId]
