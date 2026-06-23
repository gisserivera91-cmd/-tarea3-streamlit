import streamlit as st
import pandas as pd
from config.conexion import get_connection


def obtener_productos():
    conn = get_connection()
    if not conn:
        return pd.DataFrame()
    try:
        df = pd.read_sql(
            "SELECT id, nombre, descripcion, precio, stock, categoria FROM PRODUCTO ORDER BY id DESC",
            conn,
        )
        return df
    except Exception as e:
        st.error(f"Error al obtener productos: {e}")
        return pd.DataFrame()
    finally:
        conn.close()


def insertar_producto(nombre, descripcion, precio, stock, categoria):
    conn = get_connection()
    if not conn:
        return False
    try:
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO PRODUCTO (nombre, descripcion, precio, stock, categoria) VALUES (%s,%s,%s,%s,%s)",
            (nombre, descripcion, precio, stock, categoria),
        )
        conn.commit()
        return True
    except Exception as e:
        st.error(f"Error al insertar producto: {e}")
        return False
    finally:
        conn.close()


def actualizar_producto(id_, nombre, descripcion, precio, stock, categoria):
    conn = get_connection()
    if not conn:
        return False
    try:
        cur = conn.cursor()
        cur.execute(
            "UPDATE PRODUCTO SET nombre=%s, descripcion=%s, precio=%s, stock=%s, categoria=%s WHERE id=%s",
            (nombre, descripcion, precio, stock, categoria, id_),
        )
        conn.commit()
        return True
    except Exception as e:
        st.error(f"Error al actualizar producto: {e}")
        return False
    finally:
        conn.close()


def eliminar_producto(id_):
    conn = get_connection()
    if not conn:
        return False
    try:
        cur = conn.cursor()
        cur.execute("DELETE FROM PRODUCTO WHERE id=%s", (id_,))
        conn.commit()
        return True
    except Exception as e:
        st.error(f"Error al eliminar producto: {e}")
        return False
    finally:
        conn.close()


def mostrar():
    st.title("📦 Gestión de Productos")

    tab_ver, tab_nuevo, tab_editar, tab_eliminar = st.tabs(
        ["📋 Ver registros", "➕ Nuevo producto", "✏️ Editar", "🗑️ Eliminar"]
    )

    with tab_ver:
        df = obtener_productos()
        if df.empty:
            st.info("No hay productos registrados.")
        else:
            st.dataframe(df, use_container_width=True, hide_index=True)

    with tab_nuevo:
        st.subheader("Agregar nuevo producto")
        with st.form("form_nuevo_prod"):
            col1, col2 = st.columns(2)
            with col1:
                nombre = st.text_input("Nombre del producto *")
                precio = st.number_input("Precio ($) *", min_value=0.0, step=0.01, format="%.2f")
                categoria = st.text_input("Categoria")
            with col2:
                descripcion = st.text_area("Descripcion")
                stock = st.number_input("Stock *", min_value=0, step=1)
            submitted = st.form_submit_button("Guardar producto", use_container_width=True)
        if submitted:
            if not nombre:
                st.warning("El nombre del producto es obligatorio.")
            else:
                if insertar_producto(nombre, descripcion, precio, stock, categoria):
                    st.success("Producto agregado correctamente.")
                    st.rerun()

    with tab_editar:
        st.subheader("Editar producto existente")
        df_e = obtener_productos()
        if df_e.empty:
            st.info("No hay productos para editar.")
        else:
            opciones = {f"{r['id']} - {r['nombre']}": r for _, r in df_e.iterrows()}
            sel = st.selectbox("Selecciona un producto", list(opciones.keys()))
            reg = opciones[sel]
            with st.form("form_editar_prod"):
                col1, col2 = st.columns(2)
                with col1:
                    e_nom = st.text_input("Nombre", value=reg["nombre"])
                    e_precio = st.number_input("Precio", value=float(reg["precio"]), step=0.01, format="%.2f")
                    e_cat = st.text_input("Categoria", value=reg["categoria"] or "")
                with col2:
                    e_desc = st.text_area("Descripcion", value=reg["descripcion"] or "")
                    e_stock = st.number_input("Stock", value=int(reg["stock"]), step=1)
                submitted_e = st.form_submit_button("Actualizar", use_container_width=True)
            if submitted_e:
                if actualizar_producto(reg["id"], e_nom, e_desc, e_precio, e_stock, e_cat):
                    st.success("Producto actualizado.")
                    st.rerun()

    with tab_eliminar:
        st.subheader("Eliminar producto")
        df_d = obtener_productos()
        if df_d.empty:
            st.info("No hay productos para eliminar.")
        else:
            opciones_d = {f"{r['id']} - {r['nombre']}": r["id"] for _, r in df_d.iterrows()}
            sel_d = st.selectbox("Selecciona el producto a eliminar", list(opciones_d.keys()), key="del_prod")
            st.warning("Esta accion no se puede deshacer.")
            if st.button("Eliminar producto", type="primary"):
                if eliminar_producto(opciones_d[sel_d]):
                    st.success("Producto eliminado.")
                    st.rerun()