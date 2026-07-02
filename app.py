import streamlit as st
import urllib.parse
import pandas as pd
import os
from PIL import Image

# 1. Configuración de página
st.set_page_config(page_title="Natura Catálogo Interactivo", page_icon="🍃", layout="wide")

# ARCHIVO DE PERSISTENCIA
DATA_FILE = "catalogo.csv"

def cargar_datos():
    if os.path.exists(DATA_FILE):
        return pd.read_csv(DATA_FILE).to_dict('records')
    return []

def guardar_datos(lista):
    pd.DataFrame(lista).to_csv(DATA_FILE, index=False)

# Inicialización
if 'catalogo' not in st.session_state: st.session_state.catalogo = cargar_datos()
if 'admin_logged_in' not in st.session_state: st.session_state.admin_logged_in = False
if 'edit_index' not in st.session_state: st.session_state.edit_index = None

# CSS
st.markdown("""
<style>
    .header-box { background: #3a5a40; padding: 30px; border-radius: 20px; text-align: center; color: white; margin-bottom: 30px; }
    .product-card { background-color: #ffffff; padding: 20px; border-radius: 15px; box-shadow: 0 4px 10px rgba(0,0,0,0.1); margin-bottom: 20px; border-left: 5px solid #3a5a40; }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="header-box"><h1>Natura Catálogo Interactivo</h1><p>Biodiversidad amazónica para el cuidado de tu cuerpo</p></div>', unsafe_allow_html=True)

tab_cliente, tab_admin = st.tabs(["🛒 Catálogo", "🔐 Administración"])

with tab_admin:
    if not st.session_state.admin_logged_in:
        usuario = st.text_input("Usuario")
        clave = st.text_input("Contraseña", type="password")
        if st.button("Ingresar"):
            if usuario.strip() == "DCSANABRIA" and clave.strip() == "1098665319*":
                st.session_state.admin_logged_in = True
                st.rerun()
    else:
        if st.button("Cerrar Sesión"):
            st.session_state.admin_logged_in = False
            st.rerun()
            
        st.subheader("Gestión de Productos")
        prod_a_editar = st.session_state.catalogo[st.session_state.edit_index] if st.session_state.edit_index is not None else None
        
        nombre = st.text_input("Nombre", value=prod_a_editar['nombre'] if prod_a_editar else "")
        precio = st.number_input("Precio", value=int(prod_a_editar['precio']) if prod_a_editar else 0)
        desc = st.text_area("Descripción", value=prod_a_editar['descripcion'] if prod_a_editar else "")
        
        if st.button("Guardar Producto"):
            if nombre:
                nuevo_prod = {'id': prod_a_editar['id'] if prod_a_editar else len(st.session_state.catalogo)+1, 'nombre': nombre, 'precio': precio, 'descripcion': desc}
                if st.session_state.edit_index is not None:
                    st.session_state.catalogo[st.session_state.edit_index] = nuevo_prod
                else:
                    st.session_state.catalogo.append(nuevo_prod)
                guardar_datos(st.session_state.catalogo)
                st.session_state.edit_index = None
                st.rerun()
        
        for i, prod in enumerate(st.session_state.catalogo):
            col1, col2, col3 = st.columns([3, 1, 1])
            col1.write(f"**{prod['nombre']}** - ${prod['precio']:,}")
            if col2.button("✏️", key=f"e{i}"): st.session_state.edit_index = i; st.rerun()
            if col3.button("🗑️", key=f"d{i}"): st.session_state.catalogo.pop(i); guardar_datos(st.session_state.catalogo); st.rerun()

with tab_cliente:
    for prod in st.session_state.catalogo:
        st.markdown('<div class="product-card">', unsafe_allow_html=True)
        st.markdown(f"<h3>{prod['nombre']}</h3><p>{prod['descripcion']}</p><p><b>${prod['precio']:,} COP</b></p>", unsafe_allow_html=True)
        link = f"https://wa.me/573184704968?text={urllib.parse.quote('Hola Deisy, me interesa: ' + prod['nombre'])}"
        st.link_button("💬 Pedir por WhatsApp", link)
        st.markdown('</div>', unsafe_allow_html=True)
