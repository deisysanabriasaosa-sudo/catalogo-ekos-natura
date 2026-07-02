import streamlit as st
import pandas as pd
import urllib.parse
from streamlit_gsheets import GSheetsConnection

# Configuración principal
st.set_page_config(page_title="Catálogo Natura", page_icon="🍃", layout="wide")

# --- FUNCIONES DE BASE DE DATOS ---
@st.cache_data(ttl=5)
def obtener_productos():
    try:
        conn = st.connection("gsheets", type=GSheetsConnection)
        # Ahora leemos 4 columnas: Nombre, Descripción, Precio, Imagen
        df = conn.read(worksheet="Hoja1", usecols=[0, 1, 2, 3])
        return df.dropna(how="all")
    except Exception as e:
        return pd.DataFrame(columns=["Nombre", "Descripción", "Precio", "Imagen"])

def guardar_producto(nombre, descripcion, precio, imagen_url):
    conn = st.connection("gsheets", type=GSheetsConnection)
    df_actual = obtener_productos()
    nuevo_producto = pd.DataFrame([{
        "Nombre": nombre,
        "Descripción": descripcion,
        "Precio": precio,
        "Imagen": imagen_url # Guardamos el link
    }])
    df_actualizado = pd.concat([df_actual, nuevo_producto], ignore_index=True)
    conn.update(worksheet="Hoja1", data=df_actualizado)
    st.cache_data.clear()

# --- MENÚ ---
menu = st.sidebar.selectbox("Navegación", ["Catálogo para Compradores", "Módulo de Administración"])

# --- MÓDULO DE COMPRADORES ---
if menu == "Catálogo para Compradores":
    st.title("🍃 Catálogo Natura - Deisy Sanabria")
    st.divider()

    df_productos = obtener_productos()

    if not df_productos.empty:
        # Mostramos los productos en una cuadrícula
        cols = st.columns(3)
        for index, row in df_productos.iterrows():
            with cols[index % 3]:
                with st.container(border=True):
                    # --- MOSTRAR IMAGEN ---
                    if pd.notna(row['Imagen']) and str(row['Imagen']).startswith("http"):
                        st.image(row['Imagen'], use_column_width=True)
                    else:
                        # Imagen por defecto si no hay link
                        st.image("https://via.placeholder.com/300x300?text=Sin+Foto", use_column_width=True)
                   
                    st.subheader(row['Nombre'])
                    st.write(row['Descripción'])
                    st.subheader(f"${row['Precio']}")
                   
                    # WhatsApp Link
                    numero_wa = "573184704968"
                    mensaje = f"Hola Deisy, quiero el producto: *{row['Nombre']}* (${row['Precio']})."
                    link_wa = f"https://wa.me/{numero_wa}?text={urllib.parse.quote(mensaje)}"
                   
                    st.markdown(f'''<a href="{link_wa}" target="_blank" style="text-decoration:none;"><div style="background-color:#25D366;color:white;text-align:center;padding:10px;border-radius:5px;font-weight:bold;">Pedir por WhatsApp 💬</div></a>''', unsafe_allow_html=True)
    else:
        st.info("Cargando productos...")

# --- MÓDULO DE ADMINISTRACIÓN ---
elif menu == "Módulo de Administración":
    st.title("⚙️ Administrador")

    if "autenticado" not in st.session_state:
        st.session_state["autenticado"] = False

    if not st.session_state["autenticado"]:
        usuario = st.text_input("Usuario")
        contrasena = st.text_input("Contraseña", type="password")
        if st.button("Ingresar"):
            if usuario == "1098665319dc" and contrasena == "DeisyCaro2026*":
                st.session_state["autenticado"] = True
                st.rerun()
            else:
                st.error("Error")
   
    else:
        st.subheader("Añadir Producto con Imagen")
        with st.form("nuevo_p"):
            nombre = st.text_input("Nombre")
            desc = st.text_area("Descripción")
            precio = st.number_input("Precio", min_value=0)
            # Aquí pegas el link de la foto
            img = st.text_input("URL de la imagen (Link directo)")
            st.caption("Tip: Puedes buscar el producto en la web de Natura, dar clic derecho a la foto y elegir 'Copiar dirección de imagen'.")
           
            if st.form_submit_button("Guardar"):
                if nombre and img:
                    guardar_producto(nombre, desc, precio, img)
                    st.success("¡Guardado!")
                    st.rerun()

        if st.button("Cerrar Sesión"):
            st.session_state["autenticado"] = False
            st.rerun()
