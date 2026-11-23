"""
Punto de entrada principal - Fase 4 Programación (213023) - UNAD.
Ejecuta 12 simulaciones completas (operaciones válidas e inválidas) sobre Software FJ
demostrando estabilidad continua, POO, manejo avanzado de excepciones y logging.

Autor: David Esteban Bravo Martin (CC: 1032356002)
"""

from src.gestor_sistema import GestorSoftwareFJ
from src.servicios import ReservaSala, AlquilerEquipo, AsesoriaEspecializada
from src.excepciones import ErrorSoftwareFJ


def ejecutar_simulaciones() -> None:
    gestor = GestorSoftwareFJ(archivo_log="logs/software_fj.log")

    print("\n" + "=" * 75)
    print("  SISTEMA INTEGRAL SOFTWARE FJ - SIMULACIÓN DE 12 OPERACIONES COMPLETAS")
    print("=" * 75)

    # SIMULACIÓN 1: Registro válido de clientes
    c1 = gestor.registrar_cliente("CLI-01", "David Esteban Bravo Martin", "1032356002", "david.bravo@softwarefj.co", "3104567890")
    c2 = gestor.registrar_cliente("CLI-02", "Laura Camila Torres", "1023456789", "laura.torres@empresa.co", "3159876543")

    # SIMULACIÓN 2: Registro inválido de cliente (correo y teléfono mal formados)
    gestor.registrar_cliente("CLI-03", "Carlos Ruiz", "10112233", "correo_invalido_sin_arroba", "123")

    # SIMULACIÓN 3: Registro duplicado de cliente (mismo documento)
    gestor.registrar_cliente("CLI-04", "David Duplicado", "1032356002", "otro@correo.co", "3112223344")

    # SIMULACIÓN 4: Creación válida de 3 servicios especializados (Herencia + Polimorfismo)
    s_sala = ReservaSala("SRV-01", "Sala Ejecutiva Bogotá", 120000, capacidad_max=12, disponible=True)
    s_equipo = AlquilerEquipo("SRV-02", "Portátil Workstation i7", 45000, stock_disponible=5, disponible=True)
    s_asesoria = AsesoriaEspecializada("SRV-03", "Consultoría Arquitectura Python", 180000, especialidad="Backend POO", disponible=True)
    s_inactivo = ReservaSala("SRV-04", "Auditorio Principal (Mantenimiento)", 300000, capacidad_max=50, disponible=False)

    for srv in (s_sala, s_equipo, s_asesoria, s_inactivo):
        gestor.registrar_servicio(srv)

    # SIMULACIÓN 5: Creación inválida de servicio (tarifa negativa capturada con try/except)
    try:
        AlquilerEquipo("SRV-ERR", "Proyector 4K", -50000, stock_disponible=2)
    except ErrorSoftwareFJ as e:
        gestor.logger.error(f"Simulación 5 - Creación inválida de servicio interceptada: {e}")

    # SIMULACIÓN 6: Reserva exitosa de Sala con sobrecarga de parámetros (catering + descuento 10% + IVA)
    r1 = gestor.crear_y_confirmar_reserva(
        "RES-01", c1, s_sala, duracion_horas=4, asistentes=8, incluir_catering=True, descuento_pct=10.0, aplicar_iva=True
    )

    # SIMULACIÓN 7: Reserva fallida por exceder capacidad máxima de sala (encadenamiento raise ... from)
    gestor.crear_y_confirmar_reserva("RES-02", c2, s_sala, duracion_horas=3, asistentes=25)

    # SIMULACIÓN 8: Reserva exitosa de Alquiler de Equipos con seguro y sin IVA (exento)
    r3 = gestor.crear_y_confirmar_reserva(
        "RES-03", c2, s_equipo, duracion_horas=6, cantidad_equipos=3, incluir_seguro=True, aplicar_iva=False
    )

    # SIMULACIÓN 9: Reserva fallida por servicio NO disponible (mantenimiento)
    gestor.crear_y_confirmar_reserva("RES-04", c1, s_inactivo, duracion_horas=2, asistentes=10)

    # SIMULACIÓN 10: Reserva fallida por cálculo inconsistente (descuento del 80% no permitido)
    gestor.crear_y_confirmar_reserva(
        "RES-05", c1, s_asesoria, duracion_horas=5, nivel_consultor="arquitecto", urgente=True, descuento_pct=80.0
    )

    # SIMULACIÓN 11: Reserva exitosa de Asesoría Especializada urgente + procesamiento + intento de cancelación prohibida
    r6 = gestor.crear_y_confirmar_reserva(
        "RES-06", c1, s_asesoria, duracion_horas=4, nivel_consultor="arquitecto", urgente=True, descuento_pct=5.0
    )
    gestor.procesar_reserva(r6)
    gestor.cancelar_reserva(r6, motivo="Intento de cancelación tras procesamiento")

    # SIMULACIÓN 12: Cancelación exitosa de reserva confirmada (RES-03) y verificación de doble cancelación
    gestor.cancelar_reserva(r3, motivo="Reprogramación de proyecto del cliente")
    gestor.cancelar_reserva(r3, motivo="Segundo intento de cancelación")

    gestor.logger.info(
        f"=== Simulación finalizada SIN INTERRUPCIONES | "
        f"Clientes: {len(gestor.clientes)} | Servicios: {len(gestor.servicios)} | Reservas válidas: {len(gestor.reservas)} ==="
    )


if __name__ == "__main__":
    ejecutar_simulaciones()
