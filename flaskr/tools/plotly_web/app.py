# bebbug run: Python: Flask plotly
# in terminal run: python -m flask run
from flask import Flask, request, render_template
import plotly
import plotly.graph_objs as go
import json

app = Flask(__name__) # , template_folder='C:\\Temp\\Adi\\yaniv\\plotly_web\\templates'

@app.route('/')
def index():
    # Render the main page with the form to submit data
    return render_template('index.html')

@app.route('/plot', methods=['POST'])
def plot():
    # Get parameters from the web page
    data = request.data.decode()
    data_json = json.loads(data)
    x_values = data_json["x_values"] #.getlist('x_values', type=float)
    y_values = data_json["y_values"]# .getlist('y_values', type=float)

    # Create a plot using Plotly
    plot = go.Figure(data=[go.Scatter(x=x_values, y=y_values, mode='lines+markers')])
    plot_json = json.dumps(plot, cls=plotly.utils.PlotlyJSONEncoder)

    # Return the plot to the web page
    return plot_json

if __name__ == '__main__':
    app.run(debug=True)
