# Fase 4 – Sistema Integral de Gestión Software FJ (POO y Manejo de Excepciones)

**Universidad Nacional Abierta y a Distancia – UNAD**  
**Programa:** Ingeniería de Sistemas  
**Curso:** Programación – Código `213023` (Grupo `213023_503`)  
**Autor:** David Esteban Bravo Martin (C.C. `1032356002`)  
**Tutor:** Jorge Eduardo Ospina  

## Descripción del Proyecto
Aplicación orientada a objetos desarrollada en **Python 3** sin uso de motores de bases de datos para la empresa **Software FJ**, encargada de gestionar clientes, servicios especializados (*Reservas de Salas*, *Alquiler de Equipos* y *Asesorías Especializadas*) y reservas en memoria, garantizando estabilidad continua ante errores mediante manejo avanzado de excepciones y registro de auditoría (`logging`).

## Arquitectura del Repositorio
```text
Fase4-SoftwareFJ-UNAD/
├── main.py                  # Orquestador de las 12 simulaciones (válidas e inválidas)
├── README.md                # Documentación técnica del repositorio
├── .gitignore               # Exclusiones de Python (__pycache__, .venv)
├── logs/
│   └── software_fj.log      # Archivo de auditoría generado automáticamente
└── src/
    ├── __init__.py
    ├── logger_config.py     # Configuración de logging (archivo + consola)
    ├── excepciones.py       # Jerarquía de 8 excepciones personalizadas
    ├── entidad_base.py      # Clase abstracta EntidadBase (ABC)
    ├── cliente.py           # Encapsulación y validaciones Regex de Cliente
    ├── servicios.py         # Clase abstracta Servicio y 3 subclases polimórficas
    ├── reserva.py           # Ciclo de vida de Reserva con raise ... from
    └── gestor_sistema.py    # Gestión en memoria con try/except/else/finally
```

## Ejecución
```bash
python main.py
```
Al finalizar, verifique el registro completo de eventos y errores en `logs/software_fj.log`.
