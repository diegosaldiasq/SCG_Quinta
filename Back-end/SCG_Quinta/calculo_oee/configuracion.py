from .models import TurnoOEE

AREA_TORTAS = "TORTAS"
AREA_INSUMOS_KUCHEN = "INSUMOS_KUCHEN"

CONFIGURACION_PLANTAS = {
    TurnoOEE.PLANTA_ENEA: {
        "nombre": "ENEA",

        "area_por_supervisor": {
            "Fabian Moncada": AREA_TORTAS,
            "Angela Tacon": AREA_TORTAS,
            "Felipe Campos": AREA_TORTAS,
        },

        "clientes_por_area": {
            AREA_TORTAS: [
                "Jumbo",
                "SISA",
            ],
        },
    },

    TurnoOEE.PLANTA_PUERTO_VESPUCIO: {
        "nombre": "Puerto Vespucio",

        "area_por_supervisor": {
            "Sebastian Ibarra": AREA_TORTAS,
            "Andres Gonzales": AREA_TORTAS,
            "Patricio Cardenas": AREA_TORTAS,

            "Larry Torres": AREA_INSUMOS_KUCHEN,
            "Moises Mejias": AREA_INSUMOS_KUCHEN,
            "Carlos Diaz": AREA_INSUMOS_KUCHEN,
        },

        "clientes_por_area": {
            AREA_TORTAS: [
                "Walmart",
                "Unimarc",
            ],

            AREA_INSUMOS_KUCHEN: [
                "Insumo",
                "Jumbo",
                "Pasteles",
                "SISA",
                "Sub",
                "Walmart",
            ],
        },
    },
}
