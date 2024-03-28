# https://plotly.com/python/
# https://www.geeksforgeeks.org/python-plotly-tutorial/
import plotly.graph_objects as go
import numpy as np

# Data to be plotted
# x = np.outer(np.linspace(-2, 2, 30), np.ones(30))
# y = x.copy().T
# z = np.cos(x ** 2 + y ** 2)

x = np.linspace(-5, 5, 50)
y = np.linspace(-5, 5, 40)
z = np.sin(x) * np.cos(y[:, np.newaxis])

# plotting the figure
fig = go.Figure(data=[go.Surface(x=x, y=y, z=z)])

fig.update_layout(title="Plotted 3D")

fig.show()

# Create the heatmap
fig = go.Figure(data=go.Heatmap(
    z=z,
    x=x,
    y=y
))

# Show the figure
fig.show()
