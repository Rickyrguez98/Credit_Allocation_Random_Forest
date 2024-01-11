import streamlit as st
from preguntas import Preguntas
from calculos import CalculosMonto
import pandas as pd
from sklearn.impute import SimpleImputer
from joblib import load
import warnings

# # Ignorar la advertencia específica sobre versiones inconsistentes de scikit-learn
# warnings.filterwarnings("ignore", category=UserWarning, message="Trying to unpickle estimator")


def main():
    # Agregar el logo del banco
    logo_path = "logo.png"
    st.image(logo_path, width=300)
    st.title('Solicita tu Préstamo en 5 minutos!')
    preguntas = Preguntas()
    mostrar_preguntas(preguntas)
    if st.button('Solicitar Crédito'):
        preguntas.validar_datos()
        st.write("¡Tus datos han sido verificados con éxito!")


        # Creación del diccionario con los datos
        data = {
            'Credit_Mix_0': 0,
            'Credit_Mix_1': 0,
            'Credit_Mix_2': 0,
            'Delay_from_due_date': 0,
            'Credit_History_Age': preguntas.meses,
            'Annual_Income': preguntas.ingresos * 12,
            'Num_of_Loan': preguntas.cantidad_prestamos,
            'Outstanding_Debt': preguntas.monto_prestamo
        }

        # Aplicar las condiciones para determinar los valores de 'Credit_Mix_X' y 'Delay_from_due_date'
        if preguntas.porcentaje_inversion <= 30 and preguntas.num_tarjetas > 1:
            data['Credit_Mix_0'] = 1
        elif 30 < preguntas.porcentaje_inversion <= 50:
            data['Credit_Mix_1'] = 1
        else:
            data['Credit_Mix_2'] = 1

        if preguntas.respuesta_retorica == 'a' and preguntas.dias_pago <= 21:
            data['Delay_from_due_date'] = -1
        elif preguntas.respuesta_retorica == 'a' and preguntas.dias_pago > 21:
            data['Delay_from_due_date'] = 15
        elif preguntas.respuesta_retorica == 'b' and preguntas.dias_pago <= 21:
            data['Delay_from_due_date'] = 30
        elif preguntas.respuesta_retorica == 'b' and preguntas.dias_pago > 21:
            data['Delay_from_due_date'] = 60
        elif preguntas.respuesta_retorica == 'd' and preguntas.dias_pago <= 51:
            data['Delay_from_due_date'] = 90
        elif preguntas.respuesta_retorica == 'd' and preguntas.dias_pago > 51:
            data['Delay_from_due_date'] = 120
        elif preguntas.respuesta_retorica == 'c' and preguntas.dias_pago <= 81:
            data['Delay_from_due_date'] = 150
        elif preguntas.respuesta_retorica == 'c' and preguntas.dias_pago > 81:
            data['Delay_from_due_date'] = 300

        # Crear el DataFrame con una sola fila
        test = pd.DataFrame([data])

        test = test[['Delay_from_due_date',
                     'Credit_History_Age',
                     'Credit_Mix_0',
                     'Credit_Mix_1',
                     'Credit_Mix_2',
                     'Annual_Income',
                     'Num_of_Loan',
                     'Outstanding_Debt']]
        print(test)
        # Dividir el conjunto de datos en características (X) y variable objetivo (y)
        columns_to_train = ['Delay_from_due_date', 'Credit_History_Age', 'Credit_Mix_0', 'Credit_Mix_1', 'Credit_Mix_2',
                            'Annual_Income', 'Num_of_Loan', 'Outstanding_Debt']

        X_test = test[columns_to_train]

        imputer = SimpleImputer(strategy='mean')
        imputer.fit(X_test)

        X_test_imputed = imputer.transform(X_test)

        # Cargar el modelo
        Random_Forest_model = load('Random_Forest_model.joblib')
        print(X_test_imputed)

        # Realizar predicciones en el conjunto de prueba
        y_pred = Random_Forest_model.predict(X_test_imputed)
        print(y_pred)
        test['Credit_Score_Prediction'] = Random_Forest_model.predict(X_test)
        print(test)
        # Transformar valores booleanos a calificación real
        test["Credit_Score_Prediction"] = ["Poor" if i == 0 else ("Standard" if i == 1 else "Good") for i in
                                           test["Credit_Score_Prediction"]]
        print(test)
        credit_score_prediction = test["Credit_Score_Prediction"].iloc[0]
        print(credit_score_prediction)
        monto_calculado = CalculosMonto.calcular_monto_prestamo(preguntas.ingresos, credit_score_prediction,
                                                                preguntas.credito_total, preguntas.egresos,
                                                                preguntas.num_tarjetas, preguntas.credit_utilization,
                                                                preguntas.meses, preguntas.respuesta_retorica,
                                                                preguntas.dias_pago, preguntas.tiene_prestamos,
                                                                preguntas.cantidad_prestamos, preguntas.monto_prestamo,
                                                                preguntas.tipo_tarjeta, preguntas.porcentaje_inversion)
        print(monto_calculado)
        if isinstance(monto_calculado, (int, float)):
            st.write(" ")
            st.write("FELICIDADES!, ", preguntas.nombres, preguntas.paterno, preguntas.materno)
            st.write("Tu préstamo por: $", monto_calculado, 'ha sido autorizado')
            st.write("Tu Tarjeta será enviada a tu domicilio:", preguntas.domicilio)
            st.write("Te enviaremos la información detallada a tu correo electrónico:", preguntas.email)
            st.write("Si tienes dudas o comentarios, contáctanos: ")
            st.write("Tel: +52 332 76900")
            st.write("Email: help@mexflex.com")
        else:
            st.write(" ")
            st.write(preguntas.nombres, preguntas.paterno, preguntas.materno)
            st.write("Lamentablemente tu préstamo no ha sido autorizado. Monto calculado:", monto_calculado)
            st.write("Si tienes dudas o comentarios, contáctanos: ")
            st.write("Tel: +52 332 76900")
            st.write("Email: help@mexflex.com")


def mostrar_preguntas(preguntas):
    try:
        preguntas.obtener_nombre()
    except:
        pass
    try:
        preguntas.preguntas_siguiente_seccion()
        preguntas.obtener_respuesta_pregunta_retorica()
        preguntas.tiempo_pago()
    except:
        pass
    try:
        preguntas.prestamos_activos()
        preguntas.obtener_tipo_tarjeta()
        preguntas.limite_credito()
    except:
        pass
    try:
        preguntas.invierte_usuario()
    except:
        pass

        # preguntas.validar_datos()


        # st.write("Nombre: ",preguntas.nombres)
        # st.write("Tipo Tarjeta: ",preguntas.tipo_tarjeta)




    # except ValueError as e:
    #     st.error(str(e))

if __name__ == "__main__":
    main()

