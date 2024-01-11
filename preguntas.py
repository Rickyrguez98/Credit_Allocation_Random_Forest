import re
from datetime import datetime
import streamlit as st
import uuid
class Preguntas:
    def __init__(self):
        self.key_counter = 0
        self.paterno = None
        self.materno = None
        self.nombres = None
        self.edad = 0
        self.curp = None
        self.domicilio = None
        self.email = None
        self.ingresos = 0
        self.egresos = 0
        self.num_tarjetas = 0
        self.credit_utilization = 0
        self.meses = 0
        self.respuesta_retorica = None
        self.dias_pago = 0
        self.tiene_prestamos = None
        self.cantidad_prestamos = 0
        self.monto_prestamo = 0
        self.tipo_tarjeta = None
        self.credito_total = 0
        self.porcentaje_inversion = 0

    def validar_curp(self, curp):
        if len(curp) != 18:
            return False
        if not re.match(r'^[A-Z&]{4}\d{6}[HM]{1}[A-Z0-9]{5}[A-Z0-9]{1}\d{1}$', curp):
            return False
        return True

    def obtener_nombre(self):
        while not (self.paterno and self.materno and self.nombres and self.edad and self.curp):
            if not self.paterno:
                self.paterno = st.text_input("Por favor, ingresa tu Apellido Paterno:", key=f"paterno_input_{self.key_counter}")

            if not self.materno:
                self.materno = st.text_input("Por favor, ingresa tu Apellido Materno:", key=f"materno_input_{self.key_counter}")

            if not self.nombres:
                self.nombres = st.text_input("Por favor, ingresa tus Nombres:", key=f"nombres_input_{self.key_counter}")

            if not self.edad:
                while True:
                    try:
                        entrada = st.text_input("Por favor, ingresa tu edad: ", key=f"edad_input_{self.key_counter}")
                        self.edad = int(entrada)
                        break
                    except ValueError:
                        st.warning("Error: Ingresa solo valores numéricos enteros para la edad.")
            self.key_counter += 1


            if not self.curp:
                curp_usuario = st.text_input("Por favor, ingresa tu CURP:", key="curp_input")
                if self.validar_curp(curp_usuario.upper()):
                    self.curp = curp_usuario
                else:
                    st.warning("Error: La CURP ingresada no es válida. Verifica el formato.")

    def preguntas_siguiente_seccion(self):
        self.domicilio = st.text_input("Por favor, ingresa tu domicilio:")
        self.email = st.text_input("Por favor, ingresa tu dirección de Correo Electrónico:")
        self.ingresos = int(st.text_input("Por favor, ingresa tus ingresos mensuales en MXN (Solo valores numéricos):"))
        self.egresos = int(st.text_input("Por favor, ingresa tus egresos mensuales en MXN (Solo valores numéricos):"))
        self.num_tarjetas = int(st.text_input("¿Con cuántas tarjetas de crédito cuentas actualmente?:"))
        self.credit_utilization = int(st.text_input("Aproximadamente, ¿Cuánto porcentaje utilizas de tu tarjeta de crédito al mes de 0 a 100?, ej: 20% = 20, ingresa un numero entero:"))
        self.meses = int(st.text_input("¿Cuántos meses llevas con tu/tus tarjetas de crédito?:"))


    def validar_datos(self):
        errores = []

        if not self.domicilio:
            errores.append("Domicilio no puede estar vacío.")
        if not self.email:
            errores.append("Correo Electrónico no puede estar vacío.")

        if self.ingresos is None or self.egresos is None or self.num_tarjetas is None or self.credit_utilization is None or self.meses is None:
            errores.append("Por favor, completa todos los campos numéricos correctamente.")

        if self.num_tarjetas is not None and self.num_tarjetas < 0:
            errores.append("Ingresa un valor igual o mayor que cero para el número de tarjetas.")

        if self.credit_utilization is not None and not 0 <= self.credit_utilization <= 100:
            errores.append("Ingresa un valor entre 0 y 100 para la utilización de la tarjeta de crédito.")

        return errores


    def obtener_respuesta_pregunta_retorica(self):
        st.write("En un escenario en donde no tuvieras el dinero para pagar tu tarjeta de crédito, ¿Qué harías?: ")
        opciones = {
            'a': 'Pido prestado a alguien más para pagarla',
            'b': 'Pago el siguiente mes aunque sea con intereses',
            'c': 'Pago cuando tenga el dinero y me sea posible',
            'd': 'Pago el mínimo'
        }

        respuesta = st.selectbox("Selecciona tu respuesta:", list(opciones.values()))
        for key, value in opciones.items():
            if respuesta == value:
                self.respuesta_retorica = key
                break


    def tiempo_pago(self):
        while True:
            try:
                self.dias_pago = int(st.text_input("Después de tu fecha de corte, ¿Cuántos días tardas en pagar tu tarjeta de crédito? Responde únicamente con números: "))
                if self.dias_pago >= 0:
                    break
                else:
                    print("Error: Ingresa un valor igual o mayor que cero.")
            except ValueError:
                print("Error: Ingresa solo valores numéricos enteros.")

    def prestamos_activos(self):
        st.write("Actualmente, ¿Tienes préstamos activos a parte de Tarjetas de crédito?: ")
        opciones = {
            'a': 'Si',
            'b': 'No'
        }

        while True:
            tiene_prestamos = st.radio('Selecciona una opción:', list(opciones.values()))
            if tiene_prestamos == 'Si':
                self.tiene_prestamos = True
                self.cantidad_prestamos = st.text_input(
                    "¿Cuántos préstamos tienes a tu nombre, a parte de las tarjetas de Crédito? ")
                self.monto_prestamo = st.text_input(
                    "¿De cuánto es el monto de tus préstamos? (Si es más de uno, favor de sumarlos y poner el monto total): ")
                st.write(f"Entendido, tienes préstamos por un monto de {self.monto_prestamo}.")
                break
            elif tiene_prestamos == 'No':
                self.tiene_prestamos = False
                st.write("Gracias por la información. No tienes préstamos activos.")
                break

    def obtener_tipo_tarjeta(self):
        st.write("Actualmente, ¿Qué tipo de Tarjeta es la mejor que tienes?: ")
        opciones = {
            'a': 'Clasica',
            'b': 'Gold',
            'c': 'Platinum'
        }

        while True:
            tipo_tarjeta = st.radio('Selecciona una opción:', list(opciones.values()))
            if tipo_tarjeta in opciones.values():
                self.tipo_tarjeta = list(opciones.keys())[list(opciones.values()).index(tipo_tarjeta)]
                st.write("¡Bien! Gracias por responder.")
                break

    def limite_credito(self):
        while True:
            try:
                self.credito_total = int(st.text_input("¿Cuál es tu límite de crédito? (Si tienes más de una tarjeta, suma el total de todas tus líneas de crédito) Por favor, responde solo con valores numéricos: "))
                if self.credito_total >= 0:
                    print(f"Tu límite de crédito es: {self.credito_total}")
                    break
                else:
                    print("Error: Ingresa un valor igual o mayor que cero.")
            except ValueError:
                print("Error: Ingresa solo valores numéricos enteros.")



    def invierte_usuario(self):
        while True:
            porcentaje_input = st.text_input("¿Qué porcentaje de tus ingresos mensuales sueles invertir? Ingrese el porcentaje en valor entero de 0 a 100 (sin el símbolo de porcentaje): ")
            try:
                porcentaje = int(porcentaje_input)
                if 0 <= porcentaje <= 100:
                    st.write(f"Entendido, inviertes un {porcentaje}% de tus ingresos.")
                    self.porcentaje_inversion = porcentaje  # Guardar el porcentaje ingresado
                    break
                else:
                    st.write("Error: Porcentaje no válido. Por favor, ingresa un valor entre 0 y 100.")
            except ValueError:
                st.write("Error: Ingresa un número válido para el porcentaje.")


    def validar_datos(self):
        if not (self.paterno and self.materno and self.nombres and self.edad and self.curp):
            raise ValueError("Por favor, completa todos los campos antes de validar.")

        # Verificar nombre en CURP
        curp_lower = self.curp.lower()
        if not (curp_lower.startswith(self.paterno.lower()[:2]) and
                curp_lower[2] == self.materno.lower()[0] and
                curp_lower[3] == self.nombres.lower()[0]):
            raise ValueError("Verifica tus datos, tu nombre o apellidos están incorrectos.")

        # Calcular edad a partir de la CURP
        curp_year = int(self.curp[4:6])
        curp_month = int(self.curp[6:8])
        curp_day = int(self.curp[8:10])

        today = datetime.now()
        year_now = today.year % 100
        month_now = today.month
        day_now = today.day

        if curp_year > year_now:
            curp_year += 1900
        else:
            curp_year += 2000

        age = today.year - curp_year - ((today.month, today.day) < (curp_month, curp_day))

        if age != self.edad:
            raise ValueError("Verifica tu edad, parece estar incorrecta.")


    # Uso de la clase Preguntas:
    def iniciar_cuestionario(self):
        self.obtener_nombre()
        self.preguntas_siguiente_seccion()
        self.obtener_respuesta_pregunta_retorica()
        self.tiempo_pago()
        self.prestamos_activos()
        self.obtener_tipo_tarjeta()
        self.limite_credito()
        self.invierte_usuario()
        try:
            self.validar_datos()
            print("¡Tus datos han sido verificados con éxito!")
        except ValueError as e:
            print(str(e))

