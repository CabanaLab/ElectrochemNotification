# A script that emails people from the 'Cabana Server'
# This script was written by Mike Plews (2015). Email me with any questions!

# Import smtplib for the actual sending function
import smtplib
import codecs
# Here are the email package modules we'll need
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
import os, localsettings as ls, globalsettings as gs

username = ls.username
password = ls.password

def notify(user, user_email, file_name):
    COMMASPACE = ', '           # Allows multiple umail addresses to be used
        
    # Create the container (outer) email message.
    msg = MIMEMultipart()
    msg['Subject'] = 'Your Electrochemical Experiment is Done!'
    sender = ls.server_email
    to = user_email
    
    msg['From'] = '''Cabana Server <sender>'''
    if isinstance(user_email,list) and all(isinstance(x,str) for x in user_email):
        msg['To'] = COMMASPACE.join(to)
        user = COMMASPACE.join(user)
    elif isinstance(user_email,str):
        msg['To'] = to

    # html = """\
    # <html>
    #       <head></head>
    #       <body bgcolor="#FFFFFF" text="#000000">
    #       <p>Hello {user}, <br>
    #       </p>
    #       <p>You are receiving this email to notify you that your electrochemical experiment <em>"{file_name}"</em> has finished. Please collect it at your earliest convenience.</p>
    #       <p>Regards, <br>
    #       </p>
    #       <p>Cabana Server</p>
    #       <p><em>This message is automated: sent out by a bot that collects and distributes the relevant data. For questions, complaints, bug reports, or feature requests; please <a href="mailto:{moderator_email}">contact your moderator</a> ({version})</em></p>
    # </html>
    # """.format(user=user, file_name=file_name, moderator_email=ls.moderator_email, version=gs.version)

    html = make_message(user, file_name)
    
    msg.attach(MIMEText(html, 'html'))
 
    # Send the email via gmail SMTP server.
    s = smtplib.SMTP('smtp.gmail.com:587')
    s.starttls()
    s.login(username,password)
    s.sendmail(sender, msg['To'], msg.as_string())
    s.quit()
    print ('Success! Notification sent')


def make_message(user, file_name, settingsfile=ls):
    html = """\
    <html>
    <head></head>
    <body bgcolor="#FFFFFF" text="#000000">
    <p>Hello {user}, <br>
    </p>
    <p>You are receiving this email to notify you that your electrochemical experiment <em>"{file_name}"</em> has finished. Please collect it at your earliest convenience.</p>
    <p>Regards, <br>
    </p>
    <p>Cabana Server</p>
    <p><em>This message is automated: sent out by a bot that collects and distributes the relevant data. For questions, complaints, bug reports, or feature requests; please <a href="mailto:{moderator_email}">contact your moderator</a> ({version})</em></p>
    </html>
    """.format(user=user, file_name=file_name, moderator_email=settingsfile.moderator_email, version=gs.version)
    return html
