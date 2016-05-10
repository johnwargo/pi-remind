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
import unicornhat as lights
from apiclient import discovery
from oauth2client import client
from oauth2client import tools

try:
    import argparse

    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/client_secret.json
SCOPES = 'https://www.googleapis.com/auth/calendar.readonly'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Pi Remind'


def show_activity_light(status):
    global currentActivityLight

    # Turning on or off?
    if status:
        # on
        if currentActivityLight == 7:
            currentActivityLight = -1
        # increment the current light
        currentActivityLight += 1
        # set the pixel
        lights.set_pixel(currentActivityLight, 0, 0, 128, 0)
        # show the pixel
        lights.show()
    else:
        lights.off()


def flash_lights_orange(flashCount, delay, red, green, blue):
    for index in range(flashCount):
        for y in range(8):
            for x in range(8):
                lights.set_pixel(x, y, red, green, blue)
                lights.show()
        time.sleep(delay)
        lights.off()
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
    show_activity_light(True)
    # ask Google for the calendar entries
    eventsResult = service.events().list(
        calendarId='primary',
        timeMin=now.isoformat() + 'Z',
        timeMax=then.isoformat() + 'Z',
        # maxResults=10,
        singleEvents=True,
        orderBy='startTime').execute()
    show_activity_light(False)
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
            # return the first event that has a start time
            if start:
                print("Event ", start, event['summary'])
                return event
            else:
                # otherwise skip the event
                print("Skipping " + event['summary'])
        # if we got this far and haven't returned anything, then there's no appointments in the specified time
        # window. So, return None
        return None


def main():
    print("Entering main()")

    flash_lights_orange(1, 0.25, 255, 165, 0)

    # initialize the lastEventID to an invalid value to start
    lastEventID = -1

    # initialize the lastMinute variable to the current time to start
    lastMinute = datetime.datetime.now().minute
    # when starting, use the previous minute as lastMinute
    if lastMinute == 0:
        lastMinute = 59
    else:
        lastMinute -= 1

    # infinite loop to process continuously check Google Calendar for future entries
    while 1:
        # calculate current minute
        # print("Last minute: ", lastMinute)
        currentMinute = datetime.datetime.now().minute
        # print("Current minute: ", currentMinute)

        # is it the same as the last minute?
        if currentMinute != lastMinute:
            # reset last minute
            lastMinute = currentMinute
            # we've moved a minute
            # get the next calendar event (within the specified time limit [in minutes])
            nextEvent = getNextEvent(10)
            # do we get an event?
            if nextEvent != None:
                # apparently we did. Woohoo!
                print("\nWe have an event!")

                # what time is it now?
                currentTime = datetime.datetime.now()
                print("Current time: ", currentTime)

                # When does the appointment start?
                # Pull the start dateTime as a string from the event object
                es = nextEvent['start'].get('dateTime')
                # Convert the string it into a Python dateTime object so we can do math on it
                eventStart = datetime.datetime.strptime(es, '%Y-%m-%dT%H:%M:%S-04:00')
                print("Start time: ", eventStart)

                # figure out how many minutes to the appointment
                timeDelta = eventStart - currentTime
                # Round to the nearest minute
                numMinutes = timeDelta.total_seconds() // 60
                print("Next appointment in ", numMinutes, " minutes")

                # Has the appointment started yet?
                # if currentTime < eventStart:

            time.sleep(5)

    # this should never happen...
    print("Leaving main()")


# the app flashes a green light in the first row every time it connects to Google to check the calendar.
# The LED increments every time until it gets to the other side then starts over at the beginning again.
# the currentActivityLight variable keeps track of which light lit last. At start it's at -1 and goes from there.
currentActivityLight = -1
# set a specific brightness level for the Pimoroni Unicorn HAT, otherwise it's pretty bright
# comment out the line below to see what the default looks like
lights.brightness(1)

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
