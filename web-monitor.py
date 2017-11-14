import requests
from bs4 import BeautifulSoup
import time
import smtplib
from email.mime.text import MIMEText
import hashlib


url = "https://www.ic.unicamp.br/~zanoni/mo640/2017/notas/"
# set the headers like we are a browser,
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
# download the homepage
response = requests.get(url, headers=headers)
# parse the downloaded homepage and grab all text, then,
soup = BeautifulSoup(response.text, "lxml")
table = soup.find("table")
m = hashlib.md5()


with open('/PATH/biocomp_md5', 'r') as f:
	old_table_md5 = f.readline().split()[0]

m.update(str(table).encode())
table_md5 = m.hexdigest()

if table_md5 == old_table_md5:
    print("Thats ok")   # TODO: make it usefull
else:	
	# create an email message with just a subject line,
	
	sender = 'someone@something.br'
	receiver = 'gomes.bcc@gmail.com'
	msg = MIMEText(str(table.find_all("a")[5:]).encode('utf-8'), 'plain', 'utf-8')
	msg["Subject"] = "Auto-script: CheckBioCompNotes"
	msg["From"] = sender
	msg["To"] = receiver

	# setup the email server,
	server = smtplib.SMTP('smtp.students.ic.unicamp.br', 587)
	server.starttls()
	# add my account login name and password,
	server.login("ra<X>", "")

	# Print the email's contents

	print('Message: ' + msg.as_string() )

	# send the email
	server.sendmail(sender, receiver, msg.as_string())
	# disconnect from the server
	server.quit()
	with open('/PATH/biocomp_md5', 'w') as f:
		f.write(table_md5)
		
