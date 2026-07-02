import streamlit as st
import pandas as pd
import urllib.parse
from streamlit_gsheets import GSheetsConnection

# Configuración principal de la página
st.set_page_config(page_title="Catálogo Natura", page_icon="🍃", layout="wide")

# --- FUNCIONES DE BASE DE DATOS ---
# Usamos caché para no saturar las peticiones a Google Sheets
@st.cache_data(ttl=10)
def obtener_productos():
    try:
        conn = st.connection("gsheets", type=GSheetsConnection)
        df = conn.read(worksheet="Hoja1", usecols=[0, 1, 2])
        return df.dropna(how="all")
    except Exception as e:
        # Retorna un DataFrame vacío si hay error o aún no se configura la conexión
        return pd.DataFrame(columns=["Nombre", "Descripción", "Precio"])

def guardar_producto(nombre, descripcion, precio):
    conn = st.connection("gsheets", type=GSheetsConnection)
    df_actual = obtener_productos()
    nuevo_producto = pd.DataFrame([{"Nombre": nombre, "Descripción": descripcion, "Precio": precio}])
    df_actualizado = pd.concat([df_actual, nuevo_producto], ignore_index=True)
    conn.update(worksheet="Hoja1", data=df_actualizado)
    st.cache_data.clear() # Limpiar el caché para mostrar el nuevo producto inmediatamente

# --- MENÚ DE NAVEGACIÓN ---
menu = st.sidebar.selectbox("Navegación", ["Catálogo para Compradores", "Módulo de Administración"])

# --- MÓDULO DE COMPRADORES ---
if menu == "Catálogo para Compradores":
    st.title("🍃 Catálogo Natura - Deisy Sanabria")
    st.write("Explora nuestros productos disponibles. Haz clic en el botón para enviar tu pedido directamente por WhatsApp.")
    st.divider()

    df_productos = obtener_productos()

    if not df_productos.empty:
        # Crear columnas para que el catálogo se vea organizado (ej. 3 productos por fila)
        cols = st.columns(3)
        for index, row in df_productos.iterrows():
            with cols[index % 3]:
                with st.container(border=True):
                    st.subheader(row['Nombre'])
                    st.write(row['Descripción'])
                    st.markdown(f"**Precio: ${row['Precio']}**")
                   
                    # Generar enlace directo a WhatsApp (incluye indicativo +57 para Colombia)
                    numero_wa = "573184704968"
                    mensaje = f"Hola Deisy, estoy interesado en el producto del catálogo: *{row['Nombre']}* por un valor de ${row['Precio']}."
                    mensaje_codificado = urllib.parse.quote(mensaje)
                    link_wa = f"https://wa.me/{numero_wa}?text={mensaje_codificado}"
                   
                    # Botón visual de WhatsApp
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
        st.info("El catálogo está vacío o se está actualizando. Vuelve pronto.")

# --- MÓDULO DE ADMINISTRACIÓN ---
elif menu == "Módulo de Administración":
    st.title("⚙️ Administración del Catálogo")

    # Inicializar estado de sesión para el login
    if "autenticado" not in st.session_state:
        st.session_state["autenticado"] = False

    # Pantalla de Login
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
   
    # Panel de subida de productos
    else:
        st.success("Sesión iniciada correctamente.")
       
        if st.button("Cerrar Sesión"):
            st.session_state["autenticado"] = False
            st.rerun()
           
        st.subheader("Añadir un Nuevo Producto")
       
        with st.form("formulario_producto", clear_on_submit=True):
            nombre_input = st.text_input("Nombre del Producto")
            descripcion_input = st.text_area("Descripción")
            precio_input = st.number_input("Precio", min_value=0, format="%d")
           
            submit = st.form_submit_button("Subir al Catálogo")
           
            if submit:
                if nombre_input and descripcion_input and precio_input > 0:
                    try:
                        guardar_producto(nombre_input, descripcion_input, precio_input)
                        st.success(f"¡Producto '{nombre_input}' subido exitosamente y guardado para siempre!")
                    except Exception as e:
                        st.error("Hubo un error al guardar. Revisa la conexión con Google Sheets.")
                        st.write(e)
                else:
                    st.warning("Por favor, completa todos los campos correctamente.")
