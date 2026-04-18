import re
import pandas as pd

def preprocess(data):
    pattern = '\d{1,2}/\d{1,2}/\d{2},\s\d{1,2}:\d{1,2}\s(?:am|pm)\s-\s'

    message = re.split(pattern, data)[1:]
    dates = re.findall(pattern, data)
    dates = [d.replace("\u202f", " ") for d in dates]

    df = pd.DataFrame({"user_message": message, "message_date": dates})
    df["message_date"] = pd.to_datetime(df["message_date"], format='%d/%m/%y, %I:%M %p - ')
    user = []
    message = []

    for i in df["user_message"]:
        entry = re.split(pattern="([\w\W]+?):\s", string=i)
        if entry[1:]:
            user.append(entry[1])
            message.append(entry[2])
        else:
            user.append("Group Notification")
            message.append(entry[0])

    df["user"] = user
    df["message"] = message
    df.drop(columns=["user_message"], inplace=True)

    df["year"] = df["message_date"].dt.year
    df["month"] = df["message_date"].dt.month_name()
    df["month_num"] = df["message_date"].dt.month
    df["daily_date"] = df["message_date"].dt.date
    df["day"] = df["message_date"].dt.day
    df["day_name"] = df["message_date"].dt.day_name()
    df["hour"] = df["message_date"].dt.hour
    df["minute"] = df["message_date"].dt.minute
    period = []
    for i in df["hour"]:
        if i == 23:
            period.append(str(i) + "-" + str(00))
        elif i == 0:
            period.append(str(00) + "-" + str(i + 1))
        else:
            period.append(str(i) + "-" + str(i + 1))

    df["period"] = period

    return df