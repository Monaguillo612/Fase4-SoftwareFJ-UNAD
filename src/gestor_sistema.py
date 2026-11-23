"""
Controlador principal del sistema Software FJ (en memoria, sin bases de datos).
Gestiona listas internas de clientes, servicios y reservas con manejo integral de excepciones y logging.
"""

from typing import List, Optional
from src.cliente import Cliente
from src.servicios import Servicio
from src.reserva import Reserva
from src.excepciones import ErrorSoftwareFJ, OperacionNoPermitidaError
from src.logger_config import configurar_logger


class GestorSoftwareFJ:
    """Administra en memoria todas las operaciones de Software FJ con resiliencia ante fallos."""

    def __init__(self, archivo_log: str = "logs/software_fj.log"):
        self.__clientes: List[Cliente] = []
        self.__servicios: List[Servicio] = []
        self.__reservas: List[Reserva] = []
        self.logger = configurar_logger(archivo_log=archivo_log)
        self.logger.info("=== Inicialización del Sistema Integral Software FJ (Modo en Memoria) ===")

    @property
    def clientes(self) -> List[Cliente]:
        return list(self.__clientes)

    @property
    def servicios(self) -> List[Servicio]:
        return list(self.__servicios)

    @property
    def reservas(self) -> List[Reserva]:
        return list(self.__reservas)

    def registrar_cliente(self, codigo_id: str, nombre: str, documento: str, correo: str, telefono: str) -> Optional[Cliente]:
        """Registra un cliente validando duplicados con try/except/else/finally."""
        cliente_creado = None
        try:
            if any(c.codigo_id == codigo_id.strip().upper() or c.documento == documento.strip() for c in self.__clientes):
                raise OperacionNoPermitidaError(f"Ya existe un cliente registrado con ID '{codigo_id}' o documento '{documento}'.")
            cliente_creado = Cliente(codigo_id, nombre, documento, correo, telefono)
        except ErrorSoftwareFJ as e:
            self.logger.error(f"Error al registrar cliente '{codigo_id}': {e}")
        except Exception as e:
            self.logger.critical(f"Error inesperado al registrar cliente '{codigo_id}': {e}")
        else:
            self.__clientes.append(cliente_creado)
            self.logger.info(f"Cliente registrado correctamente -> {cliente_creado.obtener_resumen()}")
        finally:
            self.logger.debug(f"[FIN OPERACIÓN] Total clientes activos en memoria: {len(self.__clientes)}")
        return cliente_creado

    def registrar_servicio(self, servicio: Servicio) -> bool:
        """Agrega un servicio especializado a la lista interna."""
        exito = False
        try:
            if not isinstance(servicio, Servicio):
                raise OperacionNoPermitidaError("El objeto proporcionado no hereda de la clase abstracta Servicio.")
            if any(s.codigo_id == servicio.codigo_id for s in self.__servicios):
                raise OperacionNoPermitidaError(f"El servicio con código '{servicio.codigo_id}' ya existe.")
            self.__servicios.append(servicio)
            exito = True
        except ErrorSoftwareFJ as e:
            self.logger.error(f"Error al registrar servicio: {e}")
        else:
            self.logger.info(f"Servicio registrado correctamente -> {servicio.obtener_resumen()}")
        finally:
            self.logger.debug(f"[FIN OPERACIÓN] Total servicios en catálogo: {len(self.__servicios)}")
        return exito

    def crear_y_confirmar_reserva(
        self, codigo_id: str, cliente: Cliente, servicio: Servicio, duracion_horas: float, **opciones
    ) -> Optional[Reserva]:
        """Crea y confirma una reserva capturando excepciones encadenadas sin detener la aplicación."""
        reserva = None
        try:
            reserva = Reserva(codigo_id, cliente, servicio, duracion_horas, **opciones)
            costo = reserva.confirmar()
        except ErrorSoftwareFJ as e:
            causa = f" | Causa raíz: {e.__cause__}" if e.__cause__ else ""
            self.logger.error(f"Fallo en reserva '{codigo_id}': {e}{causa}")
            reserva = None
        except Exception as e:
            self.logger.critical(f"Fallo inesperado en reserva '{codigo_id}': {e}")
            reserva = None
        else:
            self.__reservas.append(reserva)
            self.logger.info(f"Reserva CONFIRMADA -> {reserva.obtener_resumen()} (Costo: ${costo:,.2f})")
        finally:
            self.logger.debug(f"[FIN OPERACIÓN] Total reservas registradas: {len(self.__reservas)}")
        return reserva

    def procesar_reserva(self, reserva: Optional[Reserva]) -> bool:
        """Procesa una reserva confirmada controlando transiciones inválidas."""
        try:
            if reserva is None:
                raise OperacionNoPermitidaError("No es posible procesar una referencia de reserva nula (None).")
            mensaje = reserva.procesar()
        except ErrorSoftwareFJ as e:
            self.logger.warning(f"No se pudo procesar reserva: {e}")
            return False
        else:
            self.logger.info(mensaje)
            return True

    def cancelar_reserva(self, reserva: Optional[Reserva], motivo: str) -> bool:
        """Cancela una reserva controlando si ya fue procesada o cancelada."""
        try:
            if reserva is None:
                raise OperacionNoPermitidaError("No es posible cancelar una referencia de reserva nula (None).")
            mensaje = reserva.cancelar(motivo)
        except ErrorSoftwareFJ as e:
            self.logger.warning(f"No se pudo cancelar reserva: {e}")
            return False
        else:
            self.logger.info(mensaje)
            return True
