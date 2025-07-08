# acciones.py

# ---------------- Produccion ----------------


def produccion_producir(estado):
    """
    1. Producir:
    - Si existe el flag "Prohibir Produccion" (== True), no produce nada y borra el flag (lo pone a False).
    - Si no hay prohibicion, cada maquina realiza lo siguiente:
        • Consume 40 000 insumos (resta de “Insumos disponibles”).
          -> solo si Insumos disponibles ≥ 40 000, caso contrario, esa maquina no produce nada
        • Añade 2,000 unidades al inventario (suma a “Inventario”).
        • Marca que la produccion se realiza por dos turnos:
            – Debe crear o incrementar “TurnosProduccionExtra” en 2,
              para que en el siguiente turno se pueda volver a producir,
              asi el jugador queda libre para realizar otra accion el siguiente turno.
            - La produccion extra no consume insumos, y se hace desde calcular_estado_final, punto 7
              (ver archivo estado.py)
    - Por cada empleado adicional contratado, la produccion aumenta en 10%, sin gastar insumos.
        • Esto se debe a que los empelados introducen eficiencias en el proceso productivo
    - Todos los turnos se peude producir, es decir, las maquinas no quedan ocupadas.
        • Esto se debe a que el proceso productivo tiene diferentes fases
    """
    if estado["Prohibir Produccion"]:
        estado["Prohibir Produccion"] = False
        return estado

    maquinas_activas = int(estado["Maquinas (total/activas/dañadas)"].split("/")[1])
    insumos_necesarios = 40000 * maquinas_activas
    print(insumos_necesarios)
    if estado["Insumos disponibles"] >= insumos_necesarios:
        produccion_base = 2000 * maquinas_activas * estado["EficienciaMaquinas"]
        empleados_permanentes = estado["Cantidad de empleados"]
        produccion_final = produccion_base * (1 + 0.1 * (empleados_permanentes - 4))

        estado["Inventario"] += int(produccion_final)
        estado["Insumos disponibles"] -= insumos_necesarios
        estado["TurnosProduccionExtra"] += 2

    return estado


def produccion_pedido_encargo(estado):
    """
    2. Producir por encargo:
    Aceptamso un pedido de produccion para otra fabrica,
    la cantidad producida no va al invnetario sino que se vende inmediatamente.
    - Se debe controlar que no haya prohibicion y que existan insumos.
    - Si se realiza la produccion por encargo:
        • Genera caja inmediata de S/ 50,000 (suma a “Caja disponible”).
        • Consume 10,000 insumos (resta de “Insumos disponibles”).
    - Si no se realiza:
        • No hace nada (no varia ningun campo).
    """
    if estado["Prohibir Produccion"]:
        estado["Prohibir Produccion"] = False
        return estado

    if estado["Insumos disponibles"] >= 10000:
        estado["Caja disponible"] += 50000
        estado["Insumos disponibles"] -= 10000

    return estado


def produccion_mejorar_proceso(estado):
    """
    3. Mejorar proceso:
    - Aumenta permanentemente la eficiencia de todas las maquinas.
    - Se puede elegir esta opcion en diversos turnos,
      y cada vez aumentara la producciponen un 5% de la produccion base.
    - Debes implementar una variable correspondiente en el diccionario de estados.
    - Una vez aumentada la eficiencia, tu decide como hacerla efectiva:
      • En la funcion calcular_estado_final, puedes aumentar la produccion despues de haber producido
      • O puedes modificar la formula de produccion_producir para que las 20,000 unidades a producir aumenten
    """

    estado["EficienciaMaquinas"] *= 1.05
    return estado


def produccion_mantenimiento_maquinaria(estado):
    """
    4. Mantenimiento de maquinaria:
    - Repara todas las maquinas dañadas, pasandolas a activas:
        • Ten en cuenta que las Maquinas (total/activas/dañadas) estan en formato “str/str/str”.
          Es decir, separados por el simbolo de barra diagonal "/".
          - No debes cambiar la estructura de total/activas/dañadas
            porque asi esta programado el menu de Estado de la empresa.
        • Todas las Dañadas pasan a Activas (el numero de dañadas se pone a 0,
          el numero de activas aumenta en esa cantidad).
    - Reduce el riesgo de fallas futuras:
        • Fija el flag “MantenimientoHecho = True” para que la proxima carta
          de caos que dañe maquinas sea cancelada.
        • Esta accion bloque por 3 turnos el efecto de cualquier carta del caos que involucre:
          mal funcionamiento, accidentes o siniestros, bajo rendimiento, y afines.
          (siempre y cuando la Carta de Caos guarde relacion con el estado de la maquinaria).
        • Debes implementar un contador en el Estado que indique cuantos turnos quedan de proteccion.
    - Si no hay dinero, debes decidir que hacer:
        • Opcion 1: no hacer nada, por falta de fondos
        • Opcion 2: aumentar la deuda (genera un interes total del 12%)
    """
    costo_mantenimiento = 5000

    if estado["Caja disponible"] >= costo_mantenimiento:
        estado["Caja disponible"] -= costo_mantenimiento
    else:
        falta = costo_mantenimiento - estado["Caja disponible"]
        estado["Deuda pendiente"] += falta * 1.12
        estado["Caja disponible"] = 0

    partes = estado["Maquinas (total/activas/dañadas)"].split("/")
    total, activas, danadas = map(int, partes)
    nuevas_activas = activas + danadas
    nuevas_danadas = 0
    estado["Maquinas (total/activas/dañadas)"] = (
        f"{total}/{nuevas_activas}/{nuevas_danadas}"
    )

    estado["MantenimientoHecho"] = True
    estado["ProteccionMantenimientoTurnos"] = 3

    return estado


def produccion_comprar_nueva_maquina(estado):
    """
    5. Comprar nueva maquina:
    - Resta S/ 10 000 de “Caja disponible”.
    - Añade 1 al total de maquinas y 1 a maquinas activas:
        • Actualiza “Maquinas (total/activas/dañadas)” en formato “str/str/str”.
    - Si no hay dinero, debes decidir que hacer:
        • Opcion 1: no hacer nada, por falta de fondos
        • Opcion 2: aumentar la deuda (genera intereses)
    """

    precio = 10000

    if estado["Caja disponible"] >= precio:
        estado["Caja disponible"] -= precio
    else:
        falta = precio - estado["Caja disponible"]
        estado["Deuda pendiente"] += falta * 1.12
        estado["Caja disponible"] = 0

    partes = estado["Maquinas (total/activas/dañadas)"].split("/")
    total, activas, danadas = map(int, partes)
    nuevo_total = total + 1
    nuevas_activas = activas + 1
    estado["Maquinas (total/activas/dañadas)"] = (
        f"{nuevo_total}/{nuevas_activas}/{danadas}"
    )

    return estado


def produccion_no_hacer_nada(estado):
    """
    6. No hacer nada en el area de produccion este turno:
    - Simplemente retorna el estado sin cambios.
    """
    return estado


# ---------------- Recursos Humanos ----------------


def rh_contratar_personal_permanente(estado):
    if estado["Prohibir Contrataciones"] == False: #NUEVO
        """
        1. Contratar personal permanente:
        - Aumenta permanentemente S/ 4,000 de “Total Salarios”.
        - Aumenta “Numero de empleados” en 1.
        - Si se vuelve a ejecutar esta accion, se aumentan 4,000 mas en salarios y 1 mas en numero de empleados.
        """
        estado["Cantidad de empleados"] += 1
        estado["Sueldos por pagar"] += 4000
    return estado


def rh_contratar_personal_temporal(estado):
    if estado["Prohibir Contrataciones"] == False:      #NUEVO
        """
        2. Outsourcing temporal:
        - Paga S/ 10 000 (pago unico unico) para sumar 4 empleados temporales solo este turno.
        - Aumenta la cantidad de empleados en 4, solo por este turno
            • Si deseas, puedes crear una variable adicional para la cantidad de "EmpleadosTemporales"
        """

        costo_contratacion = 10000

        if estado["Caja disponible"] >= costo_contratacion:
            estado["Caja disponible"] -= costo_contratacion
        else:
            falta = costo_contratacion - estado["Caja disponible"]
            estado["Deuda pendiente"] += falta * 1.12
            estado["Caja disponible"] = 0

        estado["EmpleadosTemporales"] += 4
    return estado


def rh_implementar_incentivos(estado):
    """
    3. Implementar incentivos:
    - Gasta S/ 5 000 en bonos.
    - Puedes fijar el flag “IncentivosActivos = True” para que, en calcular_estado_final,
      el inventario producido por 5 turnos se multiplique por 1.2 (20 % extra).
    """
    costo = 5000

    if estado["Caja disponible"] >= costo:
        estado["Caja disponible"] -= costo

    else:
        falta = costo - estado["Caja disponible"]
        estado["Deuda pendiente"] += falta * 1.12
        estado["Caja disponible"] = 0

    estado["IncentivosActivos"] = True
    estado["DuracionIncentivos"] = 5

    return estado


def rh_medicion_clima(estado):
    """
    4. Medicion de clima laboral:
    - Sin costo, se hace con el personal interno de la empresa.
    - Bloquea cartas del caos relacionadas con huelgas o bajo rendimiento de personal por 3 turnos.
    """
    estado["ClimaLaboralMedido"] = True
    estado["ProteccionClimaTurnos"] = 3
    return estado


def rh_capacitar_seguridad(estado):
    """
    5. Capacitar en seguridad:
    - Sin costo, la capacitacion la hace el propio personal de la empresa.
    - Bloquea Cartas del Caos relacionadas a Accidentes.
    """
    estado["SeguridadCapacitada"] = True
    estado["ProteccionAccidentesTurnos"] = 3
    return estado


def rh_subir_sueldos(estado):
    """
    6. Subir sueldos:
    - Aumenta en X% el salario de todos los empleados
        • Donde X toma el valor de 10% la primera vez,
          7% la segunda vez,
          4% la tercera vez,
          1.5%, el resto de veces.
    """

    veces_subidas = estado["VecesSubidaSueldos"]

    if veces_subidas == 0:
        aumento = 0.10
    elif veces_subidas == 1:
        aumento = 0.07
    elif veces_subidas == 2:
        aumento = 0.04
    else:
        aumento = 0.015

    estado["Costo por empleado"] *= 1 + aumento
    estado["VecesSubidaSueldos"] = veces_subidas + 1
    estado["Sueldos por pagar"] = (
        estado["Cantidad de empleados"] * estado["Costo por empleado"]
    )

    return estado


def rh_no_hacer_nada(estado):
    """
    7. No hacer nada en el area de Recursos Humanos este turno:
    - Retorna el estado tal cual, sin cambios.
    """
    return estado


# ---------------- Marketing ----------------


def marketing_lanzar_campania(estado):
    """
    1. Lanzar campaña de promocion:
    - Gasta S/ 8 000 de “Caja disponible”.
    - Sube “Reputacion del mercado” a “Nivel 7”
      • Si la reputacion era mayor a 7, se mantiene en el valor que tenia (no aumenta mas).
    - Añade “DemandaExtraTemporal” de +4000 unidades para el turno actual y el siguiente.
    - Aumenta nuestras ventas en 20% por dos turnos
      • Solo aumenta si existe inventario disponible para la venta.
      • Es posible vender por encima de los pedidos que teniamos (porque aparece demanda espontanea para este mismo mes).
    - Bloquea por 5 turnos las cartas del Caos relacionadas baja demanda/aceptacion.
    """

    costo_campania = 8000

    if estado["Caja disponible"] >= costo_campania:
        estado["Caja disponible"] -= costo_campania
    else:
        faltante = costo_campania - estado["Caja disponible"]
        estado["Deuda pendiente"] += faltante * 1.12
        estado["Caja disponible"] = 0

    estado["DemandaExtraTemporal"] += 4000
    estado["DuracionCampania"] = 2
    estado["BloqueoBajaDemandaTurnos"] = 5

    # Manejo de reputación
    nivel_actual = int(estado["Reputacion del mercado"].split()[1])
    if nivel_actual < 7:
        estado["Reputacion del mercado"] = "Nivel 7"

    return estado


def marketing_invertir_branding(estado):
    """
    2. Invertir en branding:
    - Gasta S/ 12 000 de “Caja disponible”.
    - Sube “Reputacion del mercado” a “Nivel 8” por 5 turnos.
        • Despues de los 5 turnos, debera regresar al valor que tenia antes.
        • Si la reputacion era mayor a 8, se mantiene en el valor que tenia.
    - Puedes fijar el flag “BrandingActivo = True” para que la demanda base
      suba un 10 % en calcular_estado_final durante estos 5 turnos.
    - Bloquea por 5 turnos las cartas del Caos relacionadas a la reputacion,
      excepto si la carta del caos es un problema puntual de branding
      (es decir, invertimos en branding, pero fue perjudicial).
    """

    costo_branding = 12000

    if estado["Caja disponible"] >= costo_branding:
        estado["Caja disponible"] -= costo_branding
    else:
        faltante = costo_branding - estado["Caja disponible"]
        estado["Deuda pendiente"] += faltante * 1.12
        estado["Caja disponible"] = 0

    estado["BrandingActivo"] = True
    estado["DuracionBranding"] = 5
    estado["BloqueoReputacionTurnos"] = 5

    nivel_actual = int(estado["Reputacion del mercado"].split()[1])
    if nivel_actual < 8:
        if "ReputacionPreviaBranding" not in estado:
            estado["ReputacionPreviaBranding"] = nivel_actual
        estado["Reputacion del mercado"] = "Nivel 8"

    return estado


def marketing_estudio_mercado(estado):
    """
    3. Estudio de mercado:
    - Gasta S/ 5 000 de “Caja disponible”.
    - Ajusta “Reputacion del mercado” a “Nivel 6”.
    - Bloquea las cartas de caos relacionadas con demanda por 5 turnos.
    """
    costo_estudio = 5000

    if estado["Caja disponible"] >= costo_estudio:
        estado["Caja disponible"] -= costo_estudio
    else:
        faltante = costo_estudio - estado["Caja disponible"]
        estado["Deuda pendiente"] += faltante * 1.12
        estado["Caja disponible"] = 0

    nivel_actual = int(estado["Reputacion del mercado"].split()[1])
    if nivel_actual < 6:
        estado["Reputacion del mercado"] = "Nivel 6"

    estado["BloqueoDemandaTurnos"] = 5
    return estado


def marketing_abrir_ecommerce(estado):
    """
    4. Abrir canal e-commerce:
    - Si “EcommerceActivo” es False:
        • Gasta S/ 20,000 de “Caja disponible”.
        • Fija “EcommerceActivo = True”.
        • Aumenta permanentemente “Pedidos por atender” en +5,000 por turno
          (se aplica en calcular_estado_final).
        • Aumenta permanentemente “Ventas” en +2,000 por turno
          (siempre y cuando exista inventario disponible para la venta).
    - Si ya existe “EcommerceActivo” True:
        • Gasta S/ 2 000 de “Caja disponible” para mantenimiento, sin aumentar la demanda.
        • Esto bloquea por 3 turnos cualquier Carta del Caos que afecte el e-comerce.
    """
    if not estado["EcommerceActivo"]:
        costo = 20000
        if estado["Caja disponible"] >= costo:
            estado["Caja disponible"] -= costo
        else:
            faltante = costo - estado["Caja disponible"]
            estado["Deuda pendiente"] += faltante * 1.12
            estado["Caja disponible"] = 0

        estado["EcommerceActivo"] = True
        estado["BloqueoEcommerceTurnos"] = 3

    else:
        costo = 2000
        if estado["Caja disponible"] >= costo:
            estado["Caja disponible"] -= costo
        else:
            faltante = costo - estado["Caja disponible"]
            estado["Deuda pendiente"] += faltante * 1.12
            estado["Caja disponible"] = 0

        estado["BloqueoEcommerceTurnos"] = 3

    return estado


def marketing_co_branding(estado):
    """
    5. Alianza co-branding con maca o influencer muy popular:
    - Gasta S/ 3 000 de “Caja disponible”.
    - Añade “DemandaExtraTemporal” de +300,000 este mes y +100,000 el proximo mes.
      • Es posible que en alianzas con marcas o influencer gigantescos
        no tengamos la capacidad para producir la cantidad de demanda que se genere.
      • Esta demanda no es permanente, si no se atiende, el nivel de demanda regres aa su valor
    - Aumenta nuestras ventas en 20% por dos turnos
      (siempre y cuando exista inventario disponible para la venta).
    """
    costo = 3000

    if estado["Caja disponible"] >= costo:
        estado["Caja disponible"] -= costo
    else:
        faltante = costo - estado["Caja disponible"]
        estado["Deuda pendiente"] += faltante * 1.12
        estado["Caja disponible"] = 0

    estado["DemandaExtraTemporal"] += 300000
    estado["DemandaExtraProxima"] = 100000
    estado["DuracionCoBranding"] = 2

    return estado


def marketing_no_hacer_nada(estado):
    """
    6. No hacer nada en el area de Marketing:
    - Retorna el estado sin cambios.
    """
    return estado


# ---------------- Compras ----------------


def compras_comprar_insumos_nacionales(estado):
    """
    1. Comprar insumos nacionales:
    - Gasta S/ 10 000 de “Caja disponible”.
    - Añade 500,000 a “Insumos disponibles”.
    """
    costo = 10000
    if estado["DescuentoCompra"]:
        costo = int(costo * 0.7)

    if estado["Caja disponible"] >= costo:
        estado["Caja disponible"] -= costo
        estado["Insumos disponibles"] += 500000
    return estado


def compras_comprar_insumos_importados(estado):
    """
    2. Comprar insumos importados:
    - Gasta S/ 14 000 de “Caja disponible”.
    - Añade 800,000 a “Insumos disponibles”.
    -
    """
    if estado["Caja disponible"] >= 14000:
        estado["Caja disponible"] -= 14000
        estado["Insumos disponibles"] += 800000
    return estado


def compras_comprar_insumos_importados_premium(estado):
    """
    3. Comprar insumos premium importados:
    - Gasta S/ 25 000 de “Caja disponible”.
    - Añade 900,000 a “Insumos disponibles”.
    - Aumenta la calidad de nuestros productos y la calidad percibida
      • Esto incrementa la demanda en un 20% por 3 meses.
      • Esto incrementa las ventas en un 20% por 3 meses.
        (siempre y cuando exista inventario disponible para la venta).
    """
    if estado["Caja disponible"] >= 25000:
        estado["Caja disponible"] -= 25000
        estado["Insumos disponibles"] += 900000
        estado["CalidadPremiumActivada"] = True
        estado["DuracionCalidadPremium"] = 3
    return estado


def compras_vender_excedentes_insumos(estado):
    """
    4. Venta de excedentes de insumos:
    - Se sabe que los meses que no hay produccion, el 10% de insumos caducan.
    - Esta accion hace que vendamos ese 10%.
      Es decir, tambien perdemos el 10% de nuestros insumos,
      pero los vendemos a 0.30 centimos cada uno.
    La accion se ejecuta por 3 turnos, incluido este.
    """
    if "TurnosVentaExcedentes" not in estado:
        estado["TurnosVentaExcedentes"] = 3

    if estado["TurnosVentaExcedentes"] > 0:
        cantidad_a_vender = int(estado["Insumos disponibles"] * 0.1)
        ganancia = cantidad_a_vender * 0.30
        estado["Insumos disponibles"] -= cantidad_a_vender
        estado["Caja disponible"] += ganancia
        estado["TurnosVentaExcedentes"] -= 1

    return estado


def compras_negociar_precio(estado):
    """
    5. Negociar precio con proveedores:
    - Gasta S/ 5 000 de “Caja disponible”.
    - Permanentemente, todas las compras nacionales costaran el 70% del precio.
    - Puedes fijar un flag “DescuentoCompra = True” o “DescuentoCompra = 0.7”
      •Debes idear la forma de que esto afecte a la funcion compras_comprar_insumos_nacionales.
    """
    if estado["Caja disponible"] >= 5000:
        estado["Caja disponible"] -= 5000
        estado["DescuentoCompra"] = True
    return estado


def compras_negociar_credito(estado):
    """
    6. Negociar credito con proveedores:
    - Gasta S/ 2 000 de “Caja disponible”.
    - Fija el flag “CreditoConcedido = True” para que el pago de mercaderia
      se postergue hasta 90 dias (es decir, 3 turnos).
    - El efecto es permanente, los insumos que compres, se paga en 90 dias.
    - Debes pensar una estructura de datos que nos permita saber cuantos soles estamos comprando a 90 dias (3 turnos)
      y cuantos turnos le queda a cada cuenta por pagar. Al momento de pagar, el dinero puede salir de caja o aumentar la deuda.
    """
    if estado["Caja disponible"] >= 2000:
        estado["Caja disponible"] -= 2000
        estado["CreditoConcedido"] = True
        estado["PlazoPagoProveedores"] = 3
    return estado


def compras_no_hacer_nada(estado):
    """
    7. No hacer nada en el area de Compras:
    - Retorna el estado sin cambios.
    """
    return estado


# ---------------- Finanzas ----------------


def finanzas_pagar_proveedores(estado):
    """
    1. Pagar proveedores:
    Esta funcion esta relacionada con compras_negociar_credito.
    Aplica para compras de insumos al credito.

    Efecto:
    Pagar al contado todas las cuentas por pagar, obteniendo un descuento del 5% por pronto pago.
    - Solo aplica para compra de insumos
    - Si no tenemos deudas a 90 dias, esta accion no hace nada.
    """
    if estado["DeudasProveedores"]:
        deuda_total = sum(monto for monto, _ in estado["DeudasProveedores"])
        descuento = deuda_total * 0.05
        monto_a_pagar = deuda_total - descuento

        if estado["Caja disponible"] >= monto_a_pagar:
            estado["Caja disponible"] -= monto_a_pagar
            estado["DeudasProveedores"] = []
        else:
            estado["DeudasProveedores"] = [(deuda_total - estado["Caja disponible"], 3)]
            estado["Caja disponible"] = 0
    return estado


def finanzas_pagar_deuda(estado):
    """
    2. Pagar deuda:

    a) Si “Caja disponible” ≥ 10 000 Y “Deuda pendiente” ≥ 10 000:
       - Restar 10 000 de “Caja disponible”.
       - Restar 10 000 de “Deuda pendiente”.

    b) Si “Caja disponible” ≥ 10 000 pero “Deuda pendiente” < 10 000:
       - Su deuda restante es menor a 10 000:
         • Restar de “Caja disponible” exactamente el monto de “Deuda pendiente”.
         • Poner “Deuda pendiente” = 0.

    c) Si “Caja disponible” < 10 000 Y “Deuda pendiente” > 0:
       - Solo podra pagar hasta lo que tenga en caja:
         • pago = “Caja disponible” (el total de caja).
         • Restar “pago” de “Deuda pendiente”.
         • Poner “Caja disponible” = 0.

    En cualquier otro caso (deuda = 0 o caja = 0), no se modifica nada.
    """
    deuda = estado["Deuda pendiente"]
    caja = estado["Caja disponible"]

    if deuda == 0 or caja == 0:
        return estado

    if caja >= 10000 and deuda >= 10000:
        estado["Caja disponible"] -= 10000
        estado["Deuda pendiente"] -= 10000
    elif caja >= 10000 and deuda < 10000:
        estado["Caja disponible"] -= deuda
        estado["Deuda pendiente"] = 0
    elif caja < 10000 and deuda > 0:
        estado["Deuda pendiente"] -= caja
        estado["Caja disponible"] = 0

    return estado


def finanzas_solicitar_prestamo(estado):
    """
    3. Solicitar prestamo:
    - Añade S/ 30 000 a “Caja disponible”.
    - Añade S/ 35 000 a “Deuda pendiente”.
    """
    estado["Caja disponible"] += 30000
    estado["Deuda pendiente"] += 35000
    return estado


def finanzas_crear_fondo_emergencia(estado):
    """
    4. Crear fondo de emergencia:
    - Si “Caja disponible” ≥ 10 000:
        • Resta 10 000 de “Caja disponible”.
        • Fija el flag “Fondo emergencia = True”.
    - En otro caso, retorna sin cambios.
    - Debe simplementar una variable que represente tener un fondo de emergencia.
    - Esta accion bloquea diversas Cartas del Caos que involcuren gastos inesperaods (sin importar su costo)
    """
    if estado["Caja disponible"] >= 10000:
        estado["Caja disponible"] -= 10000
        estado["Fondo emergencia"] = True
    return estado


def finanzas_no_hacer_nada(estado):
    """
    5. No hacer nada en el area de Finanzas:
    - Retorna el estado sin cambios.
    """
    return estado
