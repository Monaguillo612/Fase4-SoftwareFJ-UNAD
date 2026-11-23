"""
Clase abstracta base que define la estructura común de todas las entidades del sistema.
"""

from abc import ABC, abstractmethod
from datetime import datetime
from src.excepciones import DatosInvalidosError


class EntidadBase(ABC):
    """Clase abstracta que representa cualquier entidad identificable de Software FJ."""

    def __init__(self, codigo_id: str):
        if not isinstance(codigo_id, str) or not codigo_id.strip():
            raise DatosInvalidosError("El identificador de la entidad debe ser una cadena no vacía.")
        self.__codigo_id = codigo_id.strip().upper()
        self.__fecha_creacion = datetime.now()

    @property
    def codigo_id(self) -> str:
        """Retorna el identificador único encapsulado de la entidad."""
        return self.__codigo_id

    @property
    def fecha_creacion(self) -> datetime:
        """Retorna la marca temporal de creación de la entidad."""
        return self.__fecha_creacion

    @abstractmethod
    def validar(self) -> bool:
        """Valida la integridad de los atributos propios de la entidad."""
        pass

    @abstractmethod
    def obtener_resumen(self) -> str:
        """Retorna una descripción legible del estado actual de la entidad."""
        pass
