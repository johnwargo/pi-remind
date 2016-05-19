#!/usr/bin/python
'''*****************************************************************************************************************
    Pi Remind
    By John M. Wargo
    www.johnwargo.com

    This application connects to a Google Calendar and determines whether there are any appointments in the next
    few minutes and flashes some LEDs if there are. The project uses a Raspberry Pi 2 device with a Pimoroni
    Unicorn HAT (an 8x8 matrix of bright, multi-colored LEDs) to display an obnoxious reminder every minute, changing
    color at 10 minutes (white), 5 minutes (yellow) and 2 minutes (red).

    Google Calendar example code: https://developers.google.com/google-apps/calendar/quickstart/python
    Unicorn HAT example code: https://github.com/pimoroni/unicorn-hat/tree/master/python/examples
********************************************************************************************************************'''
# todo: Enforce business day start and end 8 AM to 6 PM?
# todo: Only flash lights if a reminder is set for the appointment
# todo: Implement an interesting pattern for the final appointment alert (swirly lights for example)
# todo: On network connection error, increase delay between checks to minimize repeated warnings
# todo: Add support for snooze button
# todo: Add support for cancel button

from __future__ import print_function

import colorsys
import datetime
import os
import sys
import time

import httplib2
import numpy as np
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

# Google says: If modifying these scopes, delete your previously saved credentials at ~/.credentials/client_secret.json
# JMW says: On the pi, it's in /root/.credentials/
SCOPES = 'https://www.googleapis.com/auth/calendar.readonly'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Pi Reminder'
CALENDAR_ID = 'primary'
HASH = '#'
HASHES = '########################################'


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


def flash_random_lights(flash_count, delay):
    # Copied from https://github.com/pimoroni/unicorn-hat/blob/master/python/examples/random_blinky.py
    for index in range(flash_count):
        rand_mat = np.random.rand(8, 8)
        for y in range(8):
            for x in range(8):
                h = 0.1 * rand_mat[x, y]
                s = 0.8
                v = rand_mat[x, y]
                rgb = colorsys.hsv_to_rgb(h, s, v)
                r = int(rgb[0] * 255.0)
                g = int(rgb[1] * 255.0)
                b = int(rgb[2] * 255.0)
                lights.set_pixel(x, y, r, g, b)
        lights.show()
        time.sleep(delay)
        lights.off()
        time.sleep(delay)


def get_credentials():
    # taken from https://developers.google.com/google-apps/calendar/quickstart/python
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        print('Creating', credential_dir)
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
        print('Storing credentials to', credential_path)
    return credentials


def get_next_event(search_limit):
    # modified from https://developers.google.com/google-apps/calendar/quickstart/python
    # get all of the events on the calendar from now through 10 minutes from now
    print(datetime.datetime.now(), 'Getting next event')
    # this 'now' is in a different format (UTC)
    now = datetime.datetime.utcnow()
    then = now + datetime.timedelta(minutes=search_limit)
    # turn on a sequential green LED to show that you're requesting data from the Google Calendar API
    show_activity_light(True)
    try:
        # ask Google for the calendar entries
        events_result = service.events().list(
            # get all of them between now and 10 minutes from now
            calendarId=CALENDAR_ID,
            timeMin=now.isoformat() + 'Z',
            timeMax=then.isoformat() + 'Z',
            singleEvents=True,
            orderBy='startTime').execute()
        # turn off the green LED so you'll know data was returned from the Google calendar API
        show_activity_light(False)
        # Get the event list
        event_list = events_result.get('items', [])
        # did we get a return value?
        if not event_list:
            # no? Then no upcoming events at all, so nothing to do right now
            print(datetime.datetime.now(), 'No entries returned')
            return None
        else:
            # what time is it now?
            current_time = datetime.datetime.now()
            # loop through the events in the list
            for event in event_list:
                # we only care about events that have a start time
                start = event['start'].get('dateTime')
                # return the first event that has a start time
                # so, first, do we have a start time for this event?
                if start:
                    # When does the appointment start?
                    # Convert the string it into a Python dateTime object so we can do math on it
                    event_start = datetime.datetime.strptime(start, '%Y-%m-%dT%H:%M:%S-04:00')
                    # does the event start in the future?
                    if current_time < event_start:
                        # no? So we can use it
                        print('Found event:', event['summary'])
                        print('Event starts:', start)
                        # figure out how soon it starts
                        time_delta = event_start - current_time
                        # Round to the nearest minute and return with the object
                        event['num_minutes'] = time_delta.total_seconds() // 60
                        return event
    except:
        # well, something went wrong
        # light up the array with red LEDs to indicate a problem
        flash_all_lights(1, 2, 255, 0, 0)
        # not much else we can do here except to skip this attempt and try again later
        print('Error connecting to calendar:', sys.exc_info()[0], '\n')
    # if we got this far and haven't returned anything, then there's no appointments in the specified time
    # range, or we had an error, so...
    return None


def main():
    # initialize the lastMinute variable to the current time to start
    last_minute = datetime.datetime.now().minute
    # on startup, just use the previous minute as lastMinute
    if last_minute == 0:
        last_minute = 59
    else:
        last_minute -= 1

    # infinite loop to continuously check Google Calendar for future entries
    while 1:
        # get the current minute
        current_minute = datetime.datetime.now().minute
        # is it the same minute as the last time we checked?
        if current_minute != last_minute:
            # reset last_minute to the current_minute, of course
            last_minute = current_minute
            # we've moved a minute, so we have work to do
            # get the next calendar event (within the specified time limit [in minutes])
            next_event = get_next_event(10)
            # do we get an event?
            if next_event is not None:
                num_minutes = next_event['num_minutes']
                if num_minutes != 1:
                    print('Starts in', int(num_minutes), 'minutes\n')
                else:
                    print('Starts in 1.0 minute\n')
                # is the appointment between 10 and 5 minutes from now?
                if num_minutes >= 5:
                    # Flash the lights in white
                    flash_all_lights(1, 0.25, 255, 255, 255)
                # is the appointment less than 5 minutes but more than 2 minutes from now?
                elif num_minutes > 2:
                    # Flash the lights yellow
                    flash_all_lights(2, 0.25, 255, 255, 0)
                # hmmm, less than 2 minutes, almost time to start!
                else:
                    # flash the lights red
                    flash_all_lights(3, 0.25, 255, 0, 0)
        # wait a second then check again
        # You can always increase the sleep value below to check less often
        time.sleep(1)

    # this should never happen since the above is an infinite loop
    print('Leaving main()')


# now tell the user what we're doing...
print('\n')
print(HASHES)
print(HASH, 'Pi Remind                           ', HASH)
print(HASH, 'By John M. Wargo (www.johnwargo.com)', HASH)
print(HASHES)

# The app flashes a green light in the first row every time it connects to Google to check the calendar.
# The LED increments every time until it gets to the other side then starts over at the beginning again.
# The current_activity_light variable keeps track of which light lit last. At start it's at -1 and goes from there.
current_activity_light = -1

# Set a specific brightness level for the Pimoroni Unicorn HAT, otherwise it's pretty bright.
# Comment out the line below to see what the default looks like.
# lights.brightness(1)

# flash some random LEDs just for fun...
flash_random_lights(5, 0.1)
# blink all the LEDs green to let the user know the hardware is working
flash_all_lights(1, 1, 0, 128, 0)

# Initialize the Google Calendar API stuff
credentials = get_credentials()
http = credentials.authorize(httplib2.Http())
service = discovery.build('calendar', 'v3', http=http)

print('\nApplication initialized\n')

# Now see what we're supposed to do next
if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('\nExiting application\n')
        sys.exit(0)
