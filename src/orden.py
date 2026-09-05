"""
Modulo de orden de trabajo - Sistema de Gestion Taller Mecanico "LA RUEDA"
Implementa los requerimientos RF-07 y RF-12 en lo que corresponde al
consumo de repuestos y al calculo del presupuesto.
"""

IVA = 0.15  # Impuesto al valor agregado vigente en Ecuador


class OrdenTrabajo:
    """Orden de trabajo asociada a un vehiculo (RF-05, RF-07, RF-12)."""

    def __init__(self, numero, placa_vehiculo):
        self.numero = numero
        self.placa_vehiculo = placa_vehiculo
        self.detalles = []

    def agregar_repuesto(self, repuesto, cantidad):
        """
        Agrega un repuesto a la orden (RF-07) y descuenta el stock (RF-10).
        Si el descuento falla, el detalle no se agrega a la orden.
        """
        repuesto.descontar_stock(cantidad)
        self.detalles.append({
            "codigo": repuesto.codigo,
            "nombre": repuesto.nombre,
            "cantidad": cantidad,
            "precio_unitario": repuesto.precio_venta,
        })
        return self.detalles[-1]

    def subtotal(self):
        return round(
            sum(d["cantidad"] * d["precio_unitario"] for d in self.detalles), 2
        )

    def valor_iva(self):
        return round(self.subtotal() * IVA, 2)

    def total(self):
        """Total del presupuesto con IVA incluido (RF-12)."""
        return round(self.subtotal() + self.valor_iva(), 2)
