from __future__ import print_function
from apiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
import re
import datetime

# Setup the Gmail API
SCOPES = 'https://www.googleapis.com/auth/gmail.readonly'
store = file.Storage('credentials.json')
creds = store.get()
# if not creds or creds.invalid:
#     flow = client.flow_from_clientsecrets('client_secret.json', SCOPES)
#     creds = tools.run_flow(flow, store)
service = build('gmail', 'v1', http=creds.authorize(Http()))


def get_code():
    date = datetime.datetime.today()
    after = "{0:%Y/%m/%d}".format(date)
    before = "{0:%Y/%m/%d}".format(date + datetime.timedelta(days=1))
    query = "from:instagram subject:(アカウントの認証) after:" + after + " before:" + before
    result = service.users().messages().list(userId="me", q=query, maxResults=1).execute()
    msg = result.get("messages")
    msg_str = service.users().messages().get(userId="me", id=msg[0]["id"], format='raw').execute()
    code = re.findall("[0-9]{6}", msg_str["snippet"])
    return code[0]
