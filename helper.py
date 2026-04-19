from urlextract import URLExtract
from wordcloud import WordCloud
import string
import emoji
import pandas as pd


extract = URLExtract() #object creation
def fetch_data(df, selected_user):
    if selected_user != "Overall":
        df = df[df["user"] == selected_user]
    #1. Total no. of messages
    no_of_messages = df.shape[0]
    #2. Total no. of words
    word = []
    for message in df["message"]:
        word.extend(message.split())
    #3.Total no. of media
    no_of_media = df[df["message"] == "<Media omitted>\n"].shape[0]
    #4.Total no. of links with the help of urlextract
    links = []
    for message in df["message"]:
        links.extend(extract.find_urls(message))

    return no_of_messages,len(word), no_of_media, len(links)

def most_busy_user(df):
    x = df["user"].value_counts().head()
    x = x.reset_index()
    x = x.rename(columns={"index": "user"})

    temp_df = round((df["user"].value_counts() / df.shape[0]) * 100, 2)
    temp_df = temp_df.reset_index().rename(columns={"index": "user", "count": "percentage"})
    return  x, temp_df

def create_word_cloud(df, selected_user):
    word = WordCloud(height= 500, width= 500,min_font_size= 10, background_color= 'white')
    if selected_user != "Overall":
        df = df[df["user"] == selected_user]
    temp_df = df[df["user"] != "Group Notification"]
    temp_df = temp_df[temp_df["message"] != "<Media omitted>\n"]
    temp_df = temp_df[temp_df["message"] != "This message was deleted\n"]
    df_wc = word.generate(temp_df["message"].str.cat(sep=" "))
    return df_wc

def most_common_words(df, selected_user):
    # this file is in string format while using the (if word in stop_word) intro will not count file contain introduction word also
    f = open("stop_hinglish.txt", "r")
    stop_word = set(f.read().split()) #we converted it into set ->** we have use set instead of list buz set timecomplexity of O(1) list O(n)

    if selected_user != "Overall":
        df = df[df["user"] == selected_user]
    temp_df = df[df["user"] != "Group Notification"]
    temp_df = temp_df[temp_df["message"] != "<Media omitted>\n"]
    temp_df = temp_df[temp_df["message"] != "This message was deleted\n"]
    common_words = []

    for message in temp_df["message"]:
        for word in message.split():
            cleaned_word = word.lower().strip(string.punctuation)
            if cleaned_word and cleaned_word not in stop_word:
                common_words.append(word)
    # this will treat Intro, intro, intro? such type of word as same
    common_words = [word.lower().strip(string.punctuation) for word in common_words]

    return common_words

def emoji_analysis(df, selected_user):
    if selected_user != "Overall":
        df = df[df["user"] == selected_user]

    emojis = []
    for message in df["message"]:
        emojis.extend([c for c in message if c in emoji.EMOJI_DATA])
    emoji_df = pd.DataFrame(emojis).value_counts().reset_index()
    emoji_df = emoji_df.rename(columns={0: "Emoji"})
    return emoji_df

def monthly_timeline(df, selected_user):
    if selected_user != "Overall":
        df = df[df["user"] == selected_user]
    monthly_df = df.groupby(["year", "month_num", "month"]).count()["message"].reset_index()
    time = []
    for i in range(monthly_df.shape[0]):
        time.append(str(monthly_df["year"][i]) + "-" + str(monthly_df["month"][i]))
    monthly_df["time"] = time
    return monthly_df


def daily_timeline(df, seleced_user):
    if seleced_user != "Overall":
        df = df[df["user"] == seleced_user]

    daily_df = df.groupby("daily_date").count()["message"].reset_index()
    return daily_df

def week_activity_timeline(df, seleced_user):
    if seleced_user != "Overall":
        df = df[df["user"] == seleced_user]
    week_df = df["day_name"].value_counts().reset_index()

    return week_df

def monthly_activity_timeline(df, seleced_user):
    if seleced_user != "Overall":
        df = df[df["user"] == seleced_user]

    month_bar_df = df["month"].value_counts().reset_index()
    return month_bar_df

def activity_heatmap(df, selected_user):
    if selected_user != "Overall":
        df = df[df["user"] == selected_user]
    tem_df = df[["day_name", "period"]].value_counts().reset_index()
    heatmap_df = pd.pivot_table(index= "day_name", columns= "period",data=df, values="message", aggfunc="count")
    heatmap_df = heatmap_df.fillna(0)
    return heatmap_df
