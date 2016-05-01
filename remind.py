#!/usr/bin/python
'''*****************************************************************************************************************
    PiRemind
    By John M. Wargo

    This application connects to a Google Calendar and determines whether there are any appointments in the next
     few minutes and flashes some LEDs if there are. The project uses a Raspberry Pi 2 device with a Pimoroni Unicorn
     HAT (an 8x8 matrix of bright, tri-colored LEDs) to display an obnoxious reminder at 10 minutes, 5 miniutes and
     2 minutes.

    Google Calendar example code: https://developers.google.com/google-apps/calendar/quickstart/python
    Unicorn HAT example code: https://github.com/pimoroni/unicorn-hat/tree/master/python/examples
********************************************************************************************************************'''
from __future__ import print_function

import datetime
import os
import sys
import time

import httplib2
import oauth2client
import unicornhat as unicorn
from apiclient import discovery
from oauth2client import client
from oauth2client import tools

try:
    import argparse

    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/calendar-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/calendar.readonly'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Google Calendar API Python Quickstart'


def flash_lights_orange(flashCount, delay, red, green, blue):
    for index in range(flashCount):
        for y in range(8):
            for x in range(8):
                unicorn.set_pixel(x, y, red, green, blue)
                unicorn.show()
        time.sleep(delay)
        unicorn.off()
        time.sleep(delay)


def get_credentials():
    # taken from https://developers.google.com/google-apps/calendar/quickstart/python
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir, 'pi_remind.json')
    store = oauth2client.file.Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else:  # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials


def getNextEvent(searchLimit):
    # modified from https://developers.google.com/google-apps/calendar/quickstart/python
    print('Getting next event')
    # get all of the events on the calendar from now through 10 minutes from now
    now = datetime.datetime.utcnow()
    then = now + datetime.timedelta(minutes=searchLimit)
    # ask Google for the calendar entries
    eventsResult = service.events().list(
        calendarId='primary',
        timeMin=now.isoformat() + 'Z',
        timeMax=then.isoformat() + 'Z',
        # maxResults=10,
        singleEvents=True,
        orderBy='startTime').execute()
    # Get the event list
    eventList = eventsResult.get('items', [])
    # did we get a return value?
    if not eventList:
        # no? Then no upcoming events at all.
        print(datetime.datetime.now(), "No entries returned")
        return None
    else:
        # we got a list, loop through them.
        for event in eventList:
            # we only care about events that have a start time
            start = event['start'].get('dateTime')
            if start:
                print("Event ", start, event['summary'])
                ts = time.strptime(start, '%Y-%m-%dT%H:%M:%S-04:00')
                print("Start: ", ts)
                return event
            else:
                print("Skipping " + event['summary'])


def main():
    print("Entering main()")

    flash_lights_orange(2, 0.25, 255, 165, 0)

    # initialize the lastEventID to an invalid value to start
    lastEventID = -1

    # initialize the lastMinute variable to the current time to start
    lastMinute = datetime.datetime.now().minute
    # when starting, use the previous minute as lastMinute
    if lastMinute == 0:
        lastMinute = 59
    else:
        lastMinute -= 1
    # print("Last minute: ", lastMinute)

    # continuous loop to process things forever
    while 1:
        # todo: check the last minute

        # get the next calendar event (within the specified time limit [in minutes])
        nextEvent = getNextEvent(10)
        # do we get an event?
        if nextEvent != None:
            print("We have an event!")
            # todo: calculate the time to the next appointment
            # how far is the appointment from now?
            # minLimit = nextEvent - datetime.datetime.now().minute
            # print("Next appointment in ", minLimit, " minutes")

        time.sleep(10)
    # this should never happen...
    print("Leaving main()")


# initialize the Google Calendar API stuff
credentials = get_credentials()
http = credentials.authorize(httplib2.Http())
service = discovery.build('calendar', 'v3', http=http)

# now see what we're supposed to do next
if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print >> sys.stderr, '\nExiting by user request.\n'
        sys.exit(0)
