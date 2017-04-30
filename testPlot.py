import numpy as np

from bokeh.layouts import gridplot
from bokeh.plotting import figure, save, output_file
from CodernityDB.database import Database

#Open file
#Constants
dbfile = '/opt/internetmonitor/data/imdb.sqlite'
db = Database(dbfile)
db.open()

for curr in db.all('id'):
	print curr['self']

def datetime(x):
    return np.array(x, dtype=np.datetime64)

p1 = figure(x_axis_type="datetime", title="Internet Speed")
p1.grid.grid_line_alpha=0.3
p1.xaxis.axis_label = 'Date'
p1.yaxis.axis_label = 'Internet Speed'

p1.line(datetime(AAPL['date']), AAPL['adj_close'], color='#A6CEE3', legend='Upload')
p1.line(datetime(GOOG['date']), GOOG['adj_close'], color='#B2DF8A', legend='Download')
p1.legend.location = "top_left"

output_file("/opt/internetmonitor/stocks.html", title="stocks.py example")
save(gridplot([[p1,p2]], plot_width=400, plot_height=400))
