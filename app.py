import streamlit as st
import pandas as pd
import preprocessor,helper
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.figure_factory as ff
import helper

df = pd.read_csv('athlete_events.csv')
region_df = pd.read_csv('noc_regions.csv')

df = preprocessor.preprocessor(df,region_df)

st.sidebar.title("Olympics Analysis")
st.sidebar.image('https://e7.pngegg.com/pngimages/1020/402/png-clipart-2024-summer-olympics-brand-circle-area-olympic-rings-olympics-logo-text-sport.png')
user_menu = st.sidebar.radio(
    'Select an Option',
    ('Medal Tally','Overall Analysis','Country-wise Analysis','Athlete wise Analysis')
)

if user_menu == 'Medal Tally':
    st.sidebar.header("Medal Tally")
    years,country = helper.country_year_list(df)

    selected_year = st.sidebar.selectbox("Select Year",years)
    selected_country = st.sidebar.selectbox("Select Country", country)

    medal_tally = helper.fetch_medal_tally(df,selected_year,selected_country)
    if selected_year == 'Overall' and selected_country == 'Overall':
        st.title("Overall Tally")
    if selected_year != 'Overall' and selected_country == 'Overall':
        st.title("Medal Tally in " + str(selected_year) + " Olympics")
    if selected_year == 'Overall' and selected_country != 'Overall':
        st.title(selected_country + " overall performance")
    if selected_year != 'Overall' and selected_country != 'Overall':
        st.title(selected_country + " performance in " + str(selected_year) + " Olympics")
    st.table(medal_tally)

if user_menu == 'Overall Analysis':
    editions = df['Year'].unique().shape[0] - 1
    cities = df['City'].unique().shape[0]
    sports = df['Sport'].unique().shape[0]
    events = df['Event'].unique().shape[0]
    athletes = df['Name'].unique().shape[0]
    nations = df['region'].unique().shape[0]

    st.title("Top Statistics")
    col1,col2,col3 = st.columns(3)
    with col1:
        st.header("Editions")
        st.title(editions)
    with col2:
        st.header("Hosts")
        st.title(cities)
    with col3:
        st.header("Sports")
        st.title(sports)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.header("Events")
        st.title(events)
    with col2:
        st.header("Nations")
        st.title(nations)
    with col3:
        st.header("Athletes")
        st.title(athletes)

    nations_over_time = helper.participating_nations_over_time(df)
    fig = px.line(nations_over_time,x='Edition',y='No of Countries')
    st.title("Participating Nations Over the Years")
    st.plotly_chart(fig)

    events_over_time = helper.events_nations_over_time(df)
    fig = px.line(events_over_time,x='Edition',y='No of Events')
    st.title("Events Over the Years")
    st.plotly_chart(fig)


    events_over_time = helper.athelete_over_time(df)
    fig = px.line(events_over_time,x='Edition',y='No of Atheletes')
    st.title("Atheletes Over the Years")
    st.plotly_chart(fig)


    st.title("No. of Events over time (Every Sport)")
    fig,ax=plt.subplots(figsize=(20,20))
    x = df.drop_duplicates(['Year','Sport','Event'])
    sns.heatmap(x.pivot_table(index='Sport',columns='Year',values='Event',aggfunc = 'count').fillna(0).astype('int'),annot=True)
    st.pyplot(fig)

    st.title("Most succesfull Athletes")
    sport_list = df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0,'Overall')

    selected_sport = st.selectbox('Select a sport',sport_list)
    x = helper.most_successful(df,selected_sport)
    st.table(x)

if user_menu == 'Country-wise Analysis':
    st.title("Athletes Over the Years")
    
    country_medal = df['region'].dropna().unique().tolist()
    country_medal.sort()

    country_medal_selected = st.sidebar.selectbox("Select Country",country_medal)
    medal_country_time = helper.yearwise_medal_tally(df,country_medal_selected)
    fig = px.line(medal_country_time,x='Year',y='Medal')
    st.plotly_chart(fig)
    pt = helper.country_event_heatmap(df, country_medal_selected)

    if pt is not None:
        fig, ax = plt.subplots(figsize=(20, 20))
        sns.heatmap(pt, annot=True, ax=ax)
        st.pyplot(fig)
    else:
        st.write(f"No data available for {country_medal_selected} in the selected years.")
    st.title("Top 10 athelte in "+ country_medal_selected)
    top10_df = helper.most_successful_countrywise(df,country_medal_selected)
    st.table(top10_df)
    
if user_menu =='Athlete wise Analysis':
    athlete_df = df.drop_duplicates(subset=['Name','region'])
    x1 = athlete_df['Age'].dropna()
    x2 = athlete_df[athlete_df['Medal']=='Gold']['Age'].dropna()
    x3 = athlete_df[athlete_df['Medal']=='Silver']['Age'].dropna()
    x4 = athlete_df[athlete_df['Medal']=='Bronze']['Age'].dropna()
    fig = ff.create_distplot([x1,x2,x3,x4],['OverallAge','Gold Medalist','Silver Medalist','Bronze Medalist'],show_hist=False,show_rug=False)
    st.title("Distribution of Age")
    st.plotly_chart(fig)

    sport_list = df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0,'Overall')

    selected_sportValue = st.selectbox('Select Sport',sport_list)

    if selected_sportValue == 'Overall':
        sport_data = df.drop_duplicates(subset=['Name','region'])
        sport_data['Medal'].fillna('No Medal',inplace = True)
    else:
        sport_data =  helper.weight_v_height(df,selected_sportValue)
    fig,ax=plt.subplots()
    sns.scatterplot(x= sport_data['Weight'],y=sport_data['Height'],hue=sport_data['Medal'],style=sport_data['Sex'],ax=ax)
    st.pyplot(fig)
