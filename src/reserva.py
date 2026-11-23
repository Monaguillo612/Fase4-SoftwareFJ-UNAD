"""
Módulo de gestión del ciclo de vida de Reservas con manejo avanzado de excepciones,
bloques try/except/else/finally y encadenamiento de excepciones (raise ... from).
"""

from src.entidad_base import EntidadBase
from src.cliente import Cliente
from src.servicios import Servicio
from src.excepciones import (
    ReservaInvalidaError,
    OperacionNoPermitidaError,
    ErrorSoftwareFJ,
)


class Reserva(EntidadBase):
    """Integra un Cliente, un Servicio, una duración y su ciclo de estados."""

    ESTADOS_VALIDOS = ("PENDIENTE", "CONFIRMADA", "PROCESADA", "CANCELADA")

    def __init__(self, codigo_id: str, cliente: Cliente, servicio: Servicio, duracion_horas: float, **opciones):
        super().__init__(codigo_id)
        if not isinstance(cliente, Cliente):
            raise ReservaInvalidaError("La reserva requiere una instancia válida de Cliente.")
        if not isinstance(servicio, Servicio):
            raise ReservaInvalidaError("La reserva requiere una instancia válida de Servicio.")
        if not isinstance(duracion_horas, (int, float)) or duracion_horas <= 0:
            raise ReservaInvalidaError("La duración de la reserva debe ser un valor numérico positivo.")

        self.__cliente = cliente
        self.__servicio = servicio
        self.__duracion_horas = float(duracion_horas)
        self.__opciones = opciones
        self.__estado = "PENDIENTE"
        self.__costo_total = 0.0
        self.validar()

    @property
    def cliente(self) -> Cliente:
        return self.__cliente

    @property
    def servicio(self) -> Servicio:
        return self.__servicio

    @property
    def duracion_horas(self) -> float:
        return self.__duracion_horas

    @property
    def estado(self) -> str:
        return self.__estado

    @property
    def costo_total(self) -> float:
        return self.__costo_total

    def confirmar(self) -> float:
        """
        Confirma la reserva verificando disponibilidad y calculando el costo total.
        Utiliza encadenamiento de excepciones (raise ... from) si falla la validación del servicio.
        """
        if self.__estado != "PENDIENTE":
            raise OperacionNoPermitidaError(
                f"No se puede confirmar la reserva {self.codigo_id} porque su estado actual es '{self.__estado}'."
            )
        try:
            self.__servicio.verificar_disponibilidad()
            self.__costo_total = self.__servicio.calcular_costo(self.__duracion_horas, **self.__opciones)
        except ErrorSoftwareFJ as err:
            # Encadenamiento de excepciones conservando la causa raíz original
            raise ReservaInvalidaError(
                f"Fallo al confirmar la reserva {self.codigo_id} para el servicio {self.__servicio.codigo_id}."
            ) from err
        else:
            self.__estado = "CONFIRMADA"
            return self.__costo_total

    def procesar(self) -> str:
        """Procesa una reserva previamente confirmada."""
        if self.__estado != "CONFIRMADA":
            raise OperacionNoPermitidaError(
                f"Solo se pueden procesar reservas en estado CONFIRMADA (estado actual: '{self.__estado}')."
            )
        self.__estado = "PROCESADA"
        return f"Reserva {self.codigo_id} procesada exitosamente. Total facturado: ${self.__costo_total:,.2f}"

    def cancelar(self, motivo: str = "Cancelación solicitada por el cliente") -> str:
        """Cancela una reserva siempre que no haya sido procesada ni cancelada previamente."""
        if self.__estado == "PROCESADA":
            raise OperacionNoPermitidaError(
                f"No se permite cancelar la reserva {self.codigo_id} porque ya fue PROCESADA."
            )
        if self.__estado == "CANCELADA":
            raise OperacionNoPermitidaError(f"La reserva {self.codigo_id} ya se encuentra CANCELADA.")
        self.__estado = "CANCELADA"
        return f"Reserva {self.codigo_id} cancelada. Motivo: {motivo}"

    def validar(self) -> bool:
        return self.__duracion_horas > 0 and self.__estado in self.ESTADOS_VALIDOS

    def obtener_resumen(self) -> str:
        return (
            f"Reserva[{self.codigo_id}] | Cliente: {self.__cliente.nombre} | "
            f"Servicio: {self.__servicio.nombre} | Duración: {self.__duracion_horas}h | "
            f"Estado: {self.__estado} | Total: ${self.__costo_total:,.2f}"
        )
