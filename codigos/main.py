import streamlit as st
import numpy as np
import plotly.graph_objects as go

st.set_page_config(page_title="Simulador de Proyectiles", layout="wide")
st.title("Simulador de Lanzamiento de Proyectiles")

if 'sim_velocidad0' not in st.session_state:
    st.session_state.sim_velocidad0 = 50.0
if 'sim_angulo' not in st.session_state:
    st.session_state.sim_angulo = 45.0
if 'sim_altura0'  not in st.session_state:
    st.session_state.sim_altura0 = 0.0
    
st.markdown("""Esta aplicación simula el movimiento parabolico (sin resistencia del aire) de un objeto. Ajusta los parametros en la barra lateral y presiona **Calcular Trayectoria** """)

st.sidebar.header("Parametros")

input_velocidad = st.sidebar.slider("Velocidad Inicial (m/s)", 1.0, 100.0, 50.0)
input_angulogrados = st.sidebar.slider("Ángulo de Lanzamiento (°)", 0.0, 90.0, 45.0)
input_altura = st.sidebar.number_input("Altura Inicial (m)", 0.0, 100.0, 0.0)
gravedad = 9.81

if st.sidebar.button("Calcular Trayectoria"):
    st.session_state.sim_velocidad0 = input_velocidad
    st.session_state.sim_angulo = input_angulogrados
    st.session_state.sim_altura0 = input_altura

velocidad0 = st.session_state.sim_velocidad0
angulo_grados = st.session_state.sim_angulo
altura0 = st.session_state.sim_altura0

convGrados = np.radians(angulo_grados)
vx = velocidad0 * np.cos(convGrados)
vy = velocidad0 * np.sin(convGrados)

discriminante = vy**2 + 2 * gravedad * altura0
t_vuelo = (vy + np.sqrt(discriminante)) / gravedad
t = np.linspace(0, t_vuelo, num=100)
x = vx * t
y = altura0 + vy * t -0.5 * gravedad * t**2
distancia_max=x[-1]

fig = go.Figure()

fig.add_trace(go.Scatter(
    x=x, y=y,
    mode='lines',
    name='Camino',
    line=dict(color='lightgrey', width=2, dash='dash')
))

fig.add_trace(go.Scatter(
    x=[x[0]], y=[y[0]],
    mode='markers',
    name='Proyectil',
    marker=dict(color='red', size=15)
))

frames = []

for k in range(len(t)):
    frames.append(go.Frame(
        data=[go.Scatter(x=[x[k]], y=[y[k]])],
        traces=[1],
        name=str(k)
    ))

fig.frames = frames

fig.update_layout(
    title=f"Datos de la Trayectoria<br>Velocidad={velocidad0}m/s  Ángulo={angulo_grados}°  Distancia Total={distancia_max:.2f}m",
    xaxis=dict(range=[0, max(x)*1.2], title="Distancia (m)"),
    yaxis=dict(range=[0, max(y)*1.2], rangemode="nonnegative", title="Altura(m)", scaleanchor="x",scaleratio=1,constrain='domain'),
    height=600,
    template="plotly_dark",
    updatemenus=[dict(
        type="buttons",
        bgcolor="#2E86C1",
        bordercolor="#1B4F72",
        font=dict(family="Montserrat",color="black",size=12),
        buttons=[dict(label="Reproducir",
                      method="animate",
                      args=[None, dict(frame=dict(duration=20, redraw=True),
                                       fromcurrent=True)])]
    )]
)

st.plotly_chart(fig, use_container_width=True)