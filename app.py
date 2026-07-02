import streamlit as st
import urllib.parse
from PIL import Image
import base64
import io

# 1. Configuración de la página
st.set_page_config(page_title="Natura Catálogo Interactivo", page_icon="🍃", layout="wide")

# Función para convertir imagen a base64 (necesario para el fondo de CSS)
def get_image_base64(img_obj):
    buffered = io.BytesIO()
    img_obj.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode()

# 2. Inicialización del estado
if 'catalogo' not in st.session_state:
    st.session_state.catalogo = []
if 'admin_logged_in' not in st.session_state: st.session_state.admin_logged_in = False
if 'edit_id' not in st.session_state: st.session_state.edit_id = None
if 'custom_logo' not in st.session_state: st.session_state.custom_logo = None
if 'custom_bg' not in st.session_state: st.session_state.custom_bg = None

# 3. CSS Dinámico
bg_css = ""
if st.session_state.custom_bg:
    bg_b64 = get_image_base64(st.session_state.custom_bg)
    bg_css = f"background-image: linear-gradient(rgba(247, 245, 240, 0.9), rgba(247, 245, 240, 0.9)), url('data:image/png;base64,{bg_b64}');"
else:
    bg_css = "background-color: #fcfbf7;"

st.markdown(f"""
<style>
    .stApp {{ {bg_css} background-size: cover; background-position: center; }}
    .header-box {{ background: linear-gradient(135deg, #3a5a40 0%, #588157 100%); padding: 30px; border-radius: 20px; text-align: center; color: white; margin-bottom: 30px; }}
    .product-card {{ background-color: rgba(255, 255, 255, 0.95); padding: 20px; border-radius: 15px; box-shadow: 0 4px 10px rgba(0,0,0,0.1); margin-bottom: 20px; border-left: 5px solid #3a5a40; }}
    .admin-section {{ background-color: #ffffff; padding: 20px; border-radius: 15px; border: 1px solid #ddd; margin-bottom: 20px; }}
</style>
""", unsafe_allow_html=True)

# Encabezado
if st.session_state.custom_logo:
    st.image(st.session_state.custom_logo, width=200)
else:
    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/d/d4/Natura_Logo.svg/200px-Natura_Logo.svg.png")

st.markdown('<div class="header-box"><h1>Natura Catálogo Interactivo</h1><p>Biodiversidad amazónica para el cuidado de tu cuerpo</p></div>', unsafe_allow_html=True)

# SIDEBAR
st.sidebar.header("⚙️ Configuración")
st.sidebar.write("👤 **Vendedora:** Deisy Sanabria")
telefono_vendedor = st.sidebar.text_input("WhatsApp", "573184704968")

tab_cliente, tab_admin = st.tabs(["🛒 Catálogo", "🔐 Administración"])

# --- MÓDULO ADMINISTRACIÓN ---
with tab_admin:
    if not st.session_state.admin_logged_in:
        with st.form("login"):
            if st.text_input("Usuario") == "DCSANABRIA" and st.text_input("Clave", type="password") == "1098665319*":
                if st.form_submit_button("Ingresar"):
                    st.session_state.admin_logged_in = True
                    st.rerun()
    else:
        if st.button("Cerrar Sesión"): st.session_state.admin_logged_in = False; st.rerun()
        
        st.subheader("🎨 Personalización Web")
        st.session_state.custom_logo = st.file_uploader("Logo de la web", type=["png", "jpg"], key="up_logo") or st.session_state.custom_logo
        st.session_state.custom_bg = st.file_uploader("Imagen de fondo", type=["png", "jpg"], key="up_bg") or st.session_state.custom_bg
        
        st.subheader("📦 Gestión de Productos")
        # Formulario Agregar/Editar
        with st.form("form_prod"):
            nombre = st.text_input("Nombre", value=st.session_state.catalogo[next((i for i,p in enumerate(st.session_state.catalogo) if p['id']==st.session_state.edit_id), 0)]['nombre'] if st.session_state.edit_id else "")
            precio = st.number_input("Precio", value=int(st.session_state.catalogo[next((i for i,p in enumerate(st.session_state.catalogo) if p['id']==st.session_state.edit_id), 0)]['precio']) if st.session_state.edit_id else 0)
            desc = st.text_area("Descripción", value=st.session_state.catalogo[next((i for i,p in enumerate(st.session_state.catalogo) if p['id']==st.session_state.edit_id), 0)]['descripcion'] if st.session_state.edit_id else "")
            foto = st.file_uploader("Foto del producto", type=["jpg", "png"])
            
            if st.form_submit_button("Guardar Producto"):
                if st.session_state.edit_id:
                    p = next(p for p in st.session_state.catalogo if p['id'] == st.session_state.edit_id)
                    p.update({'nombre': nombre, 'precio': precio, 'descripcion': desc})
                    if foto: p['imagen'] = Image.open(foto)
                    st.session_state.edit_id = None
                else:
                    st.session_state.catalogo.append({'id': len(st.session_state.catalogo)+1, 'nombre': nombre, 'precio': precio, 'descripcion': desc, 'imagen': Image.open(foto) if foto else None})
                st.rerun()

        for i, prod in enumerate(st.session_state.catalogo):
            c1, c2, c3 = st.columns([3, 1, 1])
            c1.write(f"{prod['nombre']} - ${prod['precio']:,}")
            if c2.button("✏️", key=f"e{prod['id']}"): st.session_state.edit_id = prod['id']; st.rerun()
            if c3.button("🗑️", key=f"d{prod['id']}"): st.session_state.catalogo.pop(i); st.rerun()

# --- VISTA CLIENTE ---
with tab_cliente:
    for prod in st.session_state.catalogo:
        st.markdown(f'<div class="product-card">', unsafe_allow_html=True)
        c1, c2 = st.columns([1, 2])
        if prod['imagen']: c1.image(prod['imagen'], use_container_width=True)
        c2.markdown(f"<h3>{prod['nombre']}</h3><p>{prod['descripcion']}</p><p class='price-tag'>${prod['precio']:,} COP</p>", unsafe_allow_html=True)
        link = f"https://wa.me/{telefono_vendedor}?text={urllib.parse.quote('Hola Deisy, me interesa: ' + prod['nombre'])}"
        c2.link_button("💬 Pedir por WhatsApp", link)
        st.markdown('</div>', unsafe_allow_html=True)
