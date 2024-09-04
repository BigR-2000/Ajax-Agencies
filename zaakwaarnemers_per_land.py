import pandas as pd
import streamlit as st
import numpy as np

##Layout 
st.set_page_config(page_title = 'Lijst zaakwaarnemers',
                   page_icon = ':briefcase:',
                   layout="wide")

st.markdown("""
    <style>
        .title-wrapper {
            display: flex;
            align-items: center;
        }
        .icon {
            margin-right: 10px;
        }
    </style>
""", unsafe_allow_html=True)

##titel en tekst
def title_with_icon(icon, title):
    st.markdown(f"<div class='title-wrapper'><div class='icon'>{icon}</div><h4>{title}</h4></div>", unsafe_allow_html=True)

title_with_icon('', "Lijst zaakwaarnemers en agentschappen")
st.divider()
st.markdown("- Vind zaakwaarnemers van bepaalde landen")
st.markdown("- Vind zaakwaarnemers van specifieke spelers")
st.markdown("- Check of er contactgegevens beschikbaar zijn van de zaakwaarnemers")
st.markdown("")


##Inlezen data spelers en zaakwaarnemers
try:
    lijst = pd.read_csv(f"Lijst_ZW.csv", encoding='latin1', sep=';')
    lijst_speler = pd.read_csv(f"Lijst_SP.csv", encoding='latin1', sep=';')
except:
    print('fout bij inlading')

##subset met enkele nodige data spelers
lijst_speler = lijst_speler.rename(columns={'ï»¿Player': 'Player'})
lijst_speler = lijst_speler[['Player', 'Club', 'Agency']]
lijst_speler.drop_duplicates(subset=['Player','Club'], inplace=True)
##Goedzetten data van de zaakwaarnemers
lijst2 = lijst 
lijst = lijst.drop(columns = ['Fax', 'Link'])
lijst = lijst.rename(columns={'Ã¸-Market value': 'Market value'})
lijst = lijst.rename(columns={'ï»¿Agency name': 'Agency'})
lijst['Link'] = lijst2['Link']

lijst['Total market value'] = lijst['Total market value'].map(lambda x:x.lstrip('â¬'))
lijst['Market value'] = lijst['Market value'].map(lambda x:x.lstrip('â¬'))

lijst.sort_values(by=['Agency', 'Players 1st tier', 'Market value'], inplace = True)
lijst.drop_duplicates(subset=['Agency'], keep = 'last', inplace = True)

##samenbrengen data zaakwaarnemers en spelers
lijst_spzw = pd.merge(lijst_speler, lijst, on= 'Agency', how='left')

##Rare letters veranderen naar de juiste letters
lijst_spzw = lijst_spzw.replace('Ã©', 'é', regex=True)
lijst_spzw = lijst_spzw.replace('Ã³', 'ó', regex=True)
lijst_spzw = lijst_spzw.replace('Ã', 'Á', regex=True)
lijst_spzw = lijst_spzw.replace('Ã¡', 'á', regex=True)
lijst_spzw = lijst_spzw.replace('Ã', 'í', regex=True)
lijst_spzw = lijst_spzw.replace('í²', 'ò', regex=True)
lijst_spzw = lijst_spzw.replace('Ä', 'ę', regex=True)
lijst_spzw = lijst_spzw.replace('í±', 'ñ', regex=True)
lijst_spzw = lijst_spzw.replace('í', 'Í', regex=True)
lijst_spzw = lijst_spzw.replace('íº', 'ú', regex=True)
lijst_spzw = lijst_spzw.replace('í¸', 'ø', regex=True)
lijst_spzw = lijst_spzw.replace('í¼', 'ü', regex=True)
lijst_spzw = lijst_spzw.replace('í', 'Ö', regex=True)
lijst_spzw = lijst_spzw.replace('í½', 'ý', regex=True)
lijst_spzw = lijst_spzw.replace('Ä±', 'ı', regex=True)
lijst_spzw = lijst_spzw.replace('í¶', 'ö', regex=True)
lijst_spzw = lijst_spzw.replace('í«', 'ë', regex=True)
lijst_spzw = lijst_spzw.replace('í', 'Ó', regex=True)
lijst_spzw = lijst_spzw.replace('í§', 'ç', regex=True)
lijst_spzw = lijst_spzw.replace('í¨', 'è', regex=True)
lijst_spzw = lijst_spzw.replace('Ä°', 'İ', regex=True)
lijst_spzw = lijst_spzw.replace('í', 'Ü', regex=True)
lijst_spzw = lijst_spzw.replace('Å', 'ş', regex=True)
lijst_spzw = lijst_spzw.replace('Ä', 'ğ', regex=True)
lijst_spzw = lijst_spzw.replace('í', 'Ç', regex=True)








## Alle selectie boxen introduceren voor het filteren van de dataset
col1, col2, col3 = st.columns([3, 0.75, 3])
with col1:
    agentschap = st.multiselect('💼 Zaakwaarnemer(s)', lijst_spzw['Agency'].unique())
    if agentschap:
        lijst_spzw = lijst_spzw.loc[lijst_spzw['Agency'].isin(agentschap)]
            
    land = st.multiselect('🌍 Land zaakwaarnemer(s)', lijst_spzw['Country'].unique())
    if land:
        lijst_spzw = lijst_spzw.loc[lijst_spzw['Country'].isin(land)]

with col3:        
    telefoon = st.selectbox('📞 Telefoonnr.', ['', 'Bekend', 'Onbekend'])
    if telefoon == 'Bekend':
        lijst_spzw = lijst_spzw.loc[lijst_spzw['Phone'] != '-'] 
        lijst_spzw = lijst_spzw.loc[lijst_spzw['Phone'].notna()]
    elif telefoon == 'Onbekend':
        lijst_spzw = lijst_spzw[(lijst_spzw['Phone'] == '-') | (lijst_spzw['Phone'].isna())]
    else:
        pass

    mail = st.selectbox('✉️ Email', ['', 'Bekend', 'Onbekend'])
    if mail == 'Bekend':
        lijst_spzw = lijst_spzw.loc[lijst_spzw['Email'] != '-'] 
        lijst_spzw = lijst_spzw.loc[lijst_spzw['Email'].notna()]
    elif mail == 'Onbekend':
        lijst_spzw = lijst_spzw[(lijst_spzw['Email'] == '-') | (lijst_spzw['Email'].isna())]
    else:
        pass

    website = st.selectbox('🌐 Website', ['', 'Bekend', 'Onbekend'])
    if website == 'Bekend':
        lijst_spzw = lijst_spzw.loc[lijst_spzw['Website'] != '-'] 
        lijst_spzw = lijst_spzw.loc[lijst_spzw['Website'].notna()]
    elif website == 'Onbekend':
        lijst_spzw = lijst_spzw[(lijst_spzw['Website'] == '-') | (lijst_spzw['Website'].isna())]
    else:
        pass

with col1:
    speler = st.multiselect('⚽ Speler(s)', lijst_spzw['Player'].unique())
    if speler:
        lijst_spzw = lijst_spzw.loc[lijst_spzw['Player'].isin(speler)]



##Weergave van de gefilterde dataset
lijst_spzw = lijst_spzw.reset_index(drop=True)
st.dataframe(lijst_spzw, height = 600)












