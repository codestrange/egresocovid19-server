from typing import Dict, List, Optional

from pydantic import BaseModel

from ..static.municipality_codes import municipality_codes
from ..static.province_codes import province_codes


class Municipality(BaseModel):
    name: str
    code: str


class Province(BaseModel):
    name: str
    code: str


class MunicipalityDetail(Municipality):
    province: Province


class ProvinceDetail(Province):
    municipalities: List[Municipality]


class ProvinceService:
    def __init__(self):
        self.provinces: Optional[List[ProvinceDetail]] = None

    @property
    def municipalities_dict(self) -> Dict[str, str]:
        return municipality_codes

    @property
    def provinces_dict(self) -> Dict[str, str]:
        return province_codes

    def get_provinces(self) -> List[ProvinceDetail]:
        if not self.provinces:
            self.provinces = [
                ProvinceDetail(
                    name=p_name,
                    code=p_code,
                    municipalities=[
                        Municipality(
                            name=m_name,
                            code=m_code,
                        )
                        for m_code, m_name in self.municipalities_dict.items()
                        if m_code.startswith(p_code)
                    ],
                )
                for p_code, p_name in self.provinces_dict.items()
            ]
        return self.provinces

    def get_municipality(self, code: str) -> Optional[MunicipalityDetail]:
        if code in self.municipalities_dict:
            p_code = next(
                (p_code for p_code in self.provinces_dict if code.startswith(p_code)),
                None,
            )
            if p_code:
                return MunicipalityDetail(
                    name=self.municipalities_dict[code],
                    code=code,
                    province=Province(
                        name=self.provinces_dict[p_code],
                        code=p_code,
                    ),
                )
