""" Huey tasks file.

Must be named tasks.py and be in the top level of an INSTALLED_APPS directory
for Huey to find it.

Additional periodic tasks may be created here. When Huey is started, it will
automatically detect and queue these tasks. """

from huey.contrib.djhuey import crontab, db_periodic_task

from metrics.models import Entry

from utils import read_top

import logging

logging.basicConfig(level=logging.DEBUG, filename='/tmp/metrics.log')


# osx
TOP_COMMAND = 'top -n 0 -l 1'  # zero processes, one repetition in logging mode
# ubuntu
# TOP_COMMAND = 'top -n 1 -b'  # one repetition in batch mode


@db_periodic_task(crontab(minute='*'))  # Once per minute
def make_new_top_entry():
    try:
        data = read_top(TOP_COMMAND)
        # Data is automatically jsonified by the JSONField in Entry
        new_entry = Entry.objects.create(command=TOP_COMMAND, data=data)
        new_entry.save()
    except:
        logging.exception('Exception raised in make_new_top_entry')


# Examples of alternative tasks.
# `make_new_top_delta_entry` runs `top -d`; the resulting Entry will contain
# the delta since the last time top was called. Can be done on the ORM/database
# levels (or even in Django), too. Doing it here is trading space for time.
# I could have made another layer of abstraction here, but I didn't want to
# spend too much time debugging my code's interaction with Huey's decorators.
# @db_periodic_task(crontab(minute='*'))
# def make_new_stats_delta_entry():
#     try:
#         data = read_top(TOP_COMMAND + ' -d')
#         command = 'top -d'
#         # Data is automatically jsonified by the JSONField in Entry
#         new_entry = Entry.objects.create(command=(TOP_COMMAND + ' -d'), data=data)
#         new_entry.save()
#     except:
#         logging.exception('Exception raised in make_new_top_delta_entry')




# @db_periodic_task(crontab(minute='*'))
# def make_new_netstat_entry():
#     try:
#         data = read_netstat(NETSTAT_COMMAND)
#         new_entry = Entry.objects.create(command=NETSTAT_COMMAND, data=data)
#         new_entry.save()
#     except:
#         logging.exception('Exception raised in make_new_netstat_entry')




