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
# ESTILOS CSS PERSONALIZADOS (ESTÉTICTA BOTÁNICA NATURA)
# ---------------------------------------------------------
NATURA_CSS = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&family=Playfair+Display:ital,wght@1,500&display=swap');

    html, body, [class*="css"] {
        font-family: 'Poppins', sans-serif;
    }

    /* Fondo general natural con textura suave */
    .main {
        background: linear-gradient(135deg, #FAF6F0 0%, #F5EFE6 100%);
    }

    /* ENCABEZADO ESTILO CORONA BOTÁNICA */
    .header-container {
        display: flex;
        justify-content: center;
        align-items: center;
        padding: 30px 10px;
        margin-bottom: 25px;
    }

    .botanical-circle {
        background-color: #FFFFFF;
        width: 320px;
        height: 320px;
        border-radius: 50%;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        text-align: center;
        padding: 25px;
        /* Sombra cálida suave */
        box-shadow: 0px 15px 35px rgba(224, 82, 6, 0.12), 0px 0px 0px 12px rgba(255, 255, 255, 0.6);
        border: 2px solid #F0E6D8;
        position: relative;
    }

    .brand-logo-text {
        font-size: 2.2rem;
        font-weight: 700;
        color: #333333;
        letter-spacing: -1px;
        margin-bottom: 0px;
        line-height: 1;
    }

    .brand-slogan {
        font-family: 'Playfair Display', serif;
        font-style: italic;
        font-size: 1.2rem;
        color: #4A3E3D;
        margin-top: 5px;
    }

    /* Tarjetas de producto */
    .natura-card {
        background-color: #FFFFFF;
        border-radius: 18px;
        padding: 18px;
        border: 1px solid #EAE5DF;
        box-shadow: 0px 4px 15px rgba(0, 0, 0, 0.03);
        transition: transform 0.25s ease, box-shadow 0.25s ease;
        margin-bottom: 20px;
    }
    
    .natura-card:hover {
        transform: translateY(-4px);
        box-shadow: 0px 10px 25px rgba(224, 82, 6, 0.1);
    }

    /* Badge de Precio */
    .price-tag {
        font-size: 1.25rem;
        font-weight: 700;
        color: #E05206;
        background: #FFF4EE;
        padding: 4px 12px;
        border-radius: 10px;
        display: inline-block;
        margin: 8px 0 12px 0;
    }

    /* Botón WhatsApp */
    .wa-button {
        display: block;
        width: 100%;
        background-color: #25D366;
        color: white !important;
        text-align: center;
        padding: 10px;
        border-radius: 12px;
        font-weight: 600;
        text-decoration: none;
        box-shadow: 0 4px 12px rgba(37, 211, 102, 0.2);
    }
    .wa-button:hover {
        background-color: #1EBE57;
        color: white !important;
    }

    /* Banner Tienda Online Directa */
    .direct-ship-banner {
        background: linear-gradient(135deg, #FF6B00 0%, #D84A00 100%);
        border-radius: 20px;
        padding: 25px;
        color: white;
        text-align: center;
        margin-bottom: 30px;
        box-shadow: 0 8px 20px rgba(216, 74, 0, 0.25);
    }

    .direct-ship-banner h3 {
        color: white !important;
        margin-bottom: 8px;
    }

    .btn-natura-official {
        display: inline-block;
        background-color: #FFFFFF;
        color: #D84A00 !important;
        font-weight: 700;
        padding: 12px 28px;
        border-radius: 30px;
        text-decoration: none;
        margin-top: 12px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.15);
    }
    .btn-natura-official:hover {
        background-color: #FFF0E6;
    }

    /* Sidebar personalizado */
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
URL_TIENDA_OFICIAL = "https://www.natura.com.co/consultoria/DCSS"

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
# MENÚ DE NAVEGACIÓN
# ---------------------------------------------------------
menu = st.sidebar.radio(
    "Navegación", 
    [
        "🌸 Catálogo Local", 
        "🚚 Envíos Directos (Tienda Oficial)", 
        "⚙️ Módulo de Administración"
    ]
)

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
# ENCABEZADO VISUAL ESTILO CIRCULAR BOTÁNICO
# ---------------------------------------------------------
st.markdown("""
<div class="header-container">
    <div class="botanical-circle">
        <div style="color: #FF6B00; font-size: 2rem; line-height: 1;">🍃</div>
        <div class="brand-logo-text">natura</div>
        <div class="brand-slogan">Bien estar bien</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# MÓDULO 1: CATÁLOGO LOCAL
# ---------------------------------------------------------
if menu == "🌸 Catálogo Local":

    # Banner promocional hacia la tienda con envío directo
    st.markdown(f"""
    <div class="direct-ship-banner">
        <h3>🚀 ¿Prefieres entrega directa a tu domicilio?</h3>
        <p>Haz tus compras en mi tienda digital Natura Colombia y recibe tu pedido en la puerta de tu casa a nivel nacional.</p>
        <a href="{URL_TIENDA_OFICIAL}" target="_blank" class="btn-natura-official">Comprar en Tienda Oficial con Envío Directo 🛒</a>
    </div>
    """, unsafe_allow_html=True)

    df_productos = obtener_productos()

    if not df_productos.empty:
        col_busqueda, col_filtro = st.columns([2, 1])
        with col_busqueda:
            busqueda = st.text_input("🔍 Buscar por nombre de producto...", "").strip().lower()
        with col_filtro:
            precio_max = float(df_productos["Precio"].max()) if not df_productos.empty else 100000.0
            precio_filtro = st.slider("Precio Máximo ($)", min_value=0, max_value=int(precio_max), value=int(precio_max), step=5000)

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

                    with st.container():
                        st.markdown('<div class="natura-card">', unsafe_allow_html=True)
                        
                        if url_imagen.startswith("http"):
                            st.image(url_imagen, use_column_width=True)
                        else:
                            st.markdown('<div style="width:100%; aspect-ratio:1/1; background-color:#F5F2ED; border-radius:12px; display:flex; align-items:center; justify-content:center; color:#A0988E; font-weight:500;">📷 Sin foto</div>', unsafe_allow_html=True)
                        
                        st.markdown(f"### {row['Nombre']}")
                        st.write(row['Descripción'])
                        st.markdown(f'<div class="price-tag">${precio_formateado}</div>', unsafe_allow_html=True)
                        
                        st.markdown(f'<a href="{link_wa}" target="_blank" class="wa-button">Pedir por WhatsApp 💬</a>', unsafe_allow_html=True)
                        st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.warning("No se encontraron productos con los criterios seleccionados.")
    else:
        st.info("El catálogo no tiene productos registrados actualmente.")

# ---------------------------------------------------------
# MÓDULO 2: ENVÍOS DIRECTOS (TIENDA OFICIAL NATURA)
# ---------------------------------------------------------
elif menu == "🚚 Envíos Directos (Tienda Oficial)":
    st.markdown("## 🚚 Envíos Directos a todo el País")
    st.write("Si deseas comprar directamente en la plataforma oficial de Natura Colombia para pagar con tarjeta de crédito, PSE o solicitar envío directo a tu ciudad, puedes hacerlo aquí:")

    st.markdown(f"""
    <div style="background-color:#FFFFFF; border-radius:18px; padding:30px; text-align:center; border:1px solid #EAE5DF; box-shadow: 0 4px 15px rgba(0,0,0,0.03);">
        <h3 style="color:#E05206;">🛍️ Mi Tienda Digital Natura Oficial</h3>
        <p style="color:#555;">Disfruta de promociones exclusivas del ciclo, cupones de descuento y entrega gestionada por Natura.</p>
        <a href="{URL_TIENDA_OFICIAL}" target="_blank" class="btn-natura-official" style="background:#FF6B00; color:white !important;">Abrir Mi Tienda Digital Natura ↗️</a>
    </div>
    """, unsafe_allow_html=True)
    
    st.divider()
    st.info("💡 **Consejo:** Para pedidos urgentes en stock o entregas personalizadas locales, puedes usar la sección **'Catálogo Local'** y hacer tu pedido por WhatsApp.")

# ---------------------------------------------------------
# MÓDULO 3: ADMINISTRACIÓN
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
                        with st.spinner("Guardando en Google Sheets..."):
                            guardar_producto(nombre_input, descripcion_input, precio_input, imagen_input)
                        st.success(f"¡Producto '{nombre_input}' publicado exitosamente!")
                    except Exception as e:
                        st.error("Error al actualizar la base de datos.")
                else:
                    st.warning("Completa los campos obligatorios.")
