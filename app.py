import streamlit as st
import urllib.parse
from PIL import Image

# 1. Configuración de la página y diseño estético natural
st.set_page_config(page_title="Natura Catálogo Interactivo", page_icon="🌿", layout="wide")

# Estilos CSS personalizados
st.markdown("""
<style>
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
        {"id": 1, "nombre": "Pulpa Hidratante para Manos Castaña", "descripcion": "Nutrición intensa y antiresequedad.", "precio": 45000, "imagen": None},
        {"id": 2, "nombre": "Néctar Hidratante Corporal Maracuyá", "descripcion": "Acción antiestrés cutáneo.", "precio": 68000, "imagen": None}
    ]

if 'admin_logged_in' not in st.session_state:
    st.session_state.admin_logged_in = False

if 'edit_id' not in st.session_state:
    st.session_state.edit_id = None

# Configuración del Teléfono y Nombre
st.sidebar.header("⚙️ Configuración del Canal")
st.sidebar.write("👤 **Vendedora:** Deisy Sanabria")
telefono_vendedor = st.sidebar.text_input("Número de WhatsApp", "573184704968")

# Encabezado Principal
st.markdown('<div class="header-box"><h1>🌿 Natura Catálogo Interactivo</h1><p>Biodiversidad amazónica para el cuidado de tu cuerpo</p></div>', unsafe_allow_html=True)

tab_cliente, tab_admin = st.tabs(["🛒 Catálogo de Clientes", "🔐 Panel de Administración"])

# ==========================================
# 3. MÓDULO DE ADMINISTRACIÓN
# ==========================================
with tab_admin:
    if not st.session_state.admin_logged_in:
        st.markdown('<div class="admin-section"><h3>Acceso Restringido</h3></div>', unsafe_allow_html=True)
        with st.form("login_form"):
            usuario = st.text_input("Usuario")
            clave = st.text_input("Contraseña", type="password")
            if st.form_submit_button("Ingresar"):
                if usuario == "DCSANABRIA" and clave == "1098665319*":
                    st.session_state.admin_logged_in = True
                    st.rerun()
                else:
                    st.error("Credenciales incorrectas.")
    else:
        if st.button("Cerrar Sesión"):
            st.session_state.admin_logged_in = False
            st.session_state.edit_id = None
            st.rerun()

        st.markdown('<div class="admin-section"><h3>Gestión de Productos</h3></div>', unsafe_allow_html=True)
        
        # Lógica de Edición
        if st.session_state.edit_id is not None:
            producto_a_editar = next((p for p in st.session_state.catalogo if p["id"] == st.session_state.edit_id), None)
            
            if producto_a_editar:
                with st.form("form_editar"):
                    edit_nombre = st.text_input("Nombre:", value=producto_a_editar['nombre'])
                    edit_desc = st.text_area("Descripción:", value=producto_a_editar['descripcion'])
                    edit_precio = st.number_input("Precio:", value=int(producto_a_editar['precio']))
                    edit_foto = st.file_uploader("Nueva Foto (opcional):", type=["jpg", "png"])
                    
                    if st.form_submit_button("Guardar Cambios"):
                        producto_a_editar['nombre'] = edit_nombre
                        producto_a_editar['descripcion'] = edit_desc
                        producto_a_editar['precio'] = edit_precio
                        if edit_foto: producto_a_editar['imagen'] = Image.open(edit_foto)
                        st.session_state.edit_id = None
                        st.rerun()
        else:
            with st.form("form_nuevo"):
                nuevo_nombre = st.text_input("Nombre del Nuevo Producto")
                nuevo_precio = st.number_input("Precio", min_value=0)
                if st.form_submit_button("Agregar"):
                    nuevo_id = max([p["id"] for p in st.session_state.catalogo], default=0) + 1
                    st.session_state.catalogo.append({"id": nuevo_id, "nombre": nuevo_nombre, "descripcion": "", "precio": nuevo_precio, "imagen": None})
                    st.rerun()

        for i, prod in enumerate(st.session_state.catalogo):
            c1, c2, c3 = st.columns([3, 1, 1])
            c1.write(f"{prod['nombre']} - ${prod['precio']}")
            if c2.button("✏️", key=f"e{prod['id']}"):
                st.session_state.edit_id = prod['id']
                st.rerun()
            if c3.button("🗑️", key=f"d{prod['id']}"):
                st.session_state.catalogo.pop(i)
                st.rerun()

# ==========================================
# 4. VISTA DEL CLIENTE
# ==========================================
with tab_cliente:
    for prod in st.session_state.catalogo:
        st.markdown(f'<div class="product-card"><h3>{prod["nombre"]}</h3><p>{prod["descripcion"]}</p><p class="price-tag">${prod["precio"]:,} COP</p>', unsafe_allow_html=True)
        msg = f"Hola Deisy, me interesa el producto: {prod['nombre']}"
        st.link_button("💬 Pedir por WhatsApp", f"https://wa.me/{telefono_vendedor}?text={urllib.parse.quote(msg)}")
        st.markdown('</div>', unsafe_allow_html=True)
