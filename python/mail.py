"""
A quick and dirty email utility.
Created: 2014-03-06
"""

import os
import imaplib
import smtplib
import email
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage

class Mail(object):
	
	def __init__(self, subject='', from_address='', to_addresslist=['']):
		self.msgRoot = MIMEMultipart('related')
		self.msgAlternative = MIMEMultipart('alternative')
		self.msgRoot.attach(self.msgAlternative)
		self.subject = subject
		self.from_address = from_address
		self.to_addresslist = to_addresslist
		self.body = ''
		self.html_body = ''
	
	def setBody(self, body):
		self.body = body
	
	def setBodyHTML(self, html_body):
		self.html_body = html_body

	def setSubject(self, subject):
		self.subject = subject
	
	def setFromAddress(self, from_address):
		self.from_address = from_address

	def setToAddressList(self, to_addresslist):
		self.to_addresslist = to_addresslist

	def format(self):
		self.msgRoot['Subject'] = self.subject
		self.msgRoot['From'] = self.from_address
		self.msgRoot['To'] = ', '.join(self.to_addresslist)
		self.msgRoot.preamble = 'Multi-part message in MIME format.'
		if self.body:
			msgText = MIMEText(self.body)
			self.msgAlternative.attach(msgText)
		if self.html_body:
			msgText = MIMEText(self.html_body, 'html')
			self.msgAlternative.attach(msgText)

	def send(self, smtp_server = 'smtp.internal.analyticobjects.com'):
		self.format()
		smtp = smtplib.SMTP(smtp_server)
		smtp.sendmail(self.from_address, self.to_addresslist, self.msgRoot.as_string())
		smtp.quit()


def download_mail(user, password, dl_path = '.', imap_server = 'imap.internal.analyticobjects.com', delete = False, exts = None, logger = None):
	"""Get IMAP email."""
	serv = imaplib.IMAP4(imap_server)
	serv.login(user, password)
	serv.select()
	resp, data = serv.search(None, 'ALL')
	if resp != 'OK':
		raise SystemError('IMAP email search response not OK: %s' % resp)
	eids = data[0].split()
	dl_list = []
	for eid in eids:
		resp, data = serv.fetch(eid, '(RFC822)')
		em = email.message_from_bytes(data[0][1])
		em_subject = em['subject']
		em_from = em['from']
		em_to = em['to']
		if logger:
			logger.info('Email subject(%s), from(%s), to(%s).' % (em_subject, em_from, em_to))
		for part in em.walk():
			if part.get_content_maintype() == 'multipart':
				continue
			filename = part.get_filename()
			if filename is None or filename == '':
				continue
			if exts:
				keep = False
				for ext in exts:
					if filename.endswith(ext):
						keep = True
				if not keep:
					if logger:
						logger.info('Email attachment download skip: %s' % filename)
					continue
				else:
					if logger:
						logger.info('Email attachment download keep: %s' % filename)
			att_path = os.path.join(dl_path, filename)
			if not os.path.isfile(att_path):
				if logger:
					logger.info('Downloading email attachment: %s' % filename)
				dl_list.append(att_path)
				with open(att_path, 'wb') as fout:
					fout.write(part.get_payload(decode = True))
	if delete:
		for eid in eids:
			serv.store(eid, '+FLAGS', '\\Deleted')
		serv.expunge()
	serv.close()
	serv.logout()
	return dl_list


