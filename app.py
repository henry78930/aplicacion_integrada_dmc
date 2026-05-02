"""
Aplicación Streamlit — Proyecto Python Fundamentals (DMC).
Autor: Henry Alex Enciso Gomez

Secciones: 
- Home
- Ejercicio 1 (flujo de caja)
- Ejercicio 2 (NumPy + DataFrame)
- Ejercicio 3 (funciones externas) 
- Ejercicio 4 (clases externas + CRUD)

"""
import numpy as np          # arrays y cálculos
import pandas as pd         # tablas y registros
import streamlit as st      # construir la app
import altair as alt        # gráficos más visuales

import importlib.util       # cargar archivos externos
import inspect              # leer parámetros automáticamente
import sys                  # control del entorno Python

from pathlib import Path    # rutas de carpetas/archivos
from typing import Optional # Puede devolver un valor o un none

# ---------------------------------------------------------------------------
# 1.0 CONFIGURACION GENERAL - Datos del Alumno
# ---------------------------------------------------------------------------
NOMBRE_ESTUDIANTE = "HENRY ALEX ENCISO GOMEZ"
NOMBRE_MODULO = "Python Fundamentals"
ANIO = 2026
TITULO_PROYECTO = "Aplicación integrada: flujo de caja, datos y librería de cálculos"

# PASO 1.1: Encontrando ruta donde está este archivo "app.py"

# Path(__file__) --> Encuentra Ruta Relativa (app.py)
# .resolve() --> Encuentra Ruta Absoluta (C:/Users/Henry/proyecto/app.py)
# .parent --> Bajo un nivel (C:/Users/Henry/proyecto)
BASE_DIR = Path(__file__).resolve().parent

# PASO 1.2 (CLASES): cargar el archivo de clases que está al lado de app.py

def _cargar_modulo_clases():
    candidatos = [BASE_DIR / "libreria_clases_proyecto1.py"]

    for ruta in candidatos:
        if ruta.is_file():
            nombre = "libreria_clases_proyecto1"
            # Aquí se lee el .py y se convierte en un módulo usable en Python.
            spec = importlib.util.spec_from_file_location(nombre, ruta)
            if spec is None or spec.loader is None:
                continue
            mod = importlib.util.module_from_spec(spec)
            sys.modules[nombre] = mod
            spec.loader.exec_module(mod)
            return mod
    return None


# PASO 1.3 (FUNCIONES): traer las funciones del otro archivo (import normal)
try:
    import libreria_funciones_proyecto1 as lib_funciones
except ImportError as e:  # pragma: no cover
    st.error(f"No se pudo importar libreria_funciones_proyecto1.py: {e}")
    lib_funciones = None  # type: ignore

# PASO 1.4 (configuración): traer las clases (usa la función del PASO 2). Si falta el archivo, queda None.
lib_clases = _cargar_modulo_clases()


# ---------------------------------------------------------------------------
# 2.0 Inicialización de session_state
# ---------------------------------------------------------------------------

# PASO 2.1: Permiten que la app “recuerde” información entre interacciones, la primera vez los inicializa con none

def _init_session_state() -> None:
    # Si no existe la variable en session_state, la creamos la primera vez.

    # Ejercicio 1: lista de movimientos de dinero
    if "movimientos" not in st.session_state:
        st.session_state.movimientos = []  

    # Ejercicio 2: columnas vacías al inicio (luego se llenan al guardar productos)
    if "e2_nombres" not in st.session_state:
        st.session_state.e2_nombres = np.array([], dtype=object)
        st.session_state.e2_categorias = np.array([], dtype=object)
        st.session_state.e2_precios = np.array([], dtype=float)
        st.session_state.e2_cantidades = np.array([], dtype=float)

    # jercicio 3: historial de lo que ejecutaste
    if "e3_historico" not in st.session_state:
        st.session_state.e3_historico = []  

    # Ejercicio 4: lista de objetos guardados (CRUD)
    if "e4_registros" not in st.session_state:
        st.session_state.e4_registros = []  

    # número a usar para el siguient ID (1, 2, 3...)
    if "e4_next_id" not in st.session_state:
        st.session_state.e4_next_id = 1  


# ---------------------------------------------------------------------------
# 3.0 HOME
# ---------------------------------------------------------------------------
def home() -> None:
    # PASO 3.1: Colocando titulo del proyecto
    st.title(TITULO_PROYECTO)

    # PASO 3.2: Colocando subtítulo y texto 
    st.subheader("Información del Proyecto")
    st.markdown(
    f"""
    **Estudiante:** {NOMBRE_ESTUDIANTE}  
    **Módulo:** {NOMBRE_MODULO}  
    **Año:** {ANIO}
    """
    )
    st.write(
        "Esta aplicación integra ejercicios de listas, NumPy, Pandas, llamadas a "
        "funciones de un módulo externo y operaciones CRUD , todo esto "
        "en una sola interfaz con navegación lateral."
    )
    st.markdown("### Librerías utilizadas")
    st.markdown(
        "- **Pandas** — Mostrar tablas y el historial\n"
        "- **NumPy** — Guardar columnas de números (productos)\n"
        "- **Streamlit** — La librería que pinta esta página web desde Python\n"
    )
    # PASO 3.3: Muestra la imagen que esta en la carpeta del proyecto
    img_path = BASE_DIR / "proyecto_imagen.png"
    if img_path.is_file():
        st.image(str(img_path), caption="Logo personal, logo de Python DMC", use_container_width=True)
    else:
        st.caption(
            "Colocar Imagen en la carpeta del proyecto"
        )


# ---------------------------------------------------------------------------
# EJERCICIO 1 — Flujo de caja con listas
# ---------------------------------------------------------------------------
def ejercicio1() -> None:
    # PASO 1: encabezado y texto de ayuda en la pantalla
    st.header("Ejercicio 1 — Flujo de caja con listas")
    st.write("Registra ingresos y gastos; el saldo se calcula automáticamente.")

    # PASO 2: tres controles de Streamlit (cada uno tiene key=... para que no se mezclen con otros ejercicios)
    concepto = st.text_input("Concepto", key="e1_concepto")  # caja de texto
    tipo = st.selectbox("Tipo de movimiento", ["Ingreso", "Gasto"], key="e1_tipo")  # lista desplegable
    valor = st.number_input(
        "Valor", min_value=0.0, step=0.1, format="%.2f", key="e1_valor"
    )  # número con flechas +/-

    # PASO 3: si el usuario pulsa el botón, revisamos datos y guardamos en session_state
    if st.button("Agregar movimiento", key="e1_agregar"):
        if not concepto.strip():  # strip = quitar espacios al inicio y al final
            st.error("Ingresa un concepto.")
        elif valor <= 0:
            st.error("El valor debe ser mayor que cero.")
        else:
            st.session_state.movimientos.append(
                {"concepto": concepto.strip(), "tipo": tipo, "valor": float(valor)}
            )
            st.success("Movimiento agregado.")
            st.rerun()  
    # PASO 4: recarga la página para que se vea la tabla nueva al instante

    # PASO 5: leer la lista guardada y mostrar tabla + totales (si hay algo guardado)
    movs = st.session_state.movimientos
    if movs:
        df = pd.DataFrame(movs)  # lista de dicts -> tabla bonita
        st.subheader("Tabla de movimientos")
        st.dataframe(df, use_container_width=True, hide_index=True)

        total_ingresos = sum(m["valor"] for m in movs if m["tipo"] == "Ingreso")
        total_gastos = sum(m["valor"] for m in movs if m["tipo"] == "Gasto")
        saldo = total_ingresos - total_gastos

        c1, c2, c3 = st.columns(3)  # tres columnas en una fila (como tres celdas)
        with c1:
            st.metric("Total ingresos", f"{total_ingresos:,.2f}")
        with c2:
            st.metric("Total gastos", f"{total_gastos:,.2f}")
        with c3:
            st.metric("Saldo final", f"{saldo:,.2f}")

        if saldo > 0:
            st.success("Resultado: flujo a favor (saldo positivo).")
        elif saldo < 0:
            st.error("Resultado: flujo en contra (saldo negativo).")
        else:
            st.write("Resultado: saldo neutro (0).")

        # PASO 6: gráfico de barraspara comparar ingresos y gastos
        st.subheader("Gráfico de barras: Ingresos vs Gastos")
        df_grafico = pd.DataFrame(
            {
                "tipo": ["Ingresos", "Gastos"],
                "valor": [total_ingresos, total_gastos],
            }
        )

        grafico = (
            alt.Chart(df_grafico)
            .mark_bar(cornerRadiusTopLeft=8, cornerRadiusTopRight=8)
            .encode(
                x=alt.X("tipo:N", title="Tipo", sort=["Ingresos", "Gastos"]),
                y=alt.Y("valor:Q", title="Valor"),
                color=alt.Color(
                    "tipo:N",
                    scale=alt.Scale(
                        domain=["Ingresos", "Gastos"],
                        range=["#2E8B57", "#E74C3C"],
                    ),
                    legend=None,
                ),
                tooltip=[
                    alt.Tooltip("tipo:N", title="Tipo"),
                    alt.Tooltip("valor:Q", title="Valor", format=",.2f"),
                ],
            )
            .properties(height=320)
        )

        etiquetas = grafico.mark_text(
            dy=-10, fontSize=14, fontWeight="bold", color="#1f1f1f"
        ).encode(text=alt.Text("valor:Q", format=",.2f"))

        st.altair_chart(grafico + etiquetas, use_container_width=True)
    else:
        st.info("Aún no hay movimientos. Agrega el primero con el botón superior.")


# ---------------------------------------------------------------------------
# EJERCICIO 2 — NumPy + DataFrame
# ---------------------------------------------------------------------------
def ejercicio2() -> None:
    # PASO 1: título y campos 
    st.header("Ejercicio 2 — Registro con NumPy y DataFrame")
    st.write("Los productos se guardan en arreglos NumPy y se muestran como tabla.")

    nombre = st.text_input("Nombre del producto", key="e2_nombre")
    categoria = st.selectbox(
        "Categoría",
        ["Alimentos", "Bebidas", "Limpieza", "Electrónica", "Otros"],
        key="e2_cat",
    )
    precio = st.number_input(
        "Precio unitario", min_value=0.0, step=0.1, format="%.2f", key="e2_precio"
    )
    cantidad = st.number_input(
        "Cantidad", min_value=0.0, step=0.1, format="%.2f", key="e2_cantidad"
    )

    total = precio * cantidad
    st.write(f"**Total (precio × cantidad):** {total:,.2f}")

    # PASO 2: botón guardar -> se agrega una fila a cada array en session_state
    if st.button("Guardar producto", key="e2_guardar"):
        if not nombre.strip():
            st.error("Ingresa el nombre del producto.")
        elif precio <= 0 or cantidad <= 0:
            st.error("Precio y cantidad deben ser mayores que cero.")
        else:
            st.session_state.e2_nombres = np.append(
                st.session_state.e2_nombres, nombre.strip()
            )
            st.session_state.e2_categorias = np.append(
                st.session_state.e2_categorias, categoria
            )
            st.session_state.e2_precios = np.append(
                st.session_state.e2_precios, float(precio)
            )
            st.session_state.e2_cantidades = np.append(
                st.session_state.e2_cantidades, float(cantidad)
            )
            st.success("Producto guardado en los arreglos NumPy.")
            st.rerun()

    # PASO 3: si ya hay productos, armar la tabla y mostrarla
    n = len(st.session_state.e2_nombres)
    if n > 0:
        totales = st.session_state.e2_precios * st.session_state.e2_cantidades  # fila por fila
        df = pd.DataFrame(
            {
                "nombre": st.session_state.e2_nombres,
                "categoria": st.session_state.e2_categorias,
                "precio": st.session_state.e2_precios,
                "cantidad": st.session_state.e2_cantidades,
                "total": totales,
            }
        )
        st.subheader("Productos registrados")
        st.dataframe(df, use_container_width=True, hide_index=True)
    else:
        st.info("No hay productos registrados todavía.")


# ---------------------------------------------------------------------------
# EJERCICIO 3 — Función externa + historial
# ---------------------------------------------------------------------------

# Listando funciones que empiezan por calcular_
def _listar_funciones_calculo():
    if lib_funciones is None:
        return []
    nombres = []
    for name in dir(lib_funciones):
        if name.startswith("calcular_"):
            obj = getattr(lib_funciones, name)
            if callable(obj):
                nombres.append(name)
    return sorted(nombres)

# Mostrar un numnero segun el parametro de la funcion que se esta ejecutando
def _valor_widget_param(nombre_func: str, pname: str, param: inspect.Parameter) -> object:

    key = f"e3_{nombre_func}_{pname}"
    ann = param.annotation
    default = 0.0 if param.default is inspect.Parameter.empty else param.default

    # FLOAT: Si el parámetro es int -> caja de número entero
    if ann is int or (getattr(ann, "__name__", "") == "int"):
        return st.number_input(
            pname,
            min_value=0,
            step=1,
            value=int(default) if default is not inspect.Parameter.empty else 0,
            key=key,
        )

    # INT: Si es float (u otro caso numérico) -> caja con decimales
    if ann is float or ann is int or str(ann).endswith("float") or str(ann).endswith("int"):
        try:
            val_def = float(default) if default is not inspect.Parameter.empty else 0.0
        except (TypeError, ValueError):
            val_def = 0.0
        return st.number_input(
            pname,
            format="%.2f",
            value=val_def,
            step=0.1,
            key=key,
        )

    # NO SABEMOS TIPO-> igual mostramos un número con decimales
    try:
        val_def = float(default) if default is not inspect.Parameter.empty else 0.0
    except (TypeError, ValueError):
        val_def = 0.0
    return st.number_input(
        pname, format="%.2f", value=val_def, step=0.1, key=key
    )


def ejercicio3() -> None:
    # PASO 1: texto en pantalla y comprobar que exista el archivo de funciones
    st.header("Ejercicio 3 — Uso de función externa")
    st.write(
        "Selecciona una función de `libreria_funciones_proyecto1.py`, completa los parámetros"
        "solicitados. Los resultados se acumularan en un historial (DataFrame)."
    )

    if lib_funciones is None:
        st.error("No está disponible el módulo de funciones.")
        return

    funciones = _listar_funciones_calculo()
    if not funciones:
        st.warning("No se encontraron funciones `calcular_*` en el archivo py")
        return

    # PASO 2: el usuario elige función y nosotros creamos los campos de sus parámetros
    elegida = st.selectbox("Función a ejecutar", funciones, key="e3_func")

    func = getattr(lib_funciones, elegida)
    sig = inspect.signature(func)
    kwargs = {}
    st.subheader("Parámetros")
    for pname, param in sig.parameters.items():
        kwargs[pname] = _valor_widget_param(elegida, pname, param)

    # PASO 3: botón ejecutar -> llamamos a la función de Python con los valores del formulario
    if st.button("Ejecutar función", key="e3_run"):
        try:
            resultado = func(**kwargs)  
            entrada_str = ", ".join(f"{k}={kwargs[k]!r}" for k in kwargs)
            if isinstance(resultado, dict):
                res_str = str(resultado)
            else:
                res_str = repr(resultado)
            # Guardar resultado en el Historial
            st.session_state.e3_historico.append(
                {
                    "función": elegida,
                    "entrada": entrada_str,
                    "resultado": res_str,
                }
            )
            # Mostrar resultados en pantalla
            st.success("Ejecución correcta.")
            st.write("**Resultado:**", resultado)
            st.rerun()

        except Exception as ex:  # noqa: BLE001 — mostrar error al usuario en UI educativa
            st.error(f"Error al ejecutar: {ex}")

    hist = st.session_state.e3_historico
    st.subheader("Historial de ejecuciones")
    if hist:
        st.dataframe(pd.DataFrame(hist), use_container_width=True, hide_index=True)
        if st.button("Limpiar historial", key="e3_clear"):
            st.session_state.e3_historico = []
            st.rerun()
    else:
        st.info("El historial está vacío.")


# ---------------------------------------------------------------------------
# EJERCICIO 4 — Clase externa + CRUD
# ---------------------------------------------------------------------------
def _clases_disponibles():
    # Ejercicio 4: diccionario de nombre_de_clase , se coloca solo las que existen en el .py
    if lib_clases is None:
        return {}
    nombres = [
        "Empleado",
        "ProyectoInversion",
        "InventarioProducto",
        "Servidor",
        "EquipoMantenimiento",
        "EstudianteCurso",
        "Paciente",
        "MezclaConcreto",
        "EspacioIluminacion",
        "ParcelaAgricola",
    ]
    return {n: getattr(lib_clases, n) for n in nombres if hasattr(lib_clases, n)}

# Sirve para convertir un texto con números separados por comas (o punto y coma) en una lista de números tipo float
def _parse_flujos(texto: str) -> list[float]:
    partes = [p.strip() for p in texto.replace(";", ",").split(",") if p.strip()]
    return [float(p) for p in partes]


def _form_kwargs_clase(
    nombre_clase: str,
    clase: type,
    *,
    key_suffix: str,
    initial: Optional[dict] = None,
) -> Optional[dict]:
    # Dibuja en Streamlit los campos que pide el __init__
    initial = initial or {}
    sig = inspect.signature(clase.__init__)  # leer qué argumentos tiene el constructor
    params = [p for n, p in sig.parameters.items() if n != "self"]
    kwargs: dict = {}   # creamos un diccionario vacio

    for p in params:
        pname = p.name
        key = f"e4_{key_suffix}_{nombre_clase}_{pname}"

        if nombre_clase == "ProyectoInversion" and pname == "flujos":
            fl_def = initial.get("flujos", [1000.0, 1200.0, 1500.0])
            txt_default = ", ".join(str(x) for x in fl_def) if isinstance(fl_def, list) else str(fl_def)
            txt = st.text_input(
                f"{pname} (lista separada por comas)",
                value=txt_default,
                key=key,
                help="Ejemplo: 1000, 1500, 2000",
            )
            try:
                kwargs[pname] = _parse_flujos(txt)
            except ValueError:
                st.error("Lista de flujos inválida. Usa números separados por comas.")
                return None
            continue

        ann = p.annotation
        default = p.default
        if pname in initial:
            default = initial[pname]
        if default is inspect.Parameter.empty:
            default_num = 0.0
        else:
            default_num = default

        if ann is int or getattr(ann, "__name__", "") == "int":
            try:
                iv = int(default_num) if isinstance(default_num, (int, float)) else 0
            except (TypeError, ValueError):
                iv = 0
            kwargs[pname] = st.number_input(pname, min_value=0, step=1, value=iv, key=key)
        elif pname in ("nombre", "nombre_proyecto", "nombre_equipo") or "nombre" in pname:
            txt_val = "" if default is inspect.Parameter.empty else str(default_num)
            kwargs[pname] = st.text_input(pname, value=txt_val, key=key)
        else:
            try:
                dv = float(default_num)
            except (TypeError, ValueError):
                dv = 0.0
            kwargs[pname] = st.number_input(
                pname, format="%.6f", value=dv, step=0.1, key=key
            )

    return kwargs


def _resumen_registro(reg: dict) -> dict:
    # Crear otra vez el objeto con los datos guardados y pedir .resumen() si existe
    clases = _clases_disponibles()
    cls = clases[reg["clase"]]
    obj = cls(**reg["datos"])
    if hasattr(obj, "resumen"):
        return obj.resumen()
    return {"clase": reg["clase"], "datos": reg["datos"]}


def ejercicio4() -> None:
    # PASO 1: encabezado y comprobar que se cargaron las clases
    st.header("Ejercicio 4 — Clase externa con CRUD")
    st.write(
        "Operaciones sobre instancias definidas en el módulo de clases del proyecto. "
        "Los registros se guardan en `st.session_state`."
    )

    clases = _clases_disponibles()
    if not clases:
        st.error(
            "No se pudo cargar el módulo de clases. Verifica que exista "
            "`libreria_clases_proyecto1.py` y este junto a `app.py`."
        )
        return

    # PASO 2: Creando las pestanas (Crear / Leer / Actualizar / Eliminar)
    tab_crear, tab_leer, tab_actualizar, tab_eliminar = st.tabs(
        ["Crear", "Leer", "Actualizar", "Eliminar"]
    )

    # Pestaña CREAR: agregar un registro nuevo a session_state
    with tab_crear:
        st.subheader("Crear registro")
        nombre_c = st.selectbox("Clase", list(clases.keys()), key="e4_c_clase")
        st.write("Completa los parámetros del constructor:")
        kwargs = _form_kwargs_clase(nombre_c, clases[nombre_c], key_suffix="create")
        if st.button("Crear", key="e4_c_btn") and kwargs is not None:
            nuevo_id = st.session_state.e4_next_id
            st.session_state.e4_registros.append(
                {"id": nuevo_id, "clase": nombre_c, "datos": kwargs}
            )
            st.session_state.e4_next_id = nuevo_id + 1
            st.success(f"Registro creado con id={nuevo_id}.")
            st.rerun()

    # Pestaña LEER: ver todo en una tabla
    with tab_leer:
        st.subheader("Leer registros")
        regs = st.session_state.e4_registros
        if not regs:
            st.info("No hay registros.")
        else:
            filas = []
            for r in regs:
                try:
                    filas.append({"id": r["id"], "clase": r["clase"], **_resumen_registro(r)})
                except Exception as ex:  
                    filas.append({"id": r["id"], "clase": r["clase"], "error": str(ex)})
            st.dataframe(pd.DataFrame(filas), use_container_width=True, hide_index=True)

    # Pestaña ACTUALIZAR: elegir un id y guardar cambios en ese registro
    with tab_actualizar:
        st.subheader("Actualizar registro")
        regs = st.session_state.e4_registros
        if not regs:
            st.info("No hay registros para actualizar.")
        else:
            opciones = {f"id {r['id']} — {r['clase']}": r["id"] for r in regs}
            label = st.selectbox("Selecciona registro", list(opciones.keys()), key="e4_u_sel")
            rid = opciones[label]
            reg = next(r for r in regs if r["id"] == rid)
            nombre_c = reg["clase"]
            st.write(f"Editando clase **{nombre_c}** (id **{rid}**).")
            kwargs = _form_kwargs_clase(
                nombre_c,
                clases[nombre_c],
                key_suffix=f"upd_{rid}",
                initial=dict(reg["datos"]),
            )
            if st.button("Guardar cambios", key="e4_u_btn") and kwargs is not None:
                reg["datos"] = kwargs
                st.success("Registro actualizado.")
                st.rerun()

    # Pestaña ELIMINAR: quitar un registro de la lista
    with tab_eliminar:
        st.subheader("Eliminar registro")
        regs = st.session_state.e4_registros
        if not regs:
            st.info("No hay registros para eliminar.")
        else:
            opciones = {f"id {r['id']} — {r['clase']}": r["id"] for r in regs}
            label = st.selectbox("Selecciona registro a eliminar", list(opciones.keys()), key="e4_d_sel")
            rid = opciones[label]
            if st.button("Eliminar", key="e4_d_btn"):
                st.session_state.e4_registros = [r for r in regs if r["id"] != rid]
                st.success("Registro eliminado.")
                st.rerun()


# ---------------------------------------------------------------------------
# Punto de entrada
# ---------------------------------------------------------------------------
def main() -> None:
    # PASO 1: configurar la página 
    st.set_page_config(
        page_title=TITULO_PROYECTO,
        layout="wide",
        initial_sidebar_state="expanded",
    )
    # PASO 2: crear las listas vacías en session_state si es la primera vez
    _init_session_state()

    # PASO 3: menú en la barra izquierda (sidebar)
    st.sidebar.title("Menú")
    # PASO 4: según lo que elija el usuario, llamamos a la función 
    pagina = st.sidebar.selectbox(
        "Navegación",
        ["Home", "Ejercicio 1", "Ejercicio 2", "Ejercicio 3", "Ejercicio 4"],
    )

    # PASO 5: Solo una sola pantalla visible a la vez 
    if pagina == "Home":
        home()
    elif pagina == "Ejercicio 1":
        ejercicio1()
    elif pagina == "Ejercicio 2":
        ejercicio2()
    elif pagina == "Ejercicio 3":
        ejercicio3()
    elif pagina == "Ejercicio 4":
        ejercicio4()


if __name__ == "__main__":
    # Punto de arranque: en consola suele usarse  streamlit run app.py
    main()
