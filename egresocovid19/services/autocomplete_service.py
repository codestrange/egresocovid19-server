from typing import List, cast

from beanie.operators import NE, Eq, RegEx
from pydantic import BaseModel

from ..database import (
    DischargeOfPositiveCasesOfCovid19EmbeddedEntity,
    PathologicalEntity,
    PatientEntity,
    SymptomEntity,
)


class AutoCompleteService:
    def __init__(self):
        pass

    async def get_polyclinics(self, query: str):
        class Projection(BaseModel):
            polyclinic: str

        async for item in PatientEntity.find(
            RegEx(PatientEntity.polyclinic, query, options="i")
        ).project(Projection):
            yield item.polyclinic

    async def get_surgeries(self, query: str):
        class Projection(BaseModel):
            surgery: str

        async for item in PatientEntity.find(
            RegEx(PatientEntity.surgery, query, options="i")
        ).project(Projection):
            yield item.surgery

    async def get_popular_councils(self, query: str):
        class Projection(BaseModel):
            popular_council: str

        async for item in PatientEntity.find(
            RegEx(PatientEntity.popular_council, query, options="i")
        ).project(Projection):
            yield item.popular_council

    async def get_neighborhoods(self, query: str):
        class Projection(BaseModel):
            neighborhood: str

        async for item in PatientEntity.find(
            RegEx(PatientEntity.neighborhood, query, options="i")
        ).project(Projection):
            yield item.neighborhood

    async def get_pathologicals(self, query: str):
        class Projection(BaseModel):
            name: str

        async for item in PathologicalEntity.find(
            RegEx(PathologicalEntity.name, query, options="i")
        ).project(Projection):
            yield item.name

    async def get_default_pathologicals(self):
        class Projection(BaseModel):
            name: str

        async for item in PathologicalEntity.find(
            Eq(PathologicalEntity.default, True)
        ).project(Projection):
            yield item.name

    async def get_antibiotics(self, query: str):
        class Interal(BaseModel):
            antibiotics: List[str]

        class Projection(BaseModel):
            discharge_of_positive_cases_of_covid_19: Interal

        antibiotics = [
            antibiotic
            async for item in PatientEntity.find(
                NE(PatientEntity.discharge_of_positive_cases_of_covid_19, None)
            ).project(Projection)
            for antibiotic in item.discharge_of_positive_cases_of_covid_19.antibiotics
        ]
        query_lower = query.lower()
        return filter(lambda x: query_lower in x.lower(), antibiotics)

    async def get_another_vaccines_against_covid(self, query: str):
        class Interal(BaseModel):
            another_vaccine_against_covid: str

        class Projection(BaseModel):
            discharge_of_positive_cases_of_covid_19: Interal

        async for item in PatientEntity.find(
            NE(PatientEntity.discharge_of_positive_cases_of_covid_19, None)
        ).find(
            NE(
                cast(
                    DischargeOfPositiveCasesOfCovid19EmbeddedEntity,
                    PatientEntity.discharge_of_positive_cases_of_covid_19,
                ).another_vaccine_against_covid,
                None,
            )
        ).find(
            RegEx(
                cast(
                    DischargeOfPositiveCasesOfCovid19EmbeddedEntity,
                    PatientEntity.discharge_of_positive_cases_of_covid_19,
                ).another_vaccine_against_covid,
                query,
                options="i",
            )
        ).project(
            Projection
        ):
            yield item.discharge_of_positive_cases_of_covid_19.another_vaccine_against_covid  # noqa: E501

    async def get_others_aftermaths(self, query: str):
        class Internal(BaseModel):
            others_aftermath: List[str]

        class Projection(BaseModel):
            discharge_of_positive_cases_of_covid_19: Internal

        others_aftermaths = [
            aftermath
            async for item in PatientEntity.find(
                NE(PatientEntity.discharge_of_positive_cases_of_covid_19, None)
            ).project(Projection)
            for aftermath in item.discharge_of_positive_cases_of_covid_19.others_aftermath  # noqa: E501
        ]
        query_lower = query.lower()
        return filter(lambda x: query_lower in x.lower(), others_aftermaths)

    async def get_symptoms(self, query: str):
        class Projection(BaseModel):
            name: str

        async for item in SymptomEntity.find(
            RegEx(SymptomEntity.name, query, options="i")
        ).project(Projection):
            yield item.name

    async def get_default_symptoms(self):
        class Projection(BaseModel):
            name: str

        async for item in SymptomEntity.find(Eq(SymptomEntity.default, True)).project(
            Projection
        ):
            yield item.name
