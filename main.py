from bot import As
from email_functions import EO
from time import sleep
import threading

"""
write your email id and password 
"""
emailId = "user email id "
password = "user email id password"

a = As(None, 150, threshold = 750)
print("Assistant object created")
e = EO(emailId, password)
print("Email object Created")
print("clearing background noise ..")

instructions = """
            Here are the instructions. 
            Send - to send an email to anyone.
            read - to read emails from your inbox.
            Stop - to stop the service .
            """


def check_mails(bot, email, interval):

    while True:
        newMails = email.check()
        if newMails > 0:
            if alerts == True:
                bot.speak("You have "+str(newMails)+" new email")
        sleep(interval)

def get_details(msg, classType, runTime = 5):
    loop = True
    while loop:
        try:
            details = classType(a.listen(msg, timeLimit = runTime).lower().replace(" ",""))
        except ValueError:
            a.speak("input not valid ")
            continue
        if details == "":
            a.speak("speak something")
            continue
    
        if classType == str:
            details = details.lower()

        while True:
            check = a.listen(f" you mean {details}?", timeLimit = runTime)

            if check == "yes":
                loop = False
                break
            elif check == "no":
                break
            else:
                a.speak("could not recognized")
    return details

def send():
    print("preparing to send email")

    to = get_details("Say receivers id, only before the at the rate symbol", str)

    print("To : ",to)

    mailProvider = get_details("tell receivers mail provider", str)
    print("Provider : ",mailProvider)

    subject = get_details("what is the subject", str, 10)
    print("\nSubject\n : ",subject)

    body = get_details("Say body of email", str, 20)
    print("\nBody\n : ",body)

    res = e.send(to+"@"+mailProvider+".com", subject, body)

    return res

def read():
    
    readcount = get_details("How many emails should i read?", int)
    a.speak(f"reading {readcount} email.")
    print(f"reading {readcount} email.")
    for sender, subject, body in e.fetch(readcount):
        print("Email : \n", sender, "\n", subject, "\n", body)

        a.speak("New Email")
        a.speak(f"From : {sender}")
        a.speak(f"Subject : {subject}")
        a.speak(f"Body : {body}")

    return "service done"


def main():
    id = get_details("What would you like to name me ?", str, 5)
    id = id[0].upper()+id[1:]

    a.set_id(id)
    print("\nAssistant named to : ",a.get_id())

    a.speak(f"You can continue with the service , by saying {id}")

    stopper = a.listen_constantly()

    emailAlertThread = threading.Thread(target = check_mails, kwargs = dict(bot = a, email = e, interval = 10))
    emailAlertThread.daemon = True
    emailAlertThread.start()


    global alerts
    alerts = True
    service = True
    while service:
        recognized_audio = a.get_recognized_audio()

        if recognized_audio not in ("", None) and recognized_audio.split()[-1] == id:

            a.set_recognized_audio(None)

            command = a.listen(" yes ", timeLimit = 5)
            print("Command : ",command, end = "")

            if command.lower() in ("send"):
                a.speak(send())
            
            elif command.lower() in ("read"):
                a.speak(read())
            
            elif command.lower() in ("instructions"):
                a.speak(instructions)
            
            elif command.lower() == "stop":
                print("\nUser asked to stop the service")
                stopper()
                service =False
            
            else:
                print("None")
                a.speak("sorry didn't get you ")

main()

print("Service stopped")
print("Made by : Pratham")

sleep(2)