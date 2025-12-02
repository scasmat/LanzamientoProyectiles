import streamlit as st
import numpy as np
import plotly.graph_objects as go

st.set_page_config(page_title="Simulador de Proyectiles", layout="wide")

st.title("Simulador de Lanzamiento de Proyectiles")
st.markdown("""
            Esta aplicación simula el movimiento parabolico (sin resistencia del aire).
            Ajusta los parametros en la barra lateral y presiona **Calcular**
            """)

st.sidebar.header("Parametros de Entrada")

velocidad0 = st.sidebar.slider("Velocidad Inicial (m/s)", 1.0, 100.0, 50.0)
angulo_grados = st.sidebar.slider("Ángulo de Lanzamiento (°)", 0.0, 90.0, 45.0)
altura0 = st.sidebar.number_input("Altura Inicial (m)", 0.0, 100.0, 0.0)
gravedad = 9.81

calcular = st.sidebar.button("Calcular Trayectoria")

if calcular:
    convGrados = np.radians(angulo_grados)

    vx = velocidad0 * np.cos(convGrados)
    vy = velocidad0 * np.sin(convGrados)

    discriminante = vy**2 + 2 * gravedad * altura0
    t_vuelo = (vy + np.sqrt(discriminante)) / gravedad

    t = np.linspace(0, t_vuelo, num=500)

    x = vx * t
    y = altura0 + vy * t -0.5 * gravedad * t**2

    altura_maxima = np.max(y)
    distancia_maxima = x[-1]

    col1, col2, col3 = st.columns(3)
    col1.metric("Tiempo de Vuelo", f"{t_vuelo:.2f} s")
    col2.metric("Altura Máxima", f"{altura_maxima:.2f} m")
    col3.metric("Distancia Total", f"{distancia_maxima:.2f} m")

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=x, y=y,
        mode='lines',
        name='Trayectoria',
        line=dict(color='firebrick', width=4)
    ))

    fig.add_trace(go.Scatter(
        x=[x[0], x[-1]], y=[y[0], y[-1]],
        mode='markers',
        name='Puntos Clave',
        marker=dict(size=10, color='blue')
    ))

    fig.update_layout(
        title="Gráfico de la Trayectoria",
        xaxis_title="Distancia (m)",
        yaxis_title="Altura (m)",
        template="plotly_white",
        height=600,
        yaxis=dict(scaleanchor="x", scaleratio=1),
    )

    st.plotly_chart(fig, use_container_width=True)

else:
    st.info("Ajusta los parámetros en la barra lateral y presiona 'Calcular' para empezar.")