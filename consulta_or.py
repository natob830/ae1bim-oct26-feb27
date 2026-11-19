"""Ejemplos de búsquedas alternativas usando la expresión lógica or_()."""

from sqlalchemy import or_
from sqlalchemy.orm import sessionmaker
from crear_base_entidades import (
    Consultorio,
    HistoriaClinica,
    Veterinario,
    engine,
)

# La sesión ORM proporciona acceso común a todas las entidades.
Session = sessionmaker(bind=engine)
session = Session()

# or_() devuelve historias cuya mascota es Max o Luna.
print("=== CONSULTA CON or_() - HISTORIAS CLÍNICAS DE MAX O LUNA ===")
historias_or = session.query(HistoriaClinica).filter(
    or_(
        HistoriaClinica.nombre_mascota == "Max",
        HistoriaClinica.nombre_mascota == "Luna"
    )
).all()

for historia in historias_or:
    print(
        f"{historia} | Veterinario: {historia.veterinario.nombres} "
        f"{historia.veterinario.apellidos}"
    )

# or_() busca consultorios que ofrecen cardiología o dermatología.
print("\n=== CONSULTORIOS DE CARDIOLOGÍA O DERMATOLOGÍA ===")
consultorios_or = session.query(Consultorio).filter(
    or_(
        Consultorio.especialidad == "Cardiología",
        Consultorio.especialidad == "Dermatología",
    )
).all()
for consultorio in consultorios_or:
    print(f"{consultorio} | Clínica: {consultorio.clinica.nombre_comercial}")

# or_() filtra veterinarios por uno de dos apellidos.
print("\n=== VETERINARIOS DE APELLIDO MENDOZA O VARGAS ===")
veterinarios_or = session.query(Veterinario).filter(
    or_(
        Veterinario.apellidos == "Mendoza",
        Veterinario.apellidos == "Vargas",
    )
).all()
for veterinario in veterinarios_or:
    print(
        f"{veterinario} | Consultorio: {veterinario.consultorio.nombre}"
    )

# Se cierra la sesión al terminar las búsquedas.
session.close()