import datetime

import numpy as np
import pandas as pd
import streamlit as st
from st_pages import add_page_title

from app.core.dao_parquet import NotebookDAO, PageSectionDAO, SentenceDAO
from app.core.servico import build_page_section_with_sentence_list
from app.model import Group, Notebook, PageSection, Sentence

st.set_page_config(layout='wide')

placehold_container_msg = st.container()
placehold_container_msg.empty()

# Either this or add_indentation() MUST be called on each page in your
# app to add indendation in the sidebar
add_page_title()


page_section_dao = PageSectionDAO()
sentence_dao = SentenceDAO()
notebook_dao = NotebookDAO()

notebooks_list = notebook_dao.get_all()
notebook_dict = {n.name: n for n in notebooks_list}

selected_notebook = st.sidebar.selectbox('Notebook:', [n.name for n in notebooks_list])
selected_day = st.sidebar.date_input('Day List', datetime.datetime.now().date(), format='DD/MM/YYYY')

notebook = notebook_dict.get(selected_notebook)

st.title(f'INSERT LIST INTO {notebook.name.upper()}')

new_data_add = []
for i in range(1, notebook.list_size + 1 ):
    new_data_add.append(
        {
            "foreign_language": f"New sentence {i}",
            "mother_tongue": f'Translation {i}',
        }
    )


df_edit = pd.DataFrame(new_data_add)


column_configuration_data = {
    "foreign_language": st.column_config.TextColumn(
        "Foreign Language", help="The sentece or word that you want to learn"
    ),
    "mother_tongue": st.column_config.TextColumn(
        "Mother Tongue", help="translation the sentece or word that you want to learn"
    ),
}

column_configuration_added = {
    "list_seq": st.column_config.TextColumn(
        "Sequence", help="List Number",
        
    ),
    "date": st.column_config.TextColumn(
        "Created At", help="Insert Date"
    ),
}

st.markdown('**Add new list of sentences**')

placehold_sentences_sheet = st.empty()
placehold_btn_insert = st.empty()
placehold_page_exists = st.empty()


df_result = placehold_sentences_sheet.data_editor(
    df_edit,
    column_config=column_configuration_data,
    num_rows="fixed",
    hide_index=True,
    use_container_width=True,
)
df_result['remembered'] = False
df_result['translated_sentence'] = ''


if placehold_btn_insert.button('INSERT NEW LIST', type='primary', use_container_width=True):

    try:
        page_section = build_page_section_with_sentence_list(dataframe=df_result,
                                                             selected_day=selected_day,
                                                             notebook=notebook,
                                                             group=Group.HEADLIST)
        placehold_sentences_sheet.success(f'{page_section} was inserted with success!')
        placehold_btn_insert.empty()
    except Exception as error:
        placehold_container_msg.error(str(error), icon="🚨")
        if 'There is already a page'.upper() in str(error).upper():
            placehold_page_exists.error(str(error), icon="🚨")


import os.path
# The directory containing this file
from pathlib import Path

HERE = os.path.abspath(os.path.dirname(__file__))
sentence_file = Path(HERE).parent / 'data_base' / 'sentence.parquet'
page_section_file = Path(HERE).parent / 'data_base' / 'page_section.parquet'
df_page = pd.read_parquet(page_section_file)
df_sentence = pd.read_parquet(sentence_file)
st.markdown('PAGE SECTIONS')
st.dataframe(df_page)
st.markdown('SENTENCES')
st.dataframe(df_sentence)