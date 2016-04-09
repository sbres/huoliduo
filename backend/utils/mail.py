import smtplib
from email.mime.text import MIMEText

# We use gmail SMTP. Why? Do you really want to setup a SMTP server?
def notify_mail(mail, subject, message):
    if mail.get('send', False) == False:
        return False
    if mail.get('Email_to_receive', []) == []:
        return False
    res = send_mail(mail.get("Email_to_send"),
              mail.get("Email_to_receive"),
              mail.get("Email_to_send_pass"),
              subject,
              message)
    return res

def send_mail(_from, to, mdp, subject, message):
	try:
		mail = MIMEText(message)
		mail['Subject'] = subject
		mail['From'] = _from
		mail['To'] = to
		s = smtplib.SMTP("smtp.zoho.com", 587)
		s.ehlo()
		s.starttls()
		s.ehlo
		s.login(_from, mdp)
		s.sendmail(_from, to, mail.as_string())
		s.quit()
		return True
	except Exception, e:
		return False

