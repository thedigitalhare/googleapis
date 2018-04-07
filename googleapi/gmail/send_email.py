from googleapi.get_credentials import get_credentials
from apiclient import discovery
import base64
from email import encoders
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import mimetypes
import os
import httplib2


def send_email(sender, to, subject, message_text, file_paths=None):
    """
    Create a message for an email.
    Args:
    sender: Email address of the sender.
    to: Email address of the receiver.
    subject: The subject of the email message.
    message_text: The text of the email message.
    file_dir: The directory containing the file to be attached.
    filename: The name of the file to be attached.
    Returns:
    An object containing a base64url encoded email object.
    """

    credentials = get_credentials('https://www.googleapis.com/auth/gmail.send')
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('gmail', 'v1', http=http)

    message = MIMEMultipart()
    message['to'] = to
    message['from'] = sender
    message['subject'] = subject

    body = MIMEText(message_text)
    message.attach(body)

    if file_paths:

        for file_path in file_paths:

            content_type, encoding = mimetypes.guess_type(file_path)

            if content_type is None or encoding is not None:
                content_type = 'application/octet-stream'
            main_type, sub_type = content_type.split('/', 1)

            if main_type == 'text':
                fp = open(file_path, 'rb')
                msg = MIMEText(fp.read(), _subtype=sub_type)
                fp.close()
            elif main_type == 'image':
                fp = open(file_path, 'rb')
                msg = MIMEImage(fp.read(), _subtype=sub_type)
                fp.close()
            elif main_type == 'audio':
                fp = open(file_path, 'rb')
                msg = MIMEAudio(fp.read(), _subtype=sub_type)
                fp.close()
            else:
                fp = open(file_path, 'rb')
                msg = MIMEBase(main_type, sub_type)
                msg.set_payload(fp.read())
                fp.close()

            encoders.encode_base64(msg)

            msg.add_header('Content-Disposition', 'attachment; filename=' + os.path.basename(file_path))
            message.attach(msg)

    raw = base64.urlsafe_b64encode(message.as_bytes())
    raw = raw.decode()

    final_message = {'raw': raw}

    email = service.users().messages().send(userId='me', body=final_message).execute()

    return email['id']
