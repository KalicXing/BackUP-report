import smtplib
from email.message import EmailMessage
from datetime import datetime
import keyring
import os
from dotenv import load_dotenv

load_dotenv()


class SendEmail:
    def __init__(self):
        # Email Access Logins
        self.username = os.getenv('EMAIL_USERNAME')
        self.password = keyring.get_password(os.getenv('USER_LOGIN'), os.getenv('EMAIL_USERNAME'))

        # Email addresses
        self.send_from_email = os.getenv('EMAIL_USERNAME')
        self.email = os.getenv('SEND_TO_EMAIL')
        self.cc_email = os.getenv('CC_EMAIL')

        # Custom Subject
        self.subject = None

        # Create the message
        self.message = EmailMessage()

    def create_message(self, reports):
        # Create the date Object
        now = datetime.now()

        # create the email message
        self.message['Subject'] = f"Backup Report as at {now.strftime('%H:%M')}" \
            if self.subject is None else self.subject
        self.message['From'] = self.send_from_email
        self.message['To'] = self.email
        self.message['Cc'] = self.cc_email

        # Send Html message
        heading = """\
                    <html>
                      <body>
                      <style>
                            th {
                                font-family:verdana;
                            }
                            th, td {
                                border-bottom: 1px solid #ddd;
                                padding: 15px;
                                text-align: left;
                            }
                            table {
                                border-collapse: collapse;
                                width: 100%;
                            }
                        </style>
                        <p>Hello ,</p>
                        <p>Find below backup report</p>
                           <table>
                            <tr>
                              <th>Server</th>
                              <th>Host</th>
                              <th>Last Attempt</th>
                            </tr>
                            """
        middle = ""

        try:
            for report in reports:
                middle += f"<tr style={report[4]}>"
                middle += f"<td> <a href={report[0]}> {report[1]} </td>"
                middle += "<td> " + report[2] + " </td>"
                middle += "<td> " + report[3] + " </td>"
                middle += "</tr>"

            bottom = """\
                             </table>
                               </body>
                             </html>
                """

            html = heading + middle + bottom

            self.message.add_alternative(html, subtype='html')

        except IndexError:
            self.message.set_content(reports)

    def send_email(self):
        with smtplib.SMTP(os.getenv('SMTP_SERVER'), 25) as smtp:
            smtp.ehlo()
            smtp.login(self.username, self.password)
            smtp.send_message(self.message)
