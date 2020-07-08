#!/usr/bin/env python2
import datetime

import requests
import icalendar
import mice
import os

def set_mumble(event, start, end):
    s = mice.murmur.getAllServers()[0]
    state = s.getChannelState(os.environ['CHANNEL_ID'])
    now = datetime.datetime.now()


    if selected_event is not None:

        relname = None
        if start < now:
            timediff = now - start
            relname = "in {} minuten".format(timediff.minute + timediff.hour * 60)
        else:
            timediff = now - end
            relname = "noch {} minuten".format(timediff.minute + timediff.hour * 60)

        state.name = "[{}] Veranstaltung: {}".format(relname, selected_event.get("summary"))
    else:
        state.name = "Veranstaltung: Keine Aktive"

r = requests.get("https://das-labor.org/termine.ics")
data = r.text

cal = icalendar.Calendar.from_ical(data)

start_date = datetime.datetime.now() - datetime.timedelta(1, 0, 0, 0, 30)
end_date = datetime.datetime.now() + datetime.timedelta(1, 0, 0, 0, 0)

selected_event = None
valid_events = 0

print("Checking between {} and {}".format(start_date, end_date))

for event in cal.subcomponents:
    start = event.decoded("dtstart")
    end = event.decoded("dtend", None)
    if isinstance(start, datetime.date):
        start = datetime.datetime.combine(start.today(), datetime.datetime.min.time())
    if end is None:
        end = start + datetime.timedelta(0, 0, 0, 0, 0, 2)

    valid_events += 1
    if start > start_date and end < end_date:
        selected_event = event
        set_mumble(event, start, end)


