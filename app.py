import streamlit as st
import urllib.parse
from PIL import Image

# 1. Configuración de la página
st.set_page_config(page_title="Natura Catálogo Interactivo", page_icon="🍃", layout="wide")

# 2. Estilos CSS con identidad Natura
st.markdown("""
<style>
    /* Fondo inspirado en texturas botánicas y colores de la marca */
    .stApp {
        background-color: #fcfbf7;
        background-image: radial-gradient(#d4d9c7 0.5px, transparent 0.5px);
        background-size: 20px 20px;
    }
    .header-box {
        background: linear-gradient(135deg, #3a5a40 0%, #588157 100%);
        padding: 40px;
        border-radius: 20px;
        text-align: center;
        color: white;
        margin-bottom: 30px;
        box-shadow: 0 10px 20px rgba(0,0,0,0.15);
    }
    .logo-container {
        text-align: center;
        margin-bottom: 20px;
    }
    .product-card {
        background-color: white;
        padding: 25px;
        border-radius: 20px;
        box-shadow: 0 8px 20px rgba(0,0,0,0.08);
        margin-bottom: 25px;
        border: 1px solid #e0e0e0;
    }
    .price-tag {
        color: #8a5a44;
        font-size: 24px;
        font-weight: 800;
        margin: 10px 0;
    }
    .admin-section {
        background-color: #ffffff;
        padding: 25px;
        border-radius: 20px;
        border-left: 5px solid #3a5a40;
        box-shadow: 0 4px 10px rgba(0,0,0,0.05);
        margin-bottom: 30px;
    }
</style>
""", unsafe_allow_html=True)

# 3. Estado de la sesión
if 'catalogo' not in st.session_state:
    st.session_state.catalogo = [
        {"id": 1, "nombre": "Pulpa Hidratante para Manos Castaña", "descripcion": "Nutrición intensa con aceite bruto de castaña.", "precio": 45000, "imagen": None},
        {"id": 2, "nombre": "Néctar Hidratante Corporal Maracuyá", "descripcion": "Acción antiestrés cutáneo y reequilibrio.", "precio": 68000, "imagen": None}
    ]
if 'admin_logged_in' not in st.session_state: st.session_state.admin_logged_in = False
if 'edit_id' not in st.session_state: st.session_state.edit_id = None

# Encabezado
st.markdown('<div class="logo-container"><img src="https://upload.wikimedia.org/wikipedia/commons/thumb/d/d4/Natura_Logo.svg/200px-Natura_Logo.svg.png"></div>', unsafe_allow_html=True)
st.markdown('<div class="header-box"><h1>Natura Catálogo Interactivo</h1><p>Biodiversidad amazónica para el cuidado de tu cuerpo</p></div>', unsafe_allow_html=True)

tab_cliente, tab_admin = st.tabs(["🛒 Catálogo de Clientes", "🔐 Panel de Administración"])

# Módulo Administración
with tab_admin:
    if not st.session_state.admin_logged_in:
        with st.form("login_form"):
            usuario = st.text_input("Usuario")
            clave = st.text_input("Contraseña", type="password")
            if st.form_submit_button("Ingresar"):
                if usuario == "DCSANABRIA" and clave == "1098665319*":
                    st.session_state.admin_logged_in = True
                    st.rerun()
    else:
        if st.button("Cerrar Sesión"):
            st.session_state.admin_logged_in = False
            st.rerun()
        
        st.markdown('<div class="admin-section"><h3>Gestión de Productos</h3></div>', unsafe_allow_html=True)
        
        # Edición
        if st.session_state.edit_id is not None:
            prod_ed = next((p for p in st.session_state.catalogo if p["id"] == st.session_state.edit_id), None)
            with st.form("edit_form"):
                n = st.text_input("Nombre", value=prod_ed['nombre'])
                p = st.number_input("Precio", value=int(prod_ed['precio']))
                if st.form_submit_button("Guardar"):
                    prod_ed['nombre'] = n
                    prod_ed['precio'] = p
                    st.session_state.edit_id = None
                    st.rerun()
        
        # Inventario
        for i, prod in enumerate(st.session_state.catalogo):
            c1, c2, c3 = st.columns([4, 1, 1])
            c1.write(f"**{prod['nombre']}** - ${prod['precio']:,} COP")
            if c2.button("✏️", key=f"e{prod['id']}"):
                st.session_state.edit_id = prod['id']
                st.rerun()
            if c3.button("🗑️", key=f"d{prod['id']}"):
                st.session_state.catalogo.pop(i)
                st.rerun()

# Vista Cliente
with tab_cliente:
    for prod in st.session_state.catalogo:
        st.markdown(f'<div class="product-card"><h3>{prod["nombre"]}</h3><p>{prod["descripcion"]}</p><p class="price-tag">${prod["precio"]:,} COP</p>', unsafe_allow_html=True)
        link = f"https://wa.me/573184704968?text={urllib.parse.quote('Hola Deisy, me interesa: ' + prod['nombre'])}"
        st.link_button("💬 Pedir por WhatsApp", link)
        st.markdown('</div>', unsafe_allow_html=True)
