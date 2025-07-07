# acciones.py
import math

def aplicar_aumento_costos(estado, monto):
    if estado.get("AumentoCostosCrisis", 0) > 0:
        return round(monto * 1.10)
    return monto


# ---------------- Produccion ----------------
def produccion_producir(estado):
    if (estado.get("Prohibir Produccion", False) or estado.get("TurnosSinProduccionDerrame", 0) > 0 or
            estado.get("TurnosSinOperacionesHuelgaNacional", 0) > 0):
        estado["Prohibir Produccion"] = False
        return estado

    else:

        total, activas, danadas = map(int, estado["Maquinas (total/activas/dañadas)"].split('/'))
        produccion_total_turno = 0
        insumos_por_maquina = 40000

        for _ in range(activas):
            if estado["Insumos disponibles"] >= insumos_por_maquina:
                estado["Insumos disponibles"] -= insumos_por_maquina
                produccion_total_turno += 2000
                estado["TurnosProduccionExtra"] = 2

        bono_empleados = produccion_total_turno * (estado["Cantidad de empleados"] * 0.10)
        produccion_total_turno += bono_empleados
        produccion_total_turno *= (1 + estado["MejoraProcesoPorcentaje"])
        if estado["TurnosIncentivosActivos"] > 0: produccion_total_turno *= 1.20
        if estado["TurnosProduccionPlaga"] > 0: produccion_total_turno *= 0.5  # Efecto carta plaga

        estado["Inventario"] += math.floor(produccion_total_turno)
        if produccion_total_turno > 0: estado["ProduccionRealizada"] = True
        return estado


def produccion_pedido_encargo(estado):
    if estado.get("Prohibir Produccion", False): return estado
    if estado["Insumos disponibles"] >= 10000:
        estado["Caja disponible"] += 50000
        estado["Insumos disponibles"] -= 10000
    return estado


def produccion_mejorar_proceso(estado):
    estado["MejoraProcesoPorcentaje"] += 0.05
    return estado


def produccion_mantenimiento_maquinaria(estado):
    costo = aplicar_aumento_costos(estado, 5000)
    if estado["Caja disponible"] >= costo:
        estado["Caja disponible"] -= costo
    else:
        estado["Deuda pendiente"] += costo * 1.12

    total, activas, danadas = map(int, estado["Maquinas (total/activas/dañadas)"].split('/'))
    activas += danadas
    danadas = 0
    estado["Maquinas (total/activas/dañadas)"] = f"{total}/{activas}/{danadas}"
    estado["TurnosProteccionMantenimiento"] = 3
    return estado


def produccion_comprar_nueva_maquina(estado):
    costo = aplicar_aumento_costos(estado,10000)
    if estado["Caja disponible"] >= costo:
        estado["Caja disponible"] -= costo
    else:
        estado["Deuda pendiente"] += costo * 1.12

    total, activas, danadas = map(int, estado["Maquinas (total/activas/dañadas)"].split('/'))
    estado["Maquinas (total/activas/dañadas)"] = f"{total + 1}/{activas + 1}/{danadas}"
    return estado


def produccion_no_hacer_nada(estado): return estado


# ---------------- Recursos Humanos ----------------
def rh_contratar_personal_permanente(estado):
    if estado.get("Prohibir Contratacion", False): return estado
    estado["Cantidad de empleados"] += 1
    return estado


def rh_contratar_personal_temporal(estado):
    if estado["Caja disponible"] >= 10000: estado["Caja disponible"] -= 10000
    return estado


def rh_implementar_incentivos(estado):
    if estado["Caja disponible"] >= aplicar_aumento_costos(estado,5000):
        estado["Caja disponible"] -= aplicar_aumento_costos(estado,5000)
        estado["TurnosIncentivosActivos"] = 5
    return estado


def rh_medicion_clima(estado):
    estado["TurnosProteccionClima"] = 3
    return estado


def rh_capacitar_seguridad(estado):
    estado["TurnosProteccionSeguridad"] = 3
    return estado


def rh_subir_sueldos(estado):
    contador = estado.get("SubidasSueldoContador", 0)
    porcentajes = {0: 0.10, 1: 0.07, 2: 0.04}
    aumento = porcentajes.get(contador, 0.015)
    estado["Costo por empleado"] *= (1 + aumento)
    estado["SubidasSueldoContador"] += 1
    return estado


def rh_no_hacer_nada(estado): return estado


# ---------------- Marketing ----------------
def marketing_lanzar_campania(estado):
    if estado["Caja disponible"] >= aplicar_aumento_costos(estado,8000):
        estado["Caja disponible"] -= aplicar_aumento_costos(estado,8000)
        nivel_actual = int(estado["Reputacion del mercado"].split(" ")[1])
        if nivel_actual < 7: estado["Reputacion del mercado"] = "Nivel 7"
        estado["TurnosDemandaExtraMarketing"] = 2
        estado["VentasExtraMarketing"] = 0.20
        estado["TurnosVentasExtraMarketing"] = 2
        estado["TurnosProteccionDemanda"] = 5
    return estado


def marketing_invertir_branding(estado):
    if estado["Caja disponible"] >= aplicar_aumento_costos(estado,12000):
        estado["Caja disponible"] -= aplicar_aumento_costos(estado,12000)
        if estado["TurnosBranding"] == 0: estado["ReputacionOriginalBranding"] = estado["Reputacion del mercado"]
        nivel_actual = int(estado["Reputacion del mercado"].split(" ")[1])
        if nivel_actual < 8: estado["Reputacion del mercado"] = "Nivel 8"
        estado["TurnosBranding"] = 5
        estado["TurnosProteccionReputacion"] = 5
    return estado


def marketing_estudio_mercado(estado):
    if estado["Caja disponible"] >= aplicar_aumento_costos(estado,5000):
        estado["Caja disponible"] -= aplicar_aumento_costos(estado,5000)
        estado["Reputacion del mercado"] = "Nivel 6"
        estado["TurnosProteccionDemanda"] = 5
    return estado


def marketing_abrir_ecommerce(estado):
    if not estado["EcommerceActivo"]:
        if estado["Caja disponible"] >= aplicar_aumento_costos(estado,20000):
            estado["Caja disponible"] -= aplicar_aumento_costos(estado,20000)
            estado["EcommerceActivo"] = True
    else:
        if estado["Caja disponible"] >= aplicar_aumento_costos(estado,2000):
            estado["Caja disponible"] -= aplicar_aumento_costos(estado,2000)
            estado["TurnosProteccionEcommerce"] = 3
    return estado


def marketing_co_branding(estado):
    if estado["Caja disponible"] >= aplicar_aumento_costos(estado,3000):
        estado["Caja disponible"] -= aplicar_aumento_costos(estado,3000)
        estado["DemandaExtraCoBranding"] = [300000, 100000]
        estado["VentasExtraCoBranding"] = 0.20
        estado["TurnosVentasExtraCoBranding"] = 2
    return estado


def marketing_no_hacer_nada(estado): return estado


# ---------------- Compras ----------------
def compras_comprar_insumos_nacionales(estado):
    costo = aplicar_aumento_costos(estado, 10000 * estado["DescuentoCompraNacional"])
    if estado.get("Prohibir Compras Nacionales", False): return estado
    if estado["CreditoConcedido"]:
        estado["CuentasPorPagar"].append((costo, 3))
        estado["Insumos disponibles"] += 500000
    elif estado["Caja disponible"] >= costo:
        estado["Caja disponible"] -= costo
        estado["Insumos disponibles"] += 500000
    return estado


def compras_comprar_insumos_importados(estado):
    costo = aplicar_aumento_costos(estado, 14000)
    if estado.get("Prohibir Importaciones", False): return estado
    if estado["CreditoConcedido"]:
        estado["CuentasPorPagar"].append((costo, 3))
        estado["Insumos disponibles"] += 800000
    elif estado["Caja disponible"] >= costo:
        estado["Caja disponible"] -= costo
        estado["Insumos disponibles"] += 800000
    return estado


def compras_comprar_insumos_importados_premium(estado):
    costo = aplicar_aumento_costos(estado, 25000)
    if estado.get("Prohibir Importaciones", False): return estado
    if estado["CreditoConcedido"]:
        estado["CuentasPorPagar"].append((costo, 3))
        estado["Insumos disponibles"] += 900000
        estado["TurnosCalidadPremium"] = 3
    elif estado["Caja disponible"] >= costo:
        estado["Caja disponible"] -= costo
        estado["Insumos disponibles"] += 900000
        estado["TurnosCalidadPremium"] = 3
    return estado


def compras_vender_excedentes_insumos(estado):
    estado["TurnosVentaExcedentes"] = 3
    return estado


def compras_negociar_precio(estado):
    if estado["Caja disponible"] >= aplicar_aumento_costos(estado,5000):
        estado["Caja disponible"] -= aplicar_aumento_costos(estado,5000)
        estado["DescuentoCompraNacional"] = 0.70
    return estado


def compras_negociar_credito(estado):
    if estado["Caja disponible"] >= aplicar_aumento_costos(estado,2000):
        estado["Caja disponible"] -= aplicar_aumento_costos(estado,2000)
        estado["CreditoConcedido"] = True
    return estado


def compras_no_hacer_nada(estado): return estado


# ---------------- Finanzas ----------------
def finanzas_pagar_proveedores(estado):
    total_a_pagar = sum(monto for monto, turnos in estado["CuentasPorPagar"])
    costo_con_descuento = total_a_pagar * 0.95
    if estado["Caja disponible"] >= costo_con_descuento:
        estado["Caja disponible"] -= costo_con_descuento
        estado["CuentasPorPagar"] = []
    return estado


def finanzas_pagar_deuda(estado):
    if estado["Deuda pendiente"] > 0:
        pago = min(estado["Caja disponible"], estado["Deuda pendiente"], 10000)
        estado["Caja disponible"] -= pago
        estado["Deuda pendiente"] -= pago
    return estado


def finanzas_solicitar_prestamo(estado):
    estado["Caja disponible"] += 30000
    estado["Deuda pendiente"] += 35000
    return estado


def finanzas_crear_fondo_emergencia(estado):
    if estado["Caja disponible"] >= aplicar_aumento_costos(estado,10000):
        estado["Caja disponible"] -= aplicar_aumento_costos(estado,10000)
        estado["Fondo emergencia"] = True
    return estado


def finanzas_no_hacer_nada(estado): return estado