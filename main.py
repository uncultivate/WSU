import pandas as pd
import streamlit as st
import numpy as np
import altair as alt


st.title('Western Sydney Census Analysis')

all_lgas = ["Blacktown","Blue Mountains","Camden","Campbelltown (NSW)","Canterbury-Bankstown","Cumberland","Fairfield","Hawkesbury","Liverpool","Parramatta","Penrith","The Hills","Wollondilly"]

with st.sidebar:
    c_2016 = st.checkbox("Census 2016", value=True)
    c_2021 = st.checkbox("Census 2021", value=True)
    c_2026 = st.checkbox("2026 Projections", value=True)

    selected_lgas = st.multiselect(
        "LGAs", options=all_lgas, default=all_lgas
    )
    category = st.radio(
    "Pick a category for analysis",
    ('Population','Education','Income','Industry'))



demo = pd.read_csv('demo3.csv', skiprows=9, nrows=4)
demo.index = demo['LGA (UR)']
industry = pd.read_csv('ind2.csv', skiprows=9, nrows=20)
income = pd.read_csv('inc2.csv', skiprows=9, nrows=20)
education = pd.read_csv('edu2.csv', skiprows=9, nrows=11)

demo16 = pd.read_csv('demo163.csv', skiprows=9, nrows=4)
demo16.index = demo['LGA (UR)']
industry16 = pd.read_csv('ind162.csv', skiprows=9, nrows=20)
income16 = pd.read_csv('inc162.csv', skiprows=9, nrows=20)
education16 = pd.read_csv('edu162.csv', skiprows=9, nrows=11)

demo26 = pd.read_csv('demo4.csv', skiprows=9, nrows=4)
demo26.index = demo['LGA (UR)']



if category == 'Population':
    st.subheader('Population')
    st.write('The ABS estimates that the population in NSW is increasing by 0.5% per year, which is probably a couple of points lower than what we are seeing here.')
    #tidy dfs
    demog = demo.iloc[:-1,:]
    demog16 = demo16.iloc[:-1,:]
    demog26 = demo26.iloc[:-1,:]

    #add DataFrames to subplots
    for lga in selected_lgas:
        st.subheader(lga)
        c16 = demog16[lga]
        c21 = demog[lga]
        c26 = demog26[lga]
        d = {'2016': c16, '2021': c21, '2026': c26}
        
        if not c_2016:
            d.pop("2016")
        if not c_2021:
            d.pop("2021")
        if not c_2026:
            d.pop("2026")
        df = pd.DataFrame(data=d)
        st.line_chart(data=df)

if category == 'Education':
    st.subheader('Education')
    st.write("This page measures the highest level of educational achievement. LGAs trending upwards for Bachelor and Post Grad are an indicator of increased demand in coming years")
    
    #tidy dfs
    edu = education.iloc[:-3,:]
    edu.index = edu['LGA (UR)']
    edu16 = education16.iloc[:-3,:-1]
    edu16.index = edu16['LGA (UR)']
    
    #add DataFrames to subplots
    for lga in selected_lgas:
        st.subheader(lga)
        c16 = edu16[lga].iloc[1:]
        c21 = edu[lga].iloc[1:]
        d = {'2016': c16, '2021': c21}
        
        if not c_2016:
            d.pop("2016")
        if not c_2021:
            d.pop("2021")
        df = pd.DataFrame(data=d)
        st.line_chart(data=df)

if category == 'Income':
    st.subheader('Income')
    st.write("LGAs where incomes are trending higher will be an indicator of a future increase in tertiary education demand, as more families enter a higher socio-economic band.")
    
    #tidy dfs
    inc = income.iloc[:-3,:]
    #inc.index = inc['LGA (UR)']
    inc16 = income16.iloc[:-4,:-1]
    #inc16.index = inc16['LGA (UR)']
    

    
    #add DataFrames to subplots
    for lga in selected_lgas:
        st.subheader(lga)
        c16 = pd.DataFrame({'lga': inc16[lga].iloc[1:], 'year':'2016'})
        c16['ind'] = inc16['LGA (UR)']
        c21 = pd.DataFrame({'lga': inc[lga].iloc[1:], 'year':'2021'})
        c21['ind'] = inc['LGA (UR)'].iloc[1:]

        df = pd.merge(c16, c21, how='outer', on=['ind','lga','year'])
        
        if not c_2016:
            df = df[df['year'] == '2021']
        if not c_2021:
            df = df[df['year'] == '2016']

        cats = ['<0','0','149','299','399','499','649','799','999','1249','1499','1749','1999','2999','3499','High']
        
        
        c = alt.Chart(df).mark_line().encode(x=alt.X('ind', sort=cats, axis=alt.Axis(title='Income')), y=alt.Y('lga', axis=alt.Axis(title='Count')), color='year')
        st.altair_chart(c, use_container_width=True)
            


if category == 'Industry':
    st.subheader('Industry')
    st.write("Analysing the key industries for each LGA and trends between censuses will be a good predictor of course demand in the coming years.")
    
    #tidy dfs
    indus = industry.iloc[:-1,:]
    indus.index = indus['LGA (UR)']
    indus16 = industry16.iloc[:-1,:-1]
    indus16.index = indus16['LGA (UR)']
    
    #add DataFrames to subplots
    for lga in selected_lgas:
        st.subheader(lga)
        c16 = pd.DataFrame({'lga': indus16[lga].iloc[1:], 'year':'2016'})
        c16['ind'] = indus16['LGA (UR)']
        c21 = pd.DataFrame({'lga': indus[lga].iloc[1:], 'year':'2021'})
        c21['ind'] = indus['LGA (UR)'].iloc[1:]

        df = pd.merge(c16, c21, how='outer', on=['ind','lga','year'])
        
        if not c_2016:
            df = df[df['year'] == '2021']
        if not c_2021:
            df = df[df['year'] == '2016']

        cats = ['<0','0','149','299','399','499','649','799','999','1249','1499','1749','1999','2999','3499','High']
        
        
        c = alt.Chart(df).mark_bar().encode(x=alt.X('lga', axis=alt.Axis(title='Count')), y=alt.Y('year', title=''), color='year', row=alt.Row('ind', title='', header=alt.Header(labelAngle=0, labelAlign='left')))
        st.altair_chart(c, use_container_width=True)
        
       