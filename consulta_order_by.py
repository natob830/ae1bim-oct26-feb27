"""Ejemplos de ordenamiento ascendente y descendente con el ORM."""

from sqlalchemy.orm import sessionmaker
from crear_base_entidades import Clinica, HistoriaClinica, Veterinario, engine

# Se crea la sesión necesaria para consultar SQLite.
Session = sessionmaker(bind=engine)
session = Session()

# asc() organiza veterinarios alfabéticamente por apellido.
print("=== CONSULTA CON order_by() - VETERINARIOS ORDENADOS POR APELLIDO ===")
veterinarios_ordenados = session.query(Veterinario).order_by(
    Veterinario.apellidos.asc()
).all()

for veterinario in veterinarios_ordenados:
    print(veterinario)

# desc() coloca primero la clínica con el nombre comercial más reciente
# en orden alfabético inverso (Z-A).
print("\n=== CLÍNICAS ORDENADAS POR NOMBRE COMERCIAL DESCENDENTE ===")
clinicas_descendentes = session.query(Clinica).order_by(
    Clinica.nombre_comercial.desc()
).all()
for clinica in clinicas_descendentes:
    print(clinica)

# desc() presenta primero las historias con fecha de atención más reciente.
print("\n=== HISTORIAS ORDENADAS POR FECHA MÁS RECIENTE ===")
historias_recientes = session.query(HistoriaClinica).order_by(
    HistoriaClinica.fecha_atencion.desc()
).all()
for historia in historias_recientes:
    print(
        f"{historia} | Veterinario: {historia.veterinario.nombres} "
        f"{historia.veterinario.apellidos}"
    )

# La sesión se cierra al finalizar los listados ordenados.
session.close()