"""Consultas con condiciones simultáneas mediante and_() y join() ORM."""

from sqlalchemy import and_
from sqlalchemy.orm import sessionmaker
from crear_base_entidades import (
    Clinica,
    Consultorio,
    HistoriaClinica,
    Veterinario,
    engine,
)

# La sesión ORM se utiliza para las consultas que combinan varias tablas.
Session = sessionmaker(bind=engine)
session = Session()

# join(Veterinario) permite combinar los datos de una historia con su autor;
# and_ exige que mascota y nombre del veterinario coincidan simultáneamente.
print("=== CONSULTA CON and_() - HISTORIAS DE TOBY ATENDIDO POR CARLOS ===")
historias_and = session.query(HistoriaClinica).join(Veterinario).filter(
    and_(
        Veterinario.nombres == "Carlos",
        HistoriaClinica.nombre_mascota == "Toby"
    )
).all()

for historia in historias_and:
    print(
        f"{historia} | Veterinario: {historia.veterinario.nombres} "
        f"{historia.veterinario.apellidos}"
    )

# El join entre consultorio y clínica permite exigir especialidad y clínica.
print("\n=== CONSULTORIOS DE MEDICINA GENERAL DE VETCARE LOJA ===")
consultorios_and = (
    session.query(Consultorio)
    .join(Clinica)
    .filter(
        and_(
            Consultorio.especialidad == "Medicina General",
            Clinica.nombre_comercial == "VetCare Loja",
        )
    )
    .all()
)
for consultorio in consultorios_and:
    print(f"{consultorio} | Dirección: {consultorio.clinica.direccion}")

# Los joins recorren veterinario → consultorio → clínica para filtrar
# profesionales de Guayaquil con la especialidad de cardiología.
print("\n=== VETERINARIOS DE CARDIOLOGÍA EN GUAYAQUIL ===")
veterinarios_and = (
    session.query(Veterinario)
    .join(Consultorio)
    .join(Clinica)
    .filter(
        and_(
            Consultorio.especialidad == "Cardiología",
            Clinica.direccion.contains("Guayaquil"),
        )
    )
    .all()
)
for veterinario in veterinarios_and:
    print(
        f"{veterinario} | Clínica: "
        f"{veterinario.consultorio.clinica.nombre_comercial}"
    )

# Se libera la sesión después de completar las consultas relacionadas.
session.close()