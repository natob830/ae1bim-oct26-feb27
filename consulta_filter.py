"""Ejemplos de filtros ORM para consultar distintas entidades del modelo."""

from datetime import date

from sqlalchemy.orm import sessionmaker
from crear_base_entidades import Clinica, Consultorio, HistoriaClinica, engine

# Se abre la sesión ORM para realizar las tres búsquedas filtradas.
Session = sessionmaker(bind=engine)
session = Session()

# filter() selecciona consultorios cuya especialidad es dermatología.
print("=== CONSULTA CON filter() - CONSULTORIOS DE ESPECIALIDAD DERMATOLOGÍA ===")
consultorios_dermatologia = session.query(Consultorio).filter(
    Consultorio.especialidad == "Dermatología"
).all()

for consultorio in consultorios_dermatologia:
    print(f"{consultorio} | Clínica: {consultorio.clinica.nombre_comercial}")

# filter() busca clínicas cuya dirección contiene el nombre de una ciudad.
print("\n=== CLÍNICAS UBICADAS EN QUITO ===")
clinicas_quito = session.query(Clinica).filter(
    Clinica.direccion.contains("Quito")
).all()
for clinica in clinicas_quito:
    print(clinica)

# filter() selecciona historias atendidas desde una fecha determinada.
print("\n=== HISTORIAS CLÍNICAS DESDE EL 1 DE NOVIEMBRE DE 2026 ===")
historias_recientes = session.query(HistoriaClinica).filter(
    HistoriaClinica.fecha_atencion >= date(2026, 11, 1)
).all()
for historia in historias_recientes:
    print(
        f"{historia} | Veterinario: {historia.veterinario.nombres} "
        f"{historia.veterinario.apellidos}"
    )
    print("==================================================================");

# Se libera la conexión al terminar las consultas.
session.close()