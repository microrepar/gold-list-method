import datetime

import pandas as pd
import streamlit as st
from st_pages import add_page_title

from app.core.dao_parquet import NotebookDAO
from app.model import Notebook

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
    col1, col2 = st.columns(2)
    list_size = col1.slider("List size", min_value=10, max_value=25, value=20)
    days_period = col2.slider("Days period", min_value=5, max_value=20, value=15)

    # Every form must have a submit button.
    submitted = st.form_submit_button("ADD NEW NOTEBOOK", type="primary", use_container_width=True)

    if submitted and notebook_name.strip():        
        notebook = Notebook(notebook_name.strip(), 
                            created_at=datetime.datetime.now().date(),
                            list_size=list_size,
                            days_period=days_period,
                            foreign_idiom=foreign_idiom, 
                            mother_idiom=mother_idiom)        
        try:
            new_notebook = notebook_dao.insert(notebook)
            placehold_error_msg.success(f'{new_notebook} was inserted successfully!')
            st.toast('Notebook was inserted successfully.')
        except Exception as error:
            placehold_error_msg.error(str(error), icon="🚨")           
            st.toast('Something went wrong!')
            st.error(str(error), icon="🚨")           
    elif submitted:
        placehold_error_msg.error('The name field must be valid value!', icon="🚨")


notebook_list = notebook_dao.get_all(Notebook())
if notebook_list:
    df = pd.concat([pd.DataFrame(n.data_to_dataframe()) for n in notebook_list], ignore_index=True)
    st.subheader('Notebooks')
    st.dataframe(df, hide_index=True, use_container_width=True)

