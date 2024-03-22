# https://plotly.com/javascript/
# bebbug run: Python: Flask plotly
# python debugger: debug python file
# in terminal run: python -m flask run
from flask import Flask, request, render_template
import plotly
import plotly.graph_objs as go
import json
import webbrowser
import numpy as np
from scipy.integrate import odeint

app = Flask(__name__ )# , template_folder='yaniv/plotly_web/templates'

@app.route('/')
def index():
    # Render the main page with the form to submit data
    return render_template('index.html')

# Initial conditions
setpoint = 1  # Desired setpoint
initial_y = 0  # Initial value of y
previous_error = 0
integral = 0
dt = 0.01  # Time step

# Define the system's model
def model(y, t, Kp, Ki, Kd):
    # Example model: dy/dt = -y + Kp*u
    u = pid_controller(y, t, Kp, Ki, Kd)
    dydt = -y + Kp*u
    return dydt

# PID controller function
def pid_controller(y, t, Kp, Ki, Kd):
    global integral, previous_error
    # Simple PID control logic (Pseudocode)
    error = setpoint - y
    integral = integral + error * dt
    derivative = (error - previous_error) / dt
    output = Kp*error + Ki*integral + Kd*derivative
    previous_error = error
    return output

# Time vector
t = np.linspace(0, 10, num=100)

# Solve ODE
y = odeint(model, initial_y, t, args=(1.0, 0.1, 0.05))

# Create the plot
fig = go.Figure()
fig.add_scatter(x=t, y=y.ravel(), mode='lines', name='Output')
fig.add_scatter(x=t, y=[setpoint]*len(t), mode='lines', name='Setpoint')
fig.layout.title = 'PID Control System Simulation'
fig.layout.xaxis.title = 'Time'
fig.layout.yaxis.title = 'Output'
fig.layout.height=350

# Interactive function to update the plot
def update(Kp=1.0, Ki=0.1, Kd=0.05):
    y = odeint(model, initial_y, t, args=(Kp, Ki, Kd))
    fig.data[0].y = y.ravel()

@app.route('/plot', methods=['POST'])
def plot():
    # Get parameters from the web page
    data = request.data.decode()
    data_json = json.loads(data)
    pk_values = float(data_json["pk"]) #.getlist('x_values', type=float)
    pd_values = float(data_json["pd"])# .getlist('y_values', type=float)
    pi_values = float(data_json["pi"])
    # Create a plot using Plotly
    update(pk_values, pi_values, pd_values)
    plot_json = fig.to_json() # json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    # Return the plot to the web page
    return plot_json

if __name__ == '__main__':
    url = "http://127.0.0.1:5000/"
    # Open the default web browser to the specified URL
    # webbrowser.open(url)
    app.run(debug=True)
