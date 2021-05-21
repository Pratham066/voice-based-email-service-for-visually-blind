from email.header import decode_header
from bs4 import BeautifulSoup
import smtplib
import imaplib
import email
import re


class EO:
    
    def __init__(user,email,password):

        user.emailAddress = email
        user.emailPassword = password
        user.emailProvider = email.split("@")[1]
        user.latestMailId = None
    
    def set_emailAddress(user, email):
        user.emailAddress = email
    
    def set_emailPassword(user, password):
        user.emailPassword = password

    def send(user,recipient,subject,body):
        try:
            with smtplib.SMTP_SSL('smtp.'+user.emailProvider, 465) as smtp:

                smtp.login(user.emailAddress, user.emailPassword)
                msg = f'Subject: {subject}\n\n\n{body}'
                smtp.sendmail(user.emailAddress,recipient, msg)
                return "Email sent"
        except Exception as ex:
            return "Couldn't send email "+str(ex)
    
    def get_body(user,msg):
        if msg.is_multipart():
            return user.get_body(msg.get_payload(0))
        else:
            return msg.get_payload(None, True)
    
    def replace(user, string, regex, replaceWith):
        string = re.sub(regex, replaceWith, string)
        return string

    def fetch(user, fetchCount):
        try:
            with imaplib.IMAP4_SSL('imap.'+user.emailProvider) as imap:
                imap.login(user.emailAddress,user.emailPassword)
                status, messages = imap.select('INBOX')
                messages = messages[0]

                for i in range(fetchCount):
                    messages = bytes(str(int(messages)-i),"utf-8")

                    status, data = imap.fetch(messages, "(RFC822)")
                    data = data[0][1]

                    rawMsg = email.message_from_bytes(data)
                    subject = rawMsg["subject"]
                    sender = rawMsg["from"]

                    body = user.get_body(rawMsg).decode("utf-8")
                    body = BeautifulSoup(body, "html.parser").get_text()
                    body = user.replace(body, r"http\S+","Link.")  
                    body = user.replace(body, r"\r|\n","")  

                    yield sender, subject, body
        except Exception as ex:
            return "Couldn't fetch email "+str(ex)

    #Checks for new emails
    def check(user):
        try:
            with imaplib.IMAP4_SSL('imap.'+user.emailProvider) as imap:
                imap.login(user.emailAddress,user.emailPassword)
                # print(imap.list())
                status, message = imap.select('INBOX', readonly = True)
                # print(message)
                result, data = imap.uid("search", None, "ALL")
                # print(data)
                idList = data[0].split()
                # print(idList)

                if user.latestMailId == None:
                        user.latestMailId = idList[-1]

                mailCount = len(idList) - idList.index(user.latestMailId) - 1
                # print(mailCount)
                user.latestMailId = idList[-1]
                
                return mailCount
        except Exception as ex:
            return 0
            

    def delete(user,emailId):
        pass