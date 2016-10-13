# A script that prepares information lists to be emailed
# This script was written by Mike Plews (2015). Email me with any questions!
import send_notification, os, localsettings as ls

def open_user_info():
	user_list, email_list = [],[]
	user_info = open(ls.user_info, 'r')	# '\t' delimited, 'user \t user_email'
	for line in user_info:
		columns = line.split('\t') 		# splits lines into columns, 'tab' delimiter
		user_list.append(columns[0])
		email_list.append(columns[1].rstrip())
	return (user_list, email_list)
	
def find_user(filename):
	user, email = [],[]
	user_info = open_user_info()
	user_list = user_info[0]
	email_list = user_info[1]
	for line in user_list:
		if line in filename:
			user_line = line
			email_line = email_list[user_list.index(user_line)]
			user.append(user_line)
			email.append(email_line)
	return (user, email)

def message_me(message):
	send_notification.notify(ls.moderator, ls.moderator_email, message)
