import streamlit as st
import pandas as pd
import urllib.parse
from streamlit_gsheets import GSheetsConnection

# Configuración principal de la página (Debe ser el primer comando)
st.set_page_config(page_title="Catálogo Natura", page_icon="🍃", layout="wide")

# --- CONFIGURACIÓN DE LA HOJA DE CÁLCULO ---
URL_NATURA = "https://docs.google.com/spreadsheets/d/1ImD9O5hdrgJJFQWdiVDTulICbas5a5vG5E5sB0sfg38/edit?usp=sharing"
NOMBRE_HOJA = "Hoja1"

# --- FUNCIONES DE BASE DE DATOS ---
@st.cache_data(ttl=60)
def obtener_productos():
    columnas_esperadas = ["Nombre", "Descripción", "Precio", "Imagen"]
    try:
        conn = st.connection("gsheets", type=GSheetsConnection)
        df = conn.read(spreadsheet=URL_NATURA, worksheet=NOMBRE_HOJA, usecols=[0, 1, 2, 3])
        
        # Eliminar filas que estén completamente vacías
        df = df.dropna(how="all")
        
        # Si el DataFrame no está vacío pero los nombres no coinciden, los forzamos
        if not df.empty and len(df.columns) == 4:
            df.columns = columnas_esperadas
        elif df.empty:
            return pd.DataFrame(columns=columnas_esperadas)
            
        return df
        
    except Exception as e:
        st.error(f"Error al conectar con la base de datos: {e}")
        return pd.DataFrame(columns=columnas_esperadas)

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
    conn.update(spreadsheet=URL_NATURA, worksheet=NOMBRE_HOJA, data=df_actualizado)
    st.cache_data.clear()

# --- MENÚ DE NAVEGACIÓN ---
menu = st.sidebar.selectbox("Navegación", ["Catálogo para Compradores", "Módulo de Administración"])

# Contacto en la barra lateral
st.sidebar.divider()
st.sidebar.subheader("📞 Contacto de Ventas")
st.sidebar.write("**Deisy Sanabria**")
st.sidebar.write("Cel. 3184704968")

# --- MÓDULO DE COMPRADORES ---
if menu == "Catálogo para Compradores":
    st.title("🍃 Catálogo Natura")
    st.write("Explora nuestros productos disponibles. Haz clic en el botón para enviar tu pedido directamente por WhatsApp.")
    st.divider()

    df_productos = obtener_productos()

    if not df_productos.empty:
        cols = st.columns(3)
        for index, row in df_productos.iterrows():
            with cols[index % 3]:
                with st.container(border=True):
                    
                    # --- NUEVO MÉTODO PARA MOSTRAR IMÁGENES ---
                    url_imagen = str(row['Imagen']).strip()
                    
                    if url_imagen.startswith("http"):
                        # Usamos HTML para que el navegador cargue la imagen directamente, saltando a Streamlit
                        st.markdown(
                            f'<img src="{url_imagen}" style="width:100%; border-radius:5px; object-fit:cover; aspect-ratio:1/1;">', 
                            unsafe_allow_html=True
                        )
                    else:
                        st.image("https://via.placeholder.com/300x300?text=Sin+Foto", use_column_width=True)
                    
                    # Espaciado para que se vea ordenado
                    st.write("") 
                    
                    st.subheader(row['Nombre'])
                    st.write(row['Descripción'])
                    st.markdown(f"**Precio:** ${row['Precio']}")
                    
                    # Generar enlace directo a WhatsApp
                    numero_wa = "573184704968"
                    mensaje = f"Hola Deisy, estoy interesado en el producto del catálogo: *{row['Nombre']}* por un valor de ${row['Precio']}."
                    mensaje_codificado = urllib.parse.quote(mensaje)
                    link_wa = f"https://wa.me/{numero_wa}?text={mensaje_codificado}"
                    
                    # Botón nativo de Streamlit
                    st.link_button("Comprar por WhatsApp 💬", link_wa, type="primary", use_container_width=True)
    else:
        st.info("El catálogo no tiene productos registrados o se está actualizando.")

    # Pie de página
    st.divider()
    st.caption("Catálogo gestionado por Deisy Sanabria | Cel. 3184704968")

# --- MÓDULO DE ADMINISTRACIÓN ---
elif menu == "Módulo de Administración":
    st.title("⚙️ Administración del Catálogo")

    if "autenticado" not in st.session_state:
        st.session_state["autenticado"] = False

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
            
        st.subheader("Añadir un Nuevo Producto al Catálogo")
        
        with st.form("formulario_producto", clear_on_submit=True):
            nombre_input = st.text_input("Nombre del Producto")
            descripcion_input = st.text_area("Descripción")
            precio_input = st.number_input("Precio", min_value=0, step=1000, format="%d")
            imagen_input = st.text_input("URL de la imagen (Usa el 'Enlace directo' de Postimages)")
            
            submit = st.form_submit_button("Subir al Catálogo")
            
            if submit:
                if nombre_input and descripcion_input and precio_input > 0:
                    try:
                        with st.spinner("Guardando en Google Sheets..."):
                            guardar_producto(nombre_input, descripcion_input, precio_input, imagen_input)
                        st.success(f"¡Producto '{nombre_input}' guardado con éxito!")
                    except Exception as e:
                        st.error("Hubo un error al guardar. Verifica que compartiste la hoja con el correo de la cuenta de servicio.")
                        st.write(e)
                else:
                    st.warning("Por favor, completa los campos obligatorios (Nombre, Descripción y Precio).")
