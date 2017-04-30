#import gspread
#from oauth2client.service_account import ServiceAccountCredentials
from lxml import html
import time
import requests
import speedtest
from collections import namedtuple
import socket
import json
import io
import sqlite3
import pprint

#Constants
dbfile = 'data/imdb.sqlite'

#Python 2/3 Compatibility
try:
    to_unicode = unicode
except NameError:
    to_unicode = str

	
CableModemChannel = namedtuple("CableModemChannel", "ChannelID Freq SNR Modulation Power")

#Setup Speedtest
s=speedtest.Speedtest()
s.get_servers([4438])
s.get_best_server()

#Setup Modem Status Page Access
channel1=dict()
channel2=dict()
channel3=dict()
channel4=dict()
row=2

dbconn=sqlite3.connect(dbfile)
db=dbconn.cursor()

def internet_connected(host="8.8.8.8", port=53):
	"""
	Host: 8.8.8.8 (google-public-dns-a.google.com)
	OpenPort: 53/tcp
	Service: domain (DNS/TCP)
	"""
	try:
		socket.setdefaulttimeout(1)
		socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
		return True
	except Exception as ex:
		pass

	return False


#Main Loop
while True:
	conn=internet_connected()
	if conn:
		internetstatus=1
	else:
		internetstatus=0
	
	try:
		page = requests.get('http://192.168.100.1/cmSignalData.htm')
		tree = html.fromstring(page.content)
	except:
		print("Unexpected error:", sys.exc_info()[0])
	ltime = time.time()
	
	id=tree.xpath('/html/body/center[1]/table/tbody/tr[2]/td[2]/text()')
	freq=tree.xpath('/html/body/center[1]/table/tbody/tr[3]/td[2]/text()')
	snr=tree.xpath('/html/body/center[1]/table/tbody/tr[4]/td[2]/text()')
	modulation=tree.xpath('/html/body/center[1]/table/tbody/tr[5]/td[2]/text()')
	power=tree.xpath('/html/body/center[1]/table/tbody/tr[6]/td[2]/text()')
	c1 = CableModemChannel(id, freq, snr, modulation, power)

	id=tree.xpath('/html/body/center[1]/table/tbody/tr[2]/td[3]/text()')
	freq=tree.xpath('/html/body/center[1]/table/tbody/tr[3]/td[3]/text()')
	snr=tree.xpath('/html/body/center[1]/table/tbody/tr[4]/td[3]/text()')
	modulation=tree.xpath('/html/body/center[1]/table/tbody/tr[5]/td[3]/text()')
	power=tree.xpath('/html/body/center[1]/table/tbody/tr[6]/td[3]/text()')
	c2 = CableModemChannel(id, freq, snr, modulation, power)

	id=tree.xpath('/html/body/center[1]/table/tbody/tr[2]/td[4]/text()')
	freq=tree.xpath('/html/body/center[1]/table/tbody/tr[3]/td[4]/text()')
	snr=tree.xpath('/html/body/center[1]/table/tbody/tr[4]/td[4]/text()')
	modulation=tree.xpath('/html/body/center[1]/table/tbody/tr[4]/td[2]/text()')
	power=tree.xpath('/html/body/center[1]/table/tbody/tr[6]/td[4]/text()')
	c3 = CableModemChannel(id, freq, snr, modulation, power)

	id=tree.xpath('/html/body/center[1]/table/tbody/tr[2]/td[5]/text()')
	freq=tree.xpath('/html/body/center[1]/table/tbody/tr[3]/td[5]/text()')
	snr=tree.xpath('/html/body/center[1]/table/tbody/tr[4]/td[5]/text()')
	modulation=tree.xpath('/html/body/center[1]/table/tbody/tr[5]/td[5]/text()')
	power=tree.xpath('/html/body/center[1]/table/tbody/tr[6]/td[5]/text()')
	c4 = CableModemChannel(id, freq, snr, modulation, power)

	upload=s.upload()
	download=s.download()

	#r = Record(InternetUp=conn, UploadSpeed=upload, DownloadSpeed=download, CableModemChannel1=c1, CableModemChannel2=c2, CableModemChannel3=c3, CableModemChannel4=c4)
	r = (ltime,upload,download,internetstatus)
	pprint.pprint(r)	
	db.execute("INSERT INTO InternetStatus(datetime,upload,download,status) VALUES (?,?,?,?)", r)
	dbconn.commit()
	time.sleep(10)
