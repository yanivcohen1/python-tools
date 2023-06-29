from datetime import datetime

def time_and_date():
    """ Calculate the time and date

    Returns:
        str: time and date
    """
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S") # 29/06/2023 18:20:49
    return dt_string

print(time_and_date())
