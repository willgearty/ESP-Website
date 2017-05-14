from script_setup import *
from datetime import datetime, timedelta

interview_type = EventType.get_from_desc('Teacher Interview')

print("This script will add a bunch of hardcoded interview times.")

program = Program.objects.get(name=raw_input("Enter the program name: "))
program2 = Program.objects.get(name=raw_input("Enter it again just to be sure: "))
assert program == program2

print("Operating on program {}".format(program))

print("BE CAREFUL")
print("==========")

print("""Type 'REPLACE' to delete pre-existing interviews and add all the
hardcoded interviews, 'ADD' to only add the hardcoded interviews, and
anything else to fail:""")
command = raw_input()
if command == 'REPLACE':
    Event.objects.filter(program=program, event_type=interview_type).delete()
else:
    assert command == 'ADD'

def starts():
    for h in [9, 10, 12, 13, 18, 19]:
        yield datetime(2017, 5, 15, h, 0)
        yield datetime(2017, 5, 15, h, 30)
    yield datetime(2017, 5, 15, 14, 0)
    yield datetime(2017, 5, 15, 20, 0)

    for h in [9, 10, 13, 15, 16, 17, 18]:
        yield datetime(2017, 5, 16, h, 0)
        yield datetime(2017, 5, 16, h, 30)
    yield datetime(2017, 5, 16, 14, 0)

    for h in [9, 10, 12, 13, 17]:
        yield datetime(2017, 5, 17, h, 0)
        yield datetime(2017, 5, 17, h, 30)
    yield datetime(2017, 5, 17, 14, 0)
    yield datetime(2017, 5, 17, 18, 0)

    for h in [9, 10, 13, 14, 15, 16, 17, 18]:
        yield datetime(2017, 5, 18, h, 0)
        yield datetime(2017, 5, 18, h, 30)
    yield datetime(2017, 5, 18, 19, 30)
    yield datetime(2017, 5, 18, 20, 0)

    for h in range(9, 20):
        yield datetime(2017, 5, 19, h, 0)
        yield datetime(2017, 5, 19, h, 30)
    yield datetime(2017, 5, 19, 20, 0)

    for h in range(9, 20):
        yield datetime(2017, 5, 20, h, 0)
        yield datetime(2017, 5, 20, h, 30)
    yield datetime(2017, 5, 20, 20, 0)

for start in starts():
    slot = Event()
    slot.start = start
    slot.end = start + timedelta(hours=0, minutes=30)
    slot.event_type = interview_type
    slot.program = program
    slot.short_description = slot.start.strftime('%A, %B %d %Y %I:%M %p') + " to " + slot.end.strftime('%I:%M %p')
    slot.description = slot.short_description
    slot.save()
