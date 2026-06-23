import streamlit as st

# ── Configuración de página ──────────────────────────────────────────────────
st.set_page_config(
    page_title="GestiónApp",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Imports internos (después de set_page_config) ────────────────────────────
from login import mostrar_login
from menu import mostrar_menu
from modulos import inicio, clientes, productos, ventas

# ── Estado de sesión por defecto ─────────────────────────────────────────────
if "autenticado" not in st.session_state:
    st.session_state["autenticado"] = False

# ── Enrutamiento principal ────────────────────────────────────────────────────
if not st.session_state["autenticado"]:
    mostrar_login()
else:
    seccion = mostrar_menu()

    if seccion == "inicio":
        inicio.mostrar()
    elif seccion == "clientes":
        clientes.mostrar()
    elif seccion == "productos":
        productos.mostrar()
    elif seccion == "ventas":
        ventas.mostrar()