import streamlit as st
import plotly.graph_objects as go
import numpy as np
import fisica  # Importamos tu módulo de lógica

st.set_page_config(page_title="Simulador Proyectiles Pro", layout="wide")

# --- Barra Lateral: Configuración ---
st.sidebar.title("🎛️ Panel de Control")

st.sidebar.subheader("Escenarios Rápidos")
escenario = st.sidebar.selectbox(
    "Selecciona un caso:",
    ["Personalizado", "Pelota de Ping Pong", "Bala de Cañón", "Balón de Fútbol"]
)

# Valores por defecto según escenario
defaults = {
    "Personalizado": {"m": 1.0, "r": 0.1, "cd": 0.47},
    "Pelota de Ping Pong": {"m": 0.0027, "r": 0.02, "cd": 0.5},
    "Bala de Cañón": {"m": 50.0, "r": 0.15, "cd": 0.47},
    "Balón de Fútbol": {"m": 0.43, "r": 0.11, "cd": 0.25}
}

params = defaults[escenario]

# Controles
st.sidebar.markdown("---")
st.sidebar.subheader("Parámetros de Lanzamiento")
v0 = st.sidebar.slider("Velocidad Inicial (m/s)", 1.0, 150.0, 50.0)
angulo = st.sidebar.slider("Ángulo (°)", 0.0, 90.0, 45.0)
h0 = st.sidebar.number_input("Altura Inicial (m)", 0.0, 100.0, 0.0)

st.sidebar.subheader("Propiedades del Objeto")
masa = st.sidebar.number_input("Masa (kg)", 0.001, 1000.0, params["m"], format="%.4f")
radio = st.sidebar.number_input("Radio (m)", 0.01, 5.0, params["r"], format="%.2f")
cd = st.sidebar.number_input("Coef. Arrastre (Cd)", 0.01, 1.0, params["cd"])

# --- Lógica Principal ---
st.title("🚀 Simulador Científico de Proyección de la Trayectoria de un Proyectil")
st.markdown("""
Este simulador compara el modelo **ideal** (vacío) contra el modelo **real** (resistencia del aire).
Útil para visualizar cómo la masa y la aerodinámica afectan el tiro.
""")

# Calcular ambas trayectorias
t_ideal, x_ideal, y_ideal = fisica.calcular_trayectoria_ideal(v0, angulo, h0)
t_aire, x_aire, y_aire = fisica.calcular_trayectoria_aire(v0, angulo, h0, masa, radio, cd)

# Métricas Clave (Comparación)
col1, col2, col3, col4 = st.columns(4)
col1.metric("Distancia Máx (Ideal)", f"{x_ideal[-1]:.2f} m")
col2.metric("Distancia Máx (Aire)", f"{x_aire[-1]:.2f} m", delta=f"{x_aire[-1]-x_ideal[-1]:.2f} m")
col3.metric("Altura Máx (Ideal)", f"{np.max(y_ideal):.2f} m")
col4.metric("Altura Máx (Aire)", f"{np.max(y_aire):.2f} m", delta=f"{np.max(y_aire)-np.max(y_ideal):.2f} m")

# Gráfica Plotly
fig = go.Figure()

# Traza sin Resistencia de Aire
fig.add_trace(go.Scatter(
    x=x_ideal, y=y_ideal, mode='lines', name='Vacío (Ideal)',
    line=dict(color='gray', width=2, dash='dash')
))

# Traza con Resistencia de Aire
fig.add_trace(go.Scatter(
    x=x_aire, y=y_aire, mode='lines', name='Con Resistencia (Real)',
    line=dict(color='#00CC96', width=4)
))

# Animación (Punto moviéndose en la curva real)
fig.add_trace(go.Scatter(
    x=[x_aire[-1]], y=[y_aire[-1]], mode='markers', name='Impacto',
    marker=dict(color='red', size=10, symbol='x')
))

fig.update_layout(
    title="Comparación de Trayectorias",
    xaxis_title="Distancia (m)",
    yaxis_title="Altura (m)",
    template="plotly_dark",
    height=600,
    hovermode="x unified"
)

st.plotly_chart(fig, use_container_width=True)

# Explicación Cientifica
with st.expander("📚 Ver Explicación Matemática (Para Exposición)"):
    st.markdown(r"""
    **Modelo con Resistencia del Aire (Método de Euler)**
    
    A diferencia del modelo ideal, aquí consideramos la fuerza de arrastre $F_d$:
    $$ F_d = \frac{1}{2} \rho v^2 C_d A $$
    
    Esto genera aceleraciones que cambian constantemente:
    $$ a_x = - \frac{F_d \cos(\theta)}{m}, \quad a_y = -g - \frac{F_d \sin(\theta)}{m} $$
    
    Se resuelve iterativamente usando $\Delta t = 0.01s$.
    """)