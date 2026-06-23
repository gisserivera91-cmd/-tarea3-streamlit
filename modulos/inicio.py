import streamlit as st
from config.conexion import get_connection


def contar_tabla(tabla):
    conn = get_connection()
    if not conn:
        return 0
    try:
        cur = conn.cursor()
        cur.execute(f"SELECT COUNT(*) FROM {tabla}")
        return cur.fetchone()[0]
    except Exception:
        return 0
    finally:
        conn.close()


def mostrar():
    st.title("🏠 Panel de inicio")
    st.markdown("Resumen general del sistema.")

    c1, c2, c3 = st.columns(3)
    with c1:
        st.metric("👥 Clientes registrados", contar_tabla("CLIENTE"))
    with c2:
        st.metric("📦 Productos en catálogo", contar_tabla("PRODUCTO"))
    with c3:
        st.metric("💰 Ventas realizadas", contar_tabla("VENTA"))

    st.markdown("---")
    st.info(
        "Usa el menú lateral para navegar entre las secciones: "
        "**Clientes**, **Productos** y **Ventas**."
    )