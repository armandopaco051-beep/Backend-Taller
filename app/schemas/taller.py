from pydantic import BaseModel
from typing import Optional
from decimal import Decimal
from datetime import datetime


class TallerCreate(BaseModel):
    nombre: str
    telefono: str
    direccion: str
    latidud: Decimal
    longitud: Decimal

class TallerUpdate(BaseModel):
    nombre: Optional[str] = None
    telefono: Optional[str] = None
    direccion: Optional[str] = None
    latidud: Optional[Decimal] = None
    longitud: Optional[Decimal] = None
    activo: Optional[bool] = None

class TallerResponse(BaseModel):
    codigo: int
    nombre: str
    telefono: str
    direccion: str
    latidud: Decimal
    longitud: Decimal
    activo: bool
    class Config:
        from_attributes = True

class TallerUsuarioCreate(BaseModel):
    id_usuario: int
    codigo_taller: int
    fecha_asignacion: datetime

class TallerUsuarioResponse(TallerUsuarioCreate):
    class Config:
        from_attributes = True