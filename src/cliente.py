"""
Módulo de gestión de clientes con encapsulación estricta y validaciones de formato.
"""

import re
from src.entidad_base import EntidadBase
from src.excepciones import ClienteInvalidoError


class Cliente(EntidadBase):
    """Representa un cliente registrado en Software FJ."""

    _PATRON_CORREO = re.compile(r"^[\w.-]+@[\w.-]+\.[a-zA-Z]{2,}$")
    _PATRON_TELEFONO = re.compile(r"^\d{7,15}$")

    def __init__(self, codigo_id: str, nombre: str, documento: str, correo: str, telefono: str):
        super().__init__(codigo_id)
        self.__nombre = ""
        self.__documento = ""
        self.__correo = ""
        self.__telefono = ""

        # Asignación mediante setters validados (encapsulación)
        self.nombre = nombre
        self.documento = documento
        self.correo = correo
        self.telefono = telefono
        self.validar()

    @property
    def nombre(self) -> str:
        return self.__nombre

    @nombre.setter
    def nombre(self, valor: str) -> None:
        if not isinstance(valor, str) or len(valor.strip()) < 3:
            raise ClienteInvalidoError("El nombre del cliente debe contener al menos 3 caracteres.")
        self.__nombre = valor.strip()

    @property
    def documento(self) -> str:
        return self.__documento

    @documento.setter
    def documento(self, valor: str) -> None:
        if not isinstance(valor, str) or not valor.strip().isdigit() or not (6 <= len(valor.strip()) <= 15):
            raise ClienteInvalidoError("El documento de identidad debe ser numérico (entre 6 y 15 dígitos).")
        self.__documento = valor.strip()

    @property
    def correo(self) -> str:
        return self.__correo

    @correo.setter
    def correo(self, valor: str) -> None:
        if not isinstance(valor, str) or not self._PATRON_CORREO.match(valor.strip()):
            raise ClienteInvalidoError(f"El correo electrónico '{valor}' no tiene un formato válido.")
        self.__correo = valor.strip().lower()

    @property
    def telefono(self) -> str:
        return self.__telefono

    @telefono.setter
    def telefono(self, valor: str) -> None:
        limpio = str(valor).strip().replace(" ", "").replace("-", "")
        if not self._PATRON_TELEFONO.match(limpio):
            raise ClienteInvalidoError(f"El teléfono '{valor}' debe contener entre 7 y 15 dígitos numéricos.")
        self.__telefono = limpio

    def validar(self) -> bool:
        """Verifica que todos los campos obligatorios del cliente estén diligenciados."""
        if not all([self.__nombre, self.__documento, self.__correo, self.__telefono]):
            raise ClienteInvalidoError("Existen atributos obligatorios vacíos en el cliente.")
        return True

    def obtener_resumen(self) -> str:
        return f"Cliente[{self.codigo_id}] {self.__nombre} (Doc: {self.__documento} | Email: {self.__correo})"
