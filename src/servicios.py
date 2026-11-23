"""
Jerarquía de servicios de Software FJ aplicando herencia, polimorfismo y sobrecarga de métodos.
Incluye la clase abstracta Servicio y tres servicios especializados:
ReservaSala, AlquilerEquipo y AsesoriaEspecializada.
"""

from abc import abstractmethod
from src.entidad_base import EntidadBase
from src.excepciones import (
    ServicioInvalidoError,
    ServicioNoDisponibleError,
    CalculoInconsistenteError,
)


class Servicio(EntidadBase):
    """Clase abstracta base para todos los servicios ofertados por Software FJ."""

    def __init__(self, codigo_id: str, nombre: str, tarifa_base_hora: float, disponible: bool = True):
        super().__init__(codigo_id)
        if not isinstance(nombre, str) or len(nombre.strip()) < 3:
            raise ServicioInvalidoError("El nombre del servicio debe tener al menos 3 caracteres.")
        if not isinstance(tarifa_base_hora, (int, float)) or tarifa_base_hora <= 0:
            raise ServicioInvalidoError("La tarifa base por hora debe ser un número positivo mayor a cero.")

        self.__nombre = nombre.strip()
        self.__tarifa_base_hora = float(tarifa_base_hora)
        self.__disponible = bool(disponible)

    @property
    def nombre(self) -> str:
        return self.__nombre

    @property
    def tarifa_base_hora(self) -> float:
        return self.__tarifa_base_hora

    @property
    def disponible(self) -> bool:
        return self.__disponible

    @disponible.setter
    def disponible(self, estado: bool) -> None:
        self.__disponible = bool(estado)

    def verificar_disponibilidad(self) -> None:
        """Lanza ServicioNoDisponibleError si el servicio no está habilitado."""
        if not self.__disponible:
            raise ServicioNoDisponibleError(f"El servicio '{self.__nombre}' ({self.codigo_id}) no está disponible.")

    @abstractmethod
    def validar_parametros(self, duracion_horas: float, **kwargs) -> bool:
        """Valida parámetros específicos del servicio antes de procesar una reserva."""
        pass

    @abstractmethod
    def calcular_costo(self, duracion_horas: float, descuento_pct: float = 0.0, aplicar_iva: bool = True, **kwargs) -> float:
        """
        Método polimórfico y sobrecargado mediante parámetros opcionales para calcular el costo total.
        Soporta descuentos, aplicación de IVA (19%) y cargos propios de cada subclase.
        """
        pass

    @abstractmethod
    def describir_servicio(self) -> str:
        """Retorna una descripción detallada propia del tipo de servicio."""
        pass

    def _aplicar_ajustes_financieros(self, subtotal: float, descuento_pct: float, aplicar_iva: bool) -> float:
        """Aplica descuentos e IVA validando consistencia matemática."""
        if not (0.0 <= descuento_pct <= 50.0):
            raise CalculoInconsistenteError(
                f"El porcentaje de descuento ({descuento_pct}%) debe estar entre 0% y 50%."
            )
        total = subtotal * (1 - descuento_pct / 100.0)
        if aplicar_iva:
            total *= 1.19
        if total <= 0:
            raise CalculoInconsistenteError("El costo calculado no puede ser menor o igual a cero.")
        return round(total, 2)

    def validar(self) -> bool:
        return self.__tarifa_base_hora > 0 and len(self.__nombre) >= 3

    def obtener_resumen(self) -> str:
        estado = "Disponible" if self.__disponible else "No disponible"
        return f"{self.describir_servicio()} | Tarifa: ${self.__tarifa_base_hora:,.0f}/h | Estado: {estado}"


class ReservaSala(Servicio):
    """Servicio especializado para reserva de salas de reuniones y auditorios."""

    def __init__(self, codigo_id: str, nombre: str, tarifa_base_hora: float, capacidad_max: int, disponible: bool = True):
        super().__init__(codigo_id, nombre, tarifa_base_hora, disponible)
        if not isinstance(capacidad_max, int) or capacidad_max <= 0:
            raise ServicioInvalidoError("La capacidad máxima de la sala debe ser un entero positivo.")
        self.__capacidad_max = capacidad_max

    @property
    def capacidad_max(self) -> int:
        return self.__capacidad_max

    def validar_parametros(self, duracion_horas: float, **kwargs) -> bool:
        asistentes = kwargs.get("asistentes", 1)
        if not isinstance(duracion_horas, (int, float)) or not (1 <= duracion_horas <= 12):
            raise ServicioInvalidoError("La duración de reserva de sala debe estar entre 1 y 12 horas.")
        if not isinstance(asistentes, int) or asistentes <= 0 or asistentes > self.__capacidad_max:
            raise ServicioInvalidoError(
                f"El número de asistentes ({asistentes}) excede la capacidad máxima de la sala ({self.__capacidad_max})."
            )
        return True

    def calcular_costo(self, duracion_horas: float, descuento_pct: float = 0.0, aplicar_iva: bool = True, **kwargs) -> float:
        self.validar_parametros(duracion_horas, **kwargs)
        catering = kwargs.get("incluir_catering", False)
        asistentes = kwargs.get("asistentes", 1)
        subtotal = self.tarifa_base_hora * duracion_horas
        if catering:
            subtotal += asistentes * 15000.0
        return self._aplicar_ajustes_financieros(subtotal, descuento_pct, aplicar_iva)

    def describir_servicio(self) -> str:
        return f"ReservaSala[{self.codigo_id}] {self.nombre} (Capacidad máx: {self.__capacidad_max} personas)"


class AlquilerEquipo(Servicio):
    """Servicio especializado para alquiler de equipos tecnológicos (portátiles, proyectores, servidores)."""

    def __init__(self, codigo_id: str, nombre: str, tarifa_base_hora: float, stock_disponible: int, disponible: bool = True):
        super().__init__(codigo_id, nombre, tarifa_base_hora, disponible)
        if not isinstance(stock_disponible, int) or stock_disponible < 0:
            raise ServicioInvalidoError("El stock de equipos debe ser un número entero no negativo.")
        self.__stock_disponible = stock_disponible
        if stock_disponible == 0:
            self.disponible = False

    @property
    def stock_disponible(self) -> int:
        return self.__stock_disponible

    def validar_parametros(self, duracion_horas: float, **kwargs) -> bool:
        cantidad = kwargs.get("cantidad_equipos", 1)
        if not isinstance(duracion_horas, (int, float)) or duracion_horas <= 0:
            raise ServicioInvalidoError("La duración del alquiler debe ser mayor a cero horas.")
        if not isinstance(cantidad, int) or cantidad <= 0:
            raise ServicioInvalidoError("La cantidad de equipos a alquilar debe ser al menos 1.")
        if cantidad > self.__stock_disponible:
            raise ServicioNoDisponibleError(
                f"Stock insuficiente para '{self.nombre}': solicitados {cantidad}, disponibles {self.__stock_disponible}."
            )
        return True

    def calcular_costo(self, duracion_horas: float, descuento_pct: float = 0.0, aplicar_iva: bool = True, **kwargs) -> float:
        self.validar_parametros(duracion_horas, **kwargs)
        cantidad = kwargs.get("cantidad_equipos", 1)
        seguro = kwargs.get("incluir_seguro", False)
        subtotal = self.tarifa_base_hora * duracion_horas * cantidad
        if seguro:
            subtotal += 25000.0 * cantidad
        return self._aplicar_ajustes_financieros(subtotal, descuento_pct, aplicar_iva)

    def describir_servicio(self) -> str:
        return f"AlquilerEquipo[{self.codigo_id}] {self.nombre} (Stock: {self.__stock_disponible} uds)"


class AsesoriaEspecializada(Servicio):
    """Servicio especializado de consultoría técnica en arquitectura, TI y ciberseguridad."""

    _NIVELES_VALIDOS = {"junior", "senior", "arquitecto"}

    def __init__(self, codigo_id: str, nombre: str, tarifa_base_hora: float, especialidad: str, disponible: bool = True):
        super().__init__(codigo_id, nombre, tarifa_base_hora, disponible)
        if not isinstance(especialidad, str) or not especialidad.strip():
            raise ServicioInvalidoError("La especialidad de la asesoría es obligatoria.")
        self.__especialidad = especialidad.strip()

    @property
    def especialidad(self) -> str:
        return self.__especialidad

    def validar_parametros(self, duracion_horas: float, **kwargs) -> bool:
        nivel = str(kwargs.get("nivel_consultor", "senior")).lower()
        if not isinstance(duracion_horas, (int, float)) or not (1 <= duracion_horas <= 40):
            raise ServicioInvalidoError("La asesoría especializada debe contratarse entre 1 y 40 horas.")
        if nivel not in self._NIVELES_VALIDOS:
            raise ServicioInvalidoError(f"Nivel de consultor '{nivel}' inválido. Use: {self._NIVELES_VALIDOS}.")
        return True

    def calcular_costo(self, duracion_horas: float, descuento_pct: float = 0.0, aplicar_iva: bool = True, **kwargs) -> float:
        self.validar_parametros(duracion_horas, **kwargs)
        urgente = kwargs.get("urgente", False)
        nivel = str(kwargs.get("nivel_consultor", "senior")).lower()
        factor_nivel = {"junior": 0.9, "senior": 1.0, "arquitecto": 1.35}[nivel]
        subtotal = self.tarifa_base_hora * duracion_horas * factor_nivel
        if urgente:
            subtotal *= 1.25  # Recargo del 25% por atención prioritaria
        return self._aplicar_ajustes_financieros(subtotal, descuento_pct, aplicar_iva)

    def describir_servicio(self) -> str:
        return f"AsesoriaEspecializada[{self.codigo_id}] {self.nombre} (Área: {self.__especialidad})"
