"""
Modulo de inventario de repuestos - Sistema de Gestion Taller Mecanico "LA RUEDA"
Implementa los requerimientos RF-09, RF-10 y RF-11 del mini SRS.

RF-09: registrar repuestos con codigo, nombre, precio de compra, precio de venta y stock.
RF-10: restar automaticamente el stock cuando se usa un repuesto en una orden.
RF-11: mostrar una alerta cuando el stock llega al nivel minimo definido.
"""


class CantidadInvalidaError(Exception):
    """Se intenta descontar una cantidad menor o igual a cero."""


class StockInsuficienteError(Exception):
    """Se intenta descontar mas unidades de las disponibles en el inventario."""


class Repuesto:
    """Repuesto del inventario del taller (RF-09)."""

    def __init__(self, codigo, nombre, precio_compra, precio_venta,
                 stock, stock_minimo=5):
        self.codigo = codigo
        self.nombre = nombre
        self.precio_compra = precio_compra
        self.precio_venta = precio_venta
        self.stock = stock
        self.stock_minimo = stock_minimo
        self._observadores = []

    # ---- Patron Observer (documentado en la seccion 5.2 de la Unidad 2) ----
    def agregar_observador(self, observador):
        """Registra un objeto que sera notificado cuando cambie el stock."""
        self._observadores.append(observador)

    def _notificar(self):
        for observador in self._observadores:
            observador.actualizar(self)

    # ---- Reglas de negocio ----
    def descontar_stock(self, cantidad):
        """
        Descuenta unidades del inventario (RF-10).

        Rechaza cantidades no positivas y cantidades mayores al stock
        disponible. Si la operacion es invalida el stock NO se modifica,
        de modo que el inventario nunca queda en negativo.
        Devuelve el stock restante.
        """
        if cantidad <= 0:
            raise CantidadInvalidaError(
                "La cantidad a descontar debe ser mayor que cero."
            )
        if cantidad > self.stock:
            raise StockInsuficienteError(
                f"Stock insuficiente para {self.nombre}: "
                f"disponible {self.stock}, solicitado {cantidad}."
            )
        self.stock -= cantidad
        self._notificar()
        return self.stock

    def necesita_alerta_stock(self):
        """Devuelve True cuando el stock llego al nivel minimo (RF-11)."""
        return self.stock <= self.stock_minimo


class PanelAlertaStock:
    """Observador que registra los avisos de stock minimo (RF-11)."""

    def __init__(self):
        self.alertas = []

    def actualizar(self, repuesto):
        if repuesto.necesita_alerta_stock():
            self.alertas.append(
                f"Stock minimo alcanzado: {repuesto.nombre} "
                f"({repuesto.stock} unidades)."
            )
