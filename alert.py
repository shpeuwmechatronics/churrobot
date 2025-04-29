import smtplib
from email.message import EmailMessage

def email_alert(subject, body, to):
    msg = EmailMessage()
    msg.set_content(body)
    msg['subject'] = subject
    msg['to'] = to

    user = "xavierbarragan1835@gmail.com"
    msg['from'] = user
    password = "jvazvtiwegleyfeh"

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(user, password)
    server.send_message(msg)

    server.quit()

phone_providers = {
    "AT&T" : "@txt.att.net",
    "Boost Mobile" : "@sms.myboostmobile.com",
    "Cricket Wireless" : "@mms.cricketwireless.net",
    "Goofle Project Fi" : "@msg.fi.google.com",
    "Republic Wireless" : "@text.republicwireless.com",
    "Sprint" : "@messaging.sprintpcs.com",
    "Straight Talk" : "@vtext.com",
    "T-Mobile" : "@tmomail.et",
    "Ting" : "@message.ting.com",
    "U.S. Cellular" : "@email.uscc.net",
    "Verizon" : "@vtext.com",
    "Virgin Mobile" : "@vmobl.com",
    "Bell Mobility" : "@txt.bellmobility.com",
    "Rogers" : "@pcs.rogers.com",
    "Fido" : "@fido.ca",
    "Telus" : "@msg.telus.com",
    "Koodo" : "@msg.koodmobile.com",
    "Virgin Mobile" : "@vmobile.ca"
}

def send_to(number, provider = "", email = ""):
    gateway = ""
    if len(provider) != 0: 
        if (len(number) != 10):
            print("Issue with phone number")
        elif provider not in phone_providers.keys():
            print("Issue with provider name")
        else:
            gateway = number + phone_providers.get(provider)
    elif len(email) != 0:
        gateway = email

    return gateway


if __name__ == '__main__':
    email_alert("Hey", "Hello world", send_to("3608270061", "Verizon"))
    email_alert("Hey", "Hello world", send_to(0, "", "xbar319@uw.edu"))

