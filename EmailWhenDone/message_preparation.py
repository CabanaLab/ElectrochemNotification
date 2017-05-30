# A script that prepares information lists to be emailed
# This script was written by Mike Plews (2015). Email me with any questions!
import sys
sys.path.append('./tests')

import send_notification, os, localsettings as ls, user_info as ui

def find_user(filename, user_list=ui):
    name_list, email_list = [], []
    for user in user_list.users:
        name, email, *ids = user
        for string in ids:
            if string in filename:
                name_list.append(name)
                email_list.append(email)
    return (name_list, email_list)

def message_me(message):
    send_notification.notify(ls.moderator, ls.moderator_email, message)
