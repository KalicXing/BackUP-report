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
    def __init__(self):
        # Logins Access
        self.s = None
        self.username = os.getenv('USER')
        self.password = keyring.get_password(os.getenv('USER_KEY'), self.username)

        # Store the report Data
        self.report = []

        # URL to Access
        self.url = None

        # Tags to check
        self.tags = ['#ffff99', '#ffcccc']

    def login(self):
        # Login to the website
        self.s = requests.Session()
        self.s.verify = False
        self.s.auth = (self.username, self.password)

    def get_summary_page(self, url):
        # Get the Raw Data
        self.url = url
        return self.s.get(url)

    def get_report(self, page):
        soup = BeautifulSoup(page.text, 'html.parser')

        if bool(soup.findAll(text="Authorization Required")):
            raise AuthException

        if "Error" in soup.find('title').string:
            # Get the first line of the error message
            paragraphs = soup.findAll('p')
            for paragraph in paragraphs:
                self.report.append([self.url, self.url.split("/")[2], "",
                                    paragraph.text.strip().split("\n")[0], ""])

        else:
            for tag in self.tags:
                color_tag = soup.findAll('tr', {"bgcolor": tag})
                for tags in color_tag:
                    host = tags.text.strip().split("\n")[0]
                    status = tags.text.strip().split("\n")[-1]
                    style = "background-color:#ffcccc" if 'failed' in status else "background-color:#ffff99"
                    self.report.append([self.url, self.url.split("/")[2], host, status, style])


class AuthException(BaseException):
    pass
