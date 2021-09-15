from typing import List, Optional, Tuple

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


class DischargeOfPositiveCasesOfCovid19EmbeddedEntity(BaseModel):
    has_symptoms: bool
    # With autocompletation base on previous data and with default options
    # SymptomEntity
    symptoms: List[PydanticObjectId]
    duration_of_symptoms: int
    diagnosis_way: DiagnosisWayEnum
    test_used_in_diagnosis: TestDiagnosisEnum
    days_from_symptoms_to_diagnosis: int
    number_pcr_performed: int
    time_from_diagnosis_to_negative_or_discharge: int
    form_of_contagion: ContagionEnum
    was_he_part_of_an_event: bool
    did_he_work_in_the_attention_to_positive_cases: bool
    hospitalization_time: str
    incomes: List[Tuple[IncomeEnum, int]]
    contacts_first_level: int
    contacts_first_level_positives: int
    contacts_second_level: int
    contacts_second_level_positives: int
    contacts_third_level: int
    contacts_third_level_positives: int
    treatments_received: List[TreatmentEnum]
    # With autocompletation base on previous data
    antibiotics: List[str]
    prophylaxis: List[ProphylaxisEnum]
    # With autocompletation base on previous data
    another_vaccine_against_covid: Optional[str]
    aftermath: List[AftermathEnum]
    # With autocompletation base on previous data
    others_aftermath: List[str]


class MunicipalityEmbeddedEntity(BaseModel):
    id: PydanticObjectId = Field(default_factory=PydanticObjectId)
    name: str


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
    # MunicipalityEmbeddedEntity
    municipality: PydanticObjectId
    # With autocompletation base on previous data
    polyclinic: str
    # With autocompletation base on previous data
    surgery: str
    # With autocompletation base on previous data
    popular_council: str
    # With autocompletation base on previous data
    neighborhood: str
    block_number: int
    # With autocompletation base on previous data and with default options
    personal_pathological_history: List[PathologicalEmbeddedEntity]
    # With autocompletation base on previous data and with default options
    family_pathological_history: List[PathologicalEmbeddedEntity]
    discharge_of_positive_cases_of_covid_19: Optional[
        DischargeOfPositiveCasesOfCovid19EmbeddedEntity
    ]

    class Collection:
        name: str = "patients"


class ProvinceEntity(BaseEntity):
    name: str
    municipalities: List[MunicipalityEmbeddedEntity]

    class Collection:
        name: str = "provinces"


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
    ProvinceEntity,
    SymptomEntity,
    UserEntity,
]
