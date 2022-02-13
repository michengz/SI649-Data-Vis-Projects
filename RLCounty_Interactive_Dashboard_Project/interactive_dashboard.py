# Michelle Cheng
# si649f20 altair transforms 2

# imports we will use
import streamlit as st
import streamlit.components.v1 as components
import altair as alt
import altair_catplot as altcat
import pandas as pd
from vega_datasets import data

alt.data_transformers.disable_max_rows()

st.set_page_config(layout="wide")


#Import data
df = pd.read_csv('datasets/MHV_MHI.csv')
df['MHV_MHI_Ratio'] = df['Median_HV']/df['Median_HI']
df = df.round(2)

df2 = pd.read_csv('datasets/Unemployment_Rate.csv').dropna()
df2['Year'] = df2['Year'].astype(str).str.extract('([0-9]{4})')

df3 = pd.read_csv('datasets/Poverty_Rate.csv').dropna()
df3['Year'] = df3['Year'].astype(str).str.extract('([0-9]{4})')

df4 = pd.read_csv('datasets/Natural_Amenities.csv')

df6 = pd.read_csv('datasets/GDP_Growth.csv')
df7 = pd.read_csv('datasets/Farm_Earnings_Percentage.csv')


###### Making of all the charts

#-------- VIS 1 (Unemployment Rate & Poverty Rate) --------# 

# Interactions
selection = alt.selection_single(fields = ['County_State'],empty = 'none')
hover = alt.selection_single(on = 'mouseover',empty = 'none')

# Bar Chart - Natural Amenities Ranking
rank_bars = alt.Chart(df4).mark_bar().encode(
    alt.X('County_State:N', 
          sort = alt.EncodingSortField(field = 'Scale', order = 'descending'),
          axis = alt.Axis(labels = False, title = None, tickSize = 0, domainOpacity = 0)
         ),
    alt.Y('Scale:Q', 
          axis = alt.Axis(labels = False, gridOpacity = 0, tickSize = 0, domainOpacity = 0, title = '')
         ),
    color=alt.condition(
        alt.datum.Scale > 0,
        alt.value("#ecca96"),  # The positive color
        alt.value("#d18954")  # The negative color
    )
).transform_window(
    sort = [alt.SortField('Scale', order = 'descending')],
    scale_rank = 'rank(*)'
).transform_filter(
    (alt.datum.scale_rank <= 10) | (alt.datum.scale_rank > 3101)
).properties(
    width = 600,
    height = 385,
    title = {
        'text': 'Natural Amenities Scale Ranking by County',
        'subtitle': 'Top 10 and Last 10 Counties',
        'align': 'left',
        'dx': -350
    }
)

line = alt.Chart(df4).mark_rule(opacity = 0.8, strokeWidth = 0.4).encode(alt.Y('Scale:Q')).transform_filter(alt.datum.Scale == 0)

base_bars = rank_bars.add_selection(selection).add_selection(
    hover
).encode(
    opacity = alt.condition(hover, alt.value(1), alt.value(0.6)),
    stroke = alt.condition(hover, alt.value('black'), alt.value('white'))
)

bar_highlight = rank_bars.encode(
    opacity = alt.condition(selection, alt.value(1), alt.value(0.6))).transform_filter(selection)

#bg = alt.Chart(df4).mark_rect(fill ='#f2f2f2', fillOpacity = 0.1).encode(
    #x=alt.value(0),
    #y=alt.value(0),
    #x2=alt.value(500),
    #y2=alt.value(350)
#)

county_pos = alt.Chart(df4).mark_text(
    angle = 315,
    align = 'right',
    baseline = 'bottom',
    fontSize = 10,
    dx = -30,
    dy = 40
).encode(
    alt.X('County_State:N',sort = alt.EncodingSortField(field = 'Scale', order = 'descending')),
    text = 'County_State',
    opacity = alt.condition(selection, alt.value(1), alt.value(0.6))
).transform_window(
    sort = [alt.SortField('Scale', order = 'descending')],
    scale_rank = 'rank(*)'
).transform_filter(
    alt.datum.scale_rank <=10
)

county_neg = alt.Chart(df4).mark_text(
    angle = 315,
    align = 'left',
    baseline = 'bottom',
    fontSize = 10,
    dx = -25,
    dy = 24
).encode(
    alt.X('County_State:N',sort = alt.EncodingSortField(field = 'Scale', order = 'descending')),
    text = 'County_State',
    opacity = alt.condition(selection, alt.value(1), alt.value(0.6))
).transform_window(
    sort = [alt.SortField('Scale', order = 'descending')],
    scale_rank = 'rank(*)'
).transform_filter(
    alt.datum.scale_rank > 3101
)

scale_pos = alt.Chart(df4).mark_text(
    baseline = 'bottom',
    fontSize = 10,
    dy = -5
).encode(
    alt.X('County_State:N',sort = alt.EncodingSortField(field = 'Scale', order = 'descending')),
    alt.Y('Scale:Q'),
    text = 'Scale',
    opacity = alt.condition(selection, alt.value(1), alt.value(0.6))
).transform_window(
    sort = [alt.SortField('Scale', order = 'descending')],
    scale_rank = 'rank(*)'
).transform_filter(
    alt.datum.scale_rank <=10
)

scale_neg = alt.Chart(df4).mark_text(
    baseline = 'bottom',
    fontSize = 10,
    dy = 15
).encode(
    alt.X('County_State:N',sort = alt.EncodingSortField(field = 'Scale', order = 'descending')),
    alt.Y('Scale:Q'),
    text = 'Scale',
    opacity = alt.condition(selection, alt.value(1), alt.value(0.6))
).transform_window(
    sort = [alt.SortField('Scale', order = 'descending')],
    scale_rank = 'rank(*)'
).transform_filter(
    alt.datum.scale_rank > 3101
)

county_text = county_pos + scale_pos + county_neg + scale_neg

# Boxplot - Unemployment Rate & Poverty Rate
def boxplot(data, y_axis, color, title):
    box = altcat.catplot(data,
                   width = 180,
                   height = 350,
                   mark = dict(type = 'point', color = color),
                   box_mark = dict(size = 17, strokeWidth = 1, opacity = 0.6, color = color),
                   whisker_mark = dict(width = 17, strokeWidth = 0.8, opacity = 0.7),
                   encoding = dict(x = alt.X('Year:N', 
                                             axis = alt.Axis(tickOpacity = 0, labelAngle = 0, title = '')),
                                   y = alt.Y(y_axis, 
                                             scale = alt.Scale(zero = False),
                                             axis = alt.Axis(tickMinStep = 5, 
                                                             gridOpacity = 0.5, 
                                                             tickOpacity = 0, 
                                                             domainOpacity = 0,
                                                             title = '')),
                                   ),
                   transform = "box"
                   ).properties(
                            title={
                              "text": title, 
                              "subtitle": '(2010 - 2015)'
                            })
    
    line_RL = alt.Chart(data).mark_line(color = '#dd4b5f').encode(
        alt.X('Year:O'),
        alt.Y(y_axis)
    ).transform_filter(alt.datum.County == 'Red Lake County')

    point_RL = alt.Chart(data).mark_point(fill = 'white', color = '#dd4b5f').encode(
        alt.X('Year:O'),
        alt.Y(y_axis)
    ).transform_filter(alt.datum.County == 'Red Lake County')
    
    text_RL = alt.Chart(data).mark_text(color = '#dd4b5f', opacity = 0.6, dy = 20, dx = -15, fontSize = 13, fontWeight = 500).encode(
        alt.X('Year:O'),
        alt.Y(y_axis),
        text = 'County_State'
    ).transform_filter((alt.datum.County == 'Red Lake County') & (alt.datum.Year == '2014'))
    
    lines = alt.Chart(data).mark_line(color = '#f2a952').encode(
        alt.X('Year:O'),
        alt.Y(y_axis)
    ).transform_filter(selection)
    
    points = alt.Chart(data).mark_point(fill = 'white', color = '#f2a952').encode(
        alt.X('Year:O'),
        alt.Y(y_axis)
    ).transform_filter(selection)
    
    texts = alt.Chart(data).mark_text(color = '#f2a952', opacity = 0.8, dy = -25, dx = 30, fontSize = 13, fontWeight = 500).encode(
        alt.X('Year:O'),
        alt.Y(y_axis),
        text = 'County_State'
    ).transform_filter(selection).transform_filter(alt.datum.Year == '2011')
    
    return box + line_RL + point_RL + lines + points + text_RL + texts

box_unemp = boxplot(df2, 'Unemployment_Rate:Q', '#55b9cf', 'County Unemployment Rate')
box_pov = boxplot(df3, 'Poverty_Rate:Q', '#a6d753', 'County Poverty Rate')

vis1 = (base_bars + bar_highlight + county_text + line | (box_unemp | box_pov)).configure_view(
    strokeWidth=0
)





#-------- VIS 2 (MHV/MHI Scatter Plot) --------# 

# Dropdown Selection (State)
state_list = df['State'].unique().tolist()
selectState = alt.selection_single(
    fields = ['State'],
    name = 'State ',
    bind = alt.binding_select(options = [None] + state_list, labels = ['All'] + state_list, name = 'State ')
)

selection = alt.selection_single(on = 'mouseover',empty = 'none')

# Scatter Plot
scatter_plot = alt.Chart(
    data = df,
    width = 600, 
    height = 500
).encode(
    alt.X('Median_HI:Q', axis = alt.Axis(format = '~s', titleFontSize = 14), scale=alt.Scale(domain=[10000, 130000])),
    alt.Y('Median_HV:Q', axis = alt.Axis(format = '~s', titleFontSize = 14), scale=alt.Scale(domain=[0, 800000])),
    tooltip = [alt.Tooltip('State:N'),
               alt.Tooltip('County:N'),
               alt.Tooltip('Median_HV:Q', title = 'Median Home Value'),
               alt.Tooltip('Median_HI:Q', title = 'Median Household Income'),
               alt.Tooltip('MHV_MHI_Ratio:Q', title = 'MHV/MHI Ratio Ratio')]
)

# All points
all_points = scatter_plot.mark_point(
    color = 'white', 
    fill = 'lightgray',
    strokeWidth = 0.8,
    opacity = 0.6,
    size = 90).add_selection(
    selectState
)

point_highlight = scatter_plot.mark_point(
    color = 'white', 
    fill = '#55b9cf',
    strokeWidth = 0.8,
    opacity = 0.6,
    size = 90).transform_filter(selectState).add_selection(
    selection
).encode(
    color = alt.condition(selection, alt.value('black'), alt.value('white'))
)

# Red Lake County
RL_point = scatter_plot.mark_point(
    color = 'white',
    fill = '#dd4b5f',
    strokeWidth = 0.8,
    size = 120
).transform_filter(
alt.datum.County == 'Red Lake County'
)

# Red Lake County Annotation
annotation = alt.Chart(df).mark_text(
    align = 'left',
    baseline = 'middle',
    fontSize = 16,
    color = '#dd4b5f',
    dx = 15
).encode(
    alt.X('Median_HI:Q'),
    alt.Y('Median_HV:Q'),
    text = 'County_State'
).transform_filter(
    alt.datum.County == 'Red Lake County'
)

# Top Histogram
top_hist = alt.Chart(
    data = df,
    width = 600,
    height = 85
).mark_bar(color = '#55b9cf', opacity = 0.6).encode(
    alt.X('Median_HI:Q', 
          bin = alt.Bin(maxbins = 50, extent = alt.Scale(domain=(10000, 130000)).domain), 
          title = None,
          axis=alt.Axis(labels=False, tickSize = 0, domainOpacity = 0.4)),
    alt.Y('count()', 
          title = '', 
          axis = alt.Axis(grid = False, labels=False, tickSize = 0, domainOpacity = 0))
).transform_filter(selectState)

# Right Histogram
right_hist = alt.Chart(
    data = df,
    width = 85,
    height = 500
).mark_bar(color = '#55b9cf', opacity = 0.6).encode(
    alt.X('count()', 
          title = '', 
          axis = alt.Axis(grid = False, labels=False, tickSize = 0, domainOpacity = 0)),
    alt.Y('Median_HV:Q', 
          bin = alt.Bin(maxbins = 40, extent = alt.Scale(domain=(0, 800000)).domain), 
          title = None,
          axis=alt.Axis(labels = False, tickSize = 0, domainOpacity = 0.4))
).transform_filter(selectState)

# Vertical & Horizontal Lines
avg_MHI = alt.Chart(df).mark_rule(strokeDash=[4,4], opacity = 0.8).encode(alt.X('mean(Median_HI):Q', title = 'Median Household Income'))
avg_MHV = alt.Chart(df).mark_rule(strokeDash=[4,4], opacity = 0.8).encode(alt.Y('mean(Median_HV):Q', title = 'Median Home Value'))

avg_MHV_text = alt.Chart(df).mark_text(
    text = 'US Average MHV',
    baseline = 'middle',
    fontSize = 12,
    color = '#555555',
    dx = -250,
    dy = -10
).encode(
    alt.Y('mean(Median_HV):Q')
)

avg_MHI_text = alt.Chart(df).mark_text(
    text = 'US Average MHI',
    baseline = 'middle',
    fontSize = 12,
    color = '#555555',
    dx = 200,
    dy = 10,
    angle = 270
).encode(
    alt.X('mean(Median_HI):Q')
)

quad = alt.Chart(df).mark_rect(fill ='#dddddd', fillOpacity = 0.1).encode(
    x=alt.value(225),
    y=alt.value(418),
    x2=alt.value(600),
    y2=alt.value(500)
)

vis2 = (top_hist & (quad + all_points + point_highlight + RL_point + annotation + avg_MHI + avg_MHI_text + avg_MHV + avg_MHV_text | right_hist)).configure_view(
    stroke=None
)



#-------- VIS 3 (GDP Growth and Farm Earnings Line Graphs) --------# 
# Interactions
counties = alt.topo_feature(data.us_10m.url, 'counties')
selection = alt.selection_single(on = 'mouseover',empty = 'none')
selectCounty = alt.selection_single(fields = ['County_State'],empty = 'none')

# US map
map = alt.Chart(counties).mark_geoshape(stroke = 'white', strokeWidth = 0.25).encode(
    color = alt.Color('Scale:Q', 
                      scale = alt.Scale(range = ['#a0651a','#f2e9d0','#a2d9d1']),
                      legend = alt.Legend(orient ='none',
                                          legendX = 200,legendY = 0,
                                          direction = 'horizontal', 
                                          title = 'Natural Amenities Scale',
                                          titleAnchor = 'middle',
                                          gradientLength = 160)),
    tooltip = [alt.Tooltip('County_State:N', title = 'County'), alt.Tooltip('Scale:Q', title = 'Natural Amenities Scale')]
).transform_lookup(
    lookup = 'id',
    from_ = alt.LookupData(df4, 'id', ['Scale','County_State'])
).project(
    type = 'albersUsa'
).properties(
    width = 400,
    height = 500
).add_selection(
    selection
).add_selection(
    selectCounty
).encode(
    stroke = alt.condition(selection, alt.value('black'), alt.value('white'))
).transform_calculate(
    state_id = "(datum.id / 1000)|0"
).transform_filter(
    (alt.datum.state_id) == 27
)

# Line Chart(Farm Earnings and GDP Growth)
line_chart_farm = alt.Chart(df7).mark_line().encode(
    alt.X('Year:N', axis = alt.Axis(tickOpacity = 0, labelAngle = 315, title = '')),
    alt.Y('Farm_Earn_Percentage:Q', scale=alt.Scale(domain=[-10, 50]), axis = alt.Axis(tickOpacity = 0, title = 'Farm Earnings Percentage (%)', domainOpacity = 0))
).properties(
    width = 600,
    height = 215
).transform_filter(selectCounty) #.transform_filter(alt.datum.County == 'Red Lake County')

line_chart_GDP = alt.Chart(df6).mark_line().encode(
    alt.X('Year:N', axis = alt.Axis(tickOpacity = 0, labelAngle = 315, title = '')),
    alt.Y('GDP_Growth_Percentage:Q', scale=alt.Scale(domain=[-50, 70]), axis = alt.Axis(tickOpacity = 0, title = 'GDP Growth (%)', domainOpacity = 0))
).properties(
    width = 600,
    height = 215
).transform_filter(selectCounty)

def marks(data, y_axis):
    line_RL = alt.Chart(data).mark_line(color = '#dd4b5f').encode(
        alt.X('Year:O'),
        alt.Y(y_axis)
    ).transform_filter(alt.datum.County == 'Red Lake County')

    point_RL = alt.Chart(data).mark_point(fill = 'white', color = '#dd4b5f').encode(
        alt.X('Year:O'),
        alt.Y(y_axis)
    ).transform_filter(alt.datum.County == 'Red Lake County')
    
    text_RL = alt.Chart(data).mark_text(color = '#dd4b5f', opacity = 0.6, dy = 20, dx = -15, fontSize = 13, fontWeight = 500).encode(
        alt.X('Year:O'),
        alt.Y(y_axis),
        text = 'County_State'
    ).transform_filter((alt.datum.County == 'Red Lake County') & (alt.datum.Year == 2014))
    
    lines = alt.Chart(data).mark_line(color = '#f2a952').encode(
        alt.X('Year:O'),
        alt.Y(y_axis)
    ).transform_filter(selectCounty)
    
    points = alt.Chart(data).mark_point(fill = 'white', color = '#f2a952').encode(
        alt.X('Year:O'),
        alt.Y(y_axis)
    ).transform_filter(selectCounty)
    
    texts = alt.Chart(data).mark_text(color = '#f2a952', opacity = 0.8, dy = 20, dx = 30, fontSize = 13, fontWeight = 500).encode(
        alt.X('Year:O'),
        alt.Y(y_axis),
        text = 'County_State'
    ).transform_filter(selectCounty).transform_filter(alt.datum.Year == 2007)
    
    return line_RL + point_RL + lines + points + text_RL + texts

mark_GDP = marks(df6, 'GDP_Growth_Percentage:Q')
mark_farm = marks(df7, 'Farm_Earn_Percentage:Q')

vis3 = (map | ((line_chart_farm + mark_farm) & (line_chart_GDP + mark_GDP))).configure_view(strokeWidth = 0) 



##### Display graphs

# Title
col1, col2= st.columns(2)
with col1:
    st.title("Is Red Lake County Really ‘America’s Worst Place to Live’?")

# Subtitle
st.write("SI649 Communicative Visualization Project (Interactive) - made by Michelle Cheng using Altair, Tableau and Streamlit")
st.write("")
st.write("")
st.write("")

# Vis 1
col3, col4, col5 = st.columns([1,5,1])
with col4:
    st.subheader("**Is living in Red Lake County affordable?**")
    st.write("Though Red Lake County is ranked last in terms of Natural Amenities, living in the county isn't actually that bad. **Try clicking on the top ranked counties from the bar chart below and compare their unemployment rate and poverty rate with Red Lake County!** As shown in the two boxplots, Red Lake County’s unemployment rate and poverty have mostly been lower than the median rate of all U.S. counties over the years.  When comparing Red Lake County with counties with higher natural amenities scale, Red Lake County's unemployment and poverty rate are mostly relatively lower over the years")
st.write("")
st.write("")
st.write("")
colA, colB, colC = st.columns([1,15,1])
with colB:
    st.write(vis1)
st.write("")
st.write("")
st.write("")

# Vis 2
col3, col4, col5 = st.columns([1,5,1])
with col4:
    st.write("As shown in the scatter plot below , Red Lake County falls in the fourth quadrant of the distribution that is divided  by the two average lines. This means that the median household income of Red Lake County is higher than the US average, while the county’s median home value is sitting lower than the U.S. average, making Red Lake County one of the counties that have a lower home value/household income ratio for people to afford their livings. **Try using the dropdown selection box to see and compare different state distributions with Red Lake County!** To look for the exact numbers for each county, mouseover through the data points on the plot. (Note: California has the highest MHV/MHI ratio, whereas Nebrask has the lowest MHV/MHI ratio. Give these two states a try!)")
st.write("")
st.write("")
colA, colB, colC = st.columns([1,2,1])
with colB:
    st.write(vis2)
st.write("")
st.write("")
st.write("")

# Vis 3
col3, col4, col5 = st.columns([1,5,1])
with col4:
    st.subheader("**What is it like to work in Red Lake County?**")
    st.write("Although Red Lake County was ranked last in terms of natural amenities, farming and agriculture still plays a significant role in supporting Red Lake County’s local economy. Lets compare Red Lake County’s farm earnings percentage and GDP growth with other counties in Minnesota . **Try clicking on the different counties from the state map below and compare the percentages with Red Lake County’s!** You’ll see that, when clicking on counties with the highest amenities score among Minnesota, not all of them relies on farm earnings more heavily than Red Lake County does. Also, a lot of them have lower GDP growth than Red Lake County does. Working in Red Lake County doesn’t sound that bad, right? (Note: Streamlit failed to show the annoations of the line graph. The red Line represents Red Lake County. The yellow Line represents the selected county.)")
st.write("")
st.write("")
st.write("")
colA, colB, colC = st.columns([1,5,1])
with colB:  
    st.write(vis3)    
st.write("")
st.write("")
st.write("")

# Vis4
col3, col4, col5 = st.columns([1,5,1])
with col4:
    st.write("In comparison with Minnesota, New York, and the entire U.S., commute time in Red Lake county is much shorter, with 35% of the employed population spending less than 10 minutes commuting to work every day.  **Try using the slider on the right side of the packed bubble chart to switch between locations and see how the time bubbles changes in size!**")
st.write("")
colA, colB, colC = st.columns([1,8,1])
with colB:  
#-------- VIS 4 (Commute Time) --------# 
    def main():
        html_temp = """<div class='tableauPlaceholder' id='viz1636737658251' style='position: relative'><noscript><a href='#'><img alt='Dashboard 8 ' src='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;Co&#47;CommVis_16365073470030&#47;Dashboard8&#47;1_rss.png' style='border: none' /></a></noscript><object class='tableauViz'  style='display:none;'><param name='host_url' value='https%3A%2F%2Fpublic.tableau.com%2F' /> <param name='embed_code_version' value='3' /> <param name='site_root' value='' /><param name='name' value='CommVis_16365073470030&#47;Dashboard8' /><param name='tabs' value='no' /><param name='toolbar' value='yes' /><param name='static_image' value='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;Co&#47;CommVis_16365073470030&#47;Dashboard8&#47;1.png' /> <param name='animate_transition' value='yes' /><param name='display_static_image' value='yes' /><param name='display_spinner' value='yes' /><param name='display_overlay' value='yes' /><param name='display_count' value='yes' /><param name='language' value='en-US' /><param name='filter' value='publish=yes' /></object></div>                <script type='text/javascript'>                    var divElement = document.getElementById('viz1636737658251');                    var vizElement = divElement.getElementsByTagName('object')[0];                    if ( divElement.offsetWidth > 800 ) { vizElement.style.width='1000px';vizElement.style.height='827px';} else if ( divElement.offsetWidth > 500 ) { vizElement.style.width='1000px';vizElement.style.height='827px';} else { vizElement.style.width='100%';vizElement.style.height='727px';}                     var scriptElement = document.createElement('script');                    scriptElement.src = 'https://public.tableau.com/javascripts/api/viz_v1.js';                    vizElement.parentNode.insertBefore(scriptElement, vizElement);                </script>"""
        components.html(html_temp, width = 1000, height = 1000)
    if __name__ == "__main__":    
        main()

st.write("")
st.write("Data Source: U.S. Census Bureau, U.S. Bureau of Economic Analysis (BEA), U.S. Bureau of Labor Statistics")
