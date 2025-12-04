# app/utils/tasa_utils.py
PERIODS_PER_YEAR = {
    "Anual": 1,
    "Semestral": 2,
    "Trimestral": 4,
    "Mensual": 12
}

def _to_decimal(rate_percent):
    return rate_percent / 100.0

def nominal_to_effective_annual_from_periodic_nominal(j_decimal, m, momento="Vencida"):
    """
    Convierte una tasa nominal j (decimal) con m capitalizaciones por año
    a tasa efectiva anual.
    """
    if momento == "Vencida":
        return (1 + j_decimal / m)**m - 1
    elif momento == "Anticipada":
        periodic_ant = j_decimal / m
        if periodic_ant >= 1.0:
            raise ValueError("La Tasa Nominal Anticipada por periodo no puede ser igual o mayor al 100%.")
        i_v_period = periodic_ant / (1 - periodic_ant)
        return (1 + i_v_period)**m - 1
    else:
        raise ValueError("momento debe ser 'Vencida' o 'Anticipada'")

def effective_period_from_effective_annual(ea_decimal, periods_per_year_target):
    """
    Convierte una tasa efectiva anual EA a tasa efectiva por periodo objetivo.
    """
    return (1 + ea_decimal)**(1.0 / periods_per_year_target) - 1

def convert_to_period_rate(rate_percent, tipo_tasa, periodo_tasa, periodicidad_pago, momento="Vencida"):
    """
    Convierte la tasa dada a tasa por periodo de pago (decimal).
    """
    if periodo_tasa not in PERIODS_PER_YEAR:
        raise ValueError(f"Periodo de tasa inválido: {periodo_tasa}")
    if periodicidad_pago not in PERIODS_PER_YEAR:
        raise ValueError(f"Periodicidad de pago inválida: {periodicidad_pago}")

    p_tasa = PERIODS_PER_YEAR[periodo_tasa]  # m_tasa
    p_pago = PERIODS_PER_YEAR[periodicidad_pago]  # periodos por año del pago

    rate_dec = _to_decimal(rate_percent)

    # -------- Efectiva ----------
    if tipo_tasa == "Efectiva":
        if momento == "Anticipada":
            if rate_dec >= 1.0:
                raise ValueError("La Tasa Efectiva Anticipada no puede ser igual o mayor al 100%.")
            i_v_period = rate_dec / (1 - rate_dec)
        else:
            i_v_period = rate_dec

        if p_tasa == 1:
            ea = i_v_period
        else:
            ea = (1 + i_v_period)**p_tasa - 1

        i_periodo = effective_period_from_effective_annual(ea, p_pago)
        return i_periodo

    # -------- Nominal ----------
    elif tipo_tasa == "Nominal":
        ea = nominal_to_effective_annual_from_periodic_nominal(rate_dec, p_tasa, momento=momento)
        i_periodo = effective_period_from_effective_annual(ea, p_pago)
        return i_periodo

    else:
        raise ValueError("tipo_tasa debe ser 'Nominal' o 'Efectiva'")