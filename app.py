import streamlit as st
import urllib.parse
from PIL import Image

# 1. Configuración de página
st.set_page_config(page_title="Natura Catálogo Interactivo", page_icon="🍃", layout="wide")

# Inicialización del estado
if 'catalogo' not in st.session_state: st.session_state.catalogo = []
if 'admin_logged_in' not in st.session_state: st.session_state.admin_logged_in = False

# CSS
st.markdown("""
<style>
    .header-box { background: #3a5a40; padding: 30px; border-radius: 20px; text-align: center; color: white; margin-bottom: 30px; }
    .product-card { background-color: #ffffff; padding: 20px; border-radius: 15px; box-shadow: 0 4px 10px rgba(0,0,0,0.1); margin-bottom: 20px; border-left: 5px solid #3a5a40; }
</style>
""", unsafe_allow_html=True)

# Encabezado
st.markdown('<div class="header-box"><h1>Natura Catálogo Interactivo</h1><p>Biodiversidad amazónica para el cuidado de tu cuerpo</p></div>', unsafe_allow_html=True)

# Tabs
tab_cliente, tab_admin = st.tabs(["🛒 Catálogo", "🔐 Administración"])

# ADMIN
with tab_admin:
    if not st.session_state.admin_logged_in:
        st.subheader("Login de Administrador")
        usuario_input = st.text_input("Usuario")
        clave_input = st.text_input("Contraseña", type="password")
        if st.button("Ingresar"):
            # Verificación estricta
            if usuario_input.strip() == "DCSANABRIA" and clave_input.strip() == "1098665319*":
                st.session_state.admin_logged_in = True
                st.rerun()
            else:
                st.error("Credenciales incorrectas")
    else:
        if st.button("Cerrar Sesión"):
            st.session_state.admin_logged_in = False
            st.rerun()
            
        st.subheader("Gestión de Productos")
        
        # Formulario de agregar
        nombre = st.text_input("Nombre del producto")
        precio = st.number_input("Precio", min_value=0)
        desc = st.text_area("Descripción")
        foto = st.file_uploader("Subir foto", type=["jpg", "png"])
        
        if st.button("Guardar Producto"):
            if nombre:
                img = Image.open(foto) if foto else None
                st.session_state.catalogo.append({
                    'id': len(st.session_state.catalogo)+1, 
                    'nombre': nombre, 
                    'precio': precio, 
                    'descripcion': desc, 
                    'imagen': img
                })
                st.success("Producto agregado")
                st.rerun()
        
        st.divider()
        for i, prod in enumerate(st.session_state.catalogo):
            col1, col2 = st.columns([4, 1])
            col1.write(f"**{prod['nombre']}** - ${prod['precio']:,}")
            if col2.button("Eliminar", key=f"del_{i}"):
                st.session_state.catalogo.pop(i)
                st.rerun()

# CLIENTE
with tab_cliente:
    if not st.session_state.catalogo:
        st.info("No hay productos disponibles actualmente.")
    for prod in st.session_state.catalogo:
        st.markdown('<div class="product-card">', unsafe_allow_html=True)
        col1, col2 = st.columns([1, 3])
        if prod.get('imagen'): col1.image(prod['imagen'], use_container_width=True)
        col2.markdown(f"<h3>{prod['nombre']}</h3><p>{prod['descripcion']}</p><p><b>${prod['precio']:,} COP</b></p>", unsafe_allow_html=True)
        link = f"https://wa.me/573184704968?text={urllib.parse.quote('Hola Deisy, me interesa: ' + prod['nombre'])}"
        col2.link_button("💬 Pedir por WhatsApp", link)
        st.markdown('</div>', unsafe_allow_html=True)
