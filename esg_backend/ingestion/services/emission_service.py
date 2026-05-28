from ingestion.models import EmissionFactor


VALID_FUEL_MAPPING = {
    'diesel': [
        'diesel'
    ],

    'gasoline': [
        'gasoline',
        'petrol'
    ],

    'jet_fuel': [
        'jet fuel',
        'aviation turbine fuel',
        'jet a-1'
    ],

    'lng': [
        'lng'
    ],

    'cng': [
        'cng'
    ]
}


INVALID_FUEL_KEYWORDS = [
    'filter',
    'lubricant',
    'hydraulic',
    'grease',
    'coolant',
    'engine oil',
    'oil filter'
]


def detect_fuel_category(fuel_type):

    if not fuel_type:
        return None

    fuel_type = fuel_type.lower()

    #
    # Reject non-fuel consumables
    #

    for invalid_keyword in INVALID_FUEL_KEYWORDS:

        if invalid_keyword in fuel_type:
            return None

    #
    # Detect actual fuel category
    #

    for category, keywords in VALID_FUEL_MAPPING.items():

        for keyword in keywords:

            if keyword in fuel_type:
                return category

    return None


def calculate_fuel_emission(fuel_type, quantity, unit):

    if not fuel_type or not quantity or not unit:
        return None

    detected_category = detect_fuel_category(fuel_type)

    if not detected_category:
        return None

    factor = EmissionFactor.objects.filter(
        category='fuel',
        factor_name=detected_category,
        unit=unit
    ).first()

    if not factor:
        return None

    return quantity * factor.emission_factor