from enum import Enum


class AftermathEnum(str, Enum):
    Fatigue = "Fatigue"
    Headache = "Headache"
    Alopecia = "Alopecia"
    RespiratorySymptoms = "RespiratorySymptoms"
    MuscleBoneNeuropathicPain = "MuscleBoneNeuropathicPain"
    PsychologicalPsychiatricDisorders = "PsychologicalPsychiatricDisorders"
    SexualDisorders = "SexualDisorders"
    SleepDisorder = "SleepDisorder"
    PersistenceOfLossOfSmell = "PersistenceOfLossOfSmell"
    PersistenceOfLossOfAppetite = "PersistenceOfLossOfAppetite"
    GastrointestinalSymptoms = "GastrointestinalSymptoms"
    Dizziness = "Dizziness"
    DesiresToVomit = "DesiresToVomit"
    Others = "Others"


class BloodTypeEnum(str, Enum):
    Aplus = "Aplus"
    Bplus = "Bplus"
    ABplus = "ABplus"
    Oplus = "Oplus"
    Aminus = "Aminus"
    Bminus = "Bminus"
    ABminus = "ABminus"
    Ominus = "Ominus"


class ContagionEnum(str, Enum):
    Traveler = "Traveler"
    Contact = "Contact"
    Indeterminate = "Indeterminate"


class DiagnosisWayEnum(str, Enum):
    GuardCorps = "GuardCorps"
    FocusControl = "FocusControl"


class IncomeEnum(str, Enum):
    Home = "Home"
    IsolationCenter = "IsolationCenter"
    HospitalRoom = "HospitalRoom"
    IntermediateTherapy = "IntermediateTherapy"
    IntensiveTherapy = "IntensiveTherapy"


class ProphylaxisEnum(str, Enum):
    Prevengovir = "Prevengovir"
    Vimang = "Vimang"
    Moringa = "Moringa"
    BiomodulinT = "BiomodulinT"
    VitaminC = "VitaminC"
    Polivit = "Polivit"
    Turmeric = "Turmeric"
    Soverana2AndPlus = "Soverana2AndPlus"
    Honey = "Honey"
    VitaminA = "VitaminA"
    Ginger = "Ginger"
    SoveranaPlus = "SoveranaPlus"
    Abdala = "Abdala"
    Covid19Previously = "Covid19Previously"
    AnotherVaccineAgainstCovid = "AnotherVaccineAgainstCovid"


class SexEnum(str, Enum):
    Female = "Female"
    Male = "Male"
    Other = "Other"


class SkinColorEnum(str, Enum):
    White = "White"
    Black = "Black"
    Other = "Other"


class TestDiagnosisEnum(str, Enum):
    AntigenTest = "AntigenTest"
    Biosensor = "Biosensor"
    PCR = "PCR"
    IgMIgGAntibodyTest = "IgMIgGAntibodyTest"


class TreatmentEnum(str, Enum):
    Herferon = "Herferon"
    InterferonGeneric = "InterferonGeneric"
    Jusvinza = "Jusvinza"
    Heberferon = "Heberferon"
    FraxiparinLowMolecularWeightHeparins = "FraxiparinLowMolecularWeightHeparins"
    Nasalferon = "Nasalferon"
    Prednisone = "Prednisone"
    Prevengovir = "Prevengovir"
    Betamethasone = "Betamethasone"
    Italizumab = "Italizumab"
    Antibiotics = "Antibiotics"
