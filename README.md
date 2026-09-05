# Sistema de Gestion para Taller Mecanico "LA RUEDA"

Modulo implementado: **Gestion de inventario de repuestos** (RF-09, RF-10, RF-11).
Asignatura: Ingenieria de Software - Universidad Estatal Amazonica. Grupo 13.

## Stack
- Lenguaje: Python 3.12
- Framework de pruebas: pytest
- Integracion continua: GitHub Actions

## Estructura
```
src/inventario.py   Reglas del inventario (descuento de stock y alerta de minimo)
src/orden.py        Orden de trabajo y calculo de presupuesto (subtotal, IVA, total)
tests/              Pruebas automatizadas (unitarias, integracion y aceptacion)
.github/workflows/  Pipeline de integracion continua
```

## Ejecutar las pruebas en local
```bash
pip install -r requirements.txt
pytest -v
```

## Flujo de ramas
- `main`: version estable y entregable.
- `develop`: integracion de los avances.
- `feature/inventario-stock`: desarrollo del modulo de inventario.
