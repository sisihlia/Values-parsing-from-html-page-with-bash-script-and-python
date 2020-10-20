from bs4 import BeautifulSoup
import requests
import json
import re
import urllib2
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from urllib2 import urlopen as uReq

#print("Hello")
url="https://voyages.carrefour.fr/serp?origin=homePage,recherche_sejours&s_c.site=B2C&s_c.type_produit=sejour_etranger,circuits&s_c.destination=MCPI.ES&ref_mmp=0,5000&s_st=base_price&byPage=12"

#opening up connection, grabbing the page
uClient=uReq(url)
page_html=uClient.read()
uClient.close()

#parsin html
page_soup=BeautifulSoup(page_html,"html.parser")
res = page_soup.findAll('script',{"type": "application/ld+json"})[-1]
json_object = json.loads(res.contents[0])


#extract the price value with json object and store them to a list
prices=[]
json_object = json.loads(res.contents[0])
for item in json_object['itemListElement']:
	price= item['offers']['price']
	prices.append(price)
	if len(prices)==4: break
print prices

age=""
#extract the value of age header
response = urllib2.urlopen(url)
info = response.info()
for header in info.headers:
	  if 'Age:' in header: age=header.replace("\n", "")
print age


body = ', '.join(prices) +"\n"+ age

#send the information to email address
TO="admin@orchestra.eu"
FROM="sisihlia.yuniyarti@gmailcom"
server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
server.login(FROM, "mypassword")
msg = MIMEMultipart()

msg['Subject'] = 'Excercise Answer'
msg['From'] = FROM
msg['To'] = TO
body = prices + age
msg.attach(MIMEText(body, 'html'))
server.sendmail(FROM,TO,body)



