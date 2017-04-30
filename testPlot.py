import numpy as np

from bokeh.layouts import column
from bokeh.plotting import figure, save, output_file
from bokeh.models import DatetimeTickFormatter
import sqlite3
import datetime
from datetime import datetime
import time

def datetime(x):
    return np.array(x, dtype='datetime64[ms]')

#Constants
dbfile = 'data/imdb.sqlite'
dbconn=sqlite3.connect(dbfile)
db=dbconn.cursor()

while true:
	db.execute('''SELECT datetime,upload,download,status from InternetStatus''')
	time = db.fetchall()
	
	timestamp,upload,download,status = (
	  [int((l[0]-14400)*1000) for l in time], 
	  [l[1]/1000000 for l in time],
	  [l[2]/1000000 for l in time],
	  [l[3] for l in time]
	)
	
	print(timestamp)
	
	p1 = figure(x_axis_type="datetime", title="Internet Speed")
	#p1 = figure(title="Internet Speed")
	
	p1.xaxis.formatter=DatetimeTickFormatter(formats=dict(
		minutes=["%d %B %Y"],
		hours=["%d %b %Y"],
		days=["%d %b %Y"],
		months=["%d %b %Y"],
		years=["%d %b %Y"]))
	
	p1.grid.grid_line_alpha=0.3
	p1.xaxis.axis_label = 'Date'
	p1.yaxis.axis_label = 'Internet Speed'
	
	p1.line(datetime(timestamp), upload, color='Red', legend='Upload')
	p1.line(datetime(timestamp), download, color='Blue', legend='Download')
	p1.legend.location = "top_left"
	p1.sizing_mode = 'scale_width'
	
	
	p2 = figure (x_axis_type="datetime", title="Internet Up/Down")
	p2.xaxis.formatter=DatetimeTickFormatter(formats=dict(
		minutes=["%d %B %Y"],
		hours=["%d %b %Y"],
		days=["%d %b %Y"],
		months=["%d %b %Y"],
		years=["%d %b %Y"]))
	
	p2.grid.grid_line_alpha=0.3
	p2.xaxis.axis_label = 'Date'
	p2.yaxis.axis_label = 'Internet Status'
	
	p2.line(datetime(timestamp), status, color='Red', legend='Status')
	p2.legend.location = "top_left"
	p2.sizing_mode='scale_width'
	
	output_file("/var/www/htdocs/InternetStatus.html", title="InternetStatus")
	p=column(p1,p2)
	column.sizing_mode = 'scale_width'
	save(p)
	time.sleep(60)
