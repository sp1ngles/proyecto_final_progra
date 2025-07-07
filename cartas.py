# cartas.py
import math
def aplicar_aumento_costos(estado, monto):
    if estado.get("AumentoCostosCrisis", 0) > 0:
        return round(monto * 1.10)
    return monto

def aplicar_carta(numero, estado):

    # —————— BLOQUE DE PROTECCIONES ——————
    # 1) Fondo de emergencia protege de gastos y multas directas
    cartas_gasto_o_multa = {5, 10, 11, 16, 25, 27, 32, 35, 36, 37}
    if numero in cartas_gasto_o_multa and estado.get("Fondo emergencia", False):
        # Se consume el fondo y se bloquea el efecto de la carta
        estado["Fondo emergencia"] = False
        return estado

    # 2) Protección de Mantenimiento (cartas que dañan máquinas o recursos humanos)
    if numero in {2, 8} and estado.get("TurnosProteccionMantenimiento", 0) > 0:
        return estado

    # 3) Protección contra clima (huelgas internas)
    if numero == 9 and estado.get("TurnosProteccionClima", 0) > 0:
        return estado

    # 4) Protección de Seguridad (accidentes, derrames químicos)
    if numero in {4, 37, 38} and estado.get("TurnosProteccionSeguridad", 0) > 0:
        return estado

    # 5) Protección de Demanda/Reputación (boicots, fake news, competidores…)
    cartas_demanda_reputacion = {12, 17, 19, 20, 23, 26, 29, 33, 34}
    if numero in cartas_demanda_reputacion and (
            estado.get("TurnosProteccionDemanda", 0) > 0
            or estado.get("TurnosProteccionReputacion", 0) > 0):
        return estado

    # 6) Protección específica de e‑commerce (virus informático que ataca visibilidad)
    if numero == 3 and estado.get("TurnosProteccionEcommerce", 0) > 0:
        return estado

    # —————— FIN BLOQUE DE PROTECCIONES ——————

    # Carta 1: Dia tranquilo:
    # No ocurre nada malo.
    if numero == 1:
        return estado

    # Carta 2: Falla critica en maquinaria:
    # Pierdes 2 maquinas activas permanentemente (hasta hacer mantenimiento)
    elif numero == 2:

        total, activas, danadas = map(int, estado["Maquinas (total/activas/dañadas)"].split('/'))
        perdidas = min(2, activas)
        activas = activas - perdidas
        danadas = danadas + perdidas
        total = activas + danadas
        estado["Maquinas (total/activas/dañadas)"] = f"{total}/{activas}/{danadas}"

        return estado

    # Carta 3: Virus informatico:
    # Se pierde visibilidad del inventario y de los insumos por 1 turno
    # No puedes producir porque no sabes cuantos insumos hay.
    # No puedes vender porque no sabes cuanto invnetario hay.
    # Los clientes se enteraron y bajo la reputacion 1 nivel
    # Duración: 2 turnos
    elif numero == 3:
        estado["SinVisibilidad"] = True
        estado["Prohibir Produccion"] = True
        estado["SePuedeVender"] = False
        estado["TurnosSinVisibilidad"] = 1
        estado["VirusInformatico"] = 2
        nivel = int(estado["Reputacion del mercado"].split()[1])
        estado["Reputacion del mercado"] = f"Nivel {max(1, nivel - 1)}"
        # Bloqueo de visibilidad, venta y producción por 2 turnos
        # Agregar estado["SePuedeVender"], estado["SinVisibilidad"] y estado["VirusInformatico"]
        return estado

    # Carta 4: Incendio en almacen
    #   - Se pierde el inventario total (al final del mes, despues de haber producido y vendido)
    elif numero == 4:

        estado["IncendioAlmacen"] = True

        return estado

    # Carta 5: Auditoria desfavorable
    #   - Aumentan las multas e indemnizaciones en +5000.
    # Los clientes se enteraron y bajo la reputacion 1 nivel
    elif numero == 5:

        estado["Multas e indemnizaciones"] += 5000
        nivel = int(estado["Reputacion del mercado"].split()[1])
        estado["Reputacion del mercado"] = f"Nivel {max(1, nivel-1)}"

        return estado

    # Carta 6: Producto retirado del mercado
    #   - Reputacion se reduce 2 niveles.
    #   - Tuvimos que reponer mercaderia equivalente a la demanda actual (elimina el inventario equivalente a la demanda)
    #   - Luego, la demanda actual se reduce en 50%
    # Duración: 2 turnos
    elif numero == 6:
        # Rebaja reputación 2 niveles
        nivel = int(estado["Reputacion del mercado"].split()[1])
        estado["Reputacion del mercado"] = f"Nivel {max(1, nivel-2)}"
        # Elimina inventario igual a la demanda actual
        demanda = estado.get("Pedidos por atender", 0)
        estado["Inventario"] = max(0, estado.get("Inventario", 0) - demanda)
        # Reduce demanda en 50%
        estado["Pedidos por atender"] = demanda // 2
        # Duración del efecto de reducción de demanda: 2 turnos
        estado["TurnosReduccionDemandaProductoRetirado"] = 2
        return estado

    # Carta 7: Robo de insumos
    #   - Pierdes 30% de insumos disponibles.
    elif numero == 7:

        estado["Insumos disponibles"] = math.floor(estado.get("Insumos disponibles", 0) * 0.7)

        return estado

    # Carta 8: Fuga de talento clave
    #   - Tras la fuga de talento, operarios sin experiencia manipularon y dañaron una maquina
    #   - Pierdes 1 maquina activa (pasa a dañada).
    #   - Pierdes 1 empleado.
    elif numero == 8:

        # Una máquina activa pasa a dañada
        total, activas, danadas = map(int, estado["Maquinas (total/activas/dañadas)"].split('/'))
        if activas > 0:
            activas -= 1
            danadas += 1
        estado["Maquinas (total/activas/dañadas)"] = f"{total}/{activas}/{danadas}"
        # Pierde un empleado
        estado["Cantidad de empleados"] = max(0, estado.get("Cantidad de empleados", 0) - 1)

        return estado

    # Carta 9: Huelga por ambiente laboral
    #   - La proxima ronda no se produce.
    #   - Los clientes se enteran de la huelga y baja la reputación 3 niveles
    # Duración: 2 turnos
    elif numero == 9:

        estado["TurnosSinProduccionDerrame"] = max(estado.get("TurnosSinProduccionDerrame", 0), 2)
        # Reputación baja 3 niveles
        nivel = int(estado["Reputacion del mercado"].split()[1])
        estado["Reputacion del mercado"] = f"Nivel {max(1, nivel-3)}"

        return estado

    # Carta 10: Cracker secuestra datos
    #   - Pierdes 5,000 de caja (si no alcanza, la diferencia se convierte en deuda al 12%)
    #   - Reputacion baja 2 niveles
    #   - Te aplican una multa de 5,000 soles por malas practicas de seguridad de la informacion
    elif numero == 10:

        # Pierde S/ 5,000 o deuda al 12%
        monto = 5000
        if estado.get("Caja disponible", 0) >= monto:
            estado["Caja disponible"] -= monto
        else:
            falt = monto - estado.get("Caja disponible", 0)
            estado["Caja disponible"] = 0
            estado["Deuda pendiente"] += round(falt * 1.12)
        # Reputación baja 2 niveles
        nivel = int(estado["Reputacion del mercado"].split()[1])
        estado["Reputacion del mercado"] = f"Nivel {max(1, nivel-2)}"
        # Multa por seguridad
        estado["Multas e indemnizaciones"] += 5000

        return estado

    # Carta 11: Multa ambiental
    #   - Aumentan “Multas e indemnizaciones” en +5000.
    #   - Reputacion del mercado −1 nivel.
    elif numero == 11:

        # Aplicar multa
        estado["Multas e indemnizaciones"] += 5000

        # Reducir reputación 1 nivel (mínimo Nivel 1)
        nivel_actual = int(estado["Reputacion del mercado"].split(" ")[1])
        nuevo_nivel = max(1, nivel_actual - 1)
        estado["Reputacion del mercado"] = f"Nivel {nuevo_nivel}"

        return estado

    # Carta 12: Boicot de clientes
    #   - Ventas de esta semana reducidas al 50%:
    # Duración: 2 turnos
    elif numero == 12:

        estado["ReduccionVentasBoicot"] = 2

        return estado

    # Carta 13: Error de etiquetado
    #   - Devuelven todas las unidades vendidas el turno actual y el turno anterior
    #     • Debes devolver el dinero obtenido por dichas ventas
    #     • Además, gastas 15,000 soles en la logística inversa
    # Duración: 3 turnos
    elif numero == 13:

        # 1) Calcular unidades vendidas de este y anterior turno
        unidades_vendidas = estado.get("Unidades vendidas", 0) + estado.get("Ventas del turno anterior", 0)
        precio = estado.get("Precio de venta", 0)

        # 2) Devolver dinero por las unidades vendidas
        monto_devolucion = unidades_vendidas * precio
        estado["Caja disponible"] = max(0, estado.get("Caja disponible", 0) - monto_devolucion)

        # 3) Restituir inventario
        estado["Inventario"] += unidades_vendidas

        # 4) Gastar en logística inversa
        costo_logistica = aplicar_aumento_costos(estado,15000)
        if estado["Caja disponible"] >= costo_logistica:
            estado["Caja disponible"] -= costo_logistica
        else:
            falt = costo_logistica - estado["Caja disponible"]
            estado["Caja disponible"] = 0
            estado["Deuda pendiente"] += round(falt * 1.12)

        return estado

    # Carta 14: Retraso en importacion
    #   - Prohibir insumos importados las siguientes 3 rondas:
    elif numero == 14:

        estado["TurnosSinImportaciones"] = 3
        estado["Prohibir Importaciones"] = True

        return estado

    # Carta 15: Proveedores en huelga
    #   - Prohibir compras nacionales las siguientes 4 rondas:
    elif numero == 15:

        estado["TurnosSinComprasNacionales"] = 4
        estado["Prohibir Compras Nacionales"] = True

        return estado

    # Carta 16: Estafa financiera
    #   - Pierdes 8,000 de caja
    elif numero == 16:

        monto = 8000

        if estado.get("Caja disponible", 0) >= monto:
            estado["Caja disponible"] -= monto
        else:
            faltante = monto - estado.get("Caja disponible", 0)
            estado["Caja disponible"] = 0
            estado["Deuda pendiente"] += round(faltante * 1.12)

        return estado

    # Carta 17: Rumor de corrupcion
    #   - Reputacion del mercado −2 niveles.
    elif numero == 17:

        # Extraer nivel actual
        nivel_actual = int(estado["Reputacion del mercado"].split(" ")[1])
        # Calcular nuevo nivel, sin bajar de 1
        nuevo_nivel = max(1, nivel_actual - 2)
        # Actualizar reputación
        estado["Reputacion del mercado"] = f"Nivel {nuevo_nivel}"

        return estado

    # Carta 18: Plaga en planta
    #   - Produccion a la mitad este turno
    # Duración: 3 turnos
    elif numero == 18:

        estado["TurnosProduccionPlaga"] = max(estado.get("TurnosProduccionPlaga", 0), 3)

        return estado

    # Carta 19: Cliente corproativo VIP cancela pedido
    #   - Peirdes un tercio de los “Pedidos por atender”.
    elif numero == 19:

        pedidos = estado.get("Pedidos por atender", 0)
        cancelados = pedidos // 3
        estado["Pedidos por atender"] = max(0, pedidos - cancelados)

        return estado

    # Carta 20: Producto defectuoso viral
    #   - Reputacion del mercado −3 niveles.
    elif numero == 20:

        nivel = int(estado["Reputacion del mercado"].split()[1])
        estado["Reputacion del mercado"] = f"Nivel {max(1, nivel - 3)}"

        return estado

    # Carta 21: Mal clima: inundacion
    #   - No se produce la siguiente ronda:
    # Duración: 2 turnos
    elif numero == 21:

        estado["TurnosSinProduccionDerrame"] = max(estado.get("TurnosSinProduccionDerrame", 0), 2)

        return estado

    # Carta 22: Licencia vencida
    #   - Multas +30,000.
    #   - Prohibir produccion la siguiente ronda.
    elif numero == 22:

        # 1) Aplicar multa ambiental
        estado["Multas e indemnizaciones"] += 30000

        # 2) Prohibir producción
        estado["Prohibir Produccion"] = True
        # Usamos un contador para controlar la duración exacta de la prohibición
        estado["TurnosSinProduccionLicencia"] = 1

        return estado

    # Carta 23: Fake news en redes
    #   - Reputacion del mercado −2 niveles.
    elif numero == 23:

        # Extraer nivel actual
        nivel_actual = int(estado["Reputacion del mercado"].split(" ")[1])
        # Calcular nuevo nivel sin bajar de Nivel 1
        nuevo_nivel = max(1, nivel_actual - 2)
        # Actualizar reputación
        estado["Reputacion del mercado"] = f"Nivel {nuevo_nivel}"

        return estado

    # Carta 24: Bloqueo logistico
    #   - No se venden unidades
    # Duración: 2 turnos
    elif numero == 24:

        estado["TurnosSinVentasBloqueo"] = max(estado.get("TurnosSinVentasBloqueo", 0), 2)

        return estado

    # Carta 25: Demanda judicial
    #   - Multas e indemnizaciones +15,000.
    elif numero == 25:

        estado["Multas e indemnizaciones"] += 15000

        return estado

    # Carta 26: Nuevo competidor agresivo
    #   - Ventas −40%:
    #   - Debemos pagar 5,000 por almacén
    # Duración: 3 turnos

    elif numero == 26:

        estado["ReduccionVentasCompetidor"] = 3

        # Restar S/ 5,000 de caja (sin generar deuda)
        estado["Caja disponible"] = max(0, estado.get("Caja disponible", 0) - 5000)

        return estado

    # Carta 27: Robo interno
    #   - Caja se reduce en 10,000.
    elif numero == 27:

        estado["Caja disponible"] = max(0, estado.get("Caja disponible", 0) - 10000)

        return estado

    # Carta 28: Crisis economica
    #   - Todos los costos +10% por los siguientes 5 turnos:
    elif numero == 28:

        estado["AumentoCostosCrisis"] = 5

        return estado

    # Carta 29: Fuga de datos
    #   - Reputacion del mercado −2 nivel.
    #   - Ventas de este mes se reducen en un 75%
    elif numero == 29:

        nivel_actual = int(estado["Reputacion del mercado"].split(" ")[1])
        nuevo_nivel = max(1, nivel_actual - 2)
        estado["Reputacion del mercado"] = f"Nivel {nuevo_nivel}"

        # 2) Marcar reducción de ventas al 25% este turno
        estado["ReduccionVentas75"] = True

        return estado

    # Carta 30: Huelga nacional
    #   - No ventas ni produccion
    #   - Debemos pagar 10,000 por almacén
    # Duración: 3 turnos
    elif numero == 30:

        # 1) Bloquear producción y ventas por 3 turnos
        estado["TurnosSinProduccionDerrame"] = max(estado.get("TurnosSinProduccionDerrame", 0), 3)
        estado["TurnosSinVentasBloqueo"] = max(estado.get("TurnosSinVentasBloqueo", 0), 3)

        # 2) Perder 10,000 de caja
        estado["Caja disponible"] = max(0, estado.get("Caja disponible", 0) - 10000)

        return estado

    # Carta 31: Rechazo de exportacion
    #   - Inventario acumulado (no se vende este mes).
    #   - Debemos pagar 10,000 por almacén
    elif numero == 31:

        costo_almacen = aplicar_aumento_costos(estado,10000)

        # Bloquear ventas este turno
        estado["NoVenderEsteTurno"] = True

        # Aplicar pago o deuda
        if estado["Caja disponible"] >= costo_almacen:
            estado["Caja disponible"] -= costo_almacen
        else:
            faltante = costo_almacen - estado["Caja disponible"]
            estado["Caja disponible"] = 0
            estado["Deuda pendiente"] += round(faltante * 1.12)

        return estado

    # Carta 32: Error contable
    #   - Caja −7000.
    elif numero == 32:

        monto_error = 7000

        if estado["Caja disponible"] >= monto_error:
            estado["Caja disponible"] -= monto_error
        else:
            faltante = monto_error - estado["Caja disponible"]
            estado["Caja disponible"] = 0
            # Se añade la parte que no se cubre como deuda con 12% de interés:
            estado["Deuda pendiente"] += round(faltante * 1.12)

        return estado

    # Carta 33: Error en codigo de barras
    #   - No se venden productos este mes:
    #   - reputación baja 2 niveles
    elif numero == 33:

        # Bloquear venta este turno
        estado["NoVenderEsteTurno"] = True

        # Reducir reputación 2 niveles (mínimo Nivel 1)
        nivel_act = int(estado["Reputacion del mercado"].split(" ")[1])
        nuevo_nivel = max(1, nivel_act - 2)
        estado["Reputacion del mercado"] = f"Nivel {nuevo_nivel}"

        return estado

    # Carta 34: Mal diseño del empaque
    #   - Ventas −25%
    #   - reputación baja 2 niveles
    # Duración: 2 turnos
    elif numero == 34:

        # Aplicar reducción de ventas por 2 turnos
        estado["TurnosReduccionVentasEmpaque"] = 2

        # Reducir reputación 2 niveles (mínimo Nivel 1)
        nivel_actual = int(estado["Reputacion del mercado"].split(" ")[1])
        nuevo_nivel = max(1, nivel_actual - 2)
        estado["Reputacion del mercado"] = f"Nivel {nuevo_nivel}"

        return estado

    # Carta 35: Cliente se intoxica
    #   - Reputacion del mercado −3 niveles.
    #   - Multas +30,000.
    elif numero == 35:

        # Aumentar multas
        estado["Multas e indemnizaciones"] += 30000

        # Reducir reputación 3 niveles (mínimo Nivel 1)
        nivel_actual = int(estado["Reputacion del mercado"].split(" ")[1])
        nuevo_nivel = max(1, nivel_actual - 3)
        estado["Reputacion del mercado"] = f"Nivel {nuevo_nivel}"

        return estado

    # Carta 36: Fraude en prestamo
    #   - Caja −15,000.
    #   - Deuda pendiente +15,000.
    #   - reputación baja 2 niveles
    elif numero == 36:

        monto = 15000

        # Restar de caja
        if estado["Caja disponible"] >= monto:
            estado["Caja disponible"] -= monto
        else:
            # Si no hay suficiente, llevar caja a 0
            estado["Caja disponible"] = 0

        # Incrementar deuda
        estado["Deuda pendiente"] += monto

        # Reducir reputación 2 niveles (mínimo Nivel 1)
        nivel_actual = int(estado["Reputacion del mercado"].split(" ")[1])
        nuevo_nivel = max(1, nivel_actual - 2)
        estado["Reputacion del mercado"] = f"Nivel {nuevo_nivel}"

        return estado

    # Carta 37: Trabajador se accidenta
    #   - Multas +4000.
    #   - Produccion −50% este mes
    #   - Temporalmente -1 trabajador por 2 turnos
    elif numero == 37:

        # 1) Multas
        estado["Multas e indemnizaciones"] += 4000

        # 2) Reducir producción a la mitad este turno
        #    reutilizamos el contador de plaga, que aplica *0.5 a la producción.
        estado["TurnosProduccionPlaga"] = 1

        # 3) Empleado accidentado
        #    quitamos inmediatamente 1 trabajador
        estado["Cantidad de empleados"] = max(0, estado["Cantidad de empleados"] - 1)
        #    y marcamos el accidente para que, al volver el contador a cero, se restituya
        estado["TurnosEmpleadoAccidentado"] = 2
        estado["_empleado_accidentado_flag"] = True

        return estado

    # Carta 38: Derrame quimico
    #   - Inventario e Insumos = 0
    #   - No puedes producir durante este mes y el siguiente
    elif numero == 38:

        # 1) Eliminar todo el inventario e insumos
        estado["Inventario"] = 0
        estado["Insumos disponibles"] = 0

        # 2) Bloquear producción por 2 turnos
        estado["TurnosSinProduccionDerrame"] = 2

        return estado

    # Carta 39: Virus contagioso
    #   Todos los empleados se quedaron en su casa por un mes
    #   No se vende ni se produce
    elif numero == 39:

        # Bloquear ventas durante 1 turno
        estado["TurnosSinVentasBloqueo"] = max(estado.get("TurnosSinVentasBloqueo", 0), 1)
        # Bloquear producción durante 1 turno
        estado["TurnosSinProduccionDerrame"] = max(estado.get("TurnosSinProduccionDerrame", 0), 1)

        return estado

    # Carta 40: Hiring Freeze
    #   No puedes contratar empleados nuevos
    # Duración: 5 turnos
    elif numero == 40:

        # Activar la prohibición de contratación
        estado["Prohibir Contratacion"] = True
        # Fijar contador de duración en 5 turnos
        estado["TurnosProhibirContratacion"] = 5

        return estado

    # Si el numero no coincide con ninguna carta:
    #    se considera Dia tranquilo (sin cambios).
    else:
        return estado