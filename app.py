import streamlit as st
import pandas as pd
import urllib.parse
from streamlit_gsheets import GSheetsConnection

# Configuración principal de la página
st.set_title = "Catálogo Natura"
st.set_page_config(page_title="Catálogo Natura", page_icon="🍃", layout="wide")

# --- CONFIGURACIÓN DE LA HOJA DE CÁLCULO NATURA ---
# Abre la hoja NATURA en el navegador de Deisy, copia todo el link de la barra de direcciones y pégalo aquí:
URL_NATURA = "https://docs.google.com/spreadsheets/d/1ImD9O5hdrgJJFQWdiVDTulICbas5a5vG5E5sB0sfg38/edit?pli=1&gid=0#gid=0"
NOMBRE_HOJA = "Hoja1"

# --- FUNCIONES DE BASE DE DATOS ---
@st.cache_data(ttl=5)
def obtener_productos():
    try:
        conn = st.connection("gsheets", type=GSheetsConnection)
        # Leemos explícitamente la hoja NATURA y la pestaña Hoja1
        df = conn.read(spreadsheet=URL_NATURA, worksheet=NOMBRE_HOJA, usecols=[0, 1, 2, 3])
        return df.dropna(how="all")
    except Exception as e:
        # Retorna estructura básica si hay un error de conexión inicial
        return pd.DataFrame(columns=["Nombre", "Descripción", "Precio", "Imagen"])

def guardar_producto(nombre, descripcion, precio, imagen_url):
    conn = st.connection("gsheets", type=GSheetsConnection)
    df_actual = obtener_productos()
    nuevo_producto = pd.DataFrame([{
        "Nombre": nombre,
        "Descripción": descripcion,
        "Precio": precio,
        "Imagen": imagen_url
    }])
    df_actualizado = pd.concat([df_actual, nuevo_producto], ignore_index=True)
    # Actualizamos directamente el archivo NATURA en Drive
    conn.update(spreadsheet=URL_NATURA, worksheet=NOMBRE_HOJA, data=df_actualizado)
    st.cache_data.clear() # Limpia el caché para ver el cambio de inmediato

# --- MENÚ DE NAVEGACIÓN ---
menu = st.sidebar.selectbox("Navegación", ["Catálogo para Compradores", "Módulo de Administración"])

# --- MÓDULO DE COMPRADORES ---
if menu == "Catálogo para Compradores":
    st.title("🍃 Catálogo Natura - Deisy Sanabria")
    st.write("Explora nuestros productos disponibles. Haz clic en el botón para enviar tu pedido directamente por WhatsApp.")
    st.divider()

    df_productos = obtener_productos()

    if not df_productos.empty:
        cols = st.columns(3)
        for index, row in df_productos.iterrows():
            with cols[index % 3]:
                with st.container(border=True):
                    # Control de visualización de la imagen
                    if pd.notna(row['Imagen']) and str(row['Imagen']).startswith("http"):
                        st.image(row['Imagen'], use_column_width=True)
                    else:
                        st.image("https://via.placeholder.com/300x300?text=Sin+Foto", use_column_width=True)
                   
                    st.subheader(row['Nombre'])
                    st.write(row['Descripción'])
                    st.markdown(f"**Precio: ${row['Precio']}**")
                   
                    # Enlace directo a WhatsApp de la vendedora
                    numero_wa = "573184704968"
                    mensaje = f"Hola Deisy, estoy interesado en el producto del catálogo: *{row['Nombre']}* por un valor de ${row['Precio']}."
                    mensaje_codificado = urllib.parse.quote(mensaje)
                    link_wa = f"https://wa.me/{numero_wa}?text={mensaje_codificado}"
                   
                    st.markdown(
                        f"""
                        <a href="{link_wa}" target="_blank" style="text-decoration: none;">
                            <div style="background-color: #25D366; color: white; text-align: center; padding: 10px; border-radius: 5px; font-weight: bold; margin-top: 10px;">
                                Comprar por WhatsApp 💬
                            </div>
                        </a>
                        """,
                        unsafe_allow_html=True
                    )
    else:
        st.info("El catálogo no tiene productos registrados en la hoja NATURA o la conexión se está estableciendo.")

# --- MÓDULO DE ADMINISTRACIÓN ---
elif menu == "Módulo de Administración":
    st.title("⚙️ Administración del Catálogo")

    if "autenticado" not in st.session_state:
        st.session_state["autenticado"] = False

    # Control de acceso con las credenciales asignadas
    if not st.session_state["autenticado"]:
        st.write("Ingresa tus credenciales para agregar productos.")
        usuario = st.text_input("Usuario")
        contrasena = st.text_input("Contraseña", type="password")
       
        if st.button("Ingresar"):
            if usuario == "1098665319dc" and contrasena == "DeisyCaro2026*":
                st.session_state["autenticado"] = True
                st.rerun()
            else:
                st.error("Credenciales incorrectas. Intenta de nuevo.")
   
    else:
        st.success("Sesión iniciada correctamente.")
       
        if st.button("Cerrar Sesión"):
            st.session_state["autenticado"] = False
            st.rerun()
           
        st.subheader("Añadir un Nuevo Producto a la hoja NATURA")
       
        with st.form("formulario_producto", clear_on_submit=True):
            nombre_input = st.text_input("Nombre del Producto")
            descripcion_input = st.text_area("Descripción")
            precio_input = st.number_input("Precio", min_value=0, format="%d")
            imagen_input = st.text_input("URL de la imagen del producto")
           
            submit = st.form_submit_button("Subir al Catálogo")
           
            if submit:
                if nombre_input and descripcion_input and precio_input > 0:
                    try:
                        guardar_producto(nombre_input, descripcion_input, precio_input, imagen_input)
                        st.success(f"¡Producto '{nombre_input}' guardado con éxito en Google Drive!")
                        st.rerun()
                    except Exception as e:
                        st.error("Hubo un error al guardar. Verifica que compartiste la hoja NATURA con el correo de la cuenta de servicio.")
                        st.write(e)
                else:
                    st.warning("Por favor, completa los campos requeridos obligatorios (Nombre, Descripción y Precio).")
Cel. 3007351747

