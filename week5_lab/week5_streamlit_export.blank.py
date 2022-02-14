# Michelle Cheng
# si649f20 altair transforms 2

# imports we will use
import altair as alt
import pandas as pd
import streamlit as st

#Title
st.title("Lab6 by Michelle Cheng")

#Import data
df1=pd.read_csv("https://raw.githubusercontent.com/eytanadar/si649public/master/lab6/hw/data/df1.csv")
df2=pd.read_csv("https://raw.githubusercontent.com/eytanadar/si649public/master/lab6/hw/data/df2_count.csv")
df3=pd.read_csv("https://raw.githubusercontent.com/eytanadar/si649public/master/lab6/hw/data/df3.csv")
df4=pd.read_csv("https://raw.githubusercontent.com/eytanadar/si649public/master/lab6/hw/data/df4.csv")

# change the 'datetime' column to be explicitly a datetime object
df2['datetime'] = pd.to_datetime(df2['datetime'])
df3['datetime'] = pd.to_datetime(df3['datetime'])
df4['datetime'] = pd.to_datetime(df4['datetime'])

#Sidebar
st.sidebar.title("Sidebar title")

st.sidebar.write("My sidebar stuff")

###### Making of all the charts


########Vis 1

##Interaction requirement 2, change opacity when hover over
##Interaction requirement 3 and 4, create brushing filter
selection = alt.selection_single(on = 'mouseover', empty = 'none')
opacityCondition = alt.condition(selection, alt.value(1), alt.value(0.6))
brush = alt.selection_interval()
filterCondition = alt.condition(brush, alt.value(0.6), alt.value(0))
##Static Component - Bars
chart_bars = alt.Chart(df1).transform_window(
    sort = [alt.SortField('PERCENT', order = 'descending')],
    emoji_rank = 'rank(*)'
).transform_filter(
    alt.datum.emoji_rank <= 10
).mark_bar(height = 15, color = 'orange', opacity = 0.6
).encode(
    alt.X('PERCENT:Q', axis = None),
    alt.Y('EMOJI:N', axis = None, sort = alt.EncodingSortField(
        field = 'emoji_rank', order = 'ascending')),
    tooltip = 'EMOJI:N',
    opacity = opacityCondition
).add_selection(selection).transform_filter(
    brush
)
base = alt.Chart(df1).mark_bar().encode(
    alt.Y('EMOJI:N', axis = None, sort = alt.EncodingSortField(
        field = 'emoji_rank', order = 'ascending')
))
##Static Component - Emojis
emojis = base.mark_text(
    align ='left',
    baseline ='middle',
    dx = -10
).encode(
    text=alt.Text('EMOJI:N'),
    opacity = opacityCondition
).add_selection(selection).add_selection(brush)
##Static Component - Text
texts = base.mark_text(
    align ='left',
    baseline ='middle',
    dx = -10
).encode(
    text=alt.Text('PERCENT_TEXT:N'),
    opacity = opacityCondition
).add_selection(selection).add_selection(brush)
##Put all together
vis1 = (emojis | texts | chart_bars).configure_view(strokeWidth = 0).configure_axis(domain = False)



########Vis 2

#Zooming and Panning
zoom_pan = alt.selection_interval(bind = 'scales', encodings = ['x'])
#vertical line
hover = alt.selection_single(on = 'mouseover', empty = 'none',nearest = True, init = {'datetime':'12:10'})
opacityCondition = alt.condition(hover, alt.value(1), alt.value(0))
#interaction dots
hover_intersection = alt.selection_single(on = 'mouseover', fields=['datetime:T'], 
                                         empty = 'none')
opacityCondition_intersection = alt.condition(hover_intersection, alt.value(1), alt.value(0))
#Static component line chart
chart_line = alt.Chart(df2).mark_line().encode(
    alt.X('datetime:T'),
    alt.Y('tweet_count:Q'),
    alt.Color('team:N')
).add_selection(zoom_pan)
vline = alt.Chart(df2).mark_rule(size = 4, color = "lightgray").encode(
    alt.X('datetime:T'),
    opacity = opacityCondition
).add_selection(hover)
intersection_dots = alt.Chart(df2).mark_circle(size = 70, color = 'black').encode(
    alt.X('datetime:T'),
    alt.Y('tweet_count:Q'),
    opacity = opacityCondition,
    tooltip = ['tweet_count', 'datetime', 'team']
).add_selection(hover_intersection)
#Put all together
vis2 = vline + chart_line + intersection_dots


########Vis3

#Altair version
selectEmoji = alt.selection_single(
    fields = ['emoji'],
    name = 'emoji',
    bind = alt.binding_radio(options = list(df3['emoji'].unique()), name = 'emoji'),
    init = {"emoji":list(df3['emoji'].unique())[0]}
)

brush = alt.selection_interval(empty = 'none')
brushCondition = alt.condition(brush, alt.value(0.6), alt.value(0))

chart = alt.Chart(df3).mark_line().encode(
    alt.X('datetime:T', axis=alt.Axis(tickCount=5)),
    alt.Y('tweet_count:Q'),
    alt.Color('emoji:N')
)

chart = chart.add_selection(selectEmoji).encode(
    opacity = alt.condition(selectEmoji, alt.value(1), alt.value(0))
)

circles = alt.Chart(df3).mark_circle(color="black",opacity=0.7).encode(
    alt.X('datetime:T'),
    alt.Y('tweet_count:Q'),
    opacity = brushCondition
).add_selection(brush).transform_filter(selectEmoji)

vis3 = chart + circles

#Streamlit widget version

emoji_select = st.radio(label = "Select Emoji", options = (🔥,😴))

brush = alt.selection_interval(empty = 'none')
brushCondition = alt.condition(brush, alt.value(0.6), alt.value(0))

chart = alt.Chart(df3).mark_line().encode(
    alt.X('datetime:T', axis=alt.Axis(tickCount=5)),
    y = emoji_select,
    alt.Color('emoji:N')
)

circles = alt.Chart(df3).mark_circle(color="black",opacity=0.7).encode(
    alt.X('datetime:T'),
    y = emoji_select,
    opacity = brushCondition
).add_selection(brush)

vis4 = chart + circles

########Vis4 BONUS OPTIONAL

#Altair version

#Streamlit widget version


##### Display graphs
st.write(vis1)
st.write(vis2)
st.write(vis3)
st.write(vi4)