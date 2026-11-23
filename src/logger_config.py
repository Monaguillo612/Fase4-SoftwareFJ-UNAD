"""
Módulo de configuración de auditoría y registro de logs (logging).
Garantiza la trazabilidad de eventos operativos y errores sin usar bases de datos.
"""

import logging
import os


def configurar_logger(nombre: str = "SoftwareFJ", archivo_log: str = "logs/software_fj.log") -> logging.Logger:
    """Configura y retorna un logger que escribe simultáneamente en archivo y consola."""
    directorio = os.path.dirname(archivo_log)
    if directorio:
        os.makedirs(directorio, exist_ok=True)

    logger = logging.getLogger(nombre)
    logger.setLevel(logging.DEBUG)

    # Evitar duplicación de handlers si se invoca múltiples veces
    if not logger.handlers:
        formato = logging.Formatter(
            fmt="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )

        # Handler de archivo persistente (UTF-8)
        file_handler = logging.FileHandler(archivo_log, mode="w", encoding="utf-8")
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formato)

        # Handler de consola para seguimiento interactivo
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(formato)

        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

    return logger
