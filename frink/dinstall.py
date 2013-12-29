import humanize
import requests

import datetime as dt
import re

DINSTALL_STATUS = "http://ftp-master.debian.org/dinstall.status"

TIME_REG = re.compile("(Dinstall start|Action start): .* \((?P<when>.*)\)")

def what_time_is_it(start):
    when = TIME_REG.match(start).groupdict()['when']
    return dt.datetime.fromtimestamp(int(when))


def get_dinstall_status():
    start, status, end = requests.get(DINSTALL_STATUS).text.splitlines()
    start, end = (what_time_is_it(x) for x in (start, end))
    _, status = (x.strip() for x in status.rsplit(":", 1))

    def h(when):
        return humanize.naturaltime(when)

    return {
        "start": start,
        "end": end,
        "status": status,
        "human_start": h(start),
        "human_end": h(end),
    }

# info = get_dinstall_status()
# print info
