UNIT_MAPPING = {
    'L': 'liters',
    'GAL': 'liters',
    'KG': 'kilograms',
    'G': 'grams',
    'PC': 'pieces',
    'DR': 'liters'
}

UNIT_CONVERSION = {
    'DR': 200,
    'L': 1,
    'PC': 1,
    'KG': 1,
    'G': 0.001
}


def normalize_unit_and_quantity(quantity, raw_unit):

    if quantity is None or raw_unit is None:
        return None, None

    # sanitize unit
    raw_unit = str(raw_unit).strip().upper()

    normalized_unit = UNIT_MAPPING.get(
        raw_unit,
        raw_unit.lower()
    )

    conversion_factor = UNIT_CONVERSION.get(
        raw_unit,
        1
    )

    normalized_quantity = float(quantity) * conversion_factor

    return normalized_quantity, normalized_unit