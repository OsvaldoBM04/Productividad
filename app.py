from flask import Flask, render_template
import pandas as pd
import os


app = Flask(__name__)

# Cargar datos desde el archivo Excel
def cargar_datos():
    ruta_excel = os.path.join('data', 'Productividad.xlsx')
    try:
        # Lee el archivo Excel
        df = pd.read_excel(ruta_excel, sheet_name='Hoja1')  # Cambia 'Datos' por el nombre de tu hoja si es necesario
        print(df.head())
        return df
    except Exception as e:
        print(f"Error al cargar datos: {e}")
        return pd.DataFrame()  # Devuelve un DataFrame vacío en caso de error
    

@app.route('/')
def index():
    datos = cargar_datos()  # Cargar los datos de Excel
    # Convertir el DataFrame a un formato que puedas usar en la plantilla
    lista_datos = datos.to_dict(orient='records')  # Convertir a lista de diccionarios
    return render_template('index.html', datos=lista_datos)

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/datos')
def datos():
    datos = cargar_datos()  # Cargar los datos de Excel
    lista_datos = datos.to_dict(orient='records')  # Convertir a lista de diccionarios
    return render_template('datos.html', datos=lista_datos)


if __name__ == '__main__':
    app.run(debug=True) # correr la aplicación en el servidor local, debug=True
    # para que se actualice automáticamente cuando se hagan cambios sin volver a correr la aplicación
    # al correr la app con run se solciita que se ejecute la aplicación "app" que se inicio al principio del código

    # para que se actualice automáticamente cuando se hagan cambios sin volver a correr la aplicación