import streamlit as st
import matplotlib.pyplot as plt
from streamlit import columns
import seaborn as sns
import helper
import preprocessor
import pandas as pd
import plotly.express as px

st.sidebar.title("Whatsapp Chat Analyzer")
# taking file input
uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    df = preprocessor.preprocess(data)

    user_list = df["user"].unique().tolist()
    user_list.remove("Group Notification")
    user_list.sort()
    user_list.insert(0, "Overall")

    seleced_user = st.sidebar.selectbox("Select Analysis wrt", user_list)
    button = st.sidebar.button("Start Analysis")

    no_of_messages, no_of_word, total_media, total_links = helper.fetch_data(df, seleced_user)


    if button:

        # Stats
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.subheader("Total Messages")
            st.subheader(f'-> {no_of_messages}')
        with col2:
            st.subheader("Total Words")
            st.subheader(f"-> {no_of_word}")
        with col3:
            st.subheader("Total Media")
            st.subheader(f"-> {total_media}")
        with col4:
            st.subheader("Total Links")
            st.subheader(f"-> {total_links}")

        # montly timeline
        st.divider()
        st.header("Monthly Messages Analysis")
        monthly_df = helper.monthly_timeline(df, seleced_user)
        fig = px.line(x="time", y="message", data_frame=monthly_df)
        st.plotly_chart(fig)

        # daily timeline
        st.divider()
        st.subheader("Daily Messages Analysis")
        daily_df = helper.daily_timeline(df, seleced_user)
        daily_df = daily_df.rename(columns= {"daily_date": "Date", "message": "Message"})
        fig = px.line(x="Date", y="Message", data_frame=daily_df,color_discrete_sequence= ["orange"])
        st.plotly_chart(fig)


        #week_activity_map

        st.divider()
        st.header("Message Activity Analysis")
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Weekly Messsages Analysis")
            week_df = helper.week_activity_timeline(df, seleced_user)
            fig, ax = plt.subplots()
            ax.barh(week_df["day_name"], week_df["count"])
            for i, v in enumerate(week_df["count"]):
                plt.text(v, i, str(v), va='center', ha='left')
            st.pyplot(fig)
        with col2:
            st.subheader("Monthly Message Analysis")
            month_bar_df = helper.monthly_activity_timeline(df, seleced_user)
            fig, ax = plt.subplots()
            ax.barh(month_bar_df["month"], month_bar_df["count"])
            for i, v in enumerate(month_bar_df["count"]):
                plt.text(v, i, str(v), va='center', ha='left')
            st.pyplot(fig)

        #Heat_Map -> time when the user is most active
        st.divider()
        st.header("Weekly Activity Map")
        heatmap_df = helper.activity_heatmap(df, seleced_user)
        fig, ax = plt.subplots()
        ax = sns.heatmap(heatmap_df)
        st.pyplot(fig)

        # Most busy User

        if seleced_user == "Overall":
            st.divider()
            st.title("Most Busy Users")
            col1, col2 = st.columns(2)
            x, temp_df = helper.most_busy_user(df)
            with col1:
                fig, ax = plt.subplots()
                ax.bar(x["user"], x["count"])
                plt.xticks(rotation="vertical")
                # value adding to bar
                for i, v in enumerate(x["count"]):
                    plt.text(i, v, str(v), ha='center', va='bottom')
                st.subheader("Bar chart")
                st.pyplot(fig)

            with col2:
                st.subheader("Percentage Contribution")
                st.dataframe(temp_df)
        # Word cloud

        st.divider()
        st.header("Word Cloud")
        wc= helper.create_word_cloud(df, seleced_user)
        fig, ax = plt.subplots()
        ax.imshow(wc)
        st.pyplot(fig)

        # Most Common word
        #issue with the stop_hinglish file

        st.divider()
        st.header(f"{seleced_user} Most Common Words")
        col1, col2 = st.columns(2)
        common_words = helper.most_common_words(df, seleced_user)
        new_df = pd.DataFrame(common_words)
        new_df = new_df[0].value_counts().reset_index()
        new_df.rename(columns={0: "Word"}, inplace=True)
        with col1:
            new_df2 = new_df.head(10)
            st.subheader("Bar Graph")
            fig , ax = plt.subplots()
            ax.barh(new_df2["Word"],new_df2["count"])
            for i, v in enumerate(new_df2["count"]):
                plt.text(v, i, str(v), va='center', ha='left')

            st.pyplot(fig)
        with col2:
            st.subheader("Table")
            st.dataframe(new_df)

        # Emoji Analysis
        st.divider()
        st.header(f"{seleced_user} Emoji Analysis")
        emoji_df = helper.emoji_analysis(df, seleced_user)
        col1, col2 = st.columns(2)
        with col1:
            st.subheader(f"-> Emoji table")
            st.dataframe(emoji_df)
        with col2:
            fig ,ax = plt.subplots()
            plt.rcParams['font.family'] = 'Segoe UI Emoji' # use to print emoji
            ax.pie(emoji_df["count"], autopct='%0.2f%%', labels=emoji_df["Emoji"])
            st.subheader(f"-> Pie Chart")
            st.pyplot(fig)


