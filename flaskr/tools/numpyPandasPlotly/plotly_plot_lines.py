# https://plotly.com/python/
# https://www.geeksforgeeks.org/python-plotly-tutorial/
import cufflinks as cf
import plotly.express as px
import plotly.graph_objects as go

# Make Plotly work in your Jupyter Notebook
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
# init_notebook_mode(connected=True)
# Use Plotly locally
# cf.go_offline()

# Plot the value of a dollar invested over time
# Use included Google price data to make one plot
df_stocks = px.data.stocks()
# px.line(df_stocks, x='date', y='NFLX', labels={ 'x':'Date',
#                                                'y':'Value of Dollar'})

# Make multiple line plots
fig = px.line(df_stocks, x='date', y=['GOOG','AAPL'], # select two columes for two lines
        labels={'x':'Date', 'y':'Value of Dollar'}, # not working take it from the colume name
        title='Apple Vs. Google')

fig.show()

# -------------- simple line --------

# using the iris dataset
df = px.data.iris()

# plotting the line chart
fig = px.line(df, x="species", y=["petal_width", "petal_length"]) # select columes

# showing the plot
fig.show()
