from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, TIMESTAMP, Numeric
from app.database import Base
from sqlalchemy.orm import relationship

class Taller(Base): 
    __tablename__= "taller"
    __table_args__ = {"schema":"taller"}
    
    codigo = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    telefono = Column(String(20), nullable=False)
    direccion = Column(String(200), nullable=False)
    latitud = Column(Numeric(10, 8), nullable=False)
    longitud = Column(Numeric(11, 8), nullable=False)
    activo = Column(Boolean, default=True, nullable=False)

    tecnicos = relationship("Tecnico", back_populates="taller")
    taller_usuarios = relationship("TallerUsuario", back_populates="taller")

class TallerUsuario(Base):
    __tablename__ = "taller_usuario"
    __table_args__ = {"schema": "taller"}
    id_usuario = Column(String(50), ForeignKey("seguridad.usuario.codigo", onupdate="CASCADE", ondelete="CASCADE"), primary_key=True)
    codigo_taller = Column(Integer, ForeignKey("taller.taller.codigo", onupdate="CASCADE", ondelete="CASCADE"), primary_key=True)
    fecha_asignacion = Column(TIMESTAMP, nullable=False)
    
    taller = relationship("Taller", back_populates="taller_usuarios")

class Tecnico(Base): 
    __tablename__ = "tecnico"
    __table_args__ = {"schema": "taller"}

    codigo = Column(Integer, primary_key=True, index=True)
    disponibilidad = Column(Boolean, nullable=False, default=True)
    latitud = Column(Numeric(10, 7), nullable=False)
    longitud = Column(Numeric(10, 7), nullable=False)
    telefono = Column(String(100), nullable=False)
    id_taller = Column(Integer, ForeignKey("taller.taller.codigo", onupdate="CASCADE", ondelete="CASCADE"), nullable=False)
    id_usuario = Column(String(50), ForeignKey("seguridad.usuario.codigo", onupdate="CASCADE", ondelete="CASCADE"), nullable=False)

    taller = relationship("Taller", back_populates="tecnicos")


    