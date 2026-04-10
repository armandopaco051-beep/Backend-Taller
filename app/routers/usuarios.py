import string
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.seguridad import Usuario, Rol, Permiso, RolPermiso
from app.schemas.usuario import (
    UsuarioResponse, UsuarioUpdate,
    RolCreate, RolResponse,
    PermisoCreate, PermisoResponse
)

router = APIRouter(prefix="/usuarios", tags=["Usuarios"])
roles_router = APIRouter(prefix="/roles", tags=["Roles"])
permisos_router = APIRouter(prefix="/permisos", tags=["Permisos"])


# CU-05 VER PERFIL 
@router.get("/{codigo}", response_model = UsuarioResponse)
def obtener_usuario(codigo : str , deb :Session = Depends(get_db)):
    usuario = deb.query(Usuario).filter(Usuario.codigo == codigo).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return usuario

#CU-05 ACTUALIZAR EL PERFIL 
@router.put ("/{codigo}", response_model = UsuarioResponse)
def actualizar_usuario(codigo: str , datos : UsuarioUpdate, db : Session = Depends(get_db)):
    usuario = db.query(Usuario).filter(Usuario.codigo == codigo).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    if datos.id_rol is not None:
        rol = db.query(Rol).filter(Rol.id == datos.id_rol).first()
        if not rol:
            raise HTTPException(status_code=404, detail="Rol no encontrado")
    for campo, valor in datos.model_dump(exclude_unset=True).items(): 
        setattr(usuario, campo, valor)
    db.commit()
    db.refresh(usuario)
    return usuario

# Listar Todos 

@router.get("/", response_model = List[UsuarioResponse])
def listar_usuarios(db:Session = Depends(get_db)):
    return db.query(Usuario).all()

# Desactivar
@router.delete("/{codigo}")
def desactivar_usuario(codigo: str, db : Session = Depends(get_db)):
    usuario = db.query(Usuario).filter(Usuario.codigo == codigo).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    usuario.activo = False
    db.commit()
    db.refresh(usuario)
    return {"mensaje:" "Usuario Desactivado"}

# CU-06 GESTIONAR ROLES 
@roles_router.get("/", response_model=RolResponse)
def listar_roles(db : Session = Depends(get_db)):
    return db.query(Rol).all()
# nuevo 
@roles_router.post ("/", response_model=RolResponse)
def crear_rol(datos: RolCreate, db: Session = Depends(get_db)):
    nuevo = Rol(nombre = datos.nombre)
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo



@roles_router.delete("/{id_rol}")
def eliminar_rol(id_rol: int , db : Session = Depends(get_db)):
    rol = db.query(Rol).filter(Rol.id == id_rol).first()
    if not rol : 
        raise HTTPException(status_code=404, detail="Rol no encontrado")
    db.delete(rol)
    db.commit()
    return {"mensaje": "Rol eliminado"}

# CU-07 GESTIONAR PERMISOS
@permisos_router.get("/", response_model=List[PermisoResponse])
def listar_permisos(db: Session = Depends(get_db)):
    return db.query(Permiso).all()

@permisos_router.post("/", response_model=PermisoResponse)
def crear_permiso(datos: PermisoCreate, db: Session = Depends(get_db)):
    nuevo = Permiso(nombre=datos.nombre)
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo

@permisos_router.post("/{id_rol}/asignar/{id_permiso}")
def asignar_permiso(id_rol: int, id_permiso: int, db: Session = Depends(get_db)):
    existe = db.query(RolPermiso).filter(
        RolPermiso.id_rol == id_rol,
        RolPermiso.id_permiso == id_permiso
    ).first()
    if existe:
        raise HTTPException(status_code=400, detail="Permiso ya asignado")
    db.add(RolPermiso(id_rol=id_rol, id_permiso=id_permiso))
    db.commit()
    return {"mensaje": "Permiso asignado correctamente"}
