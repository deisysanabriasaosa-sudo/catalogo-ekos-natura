import streamlit as st
import urllib.parse
from PIL import Image
import base64
import io

# 1. Configuración de la página
st.set_page_config(page_title="Natura Catálogo Interactivo", page_icon="🍃", layout="wide")

# Función para convertir imagen a base64
def get_image_base64(img_obj):
    buffered = io.BytesIO()
    img_obj.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode()

# 2. Inicialización del estado
if 'catalogo' not in st.session_state: st.session_state.catalogo = []
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
</style>
""", unsafe_allow_html=True)

# Encabezado
if st.session_state.custom_logo: st.image(st.session_state.custom_logo, width=200)
else: st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/d/d4/Natura_Logo.svg/200px-Natura_Logo.svg.png")

st.markdown('<div class="header-box"><h1>Natura Catálogo Interactivo</h1><p>Biodiversidad amazónica para el cuidado de tu cuerpo</p></div>', unsafe_allow_html=True)

# SIDEBAR
telefono_vendedor = st.sidebar.text_input("WhatsApp de Deisy", "573184704968")

tab_cliente, tab_admin = st.tabs(["🛒 Catálogo", "🔐 Administración"])

with tab_admin:
    if not st.session_state.admin_logged_in:
        with st.form("login"):
            if st.text_input("Usuario") == "DCSANABRIA" and st.text_input("Clave", type="password") == "1098665319*":
                if st.form_submit_button("Ingresar"): st.session_state.admin_logged_in = True; st.rerun()
    else:
        if st.button("Cerrar Sesión"): st.session_state.admin_logged_in = False; st.rerun()
        
        st.subheader("🎨 Personalización")
        st.session_state.custom_logo = st.file_uploader("Logo web", type=["png", "jpg"], key="up_logo") or st.session_state.custom_logo
        st.session_state.custom_bg = st.file_uploader("Fondo web", type=["png", "jpg"], key="up_bg") or st.session_state.custom_bg
        
        st.subheader("📦 Gestión de Productos")
        
        # Lógica de edición/creación
        prod_edit = next((p for p in st.session_state.catalogo if p['id'] == st.session_state.edit_id), None)
        
        with st.form("form_prod", clear_on_submit=True):
            nombre = st.text_input("Nombre", value=prod_edit['nombre'] if prod_edit else "")
            precio = st.number_input("Precio", value=int(prod_edit['precio']) if prod_edit else 0)
            desc = st.text_area("Descripción", value=prod_edit['descripcion'] if prod_edit else "")
            foto = st.file_uploader("Foto", type=["jpg", "png"])
            
            submit = st.form_submit_button("Guardar Producto")
            if submit:
                if prod_edit:
                    prod_edit.update({'nombre': nombre, 'precio': precio, 'descripcion': desc})
                    if foto: prod_edit['imagen'] = Image.open(foto)
                    st.session_state.edit_id = None
                else:
                    st.session_state.catalogo.append({'id': len(st.session_state.catalogo)+1, 'nombre': nombre, 'precio': precio, 'descripcion': desc, 'imagen': Image.open(foto) if foto else None})
                st.rerun()

        for i, prod in enumerate(st.session_state.catalogo):
            c1, c2, c3 = st.columns([3, 1, 1])
            c1.write(f"**{prod['nombre']}** (${prod['precio']:,})")
            if c2.button("✏️", key=f"e{prod['id']}"): st.session_state.edit_id = prod['id']; st.rerun()
            if c3.button("🗑️", key=f"d{prod['id']}"): st.session_state.catalogo.pop(i); st.rerun()

with tab_cliente:
    for prod in st.session_state.catalogo:
        st.markdown('<div class="product-card">', unsafe_allow_html=True)
        c1, c2 = st.columns([1, 2])
        if prod['imagen']: c1.image(prod['imagen'], use_container_width=True)
        c2.markdown(f"<h3>{prod['nombre']}</h3><p>{prod['descripcion']}</p><p><b>${prod['precio']:,} COP</b></p>", unsafe_allow_html=True)
        link = f"https://wa.me/{telefono_vendedor}?text={urllib.parse.quote('Hola Deisy, me interesa: ' + prod['nombre'])}"
        c2.link_button("💬 Pedir por WhatsApp", link)
        st.markdown('</div>', unsafe_allow_html=True)
