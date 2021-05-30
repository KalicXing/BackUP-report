import requests.exceptions
from Modules.get_data import GetData, AuthException
from Modules.send_email import SendEmail
from Modules.sanitize import Sanitize
import os
from dotenv import load_dotenv

load_dotenv()


class BackUp:
    def __init__(self):
        # URLS to access
        self.url_domain = os.getenv('BACKUP_LINK')
        self.url_domain_gw = os.getenv('BACKUP_LINK_GW')
        self.url_domain2 = os.getenv('BACKUP2_LINK')
        self.total_report = []

        # Priority levels
        self.ok = None

    @staticmethod
    def send_email(message):
        # Send the Report data via email
        send_email = SendEmail()

        if type(message) is str:
            send_email.email = send_email.cc_email
            send_email.subject = "! Error running Backup script check !"

        # Get the message
        send_email.create_message(message)

        # Send the combined Report
        send_email.send_email()

    def run(self):
        try:
            get_data = GetData()

            # Login to Backup website
            get_data.login()

            # Get the Reports for three websites
            get_data.get_report(get_data.get_summary_page(self.url_domain), os.getenv('DOMAIN'))
            get_data.get_report(get_data.get_summary_page(self.url_domain_gw), f"{os.getenv('DOMAIN')}GW")
            get_data.get_report(get_data.get_summary_page(self.url_domain2), f"{os.getenv('DOMAIN')}PT2")

            # close the session
            get_data.s.close()

            # Sanitize the report
            sanitize = Sanitize()

            # Send the sanitized report data on email
            self.send_email(sanitize.sanitize_report(get_data.report))

        except requests.exceptions.ConnectionError as error:
            self.send_email(f"Unable to Access URL \n\n {error}")

        except AuthException:
            self.send_email("Wrong Username or Password")
