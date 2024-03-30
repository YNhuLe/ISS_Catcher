import time

import requests
from datetime import datetime
import smtplib

MY_EMAIL = "y1011996@gmail.com"
MY_PASSWORD = "mrnyhpmwbekkwtpu"
MY_LAT = 51.507351
MY_LONG = -0.127758


def is_iss_overhead():
    """
    set the API
    return longitude, latitude
    set position within -5 and +5 degrees of iss position
    :return:
    """
    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()
    data = response.json()

    iss_latitude = float(data["iss_position"]["latitude"])
    iss_longitude = float(data["iss_position"]["longitude"])

    # Your position within +5 or -5 degrees of the iss position
    if MY_LAT - 5 <= iss_latitude <= MY_LAT + 5 and MY_LONG - 5 <= iss_longitude <= MY_LONG + 5:
        return True


def is_night():
    """
    get the time for sunset, sunrise using API with parameters
    check if it is nighttime
    :return:
    """
    parameters = {
        "lat": MY_LAT,
        "lng": MY_LONG,
        "formatted": 0,
    }
    response = requests.get(url="https://api.sunrise-sunset.org/json", params=parameters)
    response.raise_for_status()

    data = response.json()
    sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])

    time_now = datetime.now().hour
    # check if it is nighttime
    if time_now >= sunset or time_now <= sunrise:
        return True


while True:
    time.sleep(60)
    if is_iss_overhead() and is_night():
        connection = smtplib.SMTP("smtp.gmail.com")
        connection.sendmail()
        connection.login(MY_EMAIL, MY_PASSWORD)
        connection.sendmail(
            from_addr=MY_EMAIL,
            to_addrs=MY_EMAIL,
            msg="Subject: Look Up 😎\n\n The ISS is above you in the sky!!"
        )
