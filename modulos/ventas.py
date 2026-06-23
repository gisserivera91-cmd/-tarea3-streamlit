import streamlit as st
import pandas as pd
from config.conexion import get_connection


def obtener_ventas():
    conn = get_connection()
    if not conn:
        return pd.DataFrame()
    try:
        query = """
            SELECT v.id,
                   CONCAT(c.nombre, ' ', c.apellido) AS cliente,
                   p.nombre AS producto,
                   v.cantidad,
                   v.precio_unitario,
                   v.total,
                   v.fecha
            FROM VENTA v
            JOIN CLIENTE c ON v.cliente_id = c.id
            JOIN PRODUCTO p ON v.producto_id = p.id
            ORDER BY v.fecha DESC
        """
        df = pd.read_sql(query, conn)
        return df
    except Exception as e:
        st.error(f"Error al obtener ventas: {e}")
        return pd.DataFrame()
    finally:
        conn.close()


def obtener_pares(tabla, col_id, col_nombre):
    conn = get_connection()
    if not conn:
        return {}
    try:
        cur = conn.cursor()
        cur.execute(f"SELECT {col_id}, {col_nombre} FROM {tabla}")
        return {row[1]: row[0] for row in cur.fetchall()}
    except Exception:
        return {}
    finally:
        conn.close()


def insertar_venta(cliente_id, producto_id, cantidad, precio_unitario):
    conn = get_connection()
    if not conn:
        return False
    try:
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO VENTA (cliente_id, producto_id, cantidad, precio_unitario) VALUES (%s,%s,%s,%s)",
            (cliente_id, producto_id, cantidad, precio_unitario),
        )
        conn.commit()
        return True
    except Exception as e:
        st.error(f"Error al registrar venta: {e}")
        return False
    finally:
        conn.close()


def eliminar_venta(id_):
    conn = get_connection()
    if not conn:
        return False
    try:
        cur = conn.cursor()
        cur.execute("DELETE FROM VENTA WHERE id=%s", (id_,))
        conn.commit()
        return True
    except Exception as e:
        st.error(f"Error al eliminar venta: {e}")
        return False
    finally:
        conn.close()


def mostrar():
    st.title("💰 Gestión de Ventas")

    tab_ver, tab_nuevo, tab_eliminar = st.tabs(
        ["📋 Ver registros", "➕ Nueva venta", "🗑️ Eliminar"]
    )

    with tab_ver:
        df = obtener_ventas()
        if df.empty:
            st.info("No hay ventas registradas.")
        else:
            total_general = df["total"].sum() if "total" in df.columns else 0
            st.metric("Total ventas acumulado", f"${total_general:,.2f}")
            st.dataframe(df, use_container_width=True, hide_index=True)

    with tab_nuevo:
        st.subheader("Registrar nueva venta")
        clientes = obtener_pares("CLIENTE", "id", "CONCAT(nombre,' ',apellido)")
        productos = obtener_pares("PRODUCTO", "id", "nombre")

        if not clientes or not productos:
            st.warning("Necesitas tener al menos un cliente y un producto registrado.")
        else:
            with st.form("form_nueva_venta"):
                col1, col2 = st.columns(2)
                with col1:
                    sel_cli = st.selectbox("Cliente *", list(clientes.keys()))
                    cantidad = st.number_input("Cantidad *", min_value=1, step=1, value=1)
                with col2:
                    sel_prod = st.selectbox("Producto *", list(productos.keys()))
                    precio = st.number_input("Precio unitario ($) *", min_value=0.0, step=0.01, format="%.2f")
                st.info(f"Total estimado: ${cantidad * precio:,.2f}")
                submitted = st.form_submit_button("Registrar venta", use_container_width=True)
            if submitted:
                if precio <= 0:
                    st.warning("El precio unitario debe ser mayor a 0.")
                else:
                    if insertar_venta(clientes[sel_cli], productos[sel_prod], cantidad, precio):
                        st.success("Venta registrada correctamente.")
                        st.rerun()

    with tab_eliminar:
        st.subheader("Eliminar venta")
        df_d = obtener_ventas()
        if df_d.empty:
            st.info("No hay ventas para eliminar.")
        else:
            opciones_d = {
                f"#{r['id']} - {r['cliente']} | {r['producto']} | ${r['total']}": r["id"]
                for _, r in df_d.iterrows()
            }
            sel_d = st.selectbox("Selecciona la venta a eliminar", list(opciones_d.keys()), key="del_venta")
            st.warning("Esta accion no se puede deshacer.")
            if st.button("Eliminar venta", type="primary"):
                if eliminar_venta(opciones_d[sel_d]):
                    st.success("Venta eliminada.")
                    st.rerun()