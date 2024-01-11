class CalculosMonto:
    @staticmethod
    def ajustar_por_monto_prestamo(monto_prestamo):
        if monto_prestamo < 50000:
            monto_prestamo *= 0.96
        elif 51000 <= monto_prestamo <= 300000:
            monto_prestamo *= 0.93
        elif monto_prestamo > 300000:
            monto_prestamo *= 0.91
        return monto_prestamo

    @staticmethod
    def calcular_monto_prestamo(ingresos, credit_score_prediction, credito_total, egresos, num_tarjetas,
                                porcentaje, meses, respuesta_retorica, dias_pago, tiene_prestamos, num_prestamos,
                                monto_prestamo, tipo_tarjeta, porcentaje_inversion):

        # Ajustes basados en Credit Score Prediction
        if credit_score_prediction == "Good":
            maximo_posible = min(300000, credito_total * 1.3, ingresos * 1.3)
            monto_prestamo = maximo_posible
        elif credit_score_prediction == "Standard":
            monto_prestamo = min(70000, (credito_total + ingresos) / 2)
        elif credit_score_prediction == "Bad":
            monto_prestamo = min(ingresos * 0.75, credito_total * 0.75)

        # Ajustes basados en Egresos Mensuales
        porcentaje_egresos = egresos / ingresos * 100
        if porcentaje_egresos <= 30:
            monto_prestamo *= 1.05
        elif 31 <= porcentaje_egresos <= 50:
            monto_prestamo *= 1.03
        elif porcentaje_egresos > 50:
            monto_prestamo *= 0.97

        # Ajustes basados en Número de Tarjetas de Crédito
        if num_tarjetas == 0:
            return "Mejora tu historial crediticio y vuelve a intentarlo en 3 meses"
        elif 1 <= num_tarjetas <= 2:
            monto_prestamo *= 1.01 if ingresos < 10000 else 1.025
        elif num_tarjetas >= 3:
            monto_prestamo *= 1.015 if ingresos < 10000 else 1.035

        # Ajustes basados en Porcentaje de Utilización de Tarjeta de Crédito
        if porcentaje < 31:
            monto_prestamo *= 1.1
        elif 31 <= porcentaje <= 50:
            monto_prestamo *= 1.06
        elif porcentaje > 50:
            monto_prestamo *= 0.92

        # Ajustes basados en Tiempo con las Tarjetas de Crédito (Meses)
        if meses >= 180:  # 15 anos
            monto_prestamo *= 1.15
        elif 60 <= meses <= 179:
            monto_prestamo *= 1.06
        elif meses < 60:
            monto_prestamo *= 0.94

        # Ajustes basados en Riesgo
        if respuesta_retorica == 'a':
            monto_prestamo *= 1.03
        elif respuesta_retorica == 'b':
            monto_prestamo *= 1.02
        elif respuesta_retorica == 'c':
            monto_prestamo *= 0.93
        elif respuesta_retorica == 'd':
            monto_prestamo *= 0.95

        # Ajustes adicionales basados en otros factores de riesgo
        if dias_pago <= 21:
            monto_prestamo *= 1.06
        elif 21 < dias_pago <= 51:
            monto_prestamo *= 1.02
        elif dias_pago > 51:
            monto_prestamo *= 0.96

        if tiene_prestamos:
            num_prestamos = int(num_prestamos)
            if num_prestamos == 1:
                monto_prestamo *= 0.98
            elif num_prestamos == 2:
                monto_prestamo *= 0.97
            elif num_prestamos >= 3:
                monto_prestamo *= 0.96

        monto_prestamo = CalculosMonto.ajustar_por_monto_prestamo(monto_prestamo)

        if tipo_tarjeta == 'a':
            monto_prestamo *= 0.97
        elif tipo_tarjeta == 'b':
            monto_prestamo *= 1.03
        elif tipo_tarjeta == 'c':
            monto_prestamo *= 1.06

        if 1 <= porcentaje_inversion <= 100:
            monto_prestamo *= 1.025
        elif porcentaje_inversion == 0:
            monto_prestamo *= .985

        return round(monto_prestamo, 2)




