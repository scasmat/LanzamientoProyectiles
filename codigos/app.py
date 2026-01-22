import streamlit as st
import plotly.graph_objects as go
import numpy as np
import fisica

st.set_page_config(page_title="Simulador Proyectiles Pro", layout="wide")

# Barra Lateral: Configuración
st.sidebar.title("⚙️ Configuración")

st.sidebar.subheader("Escenarios Rápidos")

# Selectbox para escenarios
escenario = st.sidebar.selectbox(
    "Selecciona un caso:",
    ["Personalizado", "Pelota de Ping Pong", "Bala de Cañón", "Balón de Fútbol"]
)

# Valores por defecto
defaults = {
    "Personalizado": {"m": 1.0, "r": 0.1, "cd": 0.47},
    "Pelota de Ping Pong": {"m": 0.0027, "r": 0.02, "cd": 0.5},
    "Bala de Cañón": {"m": 50.0, "r": 0.15, "cd": 0.47},
    "Balón de Fútbol": {"m": 0.43, "r": 0.11, "cd": 0.25}
}

params = defaults[escenario]

# Lógica de bloqueo
bloquear_inputs = (escenario != "Personalizado")

# Controles de Lanzamiento
st.sidebar.markdown("---")
st.sidebar.subheader("Parámetros de Lanzamiento")
v0 = st.sidebar.slider("Velocidad Inicial (m/s)", 1.0, 150.0, 50.0)
angulo = st.sidebar.slider("Ángulo (°)", 0.0, 90.0, 45.0)
h0 = st.sidebar.number_input("Altura Inicial (m)", 0.0, 100.0, 0.0)

# Propiedades del Objeto
st.sidebar.subheader("Propiedades del Objeto")

masa = st.sidebar.number_input(
    "Masa (kg)", 
    0.001, 1000.0, 
    value=params["m"], 
    format="%.4f",
    disabled=bloquear_inputs
)

radio = st.sidebar.number_input(
    "Radio (m)", 
    0.01, 5.0, 
    value=params["r"], 
    format="%.2f",
    disabled=bloquear_inputs
)

cd = st.sidebar.number_input(
    "Coef. Arrastre (Cd)", 
    0.01, 1.0, 
    value=params["cd"],
    disabled=bloquear_inputs
)

# Titutlo Principal
st.title("🚀 Simulador del Lanzamiento de un Proyectil")
st.markdown("""
Este simulador compara el modelo **ideal** (vacío) contra el modelo **real** (resistencia del aire).
Dale al botón de **Play ▶️** para ver la simulación completa.
""")

# Calcular ambas trayectorias originales
t_ideal, x_ideal, y_ideal = fisica.calcular_trayectoria_ideal(v0, angulo, h0)
t_aire, x_aire, y_aire = fisica.calcular_trayectoria_aire(v0, angulo, h0, masa, radio, cd)

# Definición de que objeto tarda más en vuelo
max_time = max(t_ideal[-1], t_aire[-1])

# Velocidad de la animación
t_anim = np.linspace(0, max_time, 200)

# Metodo para que las 2 animaciones funcionen aunque la otra termine antes
x_ideal_anim = np.interp(t_anim, t_ideal, x_ideal)
y_ideal_anim = np.interp(t_anim, t_ideal, y_ideal)

x_aire_anim = np.interp(t_anim, t_aire, x_aire)
y_aire_anim = np.interp(t_anim, t_aire, y_aire)

# Métricas Clave
col1, col2, col3, col4 = st.columns(4)
col1.metric("Distancia Máx (Ideal)", f"{x_ideal[-1]:.2f} m")
col2.metric("Distancia Máx (Aire)", f"{x_aire[-1]:.2f} m", delta=f"{x_aire[-1]-x_ideal[-1]:.2f} m")
col3.metric("Altura Máx (Ideal)", f"{np.max(y_ideal):.2f} m")
col4.metric("Altura Máx (Aire)", f"{np.max(y_aire):.2f} m", delta=f"{np.max(y_aire)-np.max(y_ideal):.2f} m")

# Gráfica
fig = go.Figure()

# Líneas de Fondo
fig.add_trace(go.Scatter(
    x=x_ideal, y=y_ideal, mode='lines', name='Trayectoria Ideal',
    line=dict(color='gray', width=2, dash='dash')
))

fig.add_trace(go.Scatter(
    x=x_aire, y=y_aire, mode='lines', name='Trayectoria Real',
    line=dict(color='#00CC96', width=4)
))

# Bolas Animadas
fig.add_trace(go.Scatter(
    x=[x_aire_anim[0]], y=[y_aire_anim[0]], 
    mode='markers', 
    name='Proyectil Real',
    marker=dict(color='yellow', size=15, line=dict(width=2, color='black'))
))

fig.add_trace(go.Scatter(
    x=[x_ideal_anim[0]], y=[y_ideal_anim[0]], 
    mode='markers', 
    name='Proyectil Ideal',
    marker=dict(color='cyan', size=15, line=dict(width=2, color='black'))
))

# Generación de Frames para la animación
frames = []
for k in range(len(t_anim)):
    frames.append(go.Frame(
        data=[
            go.Scatter(x=[x_aire_anim[k]], y=[y_aire_anim[k]]),
            go.Scatter(x=[x_ideal_anim[k]], y=[y_ideal_anim[k]])
        ],
        traces=[2, 3]
    ))

fig.frames = frames

# 4. Layout
fig.update_layout(
    title="Comparación de Trayectorias",
    xaxis_title="Distancia (m)",
    yaxis_title="Altura (m)",
    template="plotly_dark",
    height=580,
    hovermode="x unified",
    margin=dict(l=50, r=50, t=80, b=50), 
    updatemenus=[
        dict(
            type="buttons",
            showactive=False,
            direction="left",
            x=0.12, 
            y=1.15, 
            xanchor="left", 
            yanchor="top",
            pad=dict(t=0, r=10),
            bgcolor="#1f2630",
            bordercolor="white",
            borderwidth=0.5,
            buttons=[
                dict(
                    label="Play ▶️",
                    method="animate",
                    args=[None, dict(frame=dict(duration=15, redraw=False), 
                                     fromcurrent=True, mode='immediate')]
                )
            ]
        )
    ]
)


st.plotly_chart(fig, use_container_width=True)

# Sección Explicativa
with st.expander("📚 Ver Explicación Matemática"):
    st.markdown(r"""
    **¿Por qué una llega antes?**
    La simulación muestra el paso del tiempo real.
    
    1. La bola **Real (Amarilla)** se frena por el aire, recorre menos distancia y toca el suelo antes.
    2. La bola **Ideal (Cian)** mantiene su velocidad horizontal constante, por lo que sigue volando más tiempo y llega más lejos.
    
                
    **Modelo Ideal (Tiro Parabólico)**
    
    En el vacio, el movimiento se separa en dos ejes independientes:
    
    1. Eje Horizontal ($x$):
    Velocidad constante (MRU). 
    $$ x(t) = v_0 \cdot \cos(\theta) \cdot t $$
                
    2. Eje Vertizal ($y$):
    Aceleración constante por la gravedad ($g$). 
    $$ y(t) = h_0 + v_0 \cdot t - \frac{1}{2} g t^2 $$
                
    Donde:
    * $v_0$: Velocidad Inicial
    * $\theta$: Ángulo de lanzamiento
    * $g$: Gravedad ($\approx 9.81 m/s^2$)
    
    **Modelo con Resistencia del Aire (Método de Euler)**
    
    A diferencia del modelo ideal, aquí consideramos la fuerza de arrastre $F_d$:
    $$ F_d = \frac{1}{2} \rho v^2 C_d A $$
    
    Esto genera aceleraciones que cambian constantemente:
    $$ a_x = - \frac{F_d \cos(\theta)}{m}, \quad a_y = -g - \frac{F_d \sin(\theta)}{m} $$
    
    Se resuelve iterativamente usando $\Delta t = 0.01s$.
    """)