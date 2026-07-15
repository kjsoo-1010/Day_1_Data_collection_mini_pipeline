from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class WeatherHourlyRecord(BaseModel):
    time: datetime
    temperature_2m: float
    precipitation_probability: int = Field(ge=0, le=100)


class IPInfo(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    query: str
    status: str
    country: str
    country_code: str = Field(alias="countryCode")
    region_name: str = Field(alias="regionName")
    city: str
    lat: float
    lon: float
    timezone: str
    isp: str
    org: str | None = None
    as_number: str | None = Field(default=None, alias="as")


class CountryInfo(BaseModel):
    name: str
    capital: str
    region: str
    subregion: str
    population: int
    area: float
    alpha2_code: str
    alpha3_code: str
    languages: str
    currencies: str
    flag_png: str
