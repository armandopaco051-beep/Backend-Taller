from sqlalchemy import Column, Integer, String, ForeignKey, Text, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base



class Evidencia(Base):
    __tablename__ = "evidencia"
    __table_args__ = {"schema": "multimedia"}  # ✅ ESTO ES LO QUE TE FALTA O NO ESTÁ APLICANDO

    codigo = Column(Integer, primary_key=True, index=True)
    fecha_subida = Column(DateTime, default=datetime.utcnow, nullable=False)

    transcripcion = Column(Text, nullable=True)
    url_archivo = Column(String(255), nullable=True)

    id_tipo_evidencia = Column(
        Integer,
        ForeignKey("catalogo.tipo_evidencia.codigo"),
        nullable=False
    )

    id_incidente = Column(
        Integer,
        ForeignKey(
            "operaciones.incidente.codigo",
            onupdate="CASCADE",
            ondelete="CASCADE"
        ),
        nullable=False
    )

    incidente = relationship("Incidente", back_populates="evidencias")
    