import gspread
from oauth2client.service_account import ServiceAccountCredentials
from lxml import html
import requests
import time
import speedtest

#Setup Speedtest
s=speedtest.Speedtest()
s.get_servers([4438])
s.get_best_server()

#Setup Google Sheet Access
scope = ['https://spreadsheets.google.com/feeds']
credentials = ServiceAccountCredentials.from_json_keyfile_name('InternetMonitor.json', scope)
gc = gspread.authorize(credentials)
wks = gc.open("InternetMonitor").sheet1

#Setup Modem Status Page Access
channel1=dict()
channel2=dict()
channel3=dict()
channel4=dict()
row=2

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
	if internet_connected():
		print("Good Connection")
	else:
		print("Bad Connection")
	try:
		page = requests.get('http://192.168.100.1/cmSignalData.htm')
		tree = html.fromstring(page.content)
	except:
		print("Unexpected error:", sys.exc_info()[0])
	timestr = time.strftime("%Y%m%d-%H%M%S")
	wks.update_cell(row,1,timestr)
	channel1['id']=tree.xpath('/html/body/center[1]/table/tbody/tr[2]/td[2]/text()')
	channel1['freq']=tree.xpath('/html/body/center[1]/table/tbody/tr[3]/td[2]/text()')
	channel1['snr']=tree.xpath('/html/body/center[1]/table/tbody/tr[4]/td[2]/text()')
	channel1['modulation']=tree.xpath('/html/body/center[1]/table/tbody/tr[5]/td[2]/text()')
	channel1['pwr']=tree.xpath('/html/body/center[1]/table/tbody/tr[6]/td[2]/text()')

	channel2['id']=tree.xpath('/html/body/center[1]/table/tbody/tr[2]/td[3]/text()')
	channel2['freq']=tree.xpath('/html/body/center[1]/table/tbody/tr[3]/td[3]/text()')
	channel2['snr']=tree.xpath('/html/body/center[1]/table/tbody/tr[4]/td[3]/text()')
	channel2['modulation']=tree.xpath('/html/body/center[1]/table/tbody/tr[5]/td[3]/text()')
	channel2['pwr']=tree.xpath('/html/body/center[1]/table/tbody/tr[6]/td[3]/text()')

	channel3['id']=tree.xpath('/html/body/center[1]/table/tbody/tr[2]/td[4]/text()')
	channel3['freq']=tree.xpath('/html/body/center[1]/table/tbody/tr[3]/td[4]/text()')
	channel3['snr']=tree.xpath('/html/body/center[1]/table/tbody/tr[4]/td[4]/text()')
	channel3['modulation']=tree.xpath('/html/body/center[1]/table/tbody/tr[4]/td[2]/text()')
	channel3['pwr']=tree.xpath('/html/body/center[1]/table/tbody/tr[6]/td[4]/text()')

	channel4['id']=tree.xpath('/html/body/center[1]/table/tbody/tr[2]/td[5]/text()')
	channel4['freq']=tree.xpath('/html/body/center[1]/table/tbody/tr[3]/td[5]/text()')
	channel4['snr']=tree.xpath('/html/body/center[1]/table/tbody/tr[4]/td[5]/text()')
	channel4['modulation']=tree.xpath('/html/body/center[1]/table/tbody/tr[5]/td[5]/text()')
	channel4['pwr']=tree.xpath('/html/body/center[1]/table/tbody/tr[6]/td[5]/text()')

	n=2
	for k,v in channel1.items():
		wks.update_cell(row,n,v)
		n=n+1
	for k,v in channel2.items():
		wks.update_cell(row,n,v)
		n=n+1
	for k,v in channel3.items():
		wks.update_cell(row,n,v)
		n=n+1
	for k,v in channel4.items():
		wks.update_cell(row,n,v)
		n=n+1
	
	wks.update_cell(row,n,s.download())
	n=n+1
	wks.update_cell(row,n,s.upload())
	
	time.sleep(30)
	row = row +1	
