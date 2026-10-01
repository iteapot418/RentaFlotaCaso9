# ============================================================
# RENTAFLOTA - BLOQUE D
# Integrante 4: Devolucion, disponibilidad y mantenimiento
# Trabajo Parcial - Caso 9
# Programacion estructurada en Python
#
# Restricciones respetadas:
# - Uso de funciones, listas, diccionarios y tuplas.
# - Nombres en snake_case.
# - Identificadores breves.
# ============================================================

# -------------------------
# DATOS COMPARTIDOS
# -------------------------

categorias = ("Economico", "SUV-Camioneta", "Premium")
estados_veh = ("Disponible", "Alquilado", "En mantenimiento")
ciudades = ("Lima", "Arequipa", "Cusco")

sucursales = []
vehiculos = []
clientes = []
contratos = []
manttos = []


# -------------------------
# FUNCIONES AUXILIARES
# Estas funciones existen aqui para que el bloque pueda
# probarse de forma independiente. Al integrar el proyecto,
# pueden reemplazarse por las del bloque correspondiente.
# -------------------------

def buscar_suc(cod_suc):
    for sucursal in sucursales:
        if sucursal["cod_suc"] == cod_suc:
            return sucursal
    return None


def buscar_veh(placa):
    for vehiculo in vehiculos:
        if vehiculo["placa"] == placa:
            return vehiculo
    return None


def buscar_cont(cod_cont):
    for contrato in contratos:
        if contrato["cod_cont"] == cod_cont:
            return contrato
    return None


def buscar_mant(cod_mant):
    for mantto in manttos:
        if mantto["cod_mant"] == cod_mant:
            return mantto
    return None


def leer_float(mensaje, minimo=0):
    while True:
        try:
            valor = float(input(mensaje))
            if valor < minimo:
                print(f"El valor no puede ser menor que {minimo}.")
                continue
            return valor
        except ValueError:
            print("Ingrese un numero valido.")


# -------------------------
# BLOQUE D - INTEGRANTE 4
# -------------------------

def rev_mantto(placa):
    """
    Comprueba si el vehiculo supero 5000 km desde
    su ultimo mantenimiento.

    Retorna:
        True  -> requiere mantenimiento.
        False -> no requiere mantenimiento.
        None  -> vehiculo no encontrado.
    """
    vehiculo = buscar_veh(placa)

    if vehiculo is None:
        return None

    km_actual = vehiculo["km_actual"]
    km_ult = vehiculo["km_ult_mant"]

    return (km_actual - km_ult) > 5000


def act_vehiculo(placa, km_final, suc_dev):
    """
    Actualiza kilometraje, sucursal y estado del vehiculo
    despues de una devolucion.
    """
    vehiculo = buscar_veh(placa)

    if vehiculo is None:
        return False, "Vehiculo no encontrado."

    if buscar_suc(suc_dev) is None:
        return False, "La sucursal de devolucion no existe."

    if km_final < vehiculo["km_actual"]:
        return False, "El kilometraje no puede disminuir."

    vehiculo["km_actual"] = km_final
    vehiculo["cod_suc"] = suc_dev

    if rev_mantto(placa):
        vehiculo["estado"] = "En mantenimiento"
    else:
        vehiculo["estado"] = "Disponible"

    return True, "Vehiculo actualizado correctamente."


def reg_devol():
    """
    Registra la devolucion de un vehiculo.

    Reglas:
    - El contrato debe existir y estar Activo.
    - km_final no puede ser menor que km_inicial.
    - La sucursal de devolucion debe existir.
    - Se actualiza el estado del contrato.
    - Se actualiza km, sucursal y estado del vehiculo.

    Nota de integracion:
    El costo final corresponde al Bloque C. Antes de cerrar
    definitivamente el flujo general, calc_costo debe haber
    actualizado 'costo_total' con la fecha real y km final.
    """
    print("\n--- REGISTRAR DEVOLUCION ---")

    cod_cont = input("Codigo del contrato: ").strip()
    contrato = buscar_cont(cod_cont)

    if contrato is None:
        print("Contrato no encontrado.")
        return False

    if contrato["estado_cont"] != "Activo":
        print("El contrato ya se encuentra cerrado.")
        return False

    placa = contrato["placa"]
    vehiculo = buscar_veh(placa)

    if vehiculo is None:
        print("El vehiculo asociado al contrato no existe.")
        return False

    fec_real = input("Fecha real de devolucion: ").strip()
    if fec_real == "":
        print("La fecha real es obligatoria.")
        return False

    km_final = leer_float("Kilometraje final: ", 0)

    if km_final < contrato["km_inicial"]:
        print("El km final no puede ser menor que el km inicial.")
        return False

    # Tambien evita reducir el kilometraje actual del vehiculo.
    if km_final < vehiculo["km_actual"]:
        print("El km final no puede ser menor que el km actual del vehiculo.")
        return False

    suc_dev = input("Codigo de sucursal de devolucion: ").strip()

    if buscar_suc(suc_dev) is None:
        print("La sucursal de devolucion no existe.")
        return False

    contrato["fec_real"] = fec_real
    contrato["km_final"] = km_final
    contrato["suc_dev"] = suc_dev

    ok, mensaje = act_vehiculo(placa, km_final, suc_dev)

    if not ok:
        print(mensaje)
        return False

    contrato["estado_cont"] = "Cerrado"

    print("Devolucion registrada correctamente.")
    print(mensaje)

    if vehiculo["estado"] == "En mantenimiento":
        print("ALERTA: el vehiculo supero 5000 km desde el ultimo mantenimiento.")
    else:
        print("El vehiculo vuelve a estado Disponible.")

    return True


def reg_mantto():
    """
    Registra un mantenimiento basico y actualiza km_ult_mant.
    """
    print("\n--- REGISTRAR MANTENIMIENTO ---")

    cod_mant = input("Codigo de mantenimiento: ").strip()

    if cod_mant == "":
        print("El codigo es obligatorio.")
        return False

    if buscar_mant(cod_mant) is not None:
        print("El codigo de mantenimiento ya existe.")
        return False

    placa = input("Placa del vehiculo: ").strip()
    vehiculo = buscar_veh(placa)

    if vehiculo is None:
        print("Vehiculo no encontrado.")
        return False

    fecha = input("Fecha de mantenimiento: ").strip()

    if fecha == "":
        print("La fecha es obligatoria.")
        return False

    km_mant = leer_float("Kilometraje del mantenimiento: ", 0)

    if km_mant < vehiculo["km_ult_mant"]:
        print("El kilometraje de mantenimiento no puede retroceder.")
        return False

    if km_mant > vehiculo["km_actual"]:
        print("El km de mantenimiento no puede superar el km actual.")
        return False

    tipo_mant = input("Tipo de mantenimiento: ").strip()

    if tipo_mant == "":
        print("El tipo de mantenimiento es obligatorio.")
        return False

    costo = leer_float("Costo del mantenimiento: ", 0)

    mantto = {
        "cod_mant": cod_mant,
        "placa": placa,
        "fecha": fecha,
        "km_mant": km_mant,
        "tipo_mant": tipo_mant,
        "costo": costo
    }

    manttos.append(mantto)
    vehiculo["km_ult_mant"] = km_mant

    # Luego del mantenimiento el vehiculo vuelve a Disponible.
    vehiculo["estado"] = "Disponible"

    print("Mantenimiento registrado correctamente.")
    return True


def ver_disponib(categoria="", cod_suc=""):
    """
    Muestra vehiculos Disponibles, con filtro opcional
    por categoria y sucursal.

    Retorna la lista encontrada.
    """
    encontrados = []

    if categoria != "" and categoria not in categorias:
        print("Categoria no valida.")
        return encontrados

    if cod_suc != "" and buscar_suc(cod_suc) is None:
        print("Sucursal no encontrada.")
        return encontrados

    for vehiculo in vehiculos:
        if vehiculo["estado"] != "Disponible":
            continue

        if categoria != "" and vehiculo["categoria"] != categoria:
            continue

        if cod_suc != "" and vehiculo["cod_suc"] != cod_suc:
            continue

        encontrados.append(vehiculo)

    if len(encontrados) == 0:
        print("No hay vehiculos disponibles con esos filtros.")
        return encontrados

    print("\n--- VEHICULOS DISPONIBLES ---")
    for vehiculo in encontrados:
        print(
            f'Placa: {vehiculo["placa"]} | '
            f'{vehiculo["marca"]} {vehiculo["modelo"]} | '
            f'Categoria: {vehiculo["categoria"]} | '
            f'Sucursal: {vehiculo["cod_suc"]} | '
            f'Km: {vehiculo["km_actual"]:.2f}'
        )

    return encontrados


def calc_ocup():
    """
    Calcula:
        vehiculos alquilados / total de vehiculos

    Retorna la tasa decimal.
    """
    total = len(vehiculos)

    if total == 0:
        return 0.0

    alquilados = 0

    for vehiculo in vehiculos:
        if vehiculo["estado"] == "Alquilado":
            alquilados += 1

    return alquilados / total


# -------------------------
# DATOS DE PRUEBA
# Solo se cargan al ejecutar este archivo directamente.
# No se cargan cuando el bloque se importa al archivo final.
# -------------------------

def cargar_prueba():
    if len(sucursales) == 0:
        sucursales.extend([
            {
                "cod_suc": "LIM01",
                "nom_suc": "Lima Centro",
                "ciudad": "Lima"
            },
            {
                "cod_suc": "ARE01",
                "nom_suc": "Arequipa Centro",
                "ciudad": "Arequipa"
            },
            {
                "cod_suc": "CUS01",
                "nom_suc": "Cusco Centro",
                "ciudad": "Cusco"
            }
        ])

    if len(vehiculos) == 0:
        vehiculos.extend([
            {
                "placa": "ABC123",
                "marca": "Toyota",
                "modelo": "Yaris",
                "anio": 2024,
                "categoria": "Economico",
                "tarifa_dia": 120.0,
                "km_actual": 15100.0,
                "estado": "Alquilado",
                "cod_suc": "LIM01",
                "km_ult_mant": 10000.0
            },
            {
                "placa": "SUV456",
                "marca": "Kia",
                "modelo": "Sportage",
                "anio": 2023,
                "categoria": "SUV-Camioneta",
                "tarifa_dia": 220.0,
                "km_actual": 8200.0,
                "estado": "Disponible",
                "cod_suc": "ARE01",
                "km_ult_mant": 5000.0
            },
            {
                "placa": "PRE789",
                "marca": "BMW",
                "modelo": "320i",
                "anio": 2024,
                "categoria": "Premium",
                "tarifa_dia": 380.0,
                "km_actual": 4200.0,
                "estado": "Disponible",
                "cod_suc": "CUS01",
                "km_ult_mant": 2000.0
            }
        ])

    if len(contratos) == 0:
        contratos.append({
            "cod_cont": "C001",
            "documento": "12345678",
            "placa": "ABC123",
            "suc_retiro": "LIM01",
            "fec_inicio": "20/09/2026",
            "fec_fin": "25/09/2026",
            "km_inicial": 15000.0,
            "seguro": True,
            "fec_real": "",
            "km_final": 0.0,
            "suc_dev": "",
            "costo_total": 0.0,
            "estado_cont": "Activo"
        })


# -------------------------
# MENU DE PRUEBA DEL BLOQUE D
# -------------------------

def menu_part4():
    while True:
        print("\n===================================")
        print(" RENTAFLOTA - BLOQUE D / PARTE 4")
        print("===================================")
        print("1. Registrar devolucion")
        print("2. Registrar mantenimiento")
        print("3. Consultar disponibilidad")
        print("4. Calcular tasa de ocupacion")
        print("5. Revisar mantenimiento por placa")
        print("6. Mostrar estado de vehiculos")
        print("7. Salir")

        opcion = input("Seleccione una opcion: ").strip()

        if opcion == "1":
            reg_devol()

        elif opcion == "2":
            reg_mantto()

        elif opcion == "3":
            print("\nDeje vacio un filtro para no aplicarlo.")
            categoria = input(
                "Categoria (Economico/SUV-Camioneta/Premium): "
            ).strip()
            cod_suc = input("Codigo de sucursal: ").strip()
            ver_disponib(categoria, cod_suc)

        elif opcion == "4":
            tasa = calc_ocup()
            print(f"Tasa de ocupacion: {tasa:.2%}")

        elif opcion == "5":
            placa = input("Placa: ").strip()
            resultado = rev_mantto(placa)

            if resultado is None:
                print("Vehiculo no encontrado.")
            elif resultado:
                print("El vehiculo requiere mantenimiento.")
            else:
                print("El vehiculo no requiere mantenimiento.")

        elif opcion == "6":
            print("\n--- ESTADO DE VEHICULOS ---")
            if len(vehiculos) == 0:
                print("No hay vehiculos registrados.")
            else:
                for vehiculo in vehiculos:
                    print(
                        f'{vehiculo["placa"]} | '
                        f'{vehiculo["estado"]} | '
                        f'Km: {vehiculo["km_actual"]:.2f} | '
                        f'Sucursal: {vehiculo["cod_suc"]} | '
                        f'Ult. mant.: {vehiculo["km_ult_mant"]:.2f}'
                    )

        elif opcion == "7":
            print("Fin de la prueba del Bloque D.")
            break

        else:
            print("Opcion no valida.")


if __name__ == "__main__":
    cargar_prueba()
    menu_part4()
