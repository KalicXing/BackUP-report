import requests
import keyring
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from bs4 import BeautifulSoup
import os
from dotenv import load_dotenv

load_dotenv()

# remove the SSL verification warnings
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


class GetData:
    def __init__(self, url):
        # Logins Access
        self.s = None
        self.username = os.getenv('USER')
        self.password = keyring.get_password(os.getenv('USER_KEY'), self.username)

        # Store the report Data
        self.report = []

        # URL to Access
        self.url = url

        # Tags to check
        self.tags = ['#ffff99', '#ffcccc']

        # Priority levels
        self.danger = 1
        self.medium = 2
        self.ok = 3

    def login(self):
        # Login to the website
        self.s = requests.Session()
        self.s.verify = False
        self.s.auth = (self.username, self.password)

    def get_summary_page(self, url):
        # Get the Raw Data
        return self.s.get(url)

    def get_report(self, page, which_report):
        soup = BeautifulSoup(page.text, 'html.parser')

        if bool(soup.findAll(text="Authorization Required")):
            raise AuthException

        else:
            for tag in self.tags:
                red_tags = soup.findAll('tr', {"bgcolor": tag})
                for tags in red_tags:
                    host = tags.text.strip().split("\n")[0]
                    status = tags.text.strip().split("\n")[-1]
                    style = "background-color:#ffcccc" if 'failed' in status else "background-color:#ffff99"
                    priority = self.danger if 'failed' in status else self.medium
                    if which_report == os.getenv('DOMAIN'):
                        self.report.insert(priority, [self.url[0], os.getenv('BACKUP_EMAIL'), host, status, style])
                    elif which_report == f"{os.getenv('DOMAIN')}GW":
                        self.report.insert(priority, [self.url[1], os.getenv('BACKUP_EMAIL_GW'), host, status, style])
                    elif which_report == f"{os.getenv('DOMAIN')}PT2":
                        self.report.insert(priority, [self.url[2], os.getenv('BACKUP2_EMAIL'), host, status, style])


class AuthException(BaseException):
    pass
