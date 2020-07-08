#!/usr/bin/env python2
import datetime

import requests
import icalendar
import os

def set_mumble(event, start, end):
    import mice

    s = mice.murmur.getAllServers()[0]
    state = s.getChannelState(int(os.environ['CHANNEL_ID']))
    now = datetime.datetime.now()


    if event is not None:

        relname = None
        if start < now:
            timediff = now - start
            relname = "in {} minuten".format(timediff.seconds // 60)
        else:
            timediff = now - end
            relname = "noch {} minuten".format(timediff.seconds // 60)

        state.name = "[{}] Veranstaltung: {}".format(relname, selected_event.decoded("summary"))
    else:
        state.name = "Veranstaltung: Keine Aktive Veranstaltung"

    s.setChannelState(state)

r = requests.get("https://das-labor.org/termine.ics")
data = r.text

cal = icalendar.Calendar.from_ical(data)

start_date = datetime.datetime.now() - datetime.timedelta(1, 0, 0, 0, 30)
end_date = datetime.datetime.now() + datetime.timedelta(1, 0, 0, 0, 0)

print("Checking between {} and {}".format(start_date, end_date))

selected_event = None

for event in cal.subcomponents:
    start = event.decoded("dtstart")
    end = event.decoded("dtend", None)
    if isinstance(start, datetime.date):
        start = datetime.datetime.combine(start, datetime.datetime.min.time())
    if end is None:
        end = start + datetime.timedelta(0, 0, 0, 0, 0, 2)

    if start > start_date and end < end_date:
        print("{} - {}: {}".format(start, end, event.decoded("summary")))
        selected_event = (event, start, end)


set_mumble(*selected_event)

