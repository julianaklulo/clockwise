import httplib2
import os

import apiclient
import oauth2client
from oauth2client import client, tools

from datetime import datetime, timedelta

alarm_time = datetime.utcnow() + timedelta(minutes = 1)

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

SCOPES = 'https://www.googleapis.com/auth/calendar.readonly'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Clockwise'


def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'clockwise.json')

    store = oauth2client.file.Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatability with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials


def getEvents():
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = apiclient.discovery.build('calendar', 'v3', http=http)

    now = datetime.utcnow().isoformat() + 'Z'
    tomorrow = (datetime.utcnow() + timedelta(1)).isoformat() + 'Z'

    eventsResult = service.events().list(
        calendarId='primary', timeMin=now, timeMax=tomorrow,
        maxResults=10, singleEvents=True, orderBy='startTime').execute()
    events = eventsResult.get('items', [])

    if not events:
        return ("Nada agendado!")
    events_data = ""
    events_qty = 0
    for event in events:
        event_time = event['start'].get('dateTime')
        if event['summary'] == "Alarm":
            set_alarm_time(event_time[11:19])
        else:
            events_data += "%s %s " % (event_time[11:16], event['summary'])
            events_qty += 1
    if events_qty == 0:
        return ("Nada agendado!")
    return events_data


def set_alarm_time(time): 
    global alarm_time
    alarm_time = datetime.strptime(time, "%H:%M:%S")
    print("alarm set")
