import smtplib
import imaplib
from dotenv import load_dotenv
import os
import pandas as pd
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


class EmailManager:
    def __init__(self, smtp_server, port, imap_server):
        self.smtp_server = smtp_server
        self.port = port
        self.imap_server = imap_server
        self.sender = os.getenv("sender")
        self.password = os.getenv("password")

    def send_html_message(self, topic, name_file_data, path_to_data=''):
        df = pd.read_csv(f"{path_to_data}{name_file_data}.csv")
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(self.smtp_server, self.port, context=context) as server:
            server.login(self.sender, self.password)
            for idx in range(len(df)):
                message = MIMEMultipart()
                message["Subject"] = topic
                message["From"] = self.sender
                message["To"] = df.at[idx, 'email']
                html = df.at[idx, 'html']
                part = MIMEText(html, "html")
                message.attach(part)
                server.send_message(message)

    def search_messages_by_sender(self, sender_address):
        with imaplib.IMAP4_SSL(self.imap_server) as server:
            server.login(self.sender, self.password)
            server.select("INBOX")
            _, messages_ids = server.search(None, f'FROM "{sender_address}"')
            return messages_ids

    def read_messages(self, messages_ids):
        with imaplib.IMAP4_SSL(self.imap_server) as server:
            server.login(self.sender, self.password)
            server.select("INBOX")
            for idx in messages_ids:
                server.store(idx, '+FLAGS', '\\Seen')

if __name__ == "__main__":
    load_dotenv()
    email_manager = EmailManager("smtp.yandex.ru", 465, "imap.yandex.ru")
    email_manager.send_html_message("Поздравление с Новым Годом", "New Year greetings")
    email_idx = email_manager.search_messages_by_sender("tyutyunin2004@mail.ru")
    email_manager.read_messages(email_idx)