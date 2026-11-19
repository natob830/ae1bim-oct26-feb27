"""Lista todas las entidades mediante consultas ORM con all().

La consulta principal presenta cada clínica y cuenta sus historias recorriendo
las relaciones Clínica → Consultorios → Veterinarios → Historias Clínicas.
"""

from sqlalchemy.orm import sessionmaker
from crear_base_entidades import (
    Clinica,
    Consultorio,
    HistoriaClinica,
    Veterinario,
    engine,
)

# La sesión permite ejecutar las consultas ORM contra la base SQLite.
Session = sessionmaker(bind=engine)
session = Session()

# Esta consulta principal conserva el requisito de listar clínicas y contar
# historias navegando objetos relacionados, sin consultas SQL manuales.
print("=== CONSULTA CON all() - CLÍNICAS Y TOTAL DE HISTORIAS CLÍNICAS ===")
clinicas = session.query(Clinica).all()

for clinica in clinicas:
    # Cada recorrido sigue las relaciones declaradas en el modelo ORM.
    total_historias = 0
    for consultorio in clinica.consultorios:
        for veterinario in consultorio.veterinarios:
            total_historias += len(veterinario.historias_clinicas)
    print(f"{clinica} -> Total Historias Clínicas asociadas: {total_historias}")

# all() obtiene todos los consultorios y se muestran sus datos de clínica.
print("\n=== TODOS LOS CONSULTORIOS Y SU CLÍNICA ===")
for consultorio in session.query(Consultorio).all():
    print(
        f"{consultorio} | Dirección de la clínica: "
        f"{consultorio.clinica.direccion}"
    )

# all() obtiene todos los veterinarios y se muestra su consultorio y clínica.
print("\n=== TODOS LOS VETERINARIOS Y SU CONSULTORIO ===")
for veterinario in session.query(Veterinario).all():
    print(
        f"{veterinario} | Consultorio: {veterinario.consultorio.nombre} | "
        f"Clínica: {veterinario.consultorio.clinica.nombre_comercial}"
    )

# all() obtiene todas las historias y presenta la cadena completa de relaciones.
print("\n=== TODAS LAS HISTORIAS CLÍNICAS Y SUS DATOS RELACIONADOS ===")
for historia in session.query(HistoriaClinica).all():
    veterinario = historia.veterinario
    print(
        f"{historia} | Veterinario: {veterinario.nombres} "
        f"{veterinario.apellidos} | Consultorio: "
        f"{veterinario.consultorio.nombre} | Clínica: "
        f"{veterinario.consultorio.clinica.nombre_comercial}"
    )
    print("==================================================================");

# Se cierra la sesión una vez terminadas todas las consultas.
session.close()