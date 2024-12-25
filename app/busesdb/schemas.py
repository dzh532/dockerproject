from pathlib import Path
from pydantic import BaseModel, ConfigDict, EmailStr
from typing import Optional
from datetime import date, time

BASE_DIR  = Path(__file__).resolve().parent.parent.parent

class AuthJWT(BaseModel):
    private_key_path: Path = BASE_DIR / "app" / "certs" / "jwt-private.pem"
    public_key_path: Path = BASE_DIR / "app" / "certs" / "jwt-public.pem"
    algorithm: str = "RS256"
    # access_token_expire_minutes = 15
    access_token_expire_minutes: int = 60

class UserSchema(BaseModel):
    model_config = ConfigDict(strict=True)

    name: str
    password: bytes
    email: EmailStr | None = None
    active: bool = True
    is_admin: bool = False

class BusSchema(BaseModel):
    gos_number: str
    capacity: int
    is_air_conditioner: bool

    model_config = ConfigDict(from_attributes=True)

class CompanySchema(BaseModel):
    name: str
    duration_work: int
    address: str
    number_phone: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)

class BusesInCompanySchema(BaseModel):
    buses_gos_number: str
    company_name: str

    model_config = ConfigDict(from_attributes=True)

class DriverSchema(BaseModel):
    number_vy: int
    fio: str
    experience: int
    age: int

    model_config = ConfigDict(from_attributes=True)

class DelayVoyageSchema(BaseModel):
    id: int
    number_vy: Optional[int] = None
    cause: str
    duration: time

    model_config = ConfigDict(from_attributes=True)

class ReportIncomeCompanySchema(BaseModel):
    id: int
    company_name: str
    start_period: date
    end_period: date
    revenue: int
    expenses: int
    profit: int

    model_config = ConfigDict(from_attributes=True)

class TypeRepairSchema(BaseModel):
    id: int
    detail: str
    cost_detail: int

    model_config = ConfigDict(from_attributes=True)

class OrderRepairSchema(BaseModel):
    id: int
    buses_gos_number: str
    detail_name: str
    date: date

    model_config = ConfigDict(from_attributes=True)

class StopSchema(BaseModel):
    id: int
    name: str

    model_config = ConfigDict(from_attributes=True)

class RouteSchema(BaseModel):
    number_route: str
    count_stops: int
    start_stop: str
    end_stop: str
    time_start: time
    time_end: time
    cost_travel: int

    model_config = ConfigDict(from_attributes=True)

class StopsAndRoutesSchema(BaseModel):
    id_stops: int
    number_route: str

    model_config = ConfigDict(from_attributes=True)

class PassengerSchema(BaseModel):
    id: int
    fio: str
    age: int

    model_config = ConfigDict(from_attributes=True)

class TicketSchema(BaseModel):
    id: int
    id_passenger: int
    cost_travel: int
    date_start: date
    start_stop: str
    end_stop: str

    model_config = ConfigDict(from_attributes=True)

class RouteSheetSchema(BaseModel):
   id: int
   number_vy: int
   number_route: str
   date: date
   gos_number_bus: str

   model_config=ConfigDict(from_attributes=True)

class ReviewPassengerSchema(BaseModel):
   id:int
   id_passenger:int
   gos_number_bus:str
   grade:int
   text_review: Optional[str]=None
   date: date

   model_config=ConfigDict(from_attributes=True)





# from pydantic import BaseModel, ConfigDict
#
#
# class BusSchema(BaseModel):
#     gos_number: str
#     capacity: int
#     is_air_conditioner: bool
#
#     model_config = ConfigDict(from_attributes=True)
