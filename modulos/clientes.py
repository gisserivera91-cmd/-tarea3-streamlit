import streamlit as st
import pandas as pd
from config.conexion import get_connection


def obtener_clientes():
    conn = get_connection()
    if not conn:
        return pd.DataFrame()
    try:
        df = pd.read_sql("SELECT id, nombre, apellido, email, telefono, direccion FROM CLIENTE ORDER BY id DESC", conn)
        return df
    except Exception as e:
        st.error(f"Error al obtener clientes: {e}")
        return pd.DataFrame()
    finally:
        conn.close()


def insertar_cliente(nombre, apellido, email, telefono, direccion):
    conn = get_connection()
    if not conn:
        return False
    try:
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO CLIENTE (nombre, apellido, email, telefono, direccion) VALUES (%s,%s,%s,%s,%s)",
            (nombre, apellido, email, telefono, direccion),
        )
        conn.commit()
        return True
    except Exception as e:
        st.error(f"Error al insertar cliente: {e}")
        return False
    finally:
        conn.close()


def actualizar_cliente(id_, nombre, apellido, email, telefono, direccion):
    conn = get_connection()
    if not conn:
        return False
    try:
        cur = conn.cursor()
        cur.execute(
            "UPDATE CLIENTE SET nombre=%s, apellido=%s, email=%s, telefono=%s, direccion=%s WHERE id=%s",
            (nombre, apellido, email, telefono, direccion, id_),
        )
        conn.commit()
        return True
    except Exception as e:
        st.error(f"Error al actualizar cliente: {e}")
        return False
    finally:
        conn.close()


def eliminar_cliente(id_):
    conn = get_connection()
    if not conn:
        return False
    try:
        cur = conn.cursor()
        cur.execute("DELETE FROM CLIENTE WHERE id=%s", (id_,))
        conn.commit()
        return True
    except Exception as e:
        st.error(f"Error al eliminar cliente: {e}")
        return False
    finally:
        conn.close()


def mostrar():
    st.title("👥 Gestión de Clientes")

    tab_ver, tab_nuevo, tab_editar, tab_eliminar = st.tabs(
        ["📋 Ver registros", "➕ Nuevo cliente", "✏️ Editar", "🗑️ Eliminar"]
    )

    with tab_ver:
        df = obtener_clientes()
        if df.empty:
            st.info("No hay clientes registrados aún.")
        else:
            st.dataframe(df, use_container_width=True, hide_index=True)

    with tab_nuevo:
        st.subheader("Agregar nuevo cliente")
        with st.form("form_nuevo_cliente"):
            col1, col2 = st.columns(2)
            with col1:
                nombre = st.text_input("Nombre *")
                email = st.text_input("Correo electrónico")
                direccion = st.text_area("Dirección")
            with col2:
                apellido = st.text_input("Apellido *")
                telefono = st.text_input("Teléfono")
            submitted = st.form_submit_button("Guardar cliente", use_container_width=True)
        if submitted:
            if not nombre or not apellido:
                st.warning("Nombre y apellido son obligatorios.")
            else:
                if insertar_cliente(nombre, apellido, email, telefono, direccion):
                    st.success("Cliente agregado correctamente.")
                    st.rerun()

    with tab_editar:
        st.subheader("Editar cliente existente")
        df_edit = obtener_clientes()
        if df_edit.empty:
            st.info("No hay clientes para editar.")
        else:
            opciones = {f"{r['id']} - {r['nombre']} {r['apellido']}": r for _, r in df_edit.iterrows()}
            sel = st.selectbox("Selecciona un cliente", list(opciones.keys()))
            reg = opciones[sel]
            with st.form("form_editar_cliente"):
                col1, col2 = st.columns(2)
                with col1:
                    e_nombre = st.text_input("Nombre", value=reg["nombre"])
                    e_email = st.text_input("Email", value=reg["email"] or "")
                    e_dir = st.text_area("Direccion", value=reg["direccion"] or "")
                with col2:
                    e_apellido = st.text_input("Apellido", value=reg["apellido"])
                    e_tel = st.text_input("Telefono", value=reg["telefono"] or "")
                submitted_e = st.form_submit_button("Actualizar", use_container_width=True)
            if submitted_e:
                if actualizar_cliente(reg["id"], e_nombre, e_apellido, e_email, e_tel, e_dir):
                    st.success("Cliente actualizado.")
                    st.rerun()

    with tab_eliminar:
        st.subheader("Eliminar cliente")
        df_del = obtener_clientes()
        if df_del.empty:
            st.info("No hay clientes para eliminar.")
        else:
            opciones_d = {f"{r['id']} - {r['nombre']} {r['apellido']}": r["id"] for _, r in df_del.iterrows()}
            sel_d = st.selectbox("Selecciona el cliente a eliminar", list(opciones_d.keys()), key="del_cli")
            st.warning("Esta accion no se puede deshacer.")
            if st.button("Eliminar cliente", type="primary"):
                if eliminar_cliente(opciones_d[sel_d]):
                    st.success("Cliente eliminado.")
                    st.rerun()