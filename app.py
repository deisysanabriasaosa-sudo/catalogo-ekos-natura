import streamlit as st
import urllib.parse
from PIL import Image
import io

# 1. Configuración de la página y diseño estético natural
st.set_page_config(page_title="Catálogo Natura EKOS", page_icon="🌿", layout="wide")

# Estilos CSS personalizados
st.markdown("""
<style>
    .main {
        background-color: #f7f5f0;
    }
    .header-box {
        background-color: #3a5a40;
        padding: 30px;
        border-radius: 15px;
        text-align: center;
        color: white;
        margin-bottom: 25px;
    }
    .product-card {
        background-color: white;
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
        background-color: #e9edc9;
        padding: 20px;
        border-radius: 12px;
        margin-bottom: 30px;
    }
</style>
""", unsafe_allow_html=True)

# 2. Inicialización del estado de la sesión (Catálogo, Seguridad y Edición)
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

# Variable para saber si estamos editando un producto (guarda el ID)
if 'edit_id' not in st.session_state:
    st.session_state.edit_id = None

# Configuración del Teléfono del Vendedor y Nombre
st.sidebar.header("⚙️ Configuración del Canal")
st.sidebar.write("👤 **Vendedora:** Deisy Sanabria")
telefono_vendedor = st.sidebar.text_input("Número de WhatsApp (con código de país)", "573184704968")

# Encabezado Principal
st.markdown('<div class="header-box"><h1>🌿 Natura EKOS - Catálogo Interactivo</h1><p>Biodiversidad amazónica para el cuidado de tu cuerpo</p></div>', unsafe_allow_html=True)

# Creación de pestañas
tab_cliente, tab_admin = st.tabs(["🛒 Catálogo de Clientes", "🔐 Panel de Administración"])

# ==========================================
# 3. MÓDULO DE ADMINISTRACIÓN (Pestaña Admin)
# ==========================================
with tab_admin:
    # Verificación de inicio de sesión
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
    
    # Si las credenciales son correctas, mostramos el panel
    else:
        # Botón para cerrar sesión
        col_saludo, col_salir = st.columns([4, 1])
        col_saludo.success("¡Bienvenida, Deisy! Has iniciado sesión correctamente.")
        if col_salir.button("Cerrar Sesión"):
            st.session_state.admin_logged_in = False
            st.session_state.edit_id = None # Limpiamos si estaba editando algo
            st.rerun()

        st.markdown('<div class="admin-section"><h3>Gestión de Productos</h3></div>', unsafe_allow_html=True)
        
        # --- LÓGICA DE EDICIÓN O CREACIÓN ---
        if st.session_state.edit_id is not None:
            # Buscar el producto a editar
            producto_a_editar = next((p for p in st.session_state.catalogo if p["id"] == st.session_state.edit_id), None)
            
            if producto_a_editar:
                st.info(f"✏️ Estás editando: **{producto_a_editar['nombre']}**")
                
                with st.form("form_editar", clear_on_submit=True):
                    edit_nombre = st.text_input("Nombre del Producto:", value=producto_a_editar['nombre'])
                    edit_desc = st.text_area("Descripción del Producto:", value=producto_a_editar['descripcion'])
                    edit_precio = st.number_input("Precio
