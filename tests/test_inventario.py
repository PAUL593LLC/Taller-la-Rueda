"""
Pruebas automatizadas del modulo de inventario - Taller Mecanico "LA RUEDA".
Los identificadores CP-xx corresponden a la tabla de casos de prueba
del documento (seccion 8, Plan y casos de prueba).
"""

import pytest

from src.inventario import (
    Repuesto,
    PanelAlertaStock,
    StockInsuficienteError,
    CantidadInvalidaError,
)
from src.orden import OrdenTrabajo


@pytest.fixture
def filtro_aceite():
    """Repuesto de ejemplo: 10 unidades en stock, minimo 5."""
    return Repuesto(
        codigo="RP-001",
        nombre="Filtro de aceite",
        precio_compra=4.00,
        precio_venta=7.00,
        stock=10,
        stock_minimo=5,
    )


# ---------------------------------------------------------------- UNITARIAS

def test_cp_u01_descuenta_stock_con_cantidad_valida(filtro_aceite):
    """CP-U01: descontar 3 de 10 unidades deja 7 en stock (RF-10)."""
    restante = filtro_aceite.descontar_stock(3)
    assert restante == 7
    assert filtro_aceite.stock == 7


def test_cp_u02_no_permite_descontar_mas_del_stock(filtro_aceite):
    """
    CP-U02 (CASO CRITICO): si se solicitan mas unidades de las disponibles
    el sistema rechaza la operacion y el stock queda intacto, nunca negativo.
    """
    with pytest.raises(StockInsuficienteError):
        filtro_aceite.descontar_stock(12)
    assert filtro_aceite.stock == 10


def test_cp_u03_rechaza_cantidad_no_positiva(filtro_aceite):
    """CP-U03: una cantidad de cero o negativa es invalida."""
    with pytest.raises(CantidadInvalidaError):
        filtro_aceite.descontar_stock(0)
    with pytest.raises(CantidadInvalidaError):
        filtro_aceite.descontar_stock(-4)
    assert filtro_aceite.stock == 10


def test_cp_u04_alerta_cuando_llega_al_minimo(filtro_aceite):
    """CP-U04: la alerta se activa al llegar al nivel minimo (RF-11)."""
    assert filtro_aceite.necesita_alerta_stock() is False
    filtro_aceite.descontar_stock(5)
    assert filtro_aceite.necesita_alerta_stock() is True


# -------------------------------------------------------------- INTEGRACION

def test_cp_i01_agregar_repuesto_a_orden_descuenta_y_calcula_total(filtro_aceite):
    """
    CP-I01: al agregar 2 filtros a la orden el stock baja a 8 y el
    presupuesto se calcula con subtotal, IVA y total (RF-07, RF-10, RF-12).
    """
    orden = OrdenTrabajo(numero=1, placa_vehiculo="PXA-1234")
    orden.agregar_repuesto(filtro_aceite, 2)

    assert filtro_aceite.stock == 8
    assert orden.subtotal() == 14.00
    assert orden.valor_iva() == 2.10
    assert orden.total() == 16.10


def test_cp_i02_orden_no_registra_detalle_si_falla_el_stock(filtro_aceite):
    """
    CP-I02: si el repuesto no alcanza, la orden no guarda el detalle
    y el inventario permanece sin cambios.
    """
    orden = OrdenTrabajo(numero=2, placa_vehiculo="PXA-1234")
    with pytest.raises(StockInsuficienteError):
        orden.agregar_repuesto(filtro_aceite, 25)

    assert orden.detalles == []
    assert filtro_aceite.stock == 10


def test_cp_i03_observer_notifica_al_panel_de_alertas(filtro_aceite):
    """CP-I03: el patron Observer avisa al panel al llegar al minimo (RF-11)."""
    panel = PanelAlertaStock()
    filtro_aceite.agregar_observador(panel)

    filtro_aceite.descontar_stock(2)   # quedan 8, sin alerta
    assert panel.alertas == []

    filtro_aceite.descontar_stock(3)   # quedan 5, se alcanza el minimo
    assert len(panel.alertas) == 1
    assert "Filtro de aceite" in panel.alertas[0]


# -------------------------------------------------------------- ACEPTACION

def test_cp_a01_flujo_completo_de_reparacion(filtro_aceite):
    """
    CP-A01: el mecanico registra los repuestos usados en una reparacion,
    el sistema descuenta el inventario, avisa del stock minimo y entrega
    el total del presupuesto listo para cobrar.
    """
    panel = PanelAlertaStock()
    filtro_aceite.agregar_observador(panel)
    orden = OrdenTrabajo(numero=3, placa_vehiculo="TBC-4567")

    orden.agregar_repuesto(filtro_aceite, 5)

    assert filtro_aceite.stock == 5
    assert panel.alertas != []
    assert orden.total() == 40.25   # 35.00 + 15 % de IVA
