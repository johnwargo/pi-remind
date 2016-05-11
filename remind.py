#!/usr/bin/python
'''*****************************************************************************************************************
    Pi Remind
    By John M. Wargo
    www.johnwargo.com

    This application connects to a Google Calendar and determines whether there are any appointments in the next
    few minutes and flashes some LEDs if there are. The project uses a Raspberry Pi 2 device with a Pimoroni
    Unicorn HAT (an 8x8 matrix of bright, tri-colored LEDs) to display an obnoxious reminder at 10 minutes,
    5 minutes and 2 minutes.

    Google Calendar example code: https://developers.google.com/google-apps/calendar/quickstart/python
    Unicorn HAT example code: https://github.com/pimoroni/unicorn-hat/tree/master/python/examples
********************************************************************************************************************'''
# todo: Add support for snooze button
# todo: Add support for cancel button

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

# If modifying these scopes, delete your previously saved credentials at ~/.credentials/client_secret.json
SCOPES = 'https://www.googleapis.com/auth/calendar.readonly'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Pi Remind'


def show_activity_light(status):
    global current_activity_light

    # Turning on or off?
    if status:
        # on
        if current_activity_light > 6:
            current_activity_light = -1
        # increment the current light
        current_activity_light += 1
        # set the pixel
        lights.set_pixel(current_activity_light, 0, 0, 128, 0)
        # show the pixel
        lights.show()
    else:
        lights.off()


def flash_all_lights(flash_count, delay, red, green, blue):
    for index in range(flash_count):
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


def get_next_event(search_limit):
    # modified from https://developers.google.com/google-apps/calendar/quickstart/python
    print('Getting next event')
    # get all of the events on the calendar from now through 10 minutes from now
    now = datetime.datetime.utcnow()
    then = now + datetime.timedelta(minutes=search_limit)
    show_activity_light(True)
    # ask Google for the calendar entries
    events_result = service.events().list(
        calendarId='primary',
        timeMin=now.isoformat() + 'Z',
        timeMax=then.isoformat() + 'Z',
        # maxResults=10,
        singleEvents=True,
        orderBy='startTime').execute()
    show_activity_light(False)
    # Get the event list
    event_list = events_result.get('items', [])
    # did we get a return value?
    if not event_list:
        # no? Then no upcoming events at all.
        print(datetime.datetime.now(), "No entries returned")
        return None
    else:
        # we got a list, loop through them.
        for event in event_list:
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

    flash_all_lights(1, 0.25, 255, 165, 0)

    # initialize the last_event_id to an invalid value to start
    last_event_id = -1

    # initialize the lastMinute variable to the current time to start
    last_minute = datetime.datetime.now().minute
    # when starting, use the previous minute as lastMinute
    if last_minute == 0:
        last_minute = 59
    else:
        last_minute -= 1

    # infinite loop to process continuously check Google Calendar for future entries
    while 1:
        # calculate current minute
        # print("Last minute: ", lastMinute)
        current_minute = datetime.datetime.now().minute
        # print("Current minute: ", current_minute)

        # todo: Enforce business day start and end 8 AM to 6 PM?

        # is it the same as the last minute?
        if current_minute != last_minute:
            # reset last minute
            last_minute = current_minute
            # we've moved a minute
            # get the next calendar event (within the specified time limit [in minutes])
            next_event = get_next_event(10)
            # do we get an event?
            if next_event != None:
                # apparently we did. Woohoo!
                print("\nWe have an event!")

                # what time is it now?
                current_time = datetime.datetime.now()
                print("Current time: ", current_time)

                # When does the appointment start?
                # Pull the start dateTime as a string from the event object
                es = next_event['start'].get('dateTime')
                # Convert the string it into a Python dateTime object so we can do math on it
                event_start = datetime.datetime.strptime(es, '%Y-%m-%dT%H:%M:%S-04:00')
                print("Start time: ", event_start)

                # Figure out how many minutes to the appointment
                time_delta = event_start - current_time
                # Round to the nearest minute
                num_minutes = time_delta.total_seconds() // 60
                print("Next appointment in ", num_minutes, " minutes")

                # Has the appointment started yet?
                if current_time < event_start:
                    # is the appointment between 10 and 5 minutes from now?
                    if num_minutes >= 5:
                        # Flash the lights in white
                        flash_all_lights(1, 0.25, 255, 255, 255)
                    # is the appointment less than 5 minutes but more than 2 minutes from now?
                    elif num_minutes > 2:
                        # Flash the lights yellow
                        flash_all_lights(2, 0.25, 255, 255, 0)
                    # hmmm, less than 2 minutes, big red alarm!
                    else:
                        # flash the lights red
                        flash_all_lights(3, 0.25, 255, 0, 0)
            # wait a few (5) seconds then check again
            time.sleep(5)

    # this should never happen...
    print("Leaving main()")


# The app flashes a green light in the first row every time it connects to Google to check the calendar.
# The LED increments every time until it gets to the other side then starts over at the beginning again.
# The current_activity_light variable keeps track of which light lit last. At start it's at -1 and goes from there.
current_activity_light = -1
# Set a specific brightness level for the Pimoroni Unicorn HAT, otherwise it's pretty bright.
# Comment out the line below to see what the default looks like.
lights.brightness(1)

# Initialize the Google Calendar API stuff
credentials = get_credentials()
http = credentials.authorize(httplib2.Http())
service = discovery.build('calendar', 'v3', http=http)
# Now see what we're supposed to do next
if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print >> sys.stderr, '\nExiting by user request.\n'
        sys.exit(0)
