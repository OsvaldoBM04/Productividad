from flask import Flask, render_template, request
import pandas as pd
import os


app = Flask(__name__)

# Cargar datos desde el archivo Excel
def cargar_datos():
    ruta_excel = os.path.join('data', 'Productividad.xlsx')
    try:
        # Lee el archivo Excel
        df = pd.read_excel(ruta_excel, sheet_name='Hoja1')  # Cambia 'Datos' por el nombre de tu hoja si es necesario
        print("Datos cargados con éxito:")
        print(df.head())
        return df #devuelve el data frame df
    except Exception as e:
        print(f"Error al cargar datos: {e}")
        return pd.DataFrame()  # Devuelve un DataFrame vacío en caso de error
    

@app.route('/')
def index():
    datos = cargar_datos()  # Cargar los datos de Excel
    # Convertir el DataFrame a un formato que puedas usar en la plantilla
#    lista_datos = datos.to_dict(orient='records')  # Convertir a lista de diccionarios
#    return render_template('index.html', datos=lista_datos)
    return render_template('index.html', datos=datos.to_dict(orient='records'))

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/datos', methods=['GET', 'POST'])
def datos():
    datos = cargar_datos()  # Cargar los datos de Excel

     # Obtener valores únicos de las columnas para los filtros
    municipios_unicos = datos['Municipio'].unique().tolist()  # Obtener municipios únicos
    unidades_unicas = datos['Unidad'].unique().tolist()  # Obtener unidades únicas
    meses_unicos = datos['Mes'].unique().tolist()  # Obtener meses únicos
    clues_unicos = datos['Clues'].unique().tolist()  # Obtener clues únicos
    jurisdicciones_unicas = datos['Jurisdicción'].unique().tolist()  # Obtener jurisdicciones únicas
    tipologia_unica = datos['Tipologia'].unique().tolist()  # Obtener tipologías únicas
    turnos_unicos = datos['Turno'].unique().tolist()  # Obtener turnos únicos   
    trimestre_unico = datos['Trimestre'].unique().tolist()  # Obtener trimestres únicos
    anio_unico = datos['Año'].unique().tolist()  # Obtener años únicos  

    print("Municipios únicos:", municipios_unicos)  # Imprimir municipios únicos para depuración
    print("Unidades únicas:", unidades_unicas)  # Imprimir unidades únicas para depuración
    print("Meses únicos:", meses_unicos)  # Imprimir meses únicos para depuración

     # Inicializar variables de filtro con valores predeterminados o None    
    municipio = request.form.get('municipio') if request.method == 'POST' else None    
    unidad = request.form.get('unidad') if request.method == 'POST' else None
    mes = request.form.get('mes') if request.method == 'POST' else None
    clues = request.form.get('clues') if request.method == 'POST' else None
    jurisdiccion = request.form.get('jurisdiccion') if request.method == 'POST' else None
    tipologia = request.form.get('tipologia') if request.method == 'POST' else None
    turno = request.form.get('turno') if request.method == 'POST' else None
    trimestre = request.form.get('trimestre') if request.method == 'POST' else None
    anio = request.form.get('anio') if request.method == 'POST' else None


    # Filtros
#    if request.method == 'POST':
#        municipio = request.form.get('municipio')
#        unidad = request.form.get('unidad')
#        mes = request.form.get('mes')
#        clues=request.form.get('clues')
#        jurisdiccion=request.form.get('jurisdiccion')
#        tipologia=request.form.get('tipologia')
#        turno=request.form.get('turno')
#        trimestre=request.form.get('trimestre')
#        anio=request.form.get('anio')
                 

    # Filtrado de datos según el formulario
    if municipio:
        df = df[df['Municipio'] == municipio]
    if unidad:
        df = df[df['Unidad'] == unidad]
    if mes:
        df = df[df['Mes'] == mes]
    
    # Ordenar el DataFrame por la columna 'Fecha' de manera descendente
    datos = datos.sort_values(by='Fecha', ascending=False)
    datos['Productividad']=datos['Consultas de unidad']/datos['JornadasxUnidad']
#    datos['Productividad']=datos['Productividad'].astype(float)  # Convertir la columna 'Productividad' a tipo float
#    datos['Año' ] = datos['Fecha'].dt.year  # Extraer el año de la columna 'Fecha' y crear una nueva columna 'Año'

    return render_template('datos.html', datos=datos.to_dict(orient='records'),
                           municipios_unicos=municipios_unicos, 
                           unidades=unidades_unicas, 
                           meses=meses_unicos,
                           clue=clues_unicos,
                           juris=jurisdicciones_unicas,
                           tipo=tipologia_unica,
                           turn=turnos_unicos,
                           trim=trimestre_unico,
                           anios=anio_unico)


    #if request.method == 'POST':

    lista_datos = datos.to_dict(orient='records')  # Convertir a lista de diccionarios
    return render_template('datos.html', datos=lista_datos)


if __name__ == '__main__':
    app.run(debug=True) # correr la aplicación en el servidor local, debug=True
    # para que se actualice automáticamente cuando se hagan cambios sin volver a correr la aplicación
    # al correr la app con run se solciita que se ejecute la aplicación "app" que se inicio al principio del código

    # para que se actualice automáticamente cuando se hagan cambios sin volver a correr la aplicación