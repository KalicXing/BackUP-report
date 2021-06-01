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
        self.links = [os.getenv('BACKUP_LINK'),
                      os.getenv('BACKUP_LINK_GW'),
                      os.getenv('BACKUP2_LINK')
                      ]

    @staticmethod
    def send_email(message):
        # Send the Report data via email
        send_email = SendEmail()

        if type(message) is str:
            send_email.email = send_email.sys_Admin
            send_email.subject = "! Error running Backup script check !"

        # Create the message
        send_email.create_message(message)

        # Send the combined Report
        send_email.send_email()

    def run(self):
        try:
            get_data = GetData()

            # Login to Backup website
            get_data.login()

            # Get the Reports from the websites
            for link in self.links:
                get_data.get_report(get_data.get_summary_page(link))

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
