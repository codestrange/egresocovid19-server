from enum import IntEnum, auto


class AftermathEnum(IntEnum):
    Fatigue = 0
    Headache = auto()
    Alopecia = auto()
    RespiratorySymptoms = auto()
    MuscleBoneNeuropathicPain = auto()
    PsychologicalPsychiatricDisorders = auto()
    SexualDisorders = auto()
    SleepDisorder = auto()
    PersistenceOfLossOfSmell = auto()
    PersistenceOfLossOfAppetite = auto()
    GastrointestinalSymptoms = auto()
    Dizziness = auto()
    DesiresToVomit = auto()
    Others = auto()


class BloodTypeEnum(IntEnum):
    Unknown = 0
    Aplus = auto()
    Bplus = auto()
    ABplus = auto()
    Oplus = auto()
    Aminus = auto()
    Bminus = auto()
    ABminus = auto()
    Ominus = auto()


class ContagionEnum(IntEnum):
    Traveler = 0
    Contact = auto()
    Indeterminate = auto()


class DiagnosisWayEnum(IntEnum):
    GuardCorps = 0
    FocusControl = auto()


class IncomeEnum(IntEnum):
    Home = 0
    IsolationCenter = auto()
    HospitalRoom = auto()
    IntermediateTherapy = auto()
    IntensiveTherapy = auto()


class ProphylaxisEnum(IntEnum):
    Prevengovir = 0
    Vimang = auto()
    Moringa = auto()
    BiomodulinT = auto()
    VitaminC = auto()
    Polivit = auto()
    Turmeric = auto()
    Soverana2AndPlus = auto()
    Honey = auto()
    VitaminA = auto()
    Ginger = auto()
    SoveranaPlus = auto()
    Abdala = auto()
    Covid19Previously = auto()
    AnotherVaccineAgainstCovid = auto()


class SexEnum(IntEnum):
    Female = 0
    Male = auto()
    Other = auto()


class SkinColorEnum(IntEnum):
    White = 0
    Black = auto()
    Other = auto()


class TestDiagnosisEnum(IntEnum):
    AntigenTest = 0
    Biosensor = auto()
    PCR = auto()
    IgMIgGAntibodyTest = auto()


class TreatmentEnum(IntEnum):
    Herferon = 0
    InterferonGeneric = auto()
    Jusvinza = auto()
    Heberferon = auto()
    FraxiparinLowMolecularWeightHeparins = auto()
    Nasalferon = auto()
    Prednisone = auto()
    Prevengovir = auto()
    Betamethasone = auto()
    Italizumab = auto()
    Antibiotics = auto()
