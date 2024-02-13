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
import pandas as pd

pd.options.plotting.backend = "plotly"

csv = {
    "Month": ["Jan", "Feb", "Mar", "Apr", "May", "Jun"],
    "Sales": [1000, 1200, 1500, 1800, 2000, 2200],
    "Profit": [200, 300, 400, 500, 600, 700],
    "time": [1, 2, 3],
}

table = pd.DataFrame(csv, columns=["Month", "Sales", "Profit"])  # option to fillter
# table = pd.read_csv('data.csv')

# Panda print 2 first rows
# use a list of indexes:
print(table.loc[[0, 1]])
#    Month  Sales  Profit
# 0   Jan   1000     200
# 1   Feb   1200     300

# Make multiple line plots
fig = px.line(
    table,
    x="Month",
    y=["Sales", "Profit"],  # select two columes for two lines
    # labels={'x':'Date', 'y':'Value of Dollar'}, # not working take it from the colume name
    title="Sales Vs. Profit",
    markers=True,
)

fig.update_layout(yaxis_title="Y Axis Title", legend_title="Legend Title")

fig.show()

# -------------- using panda for plot -----------------

# plot a line plot of the Sales column with points
# fig = go.Figure()
fig: go.Figure = table.plot.line(
    x="Month", y=["Sales", "Profit"], title="plot for panda data", markers=True
)

fig.update_layout(yaxis_title="Y Axis Title", legend_title="Legend Title")

fig.show()



# -------------- simple line --------

# # Plot the value of a dollar invested over time
# # Use included Google price data to make one plot
# df_stocks = px.data.stocks()
# # px.line(df_stocks, x='date', y='NFLX', labels={ 'x':'Date',
# #                                                'y':'Value of Dollar'})

# # Make multiple line plots
# fig = px.line(df_stocks, x='date', y=['GOOG','AAPL'], # select two columes for two lines
#         labels={'x':'Date', 'y':'Value of Dollar'}, # not working take it from the colume name
#         title='Apple Vs. Google')

# fig.show()

# # -------------- simple line --------

# # using the iris dataset
# df = px.data.iris()

# # plotting the line chart
# fig = px.line(df, x="species", y=["petal_width", "petal_length"]) # select columes

# # showing the plot
# fig.show()
