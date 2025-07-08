def calcular_estado_inicial():
    """
    Inicializa el diccionario `estado` con los indicadores clave de la empresa,
    incluyendo todos los flags y contadores que luego se referencian en
    calcular_estado_final().
    """
    empleados = 4
    costo_emp = 2000
    precio_venta = 4.5

    return {
        # Indicadores financieros y operativos
        "Caja disponible": 50000,
        "Inventario": 0,
        "Pedidos por atender": 0,
        "Unidades vendidas": 0,
        "Insumos disponibles": 100,
        "Cantidad de empleados": empleados,
        "Costo por empleado": costo_emp,
        "Sueldos por pagar": empleados * costo_emp,
        "Deuda pendiente": 20000,
        "Reputacion del mercado": "Nivel 3",
        "Multas e indemnizaciones": 0,
        "Maquinas (total/activas/dañadas)": "5/5/0",
        # Banderas de prohibición y seguro
        "Prohibir Produccion": False,
        "Prohibir Compras": False,
        "Prohibir Importaciones": False,
        "Fondo emergencia": False,
        # Contadores y flags temporales
        "TurnosProduccionExtra": 0,
        "ProduccionTurnoAnterior": 0,
        "DemandaExtraTemporal": 0,
        "EmpleadosTemporales": 0,
        "BrandingActivo": False,
        "MantenimientoHecho": False,
        "ProteccionMantenimientoTurnos": 0,
        "EcommerceActivo": False,
        "InventarioMesAnterior": 0,
        "Prohibir Ventas": False,                            #NUEVO
        "BloqueoVirusTurnos": 0,                             #NUEVO
        "PerderInventario": False,                           #NUEVO
        "BloqueoHuelgaTurnos": 0,                            #NUEVO
        "Prohibir Contrataciones": False,                    #NUEVO
        "BloqueoContratacionTurnos": 0,                      #NUEVO
        "Almacen": 5,                                        #NUEVO
        # rr.hh
        "IncentivosActivos": False,
        "DuracionIncentivos": 0,
        "ClimaLaboralMedido": False,
        "ProteccionClimaTurnos": 0,
        "SeguridadCapacitada": False,
        "ProteccionAccidentesTurnos": 0,
        "VecesSubidaSueldos": 0,
        # marketing
        "BloqueoBajaDemandaTurnos": 0,
        "BloqueoReputacionTurnos": 0,
        "BloqueoDemandaTurnos": 0,
        "BloqueoEcommerceTurnos": 0,
        "DuracionCampania": 0,
        "DuracionBranding": 0,
        "DuracionCoBranding": 0,
        "DemandaExtraProxima": 0,
        "ReputacionPreviaBranding": 0,                      #CAMBIO DE "" -> 0
        # compras
        "CalidadPremiumActivada": False,
        "DuracionCalidadPremium": 0,
        "TurnosVentaExcedentes": 0,
        "DescuentoCompra": False,
        "CreditoConcedido": False,
        "DeudasProveedores": [],
        "PlazoPagoProveedores": 0,
        # eficiencia - precios
        "EficienciaMaquinas": 1.0,
        "PrecioVenta": precio_venta,
    }


def calcular_estado_final(estado):
    """
    Aplica las formulas de calculo al final de cada turno (mes) en el siguiente orden:

    1) Venta automatica
       - El precio de venta se debe cargar de la función calcular_estado_inicial()
       - Vender hasta ‘Pedidos por atender’, descontar de ‘Inventario’
       - Sumar ingresos a ‘Caja disponible’
       - Incrementar ‘Unidades vendidas’
       - Descontar Pedidos por atender’
       - Si no se atiende el total de la demanda, la 'Reputacion del mercado' se reduce un nivel

    2) Actualizacion de pedidos por atender
       - Calcular la demanda del proximo mes a partir de:
         • ‘Reputacion del mercado’
         • Flags permanentes (p. ej. ‘BrandingActivo’, ‘EcommerceActivo’)
         • Incrementos temporales (‘DemandaExtraTemporal’)
       - Almacenar en ‘Pedidos por atender’
       - Fórmula para calcular pedidos nuevos es: 1,000 x (nivel de reputación)
       - Recuerde que el Branding activo aumenta la demanda en 10%
       - Recuerde que tener un e-commerce aumenta la demanda en 5,000 unidades al mes
       - Recurde que la campaña promocional aumenta la demanda en 4,000 unidades al mes
       - Recuerde que el cobranding con una marca o influencer popular ocasiona:
        • Una demanda temporal de 300,000 solo por el primer mes (luego desaparece)
        • Una demanda temporal de 150,000 solo por el segundo mes  (luego desaparece)


    3) Pago de la nomina del mes actual
       - Tomar ‘Sueldos por pagar’
       - Si ‘Caja disponible’ ≥ ‘Sueldos por pagar’:
           • Restar de ‘Caja disponible’
         Sino:
           • Calcula cuanto es lo que falta pagar (‘Sueldos por pagar’ – ‘Caja disponible’)
           • Generar deuda con el 12% de interes total.
           • Poner ‘Caja disponible’ = 0

    4) Generacion de la nomina del proximo mes
       - Calcular ‘Sueldos por pagar’ en base a la cantidad de empleados
           • No se toma en cuenta a los empleados temporales porque a ellos ya se les pago al contratarlos.

    5) Anular multas, accidentes, y demas cartas del caos
       - Esto dependera de la carta del caos que haya salido, y de los flags que tengas activos.

    6) Produccion en automatico
       - Si ‘TurnosProduccionExtra’ > 0:
         • Se produce en automatco la misma cantidad del turno anterior (sin gastar insumos).
         • No debes disminuir ‘TurnosProduccionExtra’ porque dicho valor se reduce en el punto 7)

    7) Actualizacion de flags temporales y decremento de contadores
       - Reducir en 1 las variables contadoras. Por ejemplo:
         • ‘TurnosProduccionExtra’
         • ‘DemandaExtraTemporal’
         • ‘EmpleadosTemporales’
         • Duracion de ‘MejoraProceso’, ‘BrandingActivo’, ‘MantenimientoHecho’, etc.
       - Desactivar (poner a False o 0) cualquier flag cuyo contador llegue a cero

    8) Perdida de inventario:
       - Los meses que no se produce nada, el 10% de insumos caduca.
       - Si la produccion de este mes uso menos inventario que el 10% disponible,
         entonces, el excedente caduca (hasta completar el 10% que vence).
       - Puedes apoyarte de las variables "InventarioMesAnterior" e "Inventario"
    """
    # Guardar inventario inicial para comparaciones posteriores
    estado["InventarioMesAnterior"] = estado["Inventario"]

    # 1) Venta automática
    if estado['Prohibir Ventas'] == False:              #NUEVO
        precio_venta = estado["PrecioVenta"]
        pedidos = estado["Pedidos por atender"]
        inventario = estado["Inventario"]

        unidades_base = min(pedidos, inventario)

        unidades_extra = 0
        if estado["EcommerceActivo"] and (inventario - unidades_base) >= 2000:
            unidades_extra = 2000
        elif estado["EcommerceActivo"]:
            unidades_extra = max(0, inventario - unidades_base)

        unidades_total = unidades_base + unidades_extra

        if estado["DuracionCampania"] > 0:
            unidades_total = min(int(unidades_total * 1.2), inventario)

        if estado["DuracionCoBranding"] > 0:
            unidades_total = min(int(unidades_total * 1.2), inventario)

        ingresos = unidades_total * precio_venta

        estado["Unidades vendidas"] += unidades_total
        estado["Inventario"] -= unidades_total
        estado["Caja disponible"] += ingresos
        estado["Pedidos por atender"] -= min(pedidos, unidades_total)

        # Reducir reputación si no se cubrieron todos los pedidos
        if inventario < pedidos:
            nivel_actual = int(estado["Reputacion del mercado"].split()[1])
            if nivel_actual > 1:
                estado["Reputacion del mercado"] = f"Nivel {nivel_actual - 1}"

    # 2) Actualización de pedidos por atender
    nivel_reputacion = int(estado["Reputacion del mercado"].split()[1])
    demanda_base = 1000 * nivel_reputacion

    # Aplicar modificadores de demanda

    if estado["CalidadPremiumActivada"]:
        demanda_base = int(demanda_base * 1.20)

    if estado["BrandingActivo"]:
        demanda_base = int(demanda_base * 1.10)

    if estado["EcommerceActivo"]:
        demanda_base += 5000

    if estado["DuracionCampania"] > 0:
        demanda_base += 4000

    # Manejar demanda de co-branding
    if estado["DuracionCoBranding"] > 0:
        if estado["DuracionCoBranding"] == 2:
            demanda_base += 300000
        else:  # Segundo turno
            demanda_base += 150000

    # Añadir demanda temporal
    demanda_base += estado["DemandaExtraTemporal"]
    estado["Pedidos por atender"] = demanda_base

    # 3) Pago de nómina actual
    sueldos = estado["Sueldos por pagar"]
    if estado["Caja disponible"] >= sueldos:
        estado["Caja disponible"] -= sueldos
    else:
        faltante = sueldos - estado["Caja disponible"]
        estado["Deuda pendiente"] += faltante * 1.12
        estado["Caja disponible"] = 0

    # 4) Generación de nómina del próximo mes
    estado["Sueldos por pagar"] = (
        estado["Cantidad de empleados"] * estado["Costo por empleado"]
    )

    # 5) NO LO IMPLEMENTAMOS PORQUE NO TENEMOS CARTAS :)

    # 6) Producción automática
    if estado["TurnosProduccionExtra"] > 0:
        estado["Inventario"] += estado["ProduccionTurnoAnterior"]

    # 7) Actualización de flags temporales
    contadores = [
        "TurnosProduccionExtra",
        "DemandaExtraTemporal",
        "EmpleadosTemporales",
        "DuracionIncentivos",
        "ProteccionClimaTurnos",
        "ProteccionAccidentesTurnos",
        "ProteccionMantenimientoTurnos",
        "DuracionBranding",
        "DuracionCampania",
        "DuracionCoBranding",
        "BloqueoBajaDemandaTurnos",
        "BloqueoReputacionTurnos",
        "BloqueoDemandaTurnos",
        "BloqueoEcommerceTurnos",
        "TurnosVentaExcedentes",
        "DuracionCalidadPremium",
        'BloqueoVirusTurnos',           #NUEVO
        "BloqueoHuelgaTurnos",          #NUEVO
        "BloqueoContratacionTurnos"     #NUEVO
    ]

    flags = {
        "IncentivosActivos": "DuracionIncentivos",
        "ClimaLaboralMedido": "ProteccionClimaTurnos",
        "SeguridadCapacitada": "ProteccionAccidentesTurnos",
        "MantenimientoHecho": "ProteccionMantenimientoTurnos",
        "BrandingActivo": "DuracionBranding",
        "CalidadPremiumActivada": "DuracionCalidadPremium",
    }

    for contador in contadores:
        if estado[contador] > 0:
            estado[contador] -= 1

    for flag, contador in flags.items():
        if estado[contador] == 0:
            estado[flag] = False
            if flag == "BrandingActivo" and "ReputacionPreviaBranding" in estado:
                estado["Reputacion del mercado"] = (
                    f"Nivel {estado.pop('ReputacionPreviaBranding')}"
                )

    if estado["BloqueoVirusTurnos"] == 0 and estado["BloqueoHuelgaTurnos"]:                                 #NUEVO
        estado["Prohibir Produccion"] = False
        estado["Prohibir Ventas"] = False

    if estado["BloqueoContratacionTurnos"] == 0:
        estado["Prohibir Contrataciones"] = False        


    # Manejar demanda próxima de co-branding
    if estado["DuracionCoBranding"] == 1:
        estado["DemandaExtraTemporal"] = estado["DemandaExtraProxima"]
    elif estado["DuracionCoBranding"] <= 0:
        estado["DemandaExtraProxima"] = 0

    # 8) Pérdida de insumos
    if estado["TurnosProduccionExtra"] == 0:
        perdida = int(estado["Insumos disponibles"] * 0.10)
        estado["Insumos disponibles"] -= perdida

    # 9) Incendio en almacén (si fue activado)                            #NUEVO
    if estado["PerderInventario"] == True:
        estado["Inventario"] = 0
        estado["PerderInventario"] = False
    return estado
