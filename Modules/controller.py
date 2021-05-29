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

    def sanitize_report(self, report):
        # Store report according to the color codes
        ok_report = []
        medium_report = []
        red_report = []

        for data in report:
            if 'failed' in data[3]:
                red_report.append(data)
            else:
                medium_report.append(data)

        half_report = [item for elem in (red_report + medium_report) for item in elem]

        # check if a full successful backup was made
        if self.url_domain not in half_report:
            ok_report.append([self.url_domain, os.getenv('BACKUP_EMAIL'), "", "All Backed up",
                              "background-color:#ccffcc"])

        if self.url_domain_gw not in half_report:
            ok_report.append([self.url_domain_gw, os.getenv('BACKUP_EMAIL_GW'), "", "All Backed up",
                              "background-color:#ccffcc"])

        if self.url_domain2 not in half_report:
            ok_report.append([self.url_domain2, os.getenv('BACKUP2_EMAIL'), "", "All Backed up",
                              "background-color:#ccffcc"])

        return ok_report + medium_report + red_report

    def run(self):
        try:
            # Login to Backups website
            self.get_data.login()

            # Get the Report
            self.get_data.get_report(self.get_data.get_summary_page(self.url_domain), "domain")
            self.get_data.get_report(self.get_data.get_summary_page(self.url_domain_gw), "domainGW")
            self.get_data.get_report(self.get_data.get_summary_page(self.url_domain2), "domainPT2")

            # close the session
            self.get_data.s.close()

            # Send the sanitized report data on email
            self.send_email(self.sanitize_report(self.get_data.report))

        except requests.exceptions.ConnectionError as error:
            self.send_email(f"Unable to Access URL \n\n {error}")

        except AuthException:
            self.send_email("Wrong Username or Password")
