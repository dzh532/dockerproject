from pydantic import BaseModel, ConfigDict


class BusSchema(BaseModel):
    gos_number: str
    capacity: int
    is_air_conditioner: bool

    model_config = ConfigDict(from_attributes=True)
