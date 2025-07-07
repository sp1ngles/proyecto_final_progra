# estado.py
import math

def aplicar_aumento_costos(estado, monto):
    if estado.get("AumentoCostosCrisis", 0) > 0:
        return round(monto * 1.10)
    return monto

def calcular_estado_inicial():
    """
    Inicializa el diccionario `estado` con los indicadores clave de la empresa,
    incluyendo todos los flags y contadores necesarios.
    """
    empleados = 4
    costo_emp = 2000

    return {
        # ---- Indicadores Financieros y Operativos Principales ----
        "Caja disponible": 50000,
        "Inventario": 0,
        "Pedidos por atender": 0,
        "Unidades vendidas": 0,
        "Insumos disponibles": 100000,
        "Cantidad de empleados": empleados,
        "Costo por empleado": costo_emp,
        "Sueldos por pagar": empleados * costo_emp,
        "Deuda pendiente": 20000,
        "Reputacion del mercado": "Nivel 3",
        "Multas e indemnizaciones": 0,
        "Maquinas (total/activas/dañadas)": "5/5/0",
        "Precio de venta": 4.5,
        "Ventas del turno anterior": 0,


        # ---- Banderas de estado y prohibiciones ----
        "Prohibir Produccion": False,
        "Prohibir Compras Nacionales": False,
        "Prohibir Importaciones": False,
        "Prohibir Contratacion": False,
        "Fondo emergencia": False,
        "EcommerceActivo": False,
        "ProduccionRealizada": False,
        # ----- Nuevas Cartas agregadas a estados ----
        "SePuedeVender": False,
        "VirusInformatico": False,
        "SinVisibilidad": False,
        # ---- Contadores de efectos temporales (Acciones) ----
        "TurnosProduccionExtra": 0,
        "MejoraProcesoPorcentaje": 0.0,
        "TurnosProteccionMantenimiento": 0,
        "TurnosProteccionClima": 0,
        "TurnosProteccionSeguridad": 0,
        "TurnosIncentivosActivos": 0,
        "SubidasSueldoContador": 0,
        "TurnosDemandaExtraMarketing": 0,
        "VentasExtraMarketing": 0.0,
        "TurnosVentasExtraMarketing": 0,
        "TurnosBranding": 0,
        "ReputacionOriginalBranding": "",
        "TurnosProteccionDemanda": 0,
        "TurnosProteccionReputacion": 0,
        "TurnosProteccionEcommerce": 0,
        "DemandaExtraCoBranding": [0, 0],
        "VentasExtraCoBranding": 0.0,
        "TurnosVentasExtraCoBranding": 0,
        "DescuentoCompraNacional": 1.0,
        "CreditoConcedido": False,
        "CuentasPorPagar": [],
        "TurnosVentaExcedentes": 0,
        "TurnosCalidadPremium": 0,

        # ---- Contadores de efectos temporales (Cartas del Caos) ----
        "TurnosSinVisibilidad": 0,
        "NoVenderEsteTurno": False,
        "ReduccionDemandaProductoRetirado": 0,
        "ReduccionVentasBoicot": 0,
        "TurnosProduccionPlaga": 0,
        "TurnosSinVentasBloqueo": 0,
        "ReduccionVentasCompetidor": 0,
        "ReduccionVentas75": False,
        "AumentoCostosCrisis": 0,
        "TurnosSinOperacionesHuelgaNacional": 0,
        "TurnosEmpleadoAccidentado": 0,
        "TurnosReduccionVentasEmpaque": 0,
        "TurnosSinProduccionDerrame": 0,
    #--------------------------------------------------
        "TurnosProhibirContratacion": 0,
        "TurnosSinImportaciones": 0,
        "TurnosSinComprasNacionales": 0,
        "TurnosReduccionDemandaProductoRetirado": 0,
    #--- Indicadores Carta 3 ---
        "True Inventario":0,
        "True Insumos disponibles":0,
    #--- Indicador Carta 4 ---
        "IncendioAlmacen": False,
    #--------------------------------------------------
    }


def calcular_estado_final(estado):
    """
    Aplica las formulas de calculo al final de cada turno (mes).
    """
    estado["ProduccionRealizada"] = False
    precio_venta = estado["Precio de venta"]

    # --- Pre-cálculos de Venta ---
    if estado["TurnosSinVentasBloqueo"] > 0 or estado.get("NoVenderEsteTurno", False) or estado[
        "TurnosSinOperacionesHuelgaNacional"] > 0:
        unidades_a_vender = 0
    else:
        unidades_a_vender = min(estado["Pedidos por atender"], estado["Inventario"])

    reduccion_venta_total = 1.0
    if estado["ReduccionVentasBoicot"] > 0: reduccion_venta_total *= 0.5
    if estado["ReduccionVentasCompetidor"] > 0: reduccion_venta_total *= 0.6
    if estado.get("ReduccionVentas75", False): reduccion_venta_total *= 0.25
    if estado["TurnosReduccionVentasEmpaque"] > 0: reduccion_venta_total *= 0.75

    unidades_a_vender = math.floor(unidades_a_vender * reduccion_venta_total)

    # 1) Venta automatica
    ingresos_por_ventas = unidades_a_vender * precio_venta

    if estado["TurnosVentasExtraMarketing"] > 0: ingresos_por_ventas *= (1 + estado["VentasExtraMarketing"])
    if estado["TurnosVentasExtraCoBranding"] > 0: ingresos_por_ventas *= (1 + estado["VentasExtraCoBranding"])
    if estado["TurnosCalidadPremium"] > 0: ingresos_por_ventas *= 1.20

    estado["Caja disponible"] += ingresos_por_ventas
    estado["Inventario"] -= unidades_a_vender
    estado["Unidades vendidas"] += unidades_a_vender
    estado["Ventas del turno anterior"] = unidades_a_vender

    if unidades_a_vender < estado["Pedidos por atender"]:
        nivel_actual = int(estado["Reputacion del mercado"].split(" ")[1])
        if nivel_actual > 1: estado["Reputacion del mercado"] = f"Nivel {nivel_actual - 1}"

    estado["Pedidos por atender"] = 0

    # 2) Actualizacion de pedidos
    nivel_reputacion = int(estado["Reputacion del mercado"].split(" ")[1])
    demanda_base = 1000 * nivel_reputacion

    # Aplicar reducción de demanda por producto retirado (Carta 6)
    if estado.get("TurnosReduccionDemandaProductoRetirado", 0) > 0:
       demanda_base = math.floor(demanda_base * 0.5)

    if estado["TurnosBranding"] > 0: demanda_base *= 1.10
    if estado["EcommerceActivo"]: demanda_base += 5000
    if estado["TurnosDemandaExtraMarketing"] > 0: demanda_base += 4000
    if estado["DemandaExtraCoBranding"][0] > 0: demanda_base += estado["DemandaExtraCoBranding"][0]
    if estado["TurnosCalidadPremium"] > 0: demanda_base *= 1.20
    if estado["ReduccionDemandaProductoRetirado"] > 0: demanda_base *= 0.5

    estado["Pedidos por atender"] = math.floor(demanda_base)

    # 3) Pago de la nomina y multas
    gastos_totales = estado["Sueldos por pagar"] + estado["Multas e indemnizaciones"]
    if estado["Caja disponible"] >= gastos_totales:
        estado["Caja disponible"] -= gastos_totales
    else:
        faltante = gastos_totales - estado["Caja disponible"]
        estado["Caja disponible"] = 0
        estado["Deuda pendiente"] += faltante * 1.12
    estado["Multas e indemnizaciones"] = 0

    # Pago de crédito a proveedores
    cuentas_pagadas_idx = []
    for i, (monto, turnos) in enumerate(estado["CuentasPorPagar"]):
        if turnos <= 1:
            if estado["Caja disponible"] >= monto:
                estado["Caja disponible"] -= monto
            else:
                deuda_faltante = monto - estado["Caja disponible"]
                estado["Caja disponible"] = 0
                estado["Deuda pendiente"] += deuda_faltante * 1.12
            cuentas_pagadas_idx.append(i)
    for i in sorted(cuentas_pagadas_idx, reverse=True): del estado["CuentasPorPagar"][i]

    # 4) Generacion de la nomina del proximo mes
    estado["Sueldos por pagar"] = aplicar_aumento_costos(estado,(estado["Cantidad de empleados"] * estado["Costo por empleado"]))

    # 6) Produccion en automatico
    if (estado.get("Prohibir Produccion", False) or estado.get("TurnosSinProduccionDerrame", 0) > 0 or
            estado.get("TurnosSinOperacionesHuelgaNacional", 0) > 0):
        # simplemente no hacemos nada aquí
        pass
    elif estado["TurnosProduccionExtra"] > 0:
        total, activas, danadas = map(int, estado["Maquinas (total/activas/dañadas)"].split('/'))
        produccion_base = activas * 2000
        produccion_total = produccion_base * (1 + estado["MejoraProcesoPorcentaje"])
        if estado["TurnosIncentivosActivos"] > 0: produccion_total *= 1.20
        estado["Inventario"] += math.floor(produccion_total)
        estado["ProduccionRealizada"] = True

    # 7) Actualizacion de contadores temporales
    for key in list(estado.keys()):
        if key.startswith("Turnos") and estado[key] > 0:
            estado[key] -= 1

    estado["DemandaExtraCoBranding"] = [estado["DemandaExtraCoBranding"][1], 0]

    if estado["TurnosBranding"] == 0 and estado["ReputacionOriginalBranding"]:
        estado["Reputacion del mercado"] = estado["ReputacionOriginalBranding"]
        estado["ReputacionOriginalBranding"] = ""

    for i in range(len(estado["CuentasPorPagar"])):
        estado["CuentasPorPagar"][i] = (estado["CuentasPorPagar"][i][0], estado["CuentasPorPagar"][i][1] - 1)

    if estado["TurnosEmpleadoAccidentado"] == 0 and estado.get("_empleado_accidentado_flag", False):
        estado["Cantidad de empleados"] += 1
        estado["_empleado_accidentado_flag"] = False

#-----------------------------------------------------------------------
    contador_a_flag = {
    "TurnosProhibirContratacion":   "Prohibir Contratacion",
    "TurnosSinImportaciones":        "Prohibir Importaciones",
    "TurnosSinComprasNacionales":    "Prohibir Compras Nacionales",
    "TurnosSinProduccionLicencia":   "Prohibir Produccion",
    # contadores sin flag asociado:
    "TurnosSinVisibilidad": None,
    "TurnosSinProduccionDerrame":    None,
    "TurnosProduccionPlaga":         None,
    "TurnosSinVentasBloqueo":        None,
    "ReduccionVentasBoicot":         None,
    "ReduccionVentasCompetidor":     None,
    "ReduccionVentas75":             None,
    "AumentoCostosCrisis":           None,
    "TurnosReduccionVentasEmpaque":  None,
    "TurnosReduccionDemandaProductoRetirado": None,
    "TurnosErrorEtiquetado":         None,
    # …añade aquí cualquier otro “Turnos…” que uses
    }

    for contador, flag in contador_a_flag.items():
        valor = estado.get(contador, 0)
        if valor > 0:
            estado[contador] = valor - 1
            # si justo llegó a cero, desactivamos la flag asociada
            if estado[contador] == 0 and flag is not None:
                estado[flag] = False

    if estado["TurnosSinVisibilidad"] == 0:
        estado["Inventario"] = estado["True Inventario"]
        estado["Insumos disponibles"] = estado["True Insumos disponibles"]


#-----------------------------------------------------------------------

    # Resetear flags de un solo turno
    estado["NoVenderEsteTurno"] = False
    estado["ReduccionVentas75"] = False



    if estado["TurnosVentaExcedentes"] > 0:
        insumos_a_vender = math.floor(estado["Insumos disponibles"] * 0.10)
        estado["Insumos disponibles"] -= insumos_a_vender
        estado["Caja disponible"] += insumos_a_vender * 0.30
    elif not estado["ProduccionRealizada"]:
        estado["Insumos disponibles"] = math.floor(estado["Insumos disponibles"] * 0.90)
        # 8) Perdida de insumos
        if estado["IncendioAlmacen"] == 1:
            estado["Inventario"] = 0
            estado["IncendioAlmacen"] = 0
    return estado