from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.talleres import Tecnico
from app.schemas.tecnico import (TecnicoCreate, TecnicoUpdate, TecnicoResponse)

router = APIRouter(prefix="/tecnicos", tags=["Técnicos"])


@router.post("/", response_model=TecnicoResponse, status_code=201)
def crear_tecnico(datos: TecnicoCreate, db: Session = Depends(get_db)):
    nuevo = Tecnico(**datos.model_dump(), disponibilidad=True)
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo


@router.get("/taller/{id_taller}", response_model=List[TecnicoResponse])
def listar_por_taller(id_taller: int, db: Session = Depends(get_db)):
    return db.query(Tecnico).filter(Tecnico.id_taller == id_taller).all()


@router.get("/{codigo}", response_model=TecnicoResponse)
def obtener_tecnico(codigo: int, db: Session = Depends(get_db)):
    t = db.query(Tecnico).filter(Tecnico.codigo == codigo).first()
    if not t:
        raise HTTPException(status_code=404, detail="Técnico no encontrado")
    return t


@router.put("/{codigo}", response_model=TecnicoResponse)
def actualizar_tecnico(codigo: int, datos: TecnicoUpdate, db: Session = Depends(get_db)):
    t = db.query(Tecnico).filter(Tecnico.codigo == codigo).first()
    if not t:
        raise HTTPException(status_code=404, detail="Técnico no encontrado")
    for campo, valor in datos.model_dump(exclude_unset=True).items():
        setattr(t, campo, valor)
    db.commit()
    db.refresh(t)
    return t


@router.delete("/{codigo}")
def eliminar_tecnico(codigo: int, db: Session = Depends(get_db)):
    t = db.query(Tecnico).filter(Tecnico.codigo == codigo).first()
    if not t:
        raise HTTPException(status_code=404, detail="Técnico no encontrado")
    db.delete(t)
    db.commit()
    return {"mensaje": "Técnico eliminado"}