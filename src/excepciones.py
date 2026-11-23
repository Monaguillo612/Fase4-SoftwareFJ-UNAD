"""
Jerarquía de excepciones personalizadas para el sistema de gestión Software FJ.
Permite discriminar fallos de dominio, validaciones, disponibilidad y cálculos.
"""


class ErrorSoftwareFJ(Exception):
    """Excepción base de toda la aplicación Software FJ."""

    def __init__(self, mensaje: str, codigo: str = "ERR-000"):
        self.codigo = codigo
        super().__init__(f"[{codigo}] {mensaje}")


class DatosInvalidosError(ErrorSoftwareFJ):
    """Se lanza cuando un parámetro obligatorio falta o tiene un formato inválido."""

    def __init__(self, mensaje: str):
        super().__init__(mensaje, codigo="ERR-DATOS")


class ClienteInvalidoError(DatosInvalidosError):
    """Se lanza cuando los datos de identificación o contacto de un cliente son incorrectos."""

    def __init__(self, mensaje: str):
        super().__init__(mensaje)
        self.codigo = "ERR-CLIENTE"


class ServicioInvalidoError(DatosInvalidosError):
    """Se lanza cuando los parámetros de creación o configuración de un servicio son inválidos."""

    def __init__(self, mensaje: str):
        super().__init__(mensaje)
        self.codigo = "ERR-SERVICIO"


class ServicioNoDisponibleError(ErrorSoftwareFJ):
    """Se lanza al intentar reservar un servicio inactivo, sin cupo o fuera de disponibilidad."""

    def __init__(self, mensaje: str):
        super().__init__(mensaje, codigo="ERR-DISP")


class ReservaInvalidaError(ErrorSoftwareFJ):
    """Se lanza ante duraciones inválidas, estados inconsistentes o errores de reserva."""

    def __init__(self, mensaje: str):
        super().__init__(mensaje, codigo="ERR-RESERVA")


class OperacionNoPermitidaError(ErrorSoftwareFJ):
    """Se lanza cuando una transición de estado o acción no está permitida por reglas de negocio."""

    def __init__(self, mensaje: str):
        super().__init__(mensaje, codigo="ERR-OPERACION")


class CalculoInconsistenteError(ErrorSoftwareFJ):
    """Se lanza cuando un cálculo de costo produce resultados negativos o parámetros incoherentes."""

    def __init__(self, mensaje: str):
        super().__init__(mensaje, codigo="ERR-CALCULO")
