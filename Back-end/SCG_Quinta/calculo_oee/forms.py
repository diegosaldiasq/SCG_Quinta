from django import forms
from .models import TurnoOEE
from django.forms.widgets import HiddenInput
#from .forms import CATALOGO

CATALOGO = {
  'Jumbo': [
    { 'producto': 'Torta Beatriz',                    'codigo': '393241' },
    { 'producto': 'Torta Bom Bom',                    'codigo': '393240' },
    { 'producto': 'Torta tres leches',                'codigo': '393149' },
    { 'producto': 'Torta cuatro leches',              'codigo': '393191' },
    { 'producto': 'Torta piña',                       'codigo': '393129' },
    { 'producto': 'Torta lucuma',                     'codigo': '393141' },
    { 'producto': 'Torta panqueque naranja',          'codigo': '393171' },
    { 'producto': 'Torta selva negra',                'codigo': '393145' },
    { 'producto': 'Torta truffa',                     'codigo': '393167' },
    { 'producto': 'Torta viena',                      'codigo': '393153' },
    { 'producto': 'Torta San Jorge lucuma',           'codigo': '393396' },
    { 'producto': 'Torta San Jorge guinda',           'codigo': '393397' },
    { 'producto': 'Torta San Jorge chocolate',        'codigo': '393398' },
    { 'producto': 'Torta merengue lucuma',            'codigo': '405220' },
    { 'producto': 'Torta merengue frambuesa',         'codigo': '405217' },
    { 'producto': 'Torta merengue nugat',             'codigo': '393443' },
    { 'producto': 'Torta merengue manzana frambuesa', 'codigo': '405458' },
    { 'producto': 'Torta chocolate real',             'codigo': '405254' },
    { 'producto': 'Torta caluga frambuesa',           'codigo': '393414' },
    { 'producto': 'Torta caluga nuez',                'codigo': '405548' },
    { 'producto': 'Torta selva negra vegana',         'codigo': '405258' },
    #{ 'producto': 'Torta piña vegana',                'codigo': '405260' }, Descontinuado 30-10-25
    { 'producto': 'Torta panqueque guinda chocolate', 'codigo': '402261' },
    { 'producto': 'Torta tentacion de chocolate',     'codigo': '405598' },
    { 'producto': 'Pie de frambuesa familiar',        'codigo': '393429' },
    { 'producto': 'Pie de maracuya familiar',         'codigo': '393430' },
    { 'producto': 'Pie de limon familiar',            'codigo': '393431' },
    { 'producto': 'Media torta San Jorge lucuma',     'codigo': '405414' },
    { 'producto': 'Tarta soft familiar',              'codigo': '393433' },
    { 'producto': 'Tartaleta fruta mixta familiar',   'codigo': '393432' },
  ],
  'SISA': [
    { 'producto': 'Torta amor',                       'codigo': '393266' },
    #{ 'producto': 'Torta crema manjar mediana',       'codigo': '392518' }, Descontinuado 30-10-25
    { 'producto': 'Torta crema piña',                 'codigo': '393011' },
    { 'producto': 'Torta crema selva negra',          'codigo': '393013' },
    { 'producto': 'Torta chocolate mediana',          'codigo': '405523' },
    { 'producto': 'Torta merengue frambuesa',         'codigo': '393036' },
    { 'producto': 'Torta merengue lucuma',            'codigo': '393212' },
    { 'producto': 'Torta mocaccino mediana',          'codigo': '353253' },
    { 'producto': 'Torta panqueque naranja',          'codigo': '393018' },
    { 'producto': 'Torta tres leches',                'codigo': '393015' },
    { 'producto': 'Torta yogurt',                     'codigo': '393017' },
    { 'producto': 'Torta viena',                      'codigo': '393019' },
    #{ 'producto': 'Torta guinda chocolate',           'codigo': '393362' }, Descontinuado 30-10-25
    { 'producto': 'Torta sabor lucuma',               'codigo': '393356' },
    { 'producto': 'Torta sacher',                     'codigo': '393354' },
    { 'producto': 'Torta doña isabel',                'codigo': '405256' },
    { 'producto': 'Torta cookies & cream',            'codigo': '405295' },
    #{ 'producto': 'Torta caramel macchiato',          'codigo': '405294' }, Descontinuado 30-10-25
    #{ 'producto': 'Torta piña colada',                'codigo': '405292' }, Descontinuado 30-10-25
    { 'producto': 'Torta panqueque chocolate manjar', 'codigo': '405460' },
    { 'producto': 'Tartaleta fruta mixta mediana',    'codigo': '393270' },
    { 'producto': 'Pie de limon familiar',            'codigo': '393000' },
    #{ 'producto': 'Pie de limon mediano',             'codigo': '405396' }, Descontinuado 30-10-25
    #{ 'producto': 'Pie de maracuya mediano',          'codigo': '405397' }, Descontinuado 30-10-25
  ],
  'Walmart': [
    { 'producto': 'Torta chocoguinda',                'codigo': '393058' },
    { 'producto': 'Torta chocolate manjar',           'codigo': '393347' },
    { 'producto': 'Torta chocolate 8pp',              'codigo': '393275' },
    { 'producto': 'Torta crema frambuesa',            'codigo': '393402' },
    { 'producto': 'Torta crema moka 15pp',            'codigo': '392500' },
    { 'producto': 'Torta crema piña 15pp',            'codigo': '393033' },
    { 'producto': 'Torta holandesa 15pp',             'codigo': '392498' },
    { 'producto': 'Torta mousse manjar 15pp',         'codigo': '392495' },
    { 'producto': 'Torta panqueque naranja',          'codigo': '393295' },
    { 'producto': 'Torta san jorge 15pp',             'codigo': '393250' },
    { 'producto': 'Torta selva negra 15pp',           'codigo': '393020' },
    { 'producto': 'Torta tres leches 15pp',           'codigo': '392494' },
    { 'producto': 'Torta hoja manjar chocolate artesanal', 'codigo': '405262' },
    { 'producto': 'Torta frutos del bosque',          'codigo': '405315' },
    { 'producto': 'Torta chocolate avellana',         'codigo': '393445' },
    { 'producto': 'Torta selva negra crema lactea',   'codigo': '405488' },
    { 'producto': 'Torta piña crema lactea',          'codigo': '405487' },
  ],
  'Unimarc': [
    { 'producto': 'Torta crema manjar mini',          'codigo': '393272' },
    { 'producto': 'Torta guinda mini',                'codigo': '393273' },
    { 'producto': 'Torta hoja manjar 15pp',           'codigo': '392332' },
    { 'producto': 'Torta holandesa smu',              'codigo': '393391' },
    { 'producto': 'Torta panqueque naranja',          'codigo': '393409' },
    { 'producto': 'Torta yogurt frutilla',            'codigo': '393441' },
    { 'producto': 'Torta cuatro leches',              'codigo': '393440' },
  ],
};


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
    SUPERVISOR_CHOICES = [
        ('Fabian Moncada', 'Fabian Moncada'),
        ('Angela Tacon', 'Angela Tacon'),
        ('Felipe Campos', 'Felipe Campos')
    ]
    supervisor = forms.ChoiceField(
        choices=[('', '--Seleccionar supervisor--')] + SUPERVISOR_CHOICES,
        widget=forms.Select(attrs={'id': 'id_supervisor'})
    )
    LINEA_CHOICES = [
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
    ]
    linea    = forms.ChoiceField(
        choices= [('', '--Seleccionar linea--')] + LINEA_CHOICES,
        widget=forms.Select(attrs={'id': 'id_linea'}))
    class Meta:
        model = TurnoOEE
        # 'cliente', 'producto', 'codigo', 'produccion_planeada'
        fields = ['fecha', 'linea', 'turno', 'numero_personas','lote', 'supervisor', 'tiempo_planeado', 'cliente', 'producto', 'codigo', 'produccion_planeada']
        widgets = {
            'tiempo_planeado': forms.NumberInput(attrs={
                # Valor fijo de 480 minutos (8 horas)
                'value': 480,
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
