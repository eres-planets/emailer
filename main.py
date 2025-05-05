'''
https://developers.google.com/workspace/gmail/api/guides/sending#python
'''
import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from email.mime.text import MIMEText
import base64
import pandas as pd

SUBJECT = 'ERES Abstract Decision'

TEMPLATES = {
    'NEED_TRAVEL_TALK': '''
Dear {name},

Thank you for your interest in ERES X. We received your request for travel support. Unfortunately, we are not able to provide financial support for travel at this time. However, should you still be able to attend, we still expect to be able to provide housing support for you, and you have been assigned an oral presentation.

If you have changed your mind and would be able to attend ERES with housing support alone, please fill out https://forms.gle/qiTEqQLPC4ha8JsU8. Otherwise, we thank you for your interest in ERES and hope to see you again in more financially favorable times!

Warmly,
The ERES X Organizing Committee
''',

    'NEED_TRAVEL_POSTER': '''
Dear {name},

Thank you for your interest in ERES X. We received your request for travel support. Unfortunately, we are not able to provide financial support for travel at this time. However, should you still be able to attend, we still expect to be able to provide housing support for you, and you have been assigned a poster presentation. You may also be provided option of being switched to an oral presentation should you like, availability permitting.

If you have changed your mind and would be able to attend ERES with housing support alone, please fill out https://forms.gle/qiTEqQLPC4ha8JsU8. Otherwise, we thank you for your interest in ERES and hope to see you again in more financially favorable times!

Warmly,
The ERES X Organizing Committee
''',


    'NO_NEED_ORAL': '''
Dear {name},

Thank you for your interest in ERES X. We received your registration and your volunteering to decline all forms of funding support; we thank you enormously for your selection, which has allowed us to maximize the reach of ERES X on a limited budget! You have been assigned an oral presentation slot, with a schedule to be announced shortly.

Please let us know whether you still expect to attend ERES X in absence of travel support by filling out https://forms.gle/qiTEqQLPC4ha8JsU8.

We look forward to hopefully seeing you at Princeton for ERES X shortly!
The ERES X Organizing Committee
''',

    'NO_NEED_POSTER': '''
Dear {name},

Thank you for your interest in ERES X. We received your registration and your volunteering to decline all forms of funding support; we thank you enormously for your selection, which has allowed us to maximize the reach of ERES X on a limited budget! You have been assigned a poster presentation slot as requested, with a schedule to be announced shortly.

Please let us know whether you still expect to attend ERES X in absence of travel support by filling out https://forms.gle/qiTEqQLPC4ha8JsU8.

We look forward to hopefully seeing you at Princeton for ERES X shortly!
The ERES X Organizing Committee


P.S. Hi Tiger you're the only one getting this email template I hope you feel special <3
''',

    'HOUSING_ORAL': '''
Dear {name},

Thank you for your interest in ERES X. We received your registration and your request for housing support. We are delighted to offer you the option to be housed on Princeton campus at Bloomberg Hall in a single-occupancy room at no cost to you for the nights of Sunday, June 15, and Monday, June 16. Additionally, you have been assigned an oral presentation slot, with a schedule to be announced shortly.

Please let us know whether you still expect to attend ERES X in absence of travel support by filling out https://forms.gle/qiTEqQLPC4ha8JsU8.

We look forward to hopefully seeing you at Princeton for ERES X shortly!
The ERES X Organizing Committee
''',

    'HOUSING_POSTER': '''
Dear {name},

Thank you for your interest in ERES X. We received your registration and your request for housing support. We are delighted to offer you the option to be housed on Princeton campus at Bloomberg Hall in a single-occupancy room at no cost to you for the nights of Sunday, June 15, and Monday, June 16. Additionally, you have been tentatively assigned a poster slot, with the option of being switched to an oral presentation should availability arise, and should you prefer.

Please let us know whether you still expect to attend ERES X in absence of travel support by filling out https://forms.gle/qiTEqQLPC4ha8JsU8.

We look forward to hopefully seeing you at Princeton for ERES X shortly!
The ERES X Organizing Committee
''',

    'HOUSING_NONE': '''
Dear {name},

Thank you for your interest in ERES X. We received your registration and your request for housing support. Unfortunately, since you are not presenting your work, we are unable to offer you housing at this time.

Should you like to change your selection and present an abstract, please let us know; we still expect to be able to provide housing support for you! Otherwise, we thank you for your interest in ERES and hope to see you again in future years.

Warmly,
The ERES X Organizing Committee
''',
}

def draft_email(name, talk_type):
    return TEMPLATES[talk_type].format(name=name)

def send_email(to, subject, body):
    SCOPES = ['https://www.googleapis.com/auth/gmail.send']
    def get_gmail_service():
        creds = None
        if os.path.exists('token.json'):
            creds = Credentials.from_authorized_user_file('token.json', SCOPES)
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token.json', 'w') as token:
                token.write(creds.to_json())

        service = build('gmail', 'v1', credentials=creds)
        return service

    def create_message(sender, to, subject, message_text):
        message = MIMEText(message_text)
        message['to'] = to
        message['from'] = sender
        message['subject'] = subject
        return {'raw': base64.urlsafe_b64encode(message.as_bytes()).decode()}
    service = get_gmail_service()
    message = create_message("eresorganizers@gmail.com", to, subject, body)
    send_message = service.users().messages().send(userId="me", body=message).execute()
    print('\tSent email to "%s" ("%s")' % (to, subject))

if __name__ == '__main__':
    # dat = pd.read_csv('outsheet.csv')
    dat = pd.read_csv('test.csv')
    for i, row in dat.iterrows():
        # skip first two heading rows
        if i < 2:
            continue
        print(row['Email'], SUBJECT, row['Name'], row['Email Type'])
        send_email(row['Email'], SUBJECT, draft_email(row['Name'], row['Email Type']))
