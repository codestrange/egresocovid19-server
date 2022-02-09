from datetime import datetime
from typing import List, Optional

from beanie import PydanticObjectId
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel, EmailStr, Field

from .enums import (
    AftermathEnum,
    BloodTypeEnum,
    ContagionEnum,
    DiagnosisWayEnum,
    IncomeEnum,
    ProphylaxisEnum,
    SexEnum,
    SkinColorEnum,
    TestDiagnosisEnum,
    TreatmentEnum,
)
from .settings import get_settings
from .utils.base_entity import BaseEntity

client = AsyncIOMotorClient(get_settings().database_url)


class IncomeEmbeddedEntity(BaseModel):
    income: IncomeEnum
    days: int


class DischargeOfPositiveCasesOfCovid19EmbeddedEntity(BaseModel):
    detection_date: Optional[datetime] = None
    # With autocompletation base on previous data and with default options
    # SymptomEntity
    symptoms: List[PydanticObjectId] = []
    duration_of_symptoms: Optional[int] = None
    diagnosis_way: Optional[DiagnosisWayEnum] = None
    test_used_in_diagnosis: Optional[TestDiagnosisEnum] = None
    days_from_symptoms_to_diagnosis: Optional[int] = None
    number_pcr_performed: Optional[int] = None
    time_from_diagnosis_to_negative_or_discharge: Optional[int] = None
    form_of_contagion: Optional[ContagionEnum] = None
    was_he_part_of_an_event: Optional[bool] = None
    did_he_work_in_the_attention_to_positive_cases: Optional[bool] = None
    hospitalization_time: Optional[str] = None
    incomes: List[IncomeEmbeddedEntity] = []
    contacts_first_level: Optional[int] = None
    contacts_first_level_positives: Optional[int] = None
    contacts_second_level: Optional[int] = None
    contacts_second_level_positives: Optional[int] = None
    contacts_third_level: Optional[int] = None
    contacts_third_level_positives: Optional[int] = None
    treatments_received: List[TreatmentEnum] = []
    # With autocompletation base on previous data
    antibiotics: List[str] = []
    prophylaxis: List[ProphylaxisEnum] = []
    # With autocompletation base on previous data
    another_vaccine_against_covid: Optional[str] = None
    aftermath: List[AftermathEnum] = []
    # With autocompletation base on previous data
    others_aftermath: List[str] = []


class PathologicalEmbeddedEntity(BaseModel):
    pathological: PydanticObjectId
    treatments: str


class PathologicalEntity(BaseEntity):
    name: str
    default: bool = False

    class Collection:
        name: str = "pathologicals"


class PatientEntity(BaseEntity):
    firstname: str
    lastname: str
    ci: str
    age: int
    sex: SexEnum
    skin_color: SkinColorEnum
    blood_type: Optional[BloodTypeEnum]
    address: str
    municipality_code: str
    # With autocompletation base on previous data
    polyclinic: Optional[str]
    # With autocompletation base on previous data
    surgery: Optional[str]
    # With autocompletation base on previous data
    popular_council: Optional[str]
    # With autocompletation base on previous data
    neighborhood: Optional[str]
    block_number: Optional[int]
    # With autocompletation base on previous data and with default options
    personal_pathological_history: List[PathologicalEmbeddedEntity]
    # With autocompletation base on previous data and with default options
    family_pathological_history: List[PathologicalEmbeddedEntity]
    discharge_of_positive_cases_of_covid_19: DischargeOfPositiveCasesOfCovid19EmbeddedEntity = Field(  # noqa: E501
        default_factory=DischargeOfPositiveCasesOfCovid19EmbeddedEntity
    )

    class Collection:
        name: str = "patients"


class SymptomEntity(BaseEntity):
    name: str
    default: bool = False

    class Collection:
        name: str = "symptoms"


class UserEntity(BaseEntity):
    name: str
    email: EmailStr
    phone: str
    hashed_password: str
    email_confirmed: bool = False
    phone_confirmed: bool = False
    disabled: bool = False

    class Collection:
        name: str = "users"


entities = [
    PathologicalEntity,
    PatientEntity,
    SymptomEntity,
    UserEntity,
]
