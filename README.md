# Time Based Point Alert Script

On designated days of the week, between start and end times, this script can be used to fire a random alert.

Config:

```
"start-time" : string representing the start time
"end-time" : string representing the end time
"active-days" : list of ints representing days-of-the-week the script is active
"max-delay-minutes": int max minutes to wait between decisions
"ignore-dates" : list of date strings when the script should not run
```
