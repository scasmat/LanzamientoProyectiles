import numpy as np

def calcular_trayectoria_ideal(v0, angulo_grados, h0, g=9.81):
    """Calcula la trayectoria en el vacío (Física básica)."""
    angulo_rad = np.radians(angulo_grados)
    vx = v0 * np.cos(angulo_rad)
    vy = v0 * np.sin(angulo_rad)
    
    # Tiempo total de vuelo
    discriminante = vy**2 + 2 * g * h0
    t_vuelo = (vy + np.sqrt(discriminante)) / g
    
    t = np.linspace(0, t_vuelo, num=300)
    x = vx * t
    y = h0 + vy * t - 0.5 * g * t**2
    
    return t, x, y

def calcular_trayectoria_aire(v0, angulo_grados, h0, masa, radio, Cd, g=9.81, rho=1.225):
    """Calcula la trayectoria con resistencia del aire (Método de Euler)."""
    dt = 0.01
    angulo_rad = np.radians(angulo_grados)
    area = np.pi * (radio ** 2)
    
    # Condiciones iniciales
    vx = v0 * np.cos(angulo_rad)
    vy = v0 * np.sin(angulo_rad)
    x = 0
    y = h0
    
    trayectoria_x = [x]
    trayectoria_y = [y]
    tiempos = [0]
    t = 0
    
    # Bucle de simulación (Método numérico)
    while y >= 0:
        v = np.sqrt(vx**2 + vy**2)
        
        # Fuerza de arrastre: F = 0.5 * rho * v^2 * Cd * A
        # Fuerza descompuesta en componentes (opuesta a la velocidad)
        fuerza_drag = 0.5 * rho * v * Cd * area
        
        ax = -(fuerza_drag * vx) / masa
        ay = -g - (fuerza_drag * vy) / masa
        
        # Actualizar velocidades y posiciones
        vx += ax * dt
        vy += ay * dt
        x += vx * dt
        y += vy * dt
        t += dt
        
        if y < 0: break # Tocar suelo
        
        trayectoria_x.append(x)
        trayectoria_y.append(y)
        tiempos.append(t)
        
    return np.array(tiempos), np.array(trayectoria_x), np.array(trayectoria_y)