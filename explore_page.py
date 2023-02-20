import streamlit as st 
import pandas as pd
import matplotlib.pyplot as plt

def shorten_categories(categories, cutoff):
    categorical_mp = {}
    for i in range(len(categories)):
        if categories.values[i] >= cutoff:
            categorical_mp[categories.index[i]] = categories.index[i]
        else:
            categorical_mp[categories.index[i]] = 'Other'
    return categorical_mp    

def clean_education(x):
    if 'Bachelor’s degree' in x:
        return 'Bachelor’s degree'
    if 'Master’s degree' in x:
        return 'Master’s degree'
    if 'Professional degree' in x or 'Other doctoral degree' in x:
        return 'Post grad'
    return 'Less than a Bachelors'


def clear_experience(x):
    if x == 'More than 50 years':
        return 50
    if x == 'Less than 1 year':
        return 0.5
    return float(x)

@st.cache_resource
def load_data():
    df = pd.read_csv("survey_results_public.csv")
    df = df[["Country","EdLevel","YearsCodePro","Employment","ConvertedCompYearly"]]
    df = df.rename({"ConvertedCompYearly": "Salary"}, axis=1)
    df = df[df["Salary"].notnull()]
    df = df.dropna()
    df = df[df["Employment"] == "Employed, full-time"]
    df = df.drop("Employment", axis=1)

    country_map = shorten_categories(df.Country.value_counts(), 400)
    df['Country'] = df['Country'].map(country_map)
    df = df[df['Salary'] <= 250000]
    df = df[df['Salary'] >= 10000]
    df = df[df['Country'] != 'Other']
    df['YearsCodePro'] = df['YearsCodePro'].apply(clear_experience)
    df['EdLevel'] = df['EdLevel'].apply(clean_education)
    return df

df = load_data()

def show_explore_page():
    st.title("Explore Software Engineer Salaries")
    st.write("""### Stack OVerflow Developer Survey 2022""")

    data = df["Country"].value_counts()

    fig1, ax1 = plt.subplots(1,1, figsize=(10,10))
    ax1.pie(data, labels=data.index, autopct="%10.1f%%", shadow=True, startangle=90)
    ax1.axis("equal")
    st.write("""### Number of data from diffrent countries""")
    st.pyplot(fig1)

    st.write("""### Mean salary base on country""")
    data= df.groupby(["Country"])["Salary"].mean().sort_values(ascending=True)
    st.bar_chart(data)

    st.write("""### Mean salary base on experience""")
    data= df.groupby(["YearsCodePro"])["Salary"].mean().sort_values(ascending=True)
    st.line_chart(data)