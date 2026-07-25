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
# ESTILOS CSS PERSONALIZADOS (ESTÉTICA BOTÁNICA NATURA)
# ---------------------------------------------------------
NATURA_CSS = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&family=Playfair+Display:ital,wght@1,500;1,600&display=swap');

    html, body, [class*="css"] {
        font-family: 'Poppins', sans-serif;
    }

    /* Fondo general natural con textura suave */
    .main {
        background: linear-gradient(135deg, #FAF6F0 0%, #F5EFE6 100%);
    }

    /* ENCABEZADO PRINCIPAL BOTÁNICO Y LLAMATIVO */
    .header-natura-banner {
        background: linear-gradient(135deg, #FF6B00 0%, #E05206 50%, #C03B00 100%);
        border-radius: 24px;
        padding: 40px 25px;
        color: #FFFFFF;
        text-align: center;
        box-shadow: 0px 12px 30px rgba(224, 82, 6, 0.25);
        margin-bottom: 30px;
        position: relative;
        overflow: hidden;
    }

    .header-natura-banner h1 {
        color: #FFFFFF !important;
        font-size: 2.2rem;
        font-weight: 700;
        margin-bottom: 10px;
        letter-spacing: -0.5px;
    }

    .header-natura-banner p.slogan-principal {
        font-family: 'Playfair Display', serif;
        font-style: italic;
        font-size: 1.3rem;
        opacity: 0.95;
        margin-bottom: 8px;
    }

    .header-natura-banner p.subtitulo {
        font-size: 0.95rem;
        opacity: 0.88;
        max-width: 750px;
        margin: 0 auto;
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
        background: linear-gradient(135deg, #2D5A27 0%, #1E3E1A 100%);
        border-radius: 20px;
        padding: 25px;
        color: white;
        text-align: center;
        margin-bottom: 30px;
        box-shadow: 0 8px 20px rgba(45, 90, 39, 0.2);
    }

    .direct-ship-banner h3 {
        color: white !important;
        margin-bottom: 8px;
    }

    .btn-natura-official {
        display: inline-block;
        background-color: #FF6B00;
        color: #FFFFFF !important;
        font-weight: 700;
        padding: 12px 28px;
        border-radius: 30px;
        text-decoration: none;
        margin-top: 12px;
        box-shadow: 0 4px 12px rgba(255, 107, 0, 0.3);
    }
    .btn-natura-official:hover {
        background-color: #E05206;
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

def actualizar_producto_en_indice(index_editar, nombre, descripcion, precio, imagen_url):
    conn = st.connection("gsheets", type=GSheetsConnection)
    df_actual = obtener_productos()
    
    if index_editar in df_actual.index:
        df_actual.at[index_editar, "Nombre"] = nombre
        df_actual.at[index_editar, "Descripción"] = descripcion
        df_actual.at[index_editar, "Precio"] = precio
        df_actual.at[index_editar, "Imagen"] = imagen_url
        
        conn.update(spreadsheet=URL_NATURA, worksheet=NOMBRE_HOJA, data=df_actual)
        st.cache_data.clear()
        return True
    return False

# ---------------------------------------------------------
# MENÚ DE NAVEGACIÓN
# ---------------------------------------------------------
menu = st.sidebar.radio(
    "Navegación", 
    [
        "⚡ Entrega Inmediata (Stock Local)", 
        "🌐 Productos desde mi tienda virtual Píde directamente aquí", 
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
# ENCABEZADO PRINCIPAL INSPIRADO EN NATURA
# ---------------------------------------------------------
st.markdown("""
<div class="header-natura-banner">
    <div style="font-size: 2.2rem; margin-bottom: 5px;">🍃🌸✨</div>
    <h1>Siente la Fuerza de la Naturaleza en tu Piel</h1>
    <p class="slogan-principal">"Bien estar bien: Armonía entre tu cuerpo, tu mente y el planeta"</p>
    <p class="subtitulo">Descubre la combinación perfecta de perfumería fina, activos de la biodiversidad brasileña y tratamiento cosmético avanzado.</p>
</div>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# MÓDULO 1: STOCK LOCAL / ENTREGA INMEDIATA
# ---------------------------------------------------------
if menu == "⚡ Entrega Inmediata (Stock Local)":

    st.markdown("## ⚡ Productos Disponibles para Entrega Inmediata")
    st.write("Aprovecha estos precios especiales y descuentos exclusivos en productos en stock listos para envío personal o entrega rápida por WhatsApp.")

    st.markdown(f"""
    <div class="direct-ship-banner">
        <h3>🛍️ ¿Buscas un producto que no ves en stock local?</h3>
        <p>Visita mi tienda virtual oficial para comprar directo a Natura con envío hasta la puerta de tu casa.</p>
        <a href="{URL_TIENDA_OFICIAL}" target="_blank" class="btn-natura-official">Ir a Tienda Virtual Natura ↗️</a>
    </div>
    """, unsafe_allow_html=True)

    df_productos = obtener_productos()

    if not df_productos.empty:
        col_busqueda, col_filtro = st.columns([2, 1])
        with col_busqueda:
            busqueda = st.text_input("🔍 Buscar en stock por nombre...", "").strip().lower()
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
                    mensaje = f"Hola Deisy, deseo adquirir para entrega inmediata el producto: *{row['Nombre']}* por ${precio_formateado}."
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
        st.info("El catálogo local se está actualizando.")

# ---------------------------------------------------------
# MÓDULO 2: PRODUCTOS DESDE MI TIENDA VIRTUAL
# ---------------------------------------------------------
elif menu == "🌐 Productos desde mi tienda virtual Píde directamente aquí":
    st.markdown("## 🌐 Productos desde mi tienda virtual Píde directamente aquí")
    st.write("Explora todo el portafolio completo de Natura Colombia. Realiza tu compra en línea de forma segura con tarjeta, PSE o pagos digitales y recibe el envío directo a cualquier ciudad.")

    st.markdown(f"""
    <div style="background-color:#FFFFFF; border-radius:20px; padding:35px; text-align:center; border:1px solid #EAE5DF; box-shadow: 0 4px 15px rgba(0,0,0,0.04);">
        <h3 style="color:#E05206; margin-bottom:10px;">✨ Comprar en Mi Portal Oficial Natura Colombia</h3>
        <p style="color:#555; max-width:600px; margin:0 auto 20px auto;">Accede a promociones del ciclo vigente, cupones de descuento especiales y garantía directa de fábrica Natura con entrega nacional.</p>
        <a href="{URL_TIENDA_OFICIAL}" target="_blank" class="btn-natura-official" style="font-size:1.1rem; padding:14px 32px;">Abrir Mi Tienda Virtual Natura 🛒</a>
    </div>
    """, unsafe_allow_html=True)

# ---------------------------------------------------------
# MÓDULO 3: ADMINISTRACIÓN CON EDICIÓN DE PRODUCTOS
# ---------------------------------------------------------
elif menu == "⚙️ Módulo de Administración":
    st.title("⚙️ Panel de Control Administrador")

    if "autenticado" not in st.session_state:
        st.session_state["autenticado"] = False

    if not st.session_state["autenticado"]:
        st.subheader("Acceso Restringido")
        with st.form("login_form"):
            usuario = st.text_input("Usuario")
            contrasena = st.text_input("Contraseña", type="password")
            btn_login = st.form_submit_button("Ingresar")
            
            if btn_login:
                if usuario == "1098665319" and contrasena == "2808DC":
                    st.session_state["autenticado"] = True
                    st.rerun()
                else:
                    st.error("Credenciales incorrectas. Verifica el usuario o la contraseña.")
    
    else:
        st.success("Sesión activa como Administradora.")
        if st.button("Cerrar Sesión"):
            st.session_state["autenticado"] = False
            st.rerun()
            
        st.divider()

        tab_lista, tab_agregar = st.tabs(["📋 Lista y Modificación de Productos", "➕ Agregar Nuevo Producto"])

        df_prod_admin = obtener_productos()

        # TAB 1: VER Y MODIFICAR PRODUCTOS
        with tab_lista:
            st.subheader("📦 Inventario de Productos Registrados")
            
            if not df_prod_admin.empty:
                # Muestra la tabla completa
                st.dataframe(
                    df_prod_admin.style.format({"Precio": "${:,.0f}"}), 
                    use_container_width=True
                )
                
                st.divider()
                st.subheader("✏️ Modificar o Editar un Producto Existente")
                
                opciones_prod = [f"{i} - {row['Nombre']}" for i, row in df_prod_admin.iterrows()]
                seleccion = st.selectbox("Selecciona el producto que deseas editar:", opciones_prod)

                if seleccion:
                    index_sel = int(seleccion.split(" - ")[0])
                    prod_sel = df_prod_admin.loc[index_sel]

                    with st.form("form_editar_producto"):
                        st.write(f"**Modificando:** {prod_sel['Nombre']}")
                        mod_nombre = st.text_input("Nombre del Producto", value=prod_sel['Nombre'])
                        mod_desc = st.text_area("Descripción", value=prod_sel['Descripción'])
                        mod_precio = st.number_input("Precio ($)", min_value=0, value=int(prod_sel['Precio']), step=1000)
                        mod_imagen = st.text_input("URL Imagen", value=prod_sel['Imagen'])

                        btn_guardar_edit = st.form_submit_button("💾 Guardar Cambios en Google Sheets")

                        if btn_guardar_edit:
                            with st.spinner("Actualizando en la base de datos..."):
                                exito = actualizar_producto_en_indice(
                                    index_sel, mod_nombre, mod_desc, mod_precio, mod_imagen
                                )
                            if exito:
                                st.success("¡Producto modificado con éxito!")
                                st.rerun()
                            else:
                                st.error("No se pudo actualizar el producto.")
            else:
                st.info("No hay productos cargados en la hoja de cálculo.")

        # TAB 2: AGREGAR NUEVO PRODUCTO
        with tab_agregar:
            st.subheader("➕ Agregar Nuevo Producto al Stock Local")
            
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
                            st.rerun()
                        except Exception as e:
                            st.error("Error al actualizar la base de datos.")
                    else:
                        st.warning("Completa los campos obligatorios.")
