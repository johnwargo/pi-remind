Event List
==========
The event list returns a set of default reminder options

    "defaultReminders": [
     {
       "method": "email",
       "minutes": 10
      },
     {
       "method": "popup",
       "minutes": 10
     }
    ]
 
Reminder
==========
Then, each event can have the default reminder set:

    "reminders": {
      "useDefault": true
    }
   
or it can have event-specific reminder options
   
    "reminders": {
      "useDefault": false,
      "overrides": [
        {
          "method": "popup",
          "minutes": 10
        },
        {
          "method": "email",
          "minutes": 430
        }
      ]
    }