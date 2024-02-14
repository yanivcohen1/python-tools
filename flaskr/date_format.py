from datetime import datetime

# from time import gmtime, strftime
import time


def time_and_date():
    """Calculate the time and date

    Returns:
        str: time and date
    """
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")  # 29/06/2023 18:20:49
    gmt = time.gmtime()
    print(
        "Local: " + now.strftime("%a, %d %b %Y %I:%M:%S %p %Z")
    )  # Local: Mon, 08 May 2017 11:51:07 AM IST
    print(
        "\nGMT: " + time.strftime("%a, %d %b %Y %I:%M:%S %p %Z", gmt)
    )  # GMT: Mon, 08 May 2017 06:21:07 AM GMT
    print("\nYour Time Zone is GMT", time.strftime("%z", gmt))
      # Your Time Zone is GMT +0200
    return dt_string


time_and_date()
