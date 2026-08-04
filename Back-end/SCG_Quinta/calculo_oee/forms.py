from django import forms
from .models import TurnoOEE
from django.forms.widgets import HiddenInput



class TurnoOEEForm(forms.ModelForm):
    cliente = forms.CharField(required=False, widget=HiddenInput)
    producto = forms.CharField(required=False, widget=HiddenInput)
    codigo = forms.CharField(required=False, widget=HiddenInput)
    produccion_planeada = forms.IntegerField(required=False, widget=HiddenInput)

    fecha = forms.DateField(
        widget=forms.DateInput(attrs={
            'type': 'date',
            'class': 'input',
            'id': 'id_fecha',
        }),
        help_text="Fecha del turno"
    )
    #CLIENTE_CHOICES = [
    #    ('Jumbo', 'Jumbo'),
    #    ('SISA', 'SISA'),
    #    ('Walmart', 'Walmart'),
    #    ('Unimarc', 'Unimarc'),
    #]
    #cliente = forms.ChoiceField(
    #    choices=[('', '--Seleccionar cliente--')] + [(c, c) for c in CATALOGO],
    #    widget=forms.Select(attrs={'id': 'id_cliente'}),
    #    help_text="Agregar cliente y producto siempre, si es mas de un producto ingresar detalle completo abajo en 🍰 Productos"
    #)
    #producto = forms.ChoiceField(
    #    choices=[('', '--Seleccionar cliente primero--')],
    #    widget=forms.Select(attrs={'id': 'id_producto'})
    #)
    #codigo = forms.CharField(
    #    widget=forms.TextInput(attrs={
    #        'readonly': 'readonly', 
    #        'id': 'id_codigo',
    #        'placeholder': 'Se autocompleta'
    #    })
    #)
    lote = forms.CharField(
        required=True,
        help_text="Lote del turno, ej: 123BCA",
        widget=forms.TextInput(attrs={
            'id': 'id_lote',
            'placeholder': '123BCA'
        })
    )
    numero_personas = forms.IntegerField(
        required=True,
        help_text="Número de personas que trabajan en la linea durante el turno",
        widget=forms.NumberInput(attrs={
            'id': 'id_numero_personas',
            'placeholder': 'Número de personas'
        })
    )
    TURNOS_CHOICES = [
        ('Turno A', 'Turno A'),
        ('Turno B', 'Turno B'),
        ('Turno C', 'Turno C'),
    ]
    turno = forms.ChoiceField(
        choices=[('', '--Seleccionar turno--')] + TURNOS_CHOICES,
        widget=forms.Select(attrs={'id': 'id_turno'})
    )
    SUPERVISORES_POR_PLANTA = {
        TurnoOEE.PLANTA_ENEA: [
            ('Fabian Moncada', 'Fabian Moncada'),
            ('Angela Tacon', 'Angela Tacon'),
            ('Felipe Campos', 'Felipe Campos'),
        ],
        TurnoOEE.PLANTA_PUERTO_VESPUCIO: [
            ('Sebastian Ibarra', 'Sebastian Ibarra'),
            ('Andres Gonzales', 'Andres Gonzales'),
            ('Patricio Cardenas', 'Patricio Cardenas'),
            ('Larry Torres', 'Larry Torres'),
            ('Moises Mejias', 'Moises Mejias'),
            ('Carlos Diaz', 'Cristian Diaz'),
            ],
    }
    supervisor = forms.ChoiceField(
        choices=[],
        widget=forms.Select(attrs={'id': 'id_supervisor'})
    )

    LINEAS_POR_PLANTA = {
        TurnoOEE.PLANTA_ENEA: [
            ('Línea 1', 'Línea 1'),
            ('Línea 2', 'Línea 2'),
            ('Línea 3A', 'Línea 3A'),
            ('Línea 3B', 'Línea 3B'),
            ('Isla', 'Isla'),
            ('Cakematic', 'Cakematic'),
            ('Gorreri pasteleria', 'Gorreri pasteleria'),
            ('Mesón 1', 'Mesón 1'),
            ('Mesón 2', 'Mesón 2'),
            ('Mesón 3', 'Mesón 3'),
            ('Mesón 4', 'Mesón 4'),
            ('Mesón 5', 'Mesón 5'),
        ],

        TurnoOEE.PLANTA_PUERTO_VESPUCIO: [
            ('Gorreri pasteleria', 'Gorreri pasteleria'),
            ('Linea 1', 'Linea 1'),
            ('Linea 2', 'Linea 2'),
            ('Linea 3', 'Linea 3'),
            ('Pasteles', 'Pasteles'),
            ('Gorreri batidos', 'Gorreri batidos'),
            ('Macpan', 'Macpan'),
            ('Tartomatic', 'Tartomatic'),
            ('Gorreri kuchen', 'Gorreri kuchen'),
            ('Hornos', 'Hornos'),
            ('Envasado', 'Envasado'),
        ],
    }

    linea = forms.ChoiceField(
        choices=[],
        widget=forms.Select(attrs={'id': 'id_linea'})
    )
    
    class Meta:
        model = TurnoOEE
        # 'cliente', 'producto', 'codigo', 'produccion_planeada'
        fields = ['fecha', 'linea', 'turno', 'numero_personas','lote', 'supervisor', 'tiempo_planeado', 'cliente', 'producto', 'codigo', 'produccion_planeada']
        widgets = {
            'tiempo_planeado': forms.NumberInput(attrs={
                # Valor fijo de 450 minutos (7.5 horas) (por aplicacion 42 horas semanales / 5 dias = 8 horas diarias - 30 minutos de colacion = 7.5 horas = 450 minutos)
                'value': 450,
                'id': 'id_tiempo_planeado',
                'placeholder': 'Tiempo planeado (en minutos)',
                'readonly': 'readonly'
            }),
            # … otros widgets …
            # aquí ocultamos los cuatro:
            'cliente': HiddenInput(),
            'producto': HiddenInput(),
            'codigo': HiddenInput(),
            'produccion_planeada': HiddenInput(),
        }
    def __init__(
        self,
        *args,
        planta=TurnoOEE.PLANTA_ENEA,
        **kwargs
    ):
        super().__init__(*args, **kwargs)

        self.planta = planta

        # Supervisores correspondientes a la planta
        supervisores = self.SUPERVISORES_POR_PLANTA.get(
            planta,
            [],
        )

        self.fields['supervisor'].choices = [
            ('', '--Seleccionar supervisor--'),
            *supervisores,
        ]

        # Líneas correspondientes a la planta
        lineas = self.LINEAS_POR_PLANTA.get(
            planta,
            [],
        )

        self.fields['linea'].choices = [
            ('', '--Seleccionar línea--'),
            *lineas,
        ]
    #def __init__(self, *args, **kwargs):
    #    super().__init__(*args, **kwargs)

    #    for f in ('cliente', 'producto', 'codigo', 'produccion_planeada'):
    #        self.fields.pop(f, None)

        # 1) Intentamos sacar el cliente de los datos enviados (POST)
        #cliente_sel = self.data.get('cliente')

        # 2) Si no viene en data (es un GET o validación falló), probamos en initial o en la instancia
        #if not cliente_sel:
        #    cliente_sel = self.initial.get('cliente') \
        #                  or getattr(self.instance, 'cliente', None)

        # 3) Si tenemos un cliente válido, reconstruimos las choices de producto
        #if cliente_sel in CATALOGO:
        #    opciones = [(p['producto'], p['producto']) for p in CATALOGO[cliente_sel]]
        #    self.fields['producto'].choices = [('', '--Seleccionar producto--')] + opciones

class ProduccionRealForm(forms.ModelForm):
    produccion_real = forms.IntegerField(
        required=True,
        help_text="Producción real en unidades",
        widget=forms.NumberInput(attrs={
            'id': 'id_produccion_real',
            'placeholder': 'Producción real'
        })
    )
    class Meta:
        model = TurnoOEE
        fields = ['produccion_real']
