# Your Name
# si649f20 Altair transforms 2

# imports we will use
import streamlit as st
import altair as alt
import pandas as pd

datasetURL="https://raw.githubusercontent.com/eytanadar/si649public/master/lab5/assets/hw/movie_after_1990.csv"
movies_test=pd.read_csv(datasetURL, encoding="latin-1")

#Title
st.title("Lab5 by Michelle Cheng")

### Making of all charts

# Visualization 1
line_chart = alt.Chart(movies_test, width = 800).transform_filter(
    alt.datum.year <= 1997
).mark_line().encode(
    alt.X('year:O'),
    alt.Y('mean(budget):Q')
)

dot_chart = alt.Chart(movies_test, width = 800).transform_joinaggregate(
    budget_mean = 'mean(budget)'
).transform_calculate(
    double_budget_mean = alt.datum.budget_mean * 2
).transform_filter(
    alt.datum.year <= 1997
).transform_filter(
        alt.datum.budget > alt.datum.double_budget_mean
).mark_circle().encode(
    alt.X('year:O'),
    alt.Y('budget:Q')
)

annotation = dot_chart.transform_joinaggregate(
    groupby = ['year'],
    max_budget = 'max(budget)'
).transform_filter(
    alt.datum.budget == alt.datum.max_budget
).mark_text(
    align='center',
    baseline = 'bottom',
    dy = -8
).encode(
    text = alt.Text('title:N')
)



# Visualization 2
heatmap = alt.Chart(movies_test).transform_filter(
    alt.datum.test_result != 'dubious'
).mark_rect().encode(
    x = alt.X('rating:Q', bin = alt.Bin(maxbins = 8)),
    y = alt.Y('test_result:N'),
    color = alt.Color('count(title):N')
)

txt_annotation = alt.Chart(movies_test).transform_filter(
    alt.datum.test_result != 'dubious'
).mark_text(
    align='center',
    baseline = 'middle'
).encode(
    x = alt.X('rating:Q', bin = alt.Bin(maxbins = 8)),
    y = alt.Y('test_result:N'),
    text = alt.Text('count(title)')
)

highlight = alt.Chart(movies_test).transform_joinaggregate(
    groupby = ['test_result'],
    max_rating = 'max(rating)'
).transform_filter(
    alt.datum.test_result != 'dubious'
).transform_filter(
    alt.datum.max_rating > 9
).mark_rect(stroke = 'red', fill = None).encode(
    x = alt.X('rating:Q', bin = alt.Bin(maxbins = 8)),
    y = alt.Y('test_result:N')
)




# Visualization 3
base_dom = alt.Chart(movies_test).transform_window(
    groupby = ['test_result'],
    sort = [alt.SortField('dom_gross', order = 'descending')],
    dom_gross_rk = 'rank(*)'
).transform_filter(
    alt.datum.dom_gross_rk <= 10
)


dom_bar = base_dom.mark_bar().encode(
    alt.X('mean(dom_gross):Q'),
    alt.Y('test_result:N'),
    color = alt.Color('mean(dom_gross):Q')
)


dom_text = base_dom.transform_window(
    sort = [alt.SortField('dom_gross', order = 'ascending')],
    dom_rank = 'rank(*)',
    groupby = ['test_result']
).transform_filter(
    alt.datum.dom_rank == 10 
).mark_text(
    align='left',
    baseline = 'middle'
).encode(
    alt.Y('test_result:N'),
    text = alt.Text('title:N')
)

# -------

base_int = alt.Chart(movies_test).transform_window(
    groupby = ['test_result'],
    sort = [alt.SortField('int_gross', order = 'descending')],
    int_gross_rk = 'rank(*)'
).transform_filter(
    alt.datum.int_gross_rk <= 10
)


int_bar = base_int.mark_bar().encode(
    alt.X('mean(int_gross):Q'),
    alt.Y('test_result:N'),
    color = alt.Color('mean(int_gross):Q')
)


int_text = base_int.transform_window(
    sort = [alt.SortField('int_gross', order = 'ascending')],
    int_rank = 'rank(*)',
    groupby = ['test_result']
).transform_filter(
    alt.datum.int_rank == 10 
).mark_text(
    align='left',
    baseline = 'middle'
).encode(
    alt.Y('test_result:N'),
    text = alt.Text('title')
)



# Visualization 4
chart4 = alt.Chart(movies_test).transform_fold(
    ['budget', 'int_gross'],
    as_ = ['finance', 'dollars']
).mark_bar().encode(
    alt.X('mean(dollars):Q'),
    alt.Y('finance:N'),
    color = alt.Color('finance:N')
)

### Display charts

st.write(line_chart + dot_chart + annotation)
st.write(heatmap + txt_annotation + highlight)
st.write(((dom_bar + dom_text) & (int_bar + int_text)).resolve_scale(x = 'shared', color = 'independent'))
st.write(chart4)