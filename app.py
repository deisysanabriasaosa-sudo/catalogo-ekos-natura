import streamlit as st
import urllib.parse
from PIL import Image

# 1. Configuración de la página y diseño estético natural
st.set_page_config(page_title="Natura Catálogo Interactivo", page_icon="🌿", layout="wide")

# Estilos CSS personalizados (con logo de Natura de fondo como marca de agua)
st.markdown("""
<style>
    /* Fondo principal con el logo de Natura y un filtro para que no opaque el texto */
    .stApp {
        background-image: linear-gradient(rgba(247, 245, 240, 0.90), rgba(247, 245, 240, 0.90)), url("https://upload.wikimedia.org/wikipedia/commons/thumb/d/d4/Natura_Logo.svg/512px-Natura_Logo.svg.png");
        background-size: 400px;
        background-repeat: no-repeat;
        background-position: center;
        background-attachment: fixed;
    }
    .header-box {
        background-color: #3a5a40;
        padding: 30px;
        border-radius: 15px;
        text-align: center;
        color: white;
        margin-bottom: 25px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.1);
    }
    .product-card {
        background-color: rgba(255, 255, 255, 0.95);
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
        margin-bottom: 25px;
        border-top: 4px solid #a3b18a;
    }
    .price-tag {
        color: #b56576;
        font-size: 22px;
        font-weight: bold;
    }
    .admin-section {
        background-color: rgba(233, 237, 201, 0.95);
        padding: 20px;
        border-radius: 12px;
        margin-bottom: 30px;
    }
</style>
""", unsafe_allow_html=True)

# 2. Inicialización del estado de la sesión
if 'catalogo' not in st.session_state:
    st.session_state.catalogo = [
        {
            "id": 1,
            "nombre": "Pulpa Hidratante para Manos Castaña",
            "descripcion": "Nutrición intensa y antiresequedad para tus manos. Enriquecida con aceite bruto de castaña.",
            "precio": 45000,
            "imagen": None 
        },
        {
            "id": 2,
            "nombre": "Néctar Hidratante Corporal Maracuyá",
            "descripcion": "Acción antiestrés cutáneo que calma y reequilibra la piel. Textura ligera de rápida absorción.",
            "precio": 68000,
            "imagen": None
        }
    ]

if 'admin_logged_in' not in st.session_state:
    st.session_state.admin_logged_in = False

if 'edit_id' not in st.session_state:
    st.session_state.edit_id = None

# Configuración del Teléfono del Vendedor y Nombre
st.sidebar.header("⚙️ Configuración del Canal")
st.sidebar.write("👤 **Vendedora:** Deisy Sanabria")
telefono_vendedor = st.sidebar.text_input("Número de WhatsApp (con código de país)", "573184704968")

# Encabezado Principal Actualizado
st.markdown('<div class="header-box"><h1>🌿 Natura Catálogo Interactivo</h1><p>Biodiversidad amazónica para el cuidado de tu cuerpo</p></div>', unsafe_allow_html=True)

# Creación de pestañas
tab_cliente, tab_admin = st.tabs(["🛒 Catálogo de Clientes", "🔐 Panel de Administración"])

# ==========================================
# 3. MÓDULO DE ADMINISTRACIÓN (Pestaña Admin)
# ==========================================
with tab_admin:
    if not st.session_state.admin_logged_in:
        st.markdown('<div class="admin-section"><h3>Acceso Restringido</h3><p>Por favor, ingresa tus credenciales para administrar el catálogo.</p></div>', unsafe_allow_html=True)
        
        with st.form("login_form"):
            usuario = st.text_input("Usuario")
            clave = st.text_input("Contraseña", type="password")
            btn_login = st.form_submit_button("Ingresar")
            
            if btn_login:
                if usuario == "DCSANABRIA" and clave == "1098665319*":
                    st.session_state.admin_logged_in = True
                    st.rerun()
                else:
                    st.error("Usuario o contraseña incorrectos. Inténtalo de nuevo.")
    
    else:
        col_saludo, col_salir = st.columns([4, 1])
        col_saludo.success("¡Bienvenida, Deisy! Has iniciado sesión correctamente.")
        if col_salir.button("Cerrar Sesión"):
            st.session_state.admin_logged_in = False
            st.session_state.edit_id = None
            st.rerun()

        st.markdown('<div class="admin-section"><h3>Gestión de Productos</h3></div>', unsafe_allow_html=True)
        
        # Lógica de Edición
        if st.session_state.edit_id is not None:
            producto_a_editar = next((p for p in st.session_state.catalogo if p["id"] == st.session_state.edit_id), None
