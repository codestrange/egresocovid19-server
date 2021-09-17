from datetime import datetime
from typing import List, Optional

from beanie import PydanticObjectId
from fastapi_restful.api_model import APIModel

from ...database import IncomeEmbeddedEntity
from ...enums import (
    AftermathEnum,
    BloodTypeEnum,
    ContagionEnum,
    DiagnosisWayEnum,
    ProphylaxisEnum,
    SexEnum,
    SkinColorEnum,
    TestDiagnosisEnum,
    TreatmentEnum,
)


class PathologicalSchema(APIModel):
    name: str
    treatments: str


class DischargeOfPositiveCasesOfCovid19Schema(APIModel):
    detection_date: Optional[datetime]
    symptoms: List[str]
    duration_of_symptoms: Optional[int]
    diagnosis_way: Optional[DiagnosisWayEnum]
    test_used_in_diagnosis: Optional[TestDiagnosisEnum]
    days_from_symptoms_to_diagnosis: Optional[int]
    number_pcr_performed: Optional[int]
    time_from_diagnosis_to_negative_or_discharge: Optional[int]
    form_of_contagion: Optional[ContagionEnum]
    was_he_part_of_an_event: Optional[bool]
    did_he_work_in_the_attention_to_positive_cases: Optional[bool]
    hospitalization_time: Optional[str]
    incomes: List[IncomeEmbeddedEntity]
    contacts_first_level: Optional[int]
    contacts_first_level_positives: Optional[int]
    contacts_second_level: Optional[int]
    contacts_second_level_positives: Optional[int]
    contacts_third_level: Optional[int]
    contacts_third_level_positives: Optional[int]
    treatments_received: List[TreatmentEnum]
    antibiotics: List[str]
    prophylaxis: List[ProphylaxisEnum]
    another_vaccine_against_covid: Optional[str]
    aftermath: List[AftermathEnum]
    others_aftermath: List[str]


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
