import smtplib
from email.message import EmailMessage

def email_alert(subject, body, to):
    try:
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
        print(f"Email sent to: {to}")
    except Exception as e:
        print(f"Error sending email: {e}")
        raise  #

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
    "Koodo" : "@msg.koodmobile.com"
}

def send_to(number="", provider = "", email = ""):
    if email:
        return email

    if number and provider:
        if len(number) != 10:
            print("Issue: Phone number must be 10 digits")
            return None
        if provider not in phone_providers:
            print("Issue: Unknown provider")
            return None
        return number + phone_providers[provider]

    print("Issue: You must provide either email or phone+provider")
    return None


if __name__ == '__main__':
    email_alert("Hey", "Hello world", send_to("3608270061", "Verizon"))
    email_alert("Hey", "Hello world", send_to("0", "", "xbar319@uw.edu"))

