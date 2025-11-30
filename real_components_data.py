"""
Real Component Database
Contains curated list of actual electrical components from requested manufacturers.
"""

REAL_COMPONENTS = [
    # Schneider Electric
    {
        "manufacturer": "Schneider Electric",
        "part_number": "LC1D09M7",
        "description": "TeSys D Contactor, 3P, 9A, 220V AC Coil",
        "category": "Contactor",
        "voltage_rating": "690V",
        "current_rating": "9A",
        "datasheet_url": "https://www.se.com/ww/en/product/LC1D09M7/tesys-d-contactor-3p3-no-ac3-440-v-9-a-220-v-ac-coil/",
        "supplier_id": "Schneider Direct"
    },
    {
        "manufacturer": "Schneider Electric",
        "part_number": "A9F74106",
        "description": "iC60N - miniature circuit breaker - 1P - 6A - C curve",
        "category": "Circuit Breaker",
        "voltage_rating": "230V",
        "current_rating": "6A",
        "datasheet_url": "https://www.se.com/ww/en/product/A9F74106/ic60n-miniature-circuit-breaker-1p-6a-c-curve/",
        "supplier_id": "Schneider Direct"
    },
    
    # Siemens
    {
        "manufacturer": "Siemens",
        "part_number": "3RT2015-1BB41",
        "description": "Contactor, AC-3, 3KW/400V, 1NO, DC 24V, 3-pole, Size S00",
        "category": "Contactor",
        "voltage_rating": "400V",
        "current_rating": "7A",
        "datasheet_url": "https://mall.industry.siemens.com/mall/en/WW/Catalog/Product/3RT2015-1BB41",
        "supplier_id": "Siemens Mall"
    },
    {
        "manufacturer": "Siemens",
        "part_number": "5SY4106-7",
        "description": "Miniature Circuit Breaker 230/400V 10kA, 1-pole, C, 6A",
        "category": "Circuit Breaker",
        "voltage_rating": "400V",
        "current_rating": "6A",
        "datasheet_url": "https://mall.industry.siemens.com/mall/en/WW/Catalog/Product/5SY4106-7",
        "supplier_id": "Siemens Mall"
    },

    # ABB
    {
        "manufacturer": "ABB",
        "part_number": "1SBL137001R1310",
        "description": "AF09-30-10-13 100-250V 50/60Hz / DC Contactor",
        "category": "Contactor",
        "voltage_rating": "690V",
        "current_rating": "9A",
        "datasheet_url": "https://new.abb.com/products/1SBL137001R1310/af09-30-10-13",
        "supplier_id": "ABB Products"
    },
    {
        "manufacturer": "ABB",
        "part_number": "2CDS251001R0064",
        "description": "Miniature Circuit Breaker - S200 - 1P - C - 6 ampere",
        "category": "Circuit Breaker",
        "voltage_rating": "230/400V",
        "current_rating": "6A",
        "datasheet_url": "https://new.abb.com/products/2CDS251001R0064/s201-c6",
        "supplier_id": "ABB Products"
    },

    # General Electric (GE Industrial / ABB)
    {
        "manufacturer": "General Electric",
        "part_number": "CL00A310T",
        "description": "Contactor, 3-Pole, 9A, 120VAC Coil",
        "category": "Contactor",
        "voltage_rating": "600V",
        "current_rating": "9A",
        "datasheet_url": "https://www.geindustrial.com/products/contactors/c-2000-contactors",
        "supplier_id": "GE Industrial"
    },

    # Omron
    {
        "manufacturer": "Omron",
        "part_number": "J7KC-12-10 DC24",
        "description": "Magnetic Contactor, Non-reversing, 12A, 24VDC Coil",
        "category": "Contactor",
        "voltage_rating": "440V",
        "current_rating": "12A",
        "datasheet_url": "https://www.ia.omron.com/products/family/3745/",
        "supplier_id": "Omron Automation"
    },
    {
        "manufacturer": "Omron",
        "part_number": "MY2N-D2 DC24",
        "description": "General Purpose Relay, DPDT, 5A, 24VDC, with LED/Diode",
        "category": "Relay",
        "voltage_rating": "250V",
        "current_rating": "5A",
        "datasheet_url": "https://www.ia.omron.com/products/family/948/",
        "supplier_id": "Omron Automation"
    }
]

def get_real_components(manufacturer=None):
    """Retrieve components, optionally filtered by manufacturer"""
    if manufacturer:
        return [c for c in REAL_COMPONENTS if manufacturer.lower() in c['manufacturer'].lower()]
    return REAL_COMPONENTS
