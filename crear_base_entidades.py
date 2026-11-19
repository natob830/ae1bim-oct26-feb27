# crear_base_entidades.py
"""Define el modelo relacional de clínicas veterinarias con SQLAlchemy ORM.

Las claves foráneas obligatorias aseguran que cada consultorio pertenezca a una
clínica, cada veterinario a un consultorio y cada historia a un veterinario.
"""

from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Date
from sqlalchemy.orm import declarative_base, relationship
from configuracion import cadena_base_datos

# El motor usa SQLite según la URL declarada en configuracion.py.
engine = create_engine(cadena_base_datos)
# La clase base registra las tablas que SQLAlchemy generará en SQLite.
Base = declarative_base()


class Clinica(Base):
    """Clínica veterinaria con nombre comercial, dirección y responsable."""

    __tablename__ = 'clinica'

    # Identificador único y datos requeridos de la clínica.
    id = Column(Integer, primary_key=True)
    nombre_comercial = Column(String(100), nullable=False)
    direccion = Column(String(200), nullable=False)
    veterinario_responsable = Column(String(100), nullable=False)

    # Una clínica puede tener varios consultorios; la relación inversa
    # permite recorrerlos desde el objeto ORM sin escribir SQL manual.
    consultorios = relationship("Consultorio", back_populates="clinica")

    def __repr__(self):
        return (f"Clínica: id={self.id} | Nombre={self.nombre_comercial} | "
                f"Dirección={self.direccion} | Responsable={self.veterinario_responsable}")


class Consultorio(Base):
    """Consultorio con especialidad y pertenencia obligatoria a una clínica."""

    __tablename__ = 'consultorio'

    # Identificador, nombre visible y especialidad principal del consultorio.
    id = Column(Integer, primary_key=True)
    nombre = Column(String(50), nullable=False)
    especialidad = Column(String(100), nullable=False)
    # nullable=False impide guardar consultorios huérfanos en la base de datos.
    clinica_id = Column(Integer, ForeignKey('clinica.id'), nullable=False)

    # La relación bidireccional conecta el consultorio con su clínica y
    # permite recorrer sus veterinarios.
    clinica = relationship("Clinica", back_populates="consultorios")
    veterinarios = relationship("Veterinario", back_populates="consultorio")

    def __repr__(self):
        return (f"Consultorio: id={self.id} | Nombre={self.nombre} | "
                f"Especialidad={self.especialidad} | Clínica={self.clinica.nombre_comercial}")


class Veterinario(Base):
    """Profesional identificado por licencia y asignado a un consultorio."""

    __tablename__ = 'veterinario'

    # Datos personales y profesionales requeridos para identificar al veterinario.
    id = Column(Integer, primary_key=True)
    nombres = Column(String(100), nullable=False)
    apellidos = Column(String(100), nullable=False)
    correo = Column(String(100), nullable=False)
    licencia_profesional = Column(String(50), nullable=False)
    # Cada veterinario pertenece obligatoriamente a un consultorio.
    consultorio_id = Column(Integer, ForeignKey('consultorio.id'), nullable=False)

    # Se puede navegar desde el veterinario hasta su consultorio y sus historias.
    consultorio = relationship("Consultorio", back_populates="veterinarios")
    historias_clinicas = relationship("HistoriaClinica", back_populates="veterinario")

    def __repr__(self):
        return (f"Veterinario: id={self.id} | {self.nombres} {self.apellidos} | "
                f"Licencia={self.licencia_profesional} | Correo={self.correo}")


class HistoriaClinica(Base):
    """Atención registrada para una mascota y elaborada por un veterinario."""

    __tablename__ = 'historia_clinica'

    # Los datos clínicos describen fecha, diagnóstico, tratamiento y mascota.
    id = Column(Integer, primary_key=True)
    fecha_atencion = Column(Date, nullable=False)
    diagnostico = Column(String(250), nullable=False)
    tratamiento = Column(String(250), nullable=False)
    nombre_mascota = Column(String(100), nullable=False)
    # Toda historia debe quedar asociada a un veterinario existente.
    veterinario_id = Column(Integer, ForeignKey('veterinario.id'), nullable=False)

    # back_populates completa la relación bidireccional con Veterinario.
    veterinario = relationship("Veterinario", back_populates="historias_clinicas")

    def __repr__(self):
        return (f"Historia Clínica: id={self.id} | Fecha={self.fecha_atencion} | "
                f"Mascota={self.nombre_mascota} | Diagnóstico={self.diagnostico} | "
                f"Tratamiento={self.tratamiento}")

if __name__ == "__main__":
    # Crea las tablas faltantes sin eliminar ni recrear datos existentes.
    Base.metadata.create_all(engine)
    print("Base de datos y tablas creadas exitosamente.")