# cartas.py
import math

def aplicar_aumento_costos(estado, monto):
    if estado.get("AumentoCostosCrisis", 0) > 0:
        return round(monto * 1.10)
    return monto

def aplicar_carta(numero, estado):

    if numero ==1:
        return estado # retorna el estado sin cambios

    elif numero ==2:
        # divide el string en partes usando "/"
        partes = estado["Maquinas (total/activas/dañadas)"].split("/")

        # convierte cada parte a número entero
        # map() es una forma de convetir string a enteros y asignarlos a variables
        total, activas, danadas = map(int, partes)

        # reduce las máquinas activas en 2 pero no en menos de 0
        # max() compara dos valores y devuelve el mayor, asegurando que nuevas_activas nunca sea negativo
        nuevas_activas = max(0, activas - 2)

        # aumenta las máquinas dañadas con las que dejaron de estar activas
        nuevas_danadas = danadas + (activas - nuevas_activas)

        # actualiza el estado
        estado["Maquinas (total/activas/dañadas)"] = f"{total}/{nuevas_activas}/{nuevas_danadas}"
        return estado

    elif numero == 3:
        # se bloquea la producción y las compras (True)
        estado["Prohibir Produccion"] = True
        estado["Prohibir Compras"] = True

        # activa el flag del virus
        estado["VirusInformatico"] = True

        # establece los turnos que durará el virus
        estado["DuracionVirus"] = 2

        # se obtiene el valor se divide por partes y se toma el último elemento par convertirlo en entero
        nivel_reputacion = int(estado["Reputacion del mercado"].split()[-1])

        # se le resta al nivel actual, por el max() se evita que sea un negativo y se crea un formato string para actualizar el diccionario
        estado["Reputacion del mercado"] = f"Nivel {max(1, nivel_reputacion - 1)}"
        return estado

    elif numero == 4:
        # se pierde todo el inventario
        estado["Inventario"] = 0
        return estado

    elif numero == 5:
        # se aumenta las multas en 5000
        estado["Multas e indemnizaciones"] += 5000

        # se obtiene el valor se divide por partes y se toma el último elemento par convertirlo en entero
        nivel_reputacion = int(estado["Reputacion del mercado"].split()[-1])

        # se le resta al nivel actual, por el max() se evita que sea un negativo y se crea un formato string para actualizar el diccionario
        estado["Reputacion del mercado"] = f"Nivel {max(1, nivel_reputacion - 1)}"
        return estado

    elif numero == 6:
        nivel_reputacion = int(estado["Reputacion del mercado"].split()[-1])

        #se reduce la reputación en 2 niveles
        estado["Reputacion del mercado"] = f"Nivel {max(1, nivel_reputacion - 2)}"

        # se obtiene el número de pedidos pendientes
        demanda_actual = estado["Pedidos por atender"]

        # resta la demanda actual al inventario
        estado["Inventario"] = max(0, estado["Inventario"] - demanda_actual)

        #calcula la mitad de la demanda
        estado["Pedidos por atender"] = int(demanda_actual * 0.5)

        # si hay un producto retirado se activa el flag por 2 turnos de duración
        estado["ProductoRetirado"] = True
        estado["DuracionRetiro"] = 2
        return estado

    elif numero == 7:
        # se pierde el 30% de los insumos disponibles
        estado["Insumos disponibles"] = int(estado["Insumos disponibles"] * 0.7)
        return estado

    elif numero == 8:
        # dividde el estado en partes
        partes = estado["Maquinas (total/activas/dañadas)"].split("/")

        # se asignan los valores
        total, activas, danadas = map(int, partes)

        # se resta el número de máquinas activas y se suma las dañadas mientras se actualiza el valor en el diccionario
        estado["Maquinas (total/activas/dañadas)"] = f"{total}/{max(0, activas - 1)}/{danadas + 1}"

        # se reduce el número de empleados y se actualiza
        estado["Cantidad de empleados"] = max(0, estado["Cantidad de empleados"] - 1)
        return estado

    elif numero == 9:
        # bloquea la producción durante la huelga
        estado["Prohibir Produccion"] = True
        nivel_reputacion = int(estado["Reputacion del mercado"].split()[-1])

        # reduce la reputación en 3 niveles
        estado["Reputacion del mercado"] = f"Nivel {max(1, nivel_reputacion - 3)}"

        # activa el flag por 2 turnos
        estado["HuelgaActiva"] = True
        estado["DuracionHuelga"] = 2
        return estado

    elif numero == 10:
        # si hay 5000 o mas se resta el monto de caja disponible con 5000
        # sino se salta a la linea 5
        if estado["Caja disponible"] >= 5000:
            estado["Caja disponible"] -= 5000
        else:
            # calcula cuanto dinero no alcanza para pagar los 5000
            falta = 5000 - estado["Caja disponible"]

            # añade un 12% de interes al monto que falta y lo guarda en la deuda pendiente
            estado["Deuda pendiente"] += falta * 1.12

            # la caja se vacia (se usó todo para pagar)
            estado["Caja disponible"] = 0

        # suma 5000 a las multas (independientemente de si se pudo pagar o ñe)
        estado["Multas e indemnizaciones"] += 5000

        # obtiene el nivel de reputación
        nivel_reputacion = int(estado["Reputacion del mercado"].split()[-1])

        # reduce la reputación en 2 niveles y lo actualiza
        estado["Reputacion del mercado"] = f"Nivel {max(1, nivel_reputacion - 2)}"
        return estado

#----------------------------------------------------------------------------------------------

    elif numero == 11:
        # aumenta las multas en 50000
        estado["Multas e indemnizaciones"] += 5000

        # reduce la reputación en 1 nivel
        nivel_reputacion = int(estado["Reputacion del mercado"].split()[-1])
        estado["Reputacion del mercado"] = f"Nivel {max(1, nivel_reputacion - 2)}"
        return estado

    elif numero == 12:
        # activa flag para reducri ventas al 50% durante 2 turnos
        estado["BoicotClientes"] = True
        estado["DuracionNoicot"] = 2
        return estado

    elif numero == 13:
        # calcula el total de ventas multiplicando unidades vendidas por el precio de venta
        ventas_recientes = estado["Unidades vendidas"] * estado["Precio de venta"]

        # resta las ventas recientes del dinero disponible
        estado["Caja disponible"] -= ventas_recientes

        # ve si el dinero en caja es mayor o igual a 15000
        if estado["Caja disponible"] >= 15000:

            # si hay suficiente dinero se resta 15000 de la caja
            estado["Caja disponible"] -= 15000
        else:
            # sino calcula cuánto dinero falta para los 15000
            falta = 15000 - estado["Caja disponible"]

            #añade a la deuda pendiente el monto que faltaba máss un 12%
            estado["Deuda pendiente"] += falta * 1.12

            #se actuaiza el dinero disponible (se gastó todo oño)
            estado["Caja disponible"] = 0

        # establece que hay un error que durará 3 turnos
        estado["ErrorEtiquetado"] = True
        estado["DuracionError"] = 3
        return estado

    elif numero == 14:
        # bloquea compras de insumos importados por 3 turnos
        estado["Prohibir Importaciones"] = True
        estado["DuracionRetradoImport"] = 3
        return estado

    elif numero == 15:
        # bloquea compras nacionales por 4 turnos
        estado["Prohibir Compras"] = True
        estado["DuracionHuelgaProveedores"] = 4
        return estado

    elif numero == 16:
        # comprueba valores
        if estado["Caja disponible"] >= 8000:

            # resta 8000 de la caja si es que hay al menos ese monto
            estado["Caja disponible"] -= 8000
        else:
            # sino se ve cuánto dinero falta para los 8000
            falta = 8000 - estado["Caja disponible"]

            # #añade a la deuda pendiente el monto que faltaba máss un 12%
            estado["Deuda pendiente"] += falta * 1.12

            # la caja se actualiza
            estado["Caja disponible"] = 0
        return estado

    elif numero == 17:
        # reduce reputación en 2 niveles
        nivel_reputacion = int(estado["Reputacion del mercado"].split()[-1])
        estado["Reputacion del mercado"] = f"Nivel {max(1, nivel_reputacion - 2)}"
        return estado
    elif numero == 18:
        # reduce la producción a la mitad por 3 turnos
        estado["PlagaActiva"] = True
        estado["DuracionPlaga"] = 3
        return estado

    elif numero == 19:
        # reduce los pedidos pendientes en un tercio
        estado["Pedidos por atender"] = int(estado["Pedidos por atender"] * [2/3])
        return estado

    elif numero == 20:
        # reduce reputación en 3 niveles
        nivel_reputacion = int(estado["Reputacion del mercado"].split()[-1])
        estado["Reputacion del mercado"] = f"Nivel {max(1, nivel_reputacion - 3)}"
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