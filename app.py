import streamlit as st
import pandas as pd
import urllib.parse
from streamlit_gsheets import GSheetsConnection

# ---------------------------------------------------------
# CONFIGURACIÓN DE LA PÁGINA
# ---------------------------------------------------------
st.set_page_config(
    page_title="Catálogo Natura | Deisy Sanabria",
    page_icon="🍃",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------------------------------------------------
# ESTILOS CSS PERSONALIZADOS (ESTÉTICTA NATURA)
# ---------------------------------------------------------
NATURA_CSS = """
<style>
    /* Importar fuente suave y moderna */
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Poppins', sans-serif;
    }

    /* Fondo general fresco y natural */
    .main {
        background: linear-gradient(135deg, #FAF8F5 0%, #F3EFEA 100%);
    }

    /* Encabezado principal elegante */
    .natura-header {
        background: linear-gradient(90deg, #FF6B00 0%, #E05206 100%);
        padding: 30px;
        border-radius: 20px;
        color: white;
        text-align: center;
        box-shadow: 0px 10px 25px rgba(224, 82, 6, 0.2);
        margin-bottom: 25px;
    }
    
    .natura-header h1 {
        color: #FFFFFF !important;
        font-weight: 700;
        margin-bottom: 5px;
    }

    .natura-header p {
        font-size: 1.1rem;
        opacity: 0.95;
    }

    /* Tarjetas de producto */
    .natura-card {
        background-color: #FFFFFF;
        border-radius: 16px;
        padding: 18px;
        border: 1px solid #EAE5DF;
        box-shadow: 0px 4px 15px rgba(0, 0, 0, 0.04);
        transition: transform 0.25s ease, box-shadow 0.25s ease;
        margin-bottom: 20px;
    }
    
    .natura-card:hover {
        transform: translateY(-5px);
        box-shadow: 0px 8px 25px rgba(224, 82, 6, 0.12);
    }

    /* Tag de precio */
    .price-tag {
        font-size: 1.3rem;
        font-weight: 700;
        color: #E05206;
        background: #FFF4EE;
        padding: 4px 12px;
        border-radius: 10px;
        display: inline-block;
        margin-top: 8px;
        margin-bottom: 12px;
    }

    /* Botón personalizado de WhatsApp */
    .wa-button {
        display: block;
        width: 100%;
        background-color: #25D366;
        color: white !important;
        text-align: center;
        padding: 10px 15px;
        border-radius: 12px;
        font-weight: 600;
        text-decoration: none;
        box-shadow: 0 4px 12px rgba(37, 211, 102, 0.25);
        transition: background-color 0.2s ease;
    }
    .wa-button:hover {
        background-color: #1EBE57;
        color: white !important;
        text-decoration: none;
    }

    /* Estilos del Sidebar */
    [data-testid="stSidebar"] {
        background-color: #FFFFFF;
        border-right: 1px solid #EAE5DF;
    }
</style>
"""
st.markdown(NATURA_CSS, unsafe_allow_html=True)

# ---------------------------------------------------------
# CONFIGURACIÓN DE LA HOJA DE CÁLCULO
# ---------------------------------------------------------
URL_NATURA = "https://docs.google.com/spreadsheets/d/1ImD9O5hdrgJJFQWdiVDTulICbas5a5vG5E5sB0sfg38/edit?usp=sharing"
NOMBRE_HOJA = "Hoja1"

# ---------------------------------------------------------
# FUNCIONES DE BASE DE DATOS
# ---------------------------------------------------------
@st.cache_data(ttl=60)
def obtener_productos():
    columnas_esperadas = ["Nombre", "Descripción", "Precio", "Imagen"]
    try:
        conn = st.connection("gsheets", type=GSheetsConnection)
        df = conn.read(spreadsheet=URL_NATURA, worksheet=NOMBRE_HOJA, usecols=[0, 1, 2, 3])
        df = df.dropna(how="all")
        
        if not df.empty and len(df.columns) == 4:
            df.columns = columnas_esperadas
        elif df.empty:
            return pd.DataFrame(columns=columnas_esperadas)
            
        df["Nombre"] = df["Nombre"].fillna("Producto Natura")
        df["Descripción"] = df["Descripción"].fillna("")
        df["Imagen"] = df["Imagen"].fillna("")
        df["Precio"] = pd.to_numeric(df["Precio"], errors='coerce').fillna(0)
        
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

# ---------------------------------------------------------
# MENÚ DE NAVEGACIÓN Y SIDEBAR
# ---------------------------------------------------------
st.sidebar.image("https://upload.wikimedia.org/wikipedia/commons/d/d4/Natura_Logo.svg", width=160) if False else None

menu = st.sidebar.radio("Navegación", ["🌸 Catálogo de Productos", "⚙️ Módulo de Administración"])

st.sidebar.divider()

if st.sidebar.button("🔄 Refrescar Catálogo", use_container_width=True):
    st.cache_data.clear()
    st.rerun()

st.sidebar.divider()
st.sidebar.markdown("""
<div style="background-color:#FFF4EE; padding:15px; border-radius:12px; border-left:4px solid #FF6B00;">
    <h4 style="margin:0; color:#E05206;">🛍️ Consultora Oficial</h4>
    <p style="margin:5px 0 0 0; font-weight:600; color:#333;">Deisy Sanabria</p>
    <p style="margin:0; color:#666; font-size:0.9rem;">📲 Cel: 318 470 4968</p>
</div>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# MÓDULO DE COMPRADORES
# ---------------------------------------------------------
if menu == "🌸 Catálogo de Productos":
    
    # Header Banner Estilo Natura
    st.markdown("""
    <div class="natura-header">
        <h1>🍃 Bienvenida a tu Espacio Natura</h1>
        <p>Descubre cosméticos, perfumería y cuidado personal inspirados en la naturaleza.</p>
    </div>
    """, unsafe_allow_html=True)

    df_productos = obtener_productos()

    if not df_productos.empty:
        # Buscador y Filtros
        col_busqueda, col_filtro = st.columns([2, 1])
        with col_busqueda:
            busqueda = st.text_input("🔍 Buscar producto por nombre...", "").strip().lower()
        with col_filtro:
            precio_max = float(df_productos["Precio"].max()) if not df_productos.empty else 100000.0
            precio_filtro = st.slider("Filtrar por Precio Máximo ($)", min_value=0, max_value=int(precio_max), value=int(precio_max), step=5000)

        # Aplicar filtros
        df_filtrado = df_productos[
            (df_productos["Nombre"].str.lower().str.contains(busqueda)) &
            (df_productos["Precio"] <= precio_filtro)
        ]

        st.write("")

        if not df_filtrado.empty:
            cols = st.columns(3)
            for index, row in df_filtrado.reset_index(drop=True).iterrows():
                with cols[index % 3]:
                    url_imagen = str(row['Imagen']).strip()
                    precio_formateado = f"{int(row['Precio']):,}".replace(",", ".")
                    
                    numero_wa = "573184704968"
                    mensaje = f"Hola Deisy, estoy interesada en el producto: *{row['Nombre']}* por ${precio_formateado}."
                    link_wa = f"https://wa.me/{numero_wa}?text={urllib.parse.quote(mensaje)}"

                    # Tarjeta contenedor
                    with st.container():
                        st.markdown('<div class="natura-card">', unsafe_allow_html=True)
                        
                        # Renderizado de Imagen
                        if url_imagen.startswith("http"):
                            st.image(url_imagen, use_column_width=True)
                        else:
                            st.markdown('<div style="width:100%; aspect-ratio:1/1; background-color:#F5F2ED; border-radius:12px; display:flex; align-items:center; justify-content:center; color:#A0988E; font-weight:500;">📷 Sin fotografía</div>', unsafe_allow_html=True)
                        
                        st.markdown(f"### {row['Nombre']}")
                        st.write(row['Descripción'])
                        st.markdown(f'<div class="price-tag">${precio_formateado}</div>', unsafe_allow_html=True)
                        
                        # Botón Directo WhatsApp
                        st.markdown(f'<a href="{link_wa}" target="_blank" class="wa-button">Pedir por WhatsApp 💬</a>', unsafe_allow_html=True)
                        
                        st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.warning("No se encontraron productos con los criterios seleccionados.")
    else:
        st.info("El catálogo se está actualizando o no contiene productos registrados.")

    st.divider()
    st.caption("Catálogo digital gestionado por Deisy Sanabria | Atención personalizada en Colombia")

# ---------------------------------------------------------
# MÓDULO DE ADMINISTRACIÓN
# ---------------------------------------------------------
elif menu == "⚙️ Módulo de Administración":
    st.title("⚙️ Panel de Control")

    if "autenticado" not in st.session_state:
        st.session_state["autenticado"] = False

    if not st.session_state["autenticado"]:
        st.subheader("Acceso Restringido")
        with st.form("login_form"):
            usuario = st.text_input("Usuario")
            contrasena = st.text_input("Contraseña", type="password")
            btn_login = st.form_submit_button("Ingresar")
            
            if btn_login:
                if usuario == "1098665319dc" and contrasena == "DeisyCaro2026*":
                    st.session_state["autenticado"] = True
                    st.rerun()
                else:
                    st.error("Credenciales incorrectas.")
    
    else:
        st.success("Sesión activa como Administradora.")
        if st.button("Cerrar Sesión"):
            st.session_state["autenticado"] = False
            st.rerun()
            
        st.divider()
        st.subheader("➕ Agregar Nuevo Producto")
        
        with st.form("formulario_producto", clear_on_submit=True):
            nombre_input = st.text_input("Nombre del Producto")
            descripcion_input = st.text_area("Descripción detallada")
            precio_input = st.number_input("Precio ($)", min_value=0, step=1000, format="%d")
            imagen_input = st.text_input("URL de la imagen (Directa, ej: Postimages)")
            
            submit = st.form_submit_button("Guardar en Catálogo")
            
            if submit:
                if nombre_input and descripcion_input and precio_input > 0:
                    try:
                        with st.spinner("Actualizando Google Sheets..."):
                            guardar_producto(nombre_input, descripcion_input, precio_input, imagen_input)
                        st.success(f"¡Producto '{nombre_input}' publicado exitosamente!")
                    except Exception as e:
                        st.error("Error al actualizar la base de datos. Verifica permisos de tu Google Sheet.")
                else:
                    st.warning("Completa los campos obligatorios (Nombre, Descripción y Precio).")
