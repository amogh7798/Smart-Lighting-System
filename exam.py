from pyzbar.pyzbar import decode
from PIL import Image
import pymongo
import smtplib
import urllib
import numpy as np
import cv2
import httplib2
import os
import oauth2client
from oauth2client import client, tools
import base64
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from apiclient import errors, discovery

#Extract from IP WEBCAM

url='http://192.168.43.189:8080/shot.jpg?rnd=575177'
c=""
id=""
p=0
i=0
msg=""
while True:
   imgresp=urllib.urlopen(url)
   imgnp=np.array(bytearray(imgresp.read()),dtype=np.uint8)
   img=cv2.imdecode(imgnp,-1)
   cv2.imwrite('2.png',img)
   cv2.imshow('1',img)

#Decoding the Aadhar Qr code

   image=decode(Image.open('2.png'))
   if cv2.waitKey(1) & 0xFF == ord('q'):
           break
   for x in image:
      c=c+x.data
      i=i+1
   if (i!=0):
       print "Decoded Aadhar card\n"
       break


print c

#Extracting Aadhar number from string

o="uid=";

f=c.index(o, 0,len(c))

for i in range(f+5,f+17):
       id=id+c[i]

print "Decoded Aadhar number:"
print id
print"\n"

#Checking Aadhar number from Database

client=pymongo.MongoClient('localhost',27017)
db=client.Test
collection=db.test_collection
posts=db.posts
cursor=collection.find({"uid":id})
for x in cursor:
       p=p+1

# Mailing to Emergency service


if p==0:
        print "Not a Valid Aadhar Card"
else:
    SCOPES = 'https://www.googleapis.com/auth/gmail.send'
    CLIENT_SECRET_FILE = 'client_secret.json'
    APPLICATION_NAME = 'Gmail API'

    def get_credentials():
            home_dir = os.path.expanduser('~')
            credential_dir = os.path.join(home_dir, '.credentials')
            if not os.path.exists(credential_dir):
                   os.makedirs(credential_dir)
            credential_path = os.path.join(credential_dir, 'gmail-python-email-send.json')
            store = oauth2client.file.Storage(credential_path)
            credentials = store.get()
            if not credentials or credentials.invalid:
                   flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
                   flow.user_agent = APPLICATION_NAME
                   credentials = tools.run_flow(flow, store)
                   print('Storing credentials to ' + credential_path)
            return credentials

    def SendMessage(sender, to, subject, msgHtml, msgPlain):
            credentials = get_credentials()
            http = credentials.authorize(httplib2.Http())
            service = discovery.build('gmail', 'v1', http=http)
            message1 = CreateMessage(sender, to, subject, msgHtml, msgPlain)
            SendMessageInternal(service, "me", message1)

    def SendMessageInternal(service, user_id, message):
            try:
                message = (service.users().messages().send(userId=user_id, body=message).execute())
                print('Message Id: %s' % message['id'])
                return message
            except errors.HttpError as error:
                print('An error occurred: %s' % error)

    def CreateMessage(sender, to, subject, msgHtml, msgPlain):
            msg = MIMEMultipart('alternative')
            msg['Subject'] = subject
            msg['From'] = sender
            msg['To'] = to
            msg.attach(MIMEText(msgPlain, 'plain'))
            msg.attach(MIMEText(msgHtml, 'html'))
            raw = base64.urlsafe_b64encode(msg.as_string())
            raw = raw.decode()
            body = {'raw': raw}
            return body

    def main():
            to = "amogh7798@gmail.com"
            sender = "amogh7798@gmail.com"
            subject = "Test Subject"
            msgHtml = "Aadhar number:"+id
            msgPlain = "Aadhar number:"+id
            SendMessage(sender, to, subject, msgHtml, msgPlain)

    if __name__ == '__main__':
            main()