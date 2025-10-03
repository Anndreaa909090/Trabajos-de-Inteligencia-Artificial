#crear una aplicación con streamlit que conecte a una base de datos mysql y muestre los datos de una tabla en un dataframe
import streamlit as st  
import mysql.connector
import pandas as pd 
# Configuración de la conexión a la base de datos mostrar un mensaje de error si no se puede conectar
def create_connection():
    try:
        connection = mysql.connector.connect(
            host="localhost",   # Cambia esto si tu servidor MySQL está en otro host    
            user="root",        # Cambia esto por tu usuario de MySQL
            password="",    # Cambia esto por tu contraseña de MySQL
            database="productosDB"  # Cambia esto por el nombre de tu base de datos
        )
        return connection
    except mysql.connector.Error as err:
        st.error(f"Error al conectar a la base de datos: {err}")
        return None 
# Función para obtener datos de la tabla productos
def get_productos_data(connection):
    try:
        query = "SELECT * FROM productos"
        df = pd.read_sql(query, connection)
        return df
    except mysql.connector.Error as err:
        st.error(f"Error al obtener datos: {err}")
        return pd.DataFrame()  # Retorna un DataFrame vacío en caso de error        
# Título de la aplicación
st.title("Visualización de Datos desde MySQL con Streamlit")
# Conexión a la base de datos
connection = create_connection()   
# Verificar la conexión y mostrar datos
if connection:
    st.success("Conexión exitosa a la base de datos")
    # Obtener y mostrar datos
    df = get_productos_data(connection)
    if not df.empty:
        st.dataframe(df)
    else:
        st.warning("No se encontraron datos en la tabla productos.")
    
else:
    st.error("No se pudo establecer la conexión a la base de datos.")
# Instrucciones para ejecutar la aplicación
# Crear un formulario para insertar nuevos productos
with st.form("insert_form"):
    st.subheader("Insertar Nuevo Producto")
    nombre = st.text_input("Nombre del Producto")
    precio = st.number_input("Precio del Producto", min_value=0.0, format="%.2f")
    submitted = st.form_submit_button("Insertar Producto")
    if submitted:
        if connection:
            try:
                cursor = connection.cursor()
                insert_query = "INSERT INTO productos (nombre_articulo, precio) VALUES (%s, %s)"
                cursor.execute(insert_query, (nombre, precio))
                connection.commit()
                st.success("Producto insertado correctamente.")
            except mysql.connector.Error as err:
                st.error(f"Error al insertar producto: {err}")
            finally:
                cursor.close()
        else:
            st.error("No hay conexión a la base de datos.") 
# Cerrar la conexión
connection.close()
st.info("Conexión cerrada.")
st.markdown(""" 
Para ejecutar esta aplicación, guarda este código en un archivo llamado `app.py` y luego ejecuta el siguiente comando en tu terminal:

```streamlit run app.py
```                     
Asegúrate de tener instalados los paquetes necesarios:
```pip install streamlit mysql-connector-python pandas
``` 
""")
# Nota: Asegúrate de que la base de datos y la tabla existen, y que los datos están disponibles para mostrar.   