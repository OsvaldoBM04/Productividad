from flask import Flask, render_template, request, jsonify
import pandas as pd
import os


app = Flask(__name__)

# Cargar datos desde el archivo Excel
def cargar_datos():
    ruta_excel = os.path.join('data', 'Productividad.xlsx')
    try:
        # Lee el archivo Excel
        df = pd.read_excel(ruta_excel, sheet_name='Hoja1')  # Cambia 'Datos' por el nombre de tu hoja si es necesario
        df['Fecha']=pd.to_datetime(df['Fecha'], errors='coerce')  # Asegúrate de que la columna 'Fecha' esté en el formato correcto
        print("Datos cargados con éxito:")
        print(df.head())
        return df #devuelve el data frame df
    except Exception as e:
        print(f"Error al cargar datos: {e}")
        return pd.DataFrame()  # Devuelve un DataFrame vacío en caso de error
    
def calcular_productividad_periodo(datos, meses):
    # Ordenar por la fecha para que las agrupaciones sean cronológicas
    datos = datos.sort_values(by='Fecha')
    # Asegurarse de que la columna 'Fecha' esté en formato datetime
    datos['Fecha'] = pd.to_datetime(datos['Fecha'], errors='coerce')

    # Definir frecuencia de agrupación según el periodo de meses
    if meses == 2:
        freq = '2M'  # Bimestral
    elif meses == 6:
        freq = '6M'  # Semestral
    else:  # Por defecto, si no se especifica un periodo válido, no se agrupa
      # Productividad sin agrupación (ningún periodo seleccionado)
        datos['Productividad'] = datos['Consultas de unidad'] / datos['JornadasxUnidad'].round(2)  # Calcular productividad sin agrupar
        return datos    

    # Agrupar por 'Clues', 'Unidad' y periodos de la columna 'Fecha'
    datos_agrupados = datos.groupby(
        ['Clues', 'Unidad', pd.Grouper(key='Fecha', freq=freq), 'Año']
    ).agg({
        'Consultas de unidad': 'sum',
        'JornadasxUnidad': 'sum'
    }).reset_index()

     # Verifica si los datos agrupados son correctos
    print("Datos agrupados:")
    print(datos_agrupados.head())

# Cálculo de productividad
    datos_agrupados['Productividad'] = (datos_agrupados['Consultas de unidad'] / datos_agrupados['JornadasxUnidad']).round(2)  # Calcular productividad agrupada
    # Ordenar los resultados por fecha de forma descendente
    datos_agrupados = datos_agrupados.sort_values(by='Fecha', ascending=False)
    return datos_agrupados


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
        # Ordenar el DataFrame por la columna 'Fecha' de manera descendente
    datos = datos.sort_values(by='Fecha', ascending=False) 

     # Obtener valores únicos de las columnas para los filtros
    municipios_unicos = datos['Municipio'].unique().tolist()  # Obtener municipios únicos
    unidades_unicas = datos['Unidad'].unique().tolist()  # Obtener unidades únicas
    meses_unicos = datos['Mes'].unique().tolist()  # Obtener meses únicos
    clues_unicos = datos['Clues'].unique().tolist()  # Obtener clues únicos
    jurisdicciones_unicas = datos['Jurisdicción'].unique().tolist()  # Obtener jurisdicciones únicas
    tipologia_unica = datos['Tipologia'].unique().tolist()  # Obtener tipologías únicas
    turnos_unicos = datos['Turno'].unique().tolist()  # Obtener turnos únicos   
    trimestre_unico = datos['Trimestre'].unique().tolist()  # Obtener trimestres únicos
    anio_unicos = datos['Año'].unique().tolist()  # Obtener años únicos  

    print("Municipios únicos:", municipios_unicos)  # Imprimir municipios únicos para depuración
    print("Unidades únicas:", unidades_unicas)  # Imprimir unidades únicas para depuración
    print("Meses únicos:", meses_unicos)  # Imprimir meses únicos para depuración
    print("Años unicos", anio_unicos)

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
    periodo = request.form.get('periodo') if request.method == 'POST' else None
        

    # Filtrado de datos según el formulario
    if municipio:
        datos = datos[datos['Municipio'] == municipio]
    if unidad:
        datos = datos[datos['Unidad'] == unidad]
    if anio:
        datos = datos[datos['Año'] == int(anio)]
    
       # Calcular la productividad en función del periodo seleccionado
    if periodo == "2":  # Agrupación bimestral
        datos = calcular_productividad_periodo(datos, meses=2)
    elif periodo == "6":  # Agrupación semestral
        datos = calcular_productividad_periodo(datos, meses=6)
    else:
        # Productividad sin agrupación (ningún periodo seleccionado)
        datos['Productividad'] = datos['Consultas de unidad'] / datos['JornadasxUnidad'].round(2)  # Calcular la productividad sin agrupación

    # Transformar los datos a formato de mes
    datos = transformar_a_mes(datos)
    
#    datos['Productividad']=datos['Productividad'].astype(float)  # Convertir la columna 'Productividad' a tipo float
#    datos['Año' ] = datos['Fecha'].dt.year  # Extraer el año de la columna 'Fecha' y crear una nueva columna 'Año'

    return render_template('datos.html', datos=datos.to_dict(orient='records'),
                           municipios_unicos=municipios_unicos, 
                           unidades_unicas=unidades_unicas, 
                           meses_unicos=meses_unicos,
                           clues_unicos=clues_unicos,
                           jurisdicciones_unicas=jurisdicciones_unicas,
                           tipologia_unica=tipologia_unica,
                           turnos_unicos=turnos_unicos,
                           trimestre_unico=trimestre_unico,
                           anio_unicos=anio_unicos)


    #if request.method == 'POST':

 #   lista_datos = datos.to_dict(orient='records')  # Convertir a lista de diccionarios
 #   return render_template('datos.html', datos=lista_datos)

# Transformar los datos a formato de mes
def transformar_a_mes(datos):
    meses = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']
    
    datos['Mes'] = datos['Fecha'].dt.month
    datos_agrupados_mes = datos.pivot_table(
        index=['Clues', 'Unidad', 'Año'],
        columns='Mes',
        values='Productividad',
        aggfunc='first'
    ).reset_index()

    # Verifica si los datos agrupados por mes están correctos
    print("Datos agrupados por mes:")
    print(datos_agrupados_mes.head())


        # Renombrar las columnas numéricas de meses a nombres de meses
    column_mapping = {i + 1: meses[i] for i in range(12)}  # Mapear 1-12 a nombres de meses
    datos_agrupados_mes = datos_agrupados_mes.rename(columns=column_mapping)

# Formatear las columnas de los meses para que tengan un decimal
    for mes in meses:
        if mes in datos_agrupados_mes.columns:
            datos_agrupados_mes[mes] = datos_agrupados_mes[mes].apply(
                lambda x: f"{float(x):.1f}" if isinstance(x, (int, float)) else x
            )

     # Asegurarse de que todas las columnas de meses estén presentes
    for mes in meses:
        if mes not in datos_agrupados_mes.columns:
            datos_agrupados_mes[mes] = None  # Agregar columna faltante con valores 'None'


# Si la tabla tiene más o menos de 12 columnas (más las 3 de 'Clues', 'Unidad' y 'Año'), ajusta
    if len(datos_agrupados_mes.columns) == 15:  # Tres columnas más los 12 meses
        # Renombrar las columnas para que sean los nombres de los meses
        datos_agrupados_mes.columns = ['Clues', 'Unidad', 'Año'] + meses
    else:
        # Ajusta según lo que necesites si el número de columnas no es 15
        print("Error: El número de columnas no es el esperado.")

        
  # Asegurarse de que todas las columnas de meses estén presentes, incluso si faltan en los datos
    for mes in meses:
        if mes not in datos_agrupados_mes.columns:
            datos_agrupados_mes[mes] = None  # Agregar columna faltante con valores 'None'
  # Rellenar los valores faltantes con "N/A" para visualización en HTML
    datos_agrupados_mes = datos_agrupados_mes.fillna("N/A")



    return datos_agrupados_mes


if __name__ == '__main__':
    app.run(debug=True) # correr la aplicación en el servidor local, debug=True
    # para que se actualice automáticamente cuando se hagan cambios sin volver a correr la aplicación
    # al correr la app con run se solciita que se ejecute la aplicación "app" que se inicio al principio del código

    # para que se actualice automáticamente cuando se hagan cambios sin volver a correr la aplicación