import requests.exceptions
from Modules.get_data import GetData, AuthException
from Modules.send_email import SendEmail
import os
from dotenv import load_dotenv

load_dotenv()

class BackUp:

    def __init__(self):
        # URLS to access
        self.url_domain = os.getenv('BACKUP_LINK')
        self.url_domain_gw = os.getenv('BACKUP_LINK_GW')
        self.url_domain2 = os.getenv('BACKUP2_LINK')

        self.get_data = GetData([self.url_domain, self.url_domain_gw, self.url_domain2])
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
            # Login to Backups
            self.get_data.login()

            # Get the Report
            self.get_data.get_report(self.get_data.get_summary_page(self.url_domain), "domain")
            self.get_data.get_report(self.get_data.get_summary_page(self.url_domain_gw), "domainGW")
            self.get_data.get_report(self.get_data.get_summary_page(self.url_domain2), "domainPT2")

            # close the session
            self.get_data.s.close()

            # Sanitize the report if no failed Backup
            self.total_report = [item for elem in self.get_data.report for item in elem]

            # Insert at the last position
            self.ok = len(self.total_report)

            if self.url_domain not in self.total_report:
                self.get_data.report.insert(self.ok,
                                            [self.url_domain, os.getenv('BACKUP_EMAIL'), "", "All Backed up",
                                             "background-color:#ccffcc"])
            if self.url_domain_gw not in self.total_report:
                self.get_data.report.insert(self.ok,
                                            [self.url_domain_gw, os.getenv('BACKUP_EMAIL_GW'), "", "All Backed up",
                                             "background-color:#ccffcc"])
            if self.url_domain2 not in self.total_report:
                self.get_data.report.insert(self.ok,
                                            [self.url_domain2, os.getenv('BACKUP2_EMAIL'), "", "All Backed up",
                                             "background-color:#ccffcc"])

            # Send the report data on email but in reverse order
            self.send_email(self.get_data.report[::-1])

        except requests.exceptions.ConnectionError as error:
            self.send_email(f"Unable to Access URL \n\n {error}")

        except AuthException:
            self.send_email("Wrong Username or Password")
