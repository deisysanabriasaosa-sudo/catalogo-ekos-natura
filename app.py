import streamlit as st
import urllib.parse
from PIL import Image

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

# Encabezado Principal
st.markdown('<div class="header-box"><h1>🌿 Natura EKOS - Catálogo Interactivo</h1><p>Biodiversidad amazónica para el cuidado de tu cuerpo</p></div>', unsafe_allow_html=True)

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
            producto_a_editar = next((p for p in st.session_state.catalogo if p["id"] == st.session_state.edit_id), None)
            
            if producto_a_editar:
                st.info(f"✏️ Estás editando: **{producto_a_editar['nombre']}**")
                
                with st.form("form_editar", clear_on_submit=True):
                    edit_nombre = st.text_input("Nombre del Producto:", value=producto_a_editar['nombre'])
                    edit_desc = st.text_area("Descripción del Producto:", value=producto_a_editar['descripcion'])
                    edit_precio = st.number_input("Precio de Venta ($ COP):", value=int(producto_a_editar['precio']), min_value=0, step=500)
                    st.caption("Si no deseas cambiar la foto actual, deja este espacio en blanco.")
                    edit_foto = st.file_uploader("Subir Nueva Foto (opcional):", type=["jpg", "jpeg", "png"])
                    
                    col_guardar, col_cancelar = st.columns(2)
                    btn_guardar_edicion = col_guardar.form_submit_button("Guardar Cambios")
                    btn_cancelar = col_cancelar.form_submit_button("Cancelar")
                    
                    if btn_guardar_edicion:
                        if edit_nombre and edit_precio > 0:
                            producto_a_editar['nombre'] = edit_nombre
                            producto_a_editar['descripcion'] = edit_desc
                            producto_a_editar['precio'] = edit_precio
                            if edit_foto is not None:
                                producto_a_editar['imagen'] = Image.open(edit_foto)
                            
                            st.session_state.edit_id = None
                            st.success("¡Producto actualizado exitosamente!")
                            st.rerun()
                        else:
                            st.error("Por favor ingresa un nombre válido y un precio mayor a 0.")
                            
                    if btn_cancelar:
                        st.session_state.edit_id = None
                        st.rerun()
        
        # Lógica de Creación
        else:
            with st.form("form_producto", clear_on_submit=True):
                st.markdown("#### Añadir Nuevo Producto")
                nuevo_nombre = st.text_input("Nombre del Producto:", placeholder="Ej. Manteca Corporal Ucuuba")
                nueva_desc = st.text_area("Descripción del Producto:", placeholder="Detalla los beneficios y el activo...")
                nuevo_precio = st.number_input("Precio de Venta ($ COP):", min_value=0, step=500)
                foto_perfil = st.file_uploader("Subir Foto del Producto:", type=["jpg", "jpeg", "png"])
                
                guardar = st.form_submit_button("Agregar al Catálogo")
                
                if guardar:
                    if nuevo_nombre and nuevo_precio > 0:
                        img_data = None
                        if foto_perfil is not None:
                            img_data = Image.open(foto_perfil)
                        
                        nuevo_id = max([p["id"] for p in st.session_state.catalogo], default=0) + 1
                        
                        nuevo_item = {
                            "id": nuevo_id,
                            "nombre": nuevo_nombre,
                            "descripcion": nueva_desc,
                            "precio": nuevo_precio,
                            "imagen": img_data
                        }
                        
                        st.session_state.catalogo.append(nuevo_item)
                        st.success(f"¡{nuevo_nombre} ha sido agregado exitosamente al catálogo!")
                        st.rerun()
                    else:
                        st.error("Por favor ingresa un nombre válido y un precio mayor a 0.")

        # Listado de Inventario
        if st.session_state.catalogo:
            st.divider()
            st.subheader("📦 Inventario Existente")
            for i, prod in enumerate(st.session_state.catalogo):
                col_info, col_edit, col_del = st.columns([3, 1, 1])
                
                col_info.write(f"**{prod['nombre']}** - ${prod['precio']:,} COP")
                
                if col_edit.button("✏️ Editar", key=f"edit_{prod['id']}"):
                    st.session_state.edit_id = prod['id']
                    st.rerun()
                    
                if col_del.button("🗑️ Eliminar", key=f"del_{prod['id']}"):
                    if st.session_state.edit_id == prod['id']:
                        st.session_state.edit_id = None
                        
                    st.session_state.catalogo.pop(i)
                    st.rerun()

# ==========================================
# 4. VISTA DEL CLIENTE (Pestaña Catálogo)
# ==========================================
with tab_cliente:
    if not st.session_state.catalogo:
        st.info("El catálogo está vacío actualmente. El administrador debe añadir productos.")
    else:
        for prod in st.session_state.catalogo:
            st.markdown('<div class="product-card">', unsafe_allow_html=True)
            
            col_img, col_detalles = st.columns([1, 2])
            
            with col_img:
                if prod["imagen"] is not None:
                    st.image(prod["imagen"], use_container_width=True)
                else:
                    st.image("https://images.unsplash.com/photo-1608248597481-496100c80836?q=80&w=300", caption="Imagen de referencia", use_container_width=True)
            
            with col_detalles:
                st.markdown(f"### {prod['nombre']}")
                st.write(prod["descripcion"])
                st.markdown(f'<p class="price-tag">${prod["precio"]:,} COP</p>', unsafe_allow_html=True)
                
                mensaje_comprobante = f"Hola Deisy, me interesa comprar el producto: *{prod['nombre']}* que vi en el catálogo, con un valor de *${prod['precio']:,} COP*. ¿Está disponible?"
                mensaje_codificado = urllib.parse.quote(mensaje_comprobante)
                enlace_wa = f"https://wa.me/{telefono_vendedor}?text={mensaje_codificado}"
                
                st.link_button("💬 Pedir por WhatsApp", enlace_wa, type="primary")
                
            st.markdown('</div>', unsafe_allow_html=True)
