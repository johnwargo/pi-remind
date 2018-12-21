# Changelog

## 2018-12-21

- Added a reboot timer to `remind.py`. I noticed that when I lost power in the house, the PI would come up before my network did, and never reconnect. So, when you set `REBOOT_COUNTER_ENABLED` to `True` and specify a reboot counter in `REBOOT_NUM_RETRIES` (it defaults to 10), the app will count how many times the API fails to connect, then reboots the Pi.
 
    Right now, the code doesn't check for the type of error, so any failure in checking the Google Calendar will trigger the reboot counter. the **right** way to do this would be to figure out what all the possible errors are, and trigger this only for network errors. I've been running this app in my office fr years now, so I feel comfortable with the code the way it is. 

- Added a socket timeout to `remind.py`. As I started testing this code, I noticed that the big `except` I use to catch errors connecting to the Google Calendar API was hanging. A recent update to the Google API library, or something else on the Pi was causing this to fail now when it wasn't failing before, so I added the timeout to force the error.
    
- Refactored the startup script `start-remind.py`. As I was testing the updates to the Python code, I realized that I wanted the shell script to show me which *version* of the python app it was running (by file date).  


## 2017-04-17

While my home internet connection was out one day, I noticed that the application always sets the indicator LED to blue while it's checking for new calendar events. As a user, this is confusing to me as it makes me believe that things are OK when I see that the LED is blue. So, to fix this, I added a `has_error` variable that the application checks to see if the previous calendar check resulted in an error, in this case it leaves the LED red. Also added a try/except block around the initialization code that checks the user's credentials with Google. If the network's not available, the existing code fails catastrophically, so I thought it would be nice to indicate the error with all red LEDs then exit the app.

## 2016-08-23

Added an updated .desktop file (`start-remind.desktop`) back to the project. This one actually works. ;-) 

## 2016-08-21

Removed .desktop file and replaced it with a shell script that actually works. Made some major edits to the readme.md file.

## 2016-08-16

Changed activity lights to blue for checking and green for success. That seemed to be better as it now has red for failure and green for success. Made constants out of the colors used so the app's behavior can be changed more easily in one place. 

## 2016-08-15

Updated the `show_activity_light` function, renamed the function to `set_activity_light` and updated it so it takes a `color` paremeter. Modified the flash_all_lights to take a `color` parameter. Renamed `flash_all_lights` and `flass_random_lights` to `flash_all` and `flash_random`.
 
## 2016-08-09

Added code to set the status light after flashing the LEDs. Otherwise, within 10 minutes of an event, you wouldn't see the status light indicating that the app is running. 

## 2016-06-28

Added red LED option for current_activity_light when there's a failure connecting to Google. Added this for a visual indicator when errors occur and the user misses the red flash.
 
## 2016-06-27

Fixed the progress indicator LED so it cycles from left to right and so it leaves the light blue on success so you can tell at a glance that the Pi is still running the code.

## 2016-06-20

Reader John McCabe submitted a patch to fix an issue where events with empty descriptions were causing an error. If the app encounters an event without a summary, it sets the output to `No Title`.

## 2016-06-18

Reader John McCabe submitted a patch to update the code so it takes into account the local timezone when working with dates/times. In my original code, I hardcoded my time zone into UTC conversions and intended to document this so others could update it to match their current timezone. John implemented a better solution, using some Python Date/Time utilities to properly reflect current time zone into calculations.  

