import streamlit as st
from config.conexion import get_connection


def verificar_login(username, password):
    conn = get_connection()
    if not conn:
        return None
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            "SELECT * FROM USUARIO WHERE username = %s AND password = %s AND activo = 1",
            (username, password),
        )
        usuario = cursor.fetchone()
        return usuario
    except Exception as e:
        st.error(f"Error al verificar credenciales: {e}")
        return None
    finally:
        conn.close()


def mostrar_login():
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown(
            """
            <div style='text-align:center; padding: 2rem 0 1rem;'>
                <h1 style='font-size:2.4rem; color:#1a73e8;'>🛒 GestiónApp</h1>
                <p style='color:#666; font-size:1rem;'>Sistema de gestión de clientes, productos y ventas</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        with st.form("form_login"):
            st.subheader("Iniciar sesión")
            username = st.text_input("Usuario", placeholder="Ingresa tu usuario")
            password = st.text_input(
                "Contraseña", type="password", placeholder="Ingresa tu contraseña"
            )
            submitted = st.form_submit_button("Entrar", use_container_width=True)
        if submitted:
            if not username or not password:
                st.warning("Por favor ingresa usuario y contraseña.")
            else:
                with st.spinner("Verificando credenciales..."):
                    usuario = verificar_login(username, password)
                if usuario:
                    st.session_state["autenticado"] = True
                    st.session_state["usuario"] = usuario
                    st.success(f"Bienvenido, {usuario['nombre_completo']}!")
                    st.rerun()
                else:
                    st.error("Usuario o contraseña incorrectos.")
        st.markdown(
            "<p style='text-align:center; color:#999; font-size:0.8rem; margin-top:1rem;'>"
            "Usuario de prueba: admin / admin123</p>",
            unsafe_allow_html=True,
        )