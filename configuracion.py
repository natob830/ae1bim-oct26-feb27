"""Configuración compartida de la conexión SQLite para la aplicación veterinaria."""

# SQLAlchemy crea/abre veterinaria.db en el directorio desde el que se ejecuta
# el proyecto, de modo que todos los scripts trabajen sobre la misma base local.
cadena_base_datos = "sqlite:///veterinaria.db"
