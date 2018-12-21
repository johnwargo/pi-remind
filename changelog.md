# Changelog

## 2018-12-21

- Added a reboot timer to `remind.py`. I noticed that when I lost power in the house, the PI would come up before my network did, and never reconnect. So, when you set `REBOOT_COUNTER_ENABLED` to `True` and specify a reboot counter in `REBOOT_NUM_RETRIES` (it defaults to 10), the app will count how many times the API fails to connect, then reboots the Pi.
 
    Right now, the code doesn't check for the type of error, so any failure in checking the Google Calendar will trigger the reboot counter. the **right** way to do this would be to figure out what all the possible errors are, and trigger this only for network errors. I've been running this app in my office fr years now, so I feel comfortable with the code the way it is. 

- Added a socket timeout to `remind.py`. As I started testing this code, I noticed that the big `except` I use to catch errors connecting to the Google Calendar API was hanging. A recent update to the Google API library, or something else on the Pi was causing this to fail now when it wasn't failing before, so I added the timeout to force the error.
    
- Refactored the startup script `start-remind.py`. As I was testing the updates to the Python code, I realized that I wanted the shell script to show me which *version* of the python app it was running (by file date).  
