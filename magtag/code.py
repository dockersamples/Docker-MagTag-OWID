# SPDX-FileCopyrightText: 2020 Tim C, written for Adafruit Industries
#
# SPDX-License-Identifier: Unlicense

import wifi
import ssl
import socketpool
import adafruit_requests
from adafruit_progressbar.progressbar import ProgressBar
from adafruit_magtag.magtag import MagTag


magtag = MagTag()


# Add a secrets.py to your filesystem that has a dictionary called secrets with "ssid" and
# "password" keys with your WiFi credentials. DO NOT share that file or commit it into Git or other
# source control.
# pylint: disable=no-name-in-module,wrong-import-order
try:
    from secrets import secrets
except ImportError:
    print("Credentials and tokens are kept in secrets.py, please add them there!")
    raise

# Get our username, key and desired timezone
aio_username = secrets["aio_username"]
aio_key = secrets["aio_key"]
location = secrets.get("timezone", None)
TIME_URL = (
    "https://io.adafruit.com/api/v2/%s/integrations/time/strftime?x-aio-key=%s"
    % (aio_username, aio_key)
)
TIME_URL += "&fmt=%25H%3A%25M"


print("Connecting to %s" % secrets["ssid"])
wifi.radio.connect(secrets["ssid"], secrets["password"])
print("Connected to %s!" % secrets["ssid"])

pool = socketpool.SocketPool(wifi.radio)
requests = adafruit_requests.Session(pool, ssl.create_default_context())

endpoint_iso_first = "http://raspberrypi.local:5000/iso_data/{}".format(
    secrets["iso_first"]
)

endpoint_iso_second = "http://raspberrypi.local:5000/iso_data/{}".format(
    secrets["iso_second"]
)


# set progress bar width and height relative to board's display
BAR_WIDTH = (magtag.graphics.display.width // 2) - 10
BAR_HEIGHT = 13

iso_first_BAR_X = magtag.graphics.display.width // 4 - BAR_WIDTH // 2
iso_second_BAR_X = (magtag.graphics.display.width // 4) * 3 - (BAR_WIDTH // 2)
DOSE1_BAR_Y = 66
DOSE2_BAR_Y = 81
DOSE3_BAR_Y = 96

dose1_iso_first_progress_bar = ProgressBar(
    iso_first_BAR_X,
    DOSE1_BAR_Y,
    BAR_WIDTH,
    BAR_HEIGHT,
    1.0,
    bar_color=0x999999,
    outline_color=0x000000,
)
dose1_iso_second_progress_bar = ProgressBar(
    iso_second_BAR_X,
    DOSE1_BAR_Y,
    BAR_WIDTH,
    BAR_HEIGHT,
    1.0,
    bar_color=0x999999,
    outline_color=0x000000,
)
dose2_iso_first_progress_bar = ProgressBar(
    iso_first_BAR_X,
    DOSE2_BAR_Y,
    BAR_WIDTH,
    BAR_HEIGHT,
    1.0,
    bar_color=0x999999,
    outline_color=0x000000,
)
dose2_iso_second_progress_bar = ProgressBar(
    iso_second_BAR_X,
    DOSE2_BAR_Y,
    BAR_WIDTH,
    BAR_HEIGHT,
    1.0,
    bar_color=0x999999,
    outline_color=0x000000,
)
dose3_iso_first_progress_bar = ProgressBar(
    iso_first_BAR_X,
    DOSE3_BAR_Y,
    BAR_WIDTH,
    BAR_HEIGHT,
    1.0,
    bar_color=0x999999,
    outline_color=0x000000,
)
dose3_iso_second_progress_bar = ProgressBar(
    iso_second_BAR_X,
    DOSE3_BAR_Y,
    BAR_WIDTH,
    BAR_HEIGHT,
    1.0,
    bar_color=0x999999,
    outline_color=0x000000,
)

# name
magtag.add_text(
    text_font="fonts/leaguespartan18.bdf",
    text_position=(
        (magtag.graphics.display.width // 2) - 1,
        20,
    ),
    text_anchor_point=(0.5, 0.5),
)

# NY Percent
magtag.add_text(
    text_font="fonts/leaguespartan18.bdf",
    text_position=(
        (magtag.graphics.display.width // 4) - 1,
        45,
    ),
    text_anchor_point=(0.5, 0.5),
)

# US Percent
magtag.add_text(
    text_font="fonts/leaguespartan18.bdf",
    text_position=(
        ((magtag.graphics.display.width // 4) - 1) * 3,
        45,
    ),
    text_anchor_point=(0.5, 0.5),
)

# Date
magtag.add_text(
    text_font="fonts/leaguespartan11.bdf",
    text_position=(
        (magtag.graphics.display.width // 2) - 1,
        (magtag.graphics.display.height) - 3,
    ),
    text_anchor_point=(0.5, 1.0),
)


magtag.graphics.splash.append(dose1_iso_first_progress_bar)
magtag.graphics.splash.append(dose1_iso_second_progress_bar)
magtag.graphics.splash.append(dose2_iso_first_progress_bar)
magtag.graphics.splash.append(dose2_iso_second_progress_bar)
magtag.graphics.splash.append(dose3_iso_first_progress_bar)
magtag.graphics.splash.append(dose3_iso_second_progress_bar)


response_iso_first = requests.get(endpoint_iso_first)
iso_first = response_iso_first.json()
response_iso_second = requests.get(endpoint_iso_second)
iso_second = response_iso_second.json()

magtag.set_text(f"Population Vaccinated", index=0, auto_refresh=False)

Date = iso_second["data"]["date"]

magtag.set_text(
    f"{iso_first['iso_code']}: {iso_first['data']['people_fully_vaccinated_per_hundred']}%",
    index=1,
    auto_refresh=False,
)
dose1_iso_first_progress_bar.progress = (
    iso_first["data"]["people_vaccinated_per_hundred"] / 100.0
)
dose2_iso_first_progress_bar.progress = (
    iso_first["data"]["people_fully_vaccinated_per_hundred"] / 100.0
)
dose3_iso_first_progress_bar.progress = (
    iso_first["data"]["total_boosters_per_hundred"] / 100.0
)


magtag.set_text(
    f"{iso_second['iso_code']}: {iso_second['data']['people_fully_vaccinated_per_hundred']}%",
    index=2,
    auto_refresh=False,
)
dose1_iso_second_progress_bar.progress = (
    iso_second["data"]["people_vaccinated_per_hundred"] / 100.0
)
dose2_iso_second_progress_bar.progress = (
    iso_second["data"]["people_fully_vaccinated_per_hundred"] / 100.0
)
dose3_iso_second_progress_bar.progress = (
    iso_second["data"]["total_boosters_per_hundred"] / 100.0
)

response = requests.get(TIME_URL)

Date += f" at {response.text}"
magtag.set_text(f"{Date}", index=3, auto_refresh=False)

time_8pm = 20 * 60 * 60
time_now = (int(response.text[:2]) * 60 * 60) + (int(response.text[-2:]) * 60)
if time_now == time_8pm:
    deep_sleep = 24 * 60 * 60
elif time_now < time_8pm:
    deep_sleep = time_8pm - time_now
else:
    deep_sleep = ((24 * 60 * 60) - time_now) + time_8pm


print(deep_sleep)

magtag.refresh()
magtag.exit_and_deep_sleep(deep_sleep)
