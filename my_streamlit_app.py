import streamlit as st
import pandas as pd
import seaborn as sns
import altair as alt


st.title('Cars data')


link = "https://raw.githubusercontent.com/murpi/wilddata/master/quests/cars.csv"
df_cars = pd.read_csv(link)

#### heatmap
st.write("Here we can observe the relations between the different cars specifications. Some may appear obvious, but others can be counter intuitive. Let's dig a little bit deeper in some of them.")

viz_correlation = sns.heatmap(df_cars.corr(), 
								center=0,
								cmap = sns.color_palette("vlag", as_cmap=True)
								)

st.pyplot(viz_correlation.figure)

print('/n')
print()
print()

#### correlations
### time to 60 / hp
st.write("\n\n\n")
st.title("Obvious correlation")
st.write("However spare some time to select the continent on the dropdown menu in order to observe the differences.")

alt.data_transformers.disable_max_rows()

continent_list = list(df_cars['continent'].unique())

input_dropdown = alt.binding_select(options=continent_list)
selection = alt.selection_single(fields=['continent'], bind=input_dropdown, name='Select')

alt_plot = alt.Chart(df_cars, height=400, width=800).mark_point().encode(
    x='hp',
    y='time-to-60',
    tooltip='time-to-60'
).add_selection(
    selection
).transform_filter(
    selection
)

alt_plot

st.write("---")

### mpg /weight

mean_mpg_year = df_cars.groupby(['year','continent']).agg('mean').reset_index()


st.write("\n\n\n")
st.title("Not so obvious correlation")
st.write("Good to know that the average range of a car has increased over the years.\n\nAlthough the progression is flatter in Japan, overall they are doing better than US.")

alt.data_transformers.disable_max_rows()

continent_list = list(mean_mpg_year['continent'].unique())

input_dropdown = alt.binding_select(options=continent_list)
selection = alt.selection_single(fields=['continent'], bind=input_dropdown, name='Select')

alt_plot = alt.Chart(mean_mpg_year, height=400, width=800).mark_bar().encode(
    x = alt.X('year:N', scale=alt.Scale(zero=False)),
    y='mpg',
    tooltip='mpg'
).add_selection(
    selection
).transform_filter(
    selection
)

alt_plot

st.write("---")


### number of cylinders

cylinders_distribution = df_cars.groupby(['cylinders','continent']).size().to_frame('number_of_cars').reset_index()


st.write("\n\n\n")
st.title("Distribution of the cars over the numbers of cylinders")
st.write("Japan is the only region where you can find 3.\n\nUS is the only region where you can find 8, where it's actually the most common number of cylinders.")

alt.data_transformers.disable_max_rows()

continent_list = list(cylinders_distribution['continent'].unique())

input_dropdown = alt.binding_select(options=continent_list)
selection = alt.selection_single(fields=['continent'], bind=input_dropdown, name='Select')

alt_plot = alt.Chart(cylinders_distribution, height=400, width=800).mark_bar().encode(
    x = alt.X('number_of_cars', scale=alt.Scale(zero=False)),
    y='cylinders:N',
    tooltip='cylinders:N'
).add_selection(
    selection
).transform_filter(
    selection
)

alt_plot
