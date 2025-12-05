def validate_number(value_str, field_name, must_be_positive=True):
    """
    Convierte string a float (acepta coma o punto).
    Lanza ValueError con mensaje amigable si falla.
    """
    if not value_str:
        raise ValueError(f"El campo '{field_name}' no puede estar vacío.")

    cleaned_value = value_str.strip().replace(',', '.')
    
    try:
        val = float(cleaned_value)
    except ValueError:
        raise ValueError(f"El valor '{value_str}' en '{field_name}' no es un número válido.")

    if must_be_positive and val < 0:
        raise ValueError(f"El campo '{field_name}' no puede ser negativo.")
        
    return val