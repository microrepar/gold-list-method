from pathlib import Path
from typing import List

import os.path
import numpy as np
import pandas as pd
import streamlit as st
from st_pages import add_page_title, show_pages_from_config

from app.core.dao_parquet import NotebookDAO
from app.model import Notebook
import pandas as pd

st.set_page_config(layout='wide')

notebook_dao = NotebookDAO()

# Either this or add_indentation() MUST be called on each page in your
# app to add indendation in the sidebar
placehold_error_msg = st.empty()
add_page_title()
 
# st.title('NEW NOTEBOOK')

with st.form("my_form"):   
    st.write("Create Notebook")
    notebook_name = st.text_input('Notebook name')
    col1, col2 = st.columns(2)
    foreign_idiom = col1.text_input('Foreign idiom')
    mother_idiom = col2.text_input('Mother idiom')
    list_size = st.slider("List size", min_value=10, max_value=25, value=20)

    # Every form must have a submit button.
    submitted = st.form_submit_button("ADD NEW NOTEBOOK", type="primary", use_container_width=True)
    if submitted and notebook_name.strip():        
        notebook = Notebook(notebook_name.strip(), list_size=list_size, 
                            foreign_idiom=foreign_idiom, mother_idiom=mother_idiom)        
        try:
            new_notebook = notebook_dao.insert(notebook)
            placehold_error_msg.success(f'{new_notebook} was inserted with success!')
        except Exception as error:
            placehold_error_msg.error(str(error), icon="🚨")           
    elif submitted:
        placehold_error_msg.error('The name field must be value valid!', icon="🚨")


notebook_list = notebook_dao.get_all(Notebook())
if notebook_list:
    df = pd.concat([pd.DataFrame(n.data_to_dataframe()) for n in notebook_list], ignore_index=True)
    st.subheader('Notebooks')
    st.dataframe(df, use_container_width=True)

