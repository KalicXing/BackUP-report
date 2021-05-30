import os
from dotenv import load_dotenv

load_dotenv()


class Sanitize:
    def __init__(self):
        # Website URLS
        self.url_domain = os.getenv('BACKUP_LINK')
        self.url_domain_gw = os.getenv('BACKUP_LINK_GW')
        self.url_domain2 = os.getenv('BACKUP2_LINK')

    def sanitize_report(self, report):
        # Store report according to the color codes
        ok_report = []
        medium_report = []
        red_report = []

        # In case no data was found, stores the error message
        unknown_report = []

        for data in report:
            if '#ffcccc' in data[4]:
                red_report.append(data)
            elif '#ffff99' in data[4]:
                medium_report.append(data)
            else:
                unknown_report.append(data)

        # Combine the color reports
        color_reports = red_report + medium_report + unknown_report

        # Split the list in list to strings for easier check
        half_report = [item for elem in color_reports for item in elem]

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

        total_report = ok_report + unknown_report + medium_report + red_report

        return total_report
