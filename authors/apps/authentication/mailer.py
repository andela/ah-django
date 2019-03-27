import sendgrid
import os
from sendgrid.helpers.mail import Email, Content, Mail



class RecoverPassword:

    def send_email(self):

        sg = sendgrid.SendGridAPIClient(
            api_key=os.environ.get('SENDGRID_API_KEY'))
        from_email = Email("misochobrian01@gmail.com")
        to_email = Email("misochobrian@gmail.com")
        subject = "Sending with sendgrid is Fun"
        content = Content(
            "text/plain", "and easy to do anywhere, even with python")
        mail = Mail(from_email, subject, to_email, content)
        response = sg.client.mail.send.post(request_body=mail.get())
        return response
