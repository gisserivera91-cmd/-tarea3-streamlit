import streamlit as st


SECCIONES = {
    "🏠 Inicio": "inicio",
    "👥 Clientes": "clientes",
    "📦 Productos": "productos",
    "💰 Ventas": "ventas",
}


def mostrar_menu():
    usuario = st.session_state.get("usuario", {})
    nombre = usuario.get("nombre_completo", "Usuario")

    with st.sidebar:
        st.markdown(
            f"""
            <div style='padding:1rem 0 0.5rem;'>
                <p style='margin:0; font-size:0.75rem; color:#888;'>Sesión activa</p>
                <p style='margin:0; font-size:1rem; font-weight:600; color:#1a73e8;'>👤 {nombre}</p>
            </div>
            <hr style='margin: 0.75rem 0; border-color:#e0e0e0;'>
            """,
            unsafe_allow_html=True,
        )

        st.markdown("**Navegación**")
        seleccion = st.radio(
            label="Secciones",
            options=list(SECCIONES.keys()),
            label_visibility="collapsed",
        )

        st.markdown("<hr style='border-color:#e0e0e0;'>", unsafe_allow_html=True)
        if st.button("🚪 Cerrar sesión", use_container_width=True):
            st.session_state.clear()
            st.rerun()

    return SECCIONES[seleccion]