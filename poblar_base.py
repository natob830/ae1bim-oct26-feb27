"""Carga datos variados en las cuatro entidades usando SQLAlchemy ORM.

El sembrado conserva cualquier registro preexistente y comprueba claves
naturales antes de insertar, por lo que ejecutar el archivo varias veces no
duplica los datos de ejemplo. En total deja al menos 4 clínicas, 8 consultorios,
10 veterinarios y 18 historias clínicas.
"""

from datetime import date

from sqlalchemy.orm import sessionmaker

from crear_base_entidades import (
    Clinica,
    Consultorio,
    HistoriaClinica,
    Veterinario,
    engine,
)

# Se crea una sesión ORM vinculada al motor SQLite del modelo.
Session = sessionmaker(bind=engine)
session = Session()

# Estos son los dos registros originales y dos clínicas adicionales de
# Guayaquil y Cuenca; se conservan los existentes y se completan los faltantes.
datos_clinicas = [
    {
        "nombre_comercial": "VetCare Loja",
        "direccion": "Av. Universitaria y 10 de Agosto, Loja, Ecuador",
        "ciudad": "Loja",
        "veterinario_responsable": "Dr. Carlos Mendoza",
    },
    {
        "nombre_comercial": "PetSalud Quito",
        "direccion": "Av. Amazonas N34-120, Quito, Ecuador",
        "ciudad": "Quito",
        "veterinario_responsable": "Dra. Elena Vargas",
    },
    {
        "nombre_comercial": "Animalia Guayaquil",
        "direccion": "Av. Francisco de Orellana 510, Guayaquil, Ecuador",
        "ciudad": "Guayaquil",
        "veterinario_responsable": "Dr. Andrés Cedeño",
    },
    {
        "nombre_comercial": "Huellas del Austro",
        "direccion": "Av. Solano 4-65, Cuenca, Ecuador",
        "ciudad": "Cuenca",
        "veterinario_responsable": "Dra. Verónica León",
    },
]

# Se reutilizan las clínicas por nombre comercial para hacer idempotente la carga.
clinicas = {}
for datos in datos_clinicas:
    # ciudad solo ayuda al sembrado a completar direcciones antiguas; no es
    # una columna nueva y por eso se excluye al construir el modelo Clinica.
    ciudad = datos["ciudad"]
    atributos_clinica = {
        clave: valor for clave, valor in datos.items() if clave != "ciudad"
    }
    clinica = (
        session.query(Clinica)
        .filter_by(nombre_comercial=datos["nombre_comercial"])
        .first()
    )
    if clinica is None:
        # Cada instancia representa una nueva fila de la tabla clinica.
        clinica = Clinica(**atributos_clinica)
        session.add(clinica)
    elif ciudad.lower() not in clinica.direccion.lower():
        # Se conserva la dirección existente y se añade la ciudad faltante.
        clinica.direccion = f"{clinica.direccion}, {ciudad}, Ecuador"
    clinicas[datos["nombre_comercial"]] = clinica

# flush asigna identificadores y permite insertar los consultorios relacionados
# dentro de la misma transacción, sin hacer commits parciales.
session.flush()

# Los tres consultorios originales se mantienen y se agregan cinco más.
datos_consultorios = [
    ("VetCare Loja", "Consultorio 101", "Medicina General"),
    ("VetCare Loja", "Consultorio 102", "Cirugía"),
    ("PetSalud Quito", "Consultorio 201", "Dermatología"),
    ("Animalia Guayaquil", "Consultorio 301", "Medicina General"),
    ("Animalia Guayaquil", "Consultorio 302", "Cardiología"),
    ("Animalia Guayaquil", "Consultorio 303", "Odontología Veterinaria"),
    ("Huellas del Austro", "Consultorio 401", "Dermatología"),
    ("Huellas del Austro", "Consultorio 402", "Oftalmología"),
]

# La combinación de clínica y nombre identifica cada consultorio en el sembrado.
consultorios = {}
for nombre_clinica, nombre, especialidad in datos_consultorios:
    clinica = clinicas[nombre_clinica]
    consultorio = (
        session.query(Consultorio)
        .filter_by(nombre=nombre, clinica_id=clinica.id)
        .first()
    )
    if consultorio is None:
        # La asignación ORM establece la clave foránea obligatoria clinica_id.
        consultorio = Consultorio(
            nombre=nombre,
            especialidad=especialidad,
            clinica=clinica,
        )
        session.add(consultorio)
    consultorios[(nombre_clinica, nombre)] = consultorio

session.flush()

# Se conservan los tres veterinarios iniciales y se distribuyen siete
# profesionales adicionales entre los consultorios de las cuatro ciudades.
datos_veterinarios = [
    ("VET-1001", "Carlos", "Mendoza", "cmendoza@vetcare.ec", "VetCare Loja", "Consultorio 101"),
    ("VET-1002", "Sofía", "Paredes", "sparedes@vetcare.ec", "VetCare Loja", "Consultorio 102"),
    ("VET-2001", "Elena", "Vargas", "evargas@petsalud.ec", "PetSalud Quito", "Consultorio 201"),
    ("VET-3001", "Andrés", "Cedeño", "acedeno@animalia.ec", "Animalia Guayaquil", "Consultorio 301"),
    ("VET-3002", "María José", "Loor", "mloor@animalia.ec", "Animalia Guayaquil", "Consultorio 301"),
    ("VET-3003", "Diego", "Macias", "dmacias@animalia.ec", "Animalia Guayaquil", "Consultorio 302"),
    ("VET-3004", "Paola", "Vera", "pvera@animalia.ec", "Animalia Guayaquil", "Consultorio 303"),
    ("VET-4001", "Verónica", "León", "vleon@huellasaustro.ec", "Huellas del Austro", "Consultorio 401"),
    ("VET-4002", "Mateo", "Cárdenas", "mcardenas@huellasaustro.ec", "Huellas del Austro", "Consultorio 402"),
    ("VET-4003", "Isabel", "Calle", "icalle@huellasaustro.ec", "Huellas del Austro", "Consultorio 402"),
]

# La licencia profesional se usa como identificador estable de cada veterinario.
veterinarios = {}
for licencia, nombres, apellidos, correo, nombre_clinica, nombre_consultorio in datos_veterinarios:
    veterinario = (
        session.query(Veterinario)
        .filter_by(licencia_profesional=licencia)
        .first()
    )
    if veterinario is None:
        # La relación consultorio asigna la FK y mantiene la integridad del modelo.
        veterinario = Veterinario(
            nombres=nombres,
            apellidos=apellidos,
            correo=correo,
            licencia_profesional=licencia,
            consultorio=consultorios[(nombre_clinica, nombre_consultorio)],
        )
        session.add(veterinario)
    veterinarios[licencia] = veterinario

session.flush()

# Cuatro historias originales y catorce nuevas incluyen fechas, diagnósticos,
# tratamientos y mascotas diferentes, repartidas entre varios veterinarios.
datos_historias = [
    ("VET-1001", date(2026, 10, 15), "Max", "Gastroenteritis leve", "Dieta blanda y probióticos por 5 días"),
    ("VET-1002", date(2026, 10, 18), "Luna", "Fractura de radio derecho", "Inmovilización y analgésicos"),
    ("VET-2001", date(2026, 11, 2), "Rocky", "Dermatitis alérgica", "Baños medicados y antihistamínico"),
    ("VET-1001", date(2026, 11, 10), "Toby", "Control de vacunación anual", "Refuerzo séxtuple y antirrábica"),
    ("VET-3001", date(2026, 9, 12), "Nube", "Otitis externa", "Limpieza ótica y gotas antibióticas por 7 días"),
    ("VET-3002", date(2026, 9, 19), "Simba", "Gingivitis moderada", "Profilaxis dental y control en 30 días"),
    ("VET-3003", date(2026, 10, 3), "Mora", "Soplo cardíaco grado II", "Ecocardiograma y seguimiento cardiológico"),
    ("VET-3004", date(2026, 10, 7), "Kira", "Acumulación de sarro dental", "Limpieza dental bajo anestesia"),
    ("VET-4001", date(2026, 10, 21), "Coco", "Dermatitis por pulgas", "Antiparasitario y champú dermatológico"),
    ("VET-4002", date(2026, 10, 26), "Pelusa", "Conjuntivitis bilateral", "Gotas oftálmicas y limpieza ocular"),
    ("VET-4003", date(2026, 11, 4), "Bruno", "Catarata incipiente", "Evaluación oftalmológica y control trimestral"),
    ("VET-3001", date(2026, 11, 8), "Canela", "Parvovirosis en recuperación", "Fluidoterapia y aislamiento domiciliario"),
    ("VET-1002", date(2026, 11, 12), "Manchas", "Luxación de rótula", "Reposo, antiinflamatorio y valoración quirúrgica"),
    ("VET-2001", date(2026, 11, 15), "Lola", "Alergia alimentaria", "Dieta hipoalergénica de eliminación por 8 semanas"),
    ("VET-3002", date(2026, 11, 16), "Firulais", "Control geriátrico", "Perfil sanguíneo y ajuste de dieta"),
    ("VET-4001", date(2026, 11, 17), "Chispa", "Sarna sarcóptica", "Tratamiento acaricida y desinfección del entorno"),
    ("VET-3003", date(2026, 11, 18), "Dante", "Insuficiencia cardíaca congestiva", "Tratamiento cardiológico y control en 15 días"),
    ("VET-4002", date(2026, 11, 19), "Milu", "Úlcera corneal superficial", "Antibiótico oftálmico y collar isabelino"),
]

# Veterinario, fecha y mascota evitan volver a agregar una atención ya sembrada.
for licencia, fecha, mascota, diagnostico, tratamiento in datos_historias:
    veterinario = veterinarios[licencia]
    historia_existente = (
        session.query(HistoriaClinica)
        .filter_by(
            veterinario_id=veterinario.id,
            fecha_atencion=fecha,
            nombre_mascota=mascota,
        )
        .first()
    )
    if historia_existente is None:
        # La relación veterinario guarda la FK requerida en historia_clinica.
        session.add(
            HistoriaClinica(
                fecha_atencion=fecha,
                diagnostico=diagnostico,
                tratamiento=tratamiento,
                nombre_mascota=mascota,
                veterinario=veterinario,
            )
        )

# Un único commit confirma todos los registros sin eliminar los datos anteriores.
session.commit()
print("Datos verificados e ingresados en las cuatro entidades.")
session.close()
