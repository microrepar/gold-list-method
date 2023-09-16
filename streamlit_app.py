import datetime

import pandas as pd
import streamlit as st
from st_pages import Page, Section, add_page_title, show_pages

from app.core.dao_parquet import NotebookDAO
from app.model import Group
from app.core.servico import build_page_section_with_sentence_list

st.set_page_config(layout='wide')

show_pages(
    [
        Page("streamlit_app.py", "Distillation", "🧠"),
        Section(name="Notebooks", icon=":books:"),
        # Can use :<icon-name>: or the actual icon
        Page("app/pages/add_new_notebook.py", "Add New Notebook", "📖"),
        Page("app/pages/add_new_list.py", "Add New List", "📃"),
    ]
)

placehold_container_msg = st.container()
placehold_container_msg.empty()

add_page_title()  # Optional method to add title and icon to current page

notebook_dao = NotebookDAO()
notebooks_list = notebook_dao.get_all()
notebook_dict = {n.name: n for n in notebooks_list}

selected_notebook = st.sidebar.selectbox('**NOTEBOOK:**', [n.name for n in notebooks_list])
selected_day = st.sidebar.date_input('**LIST OF DAY:**', datetime.datetime.now().date(), format='DD/MM/YYYY')

if len(notebooks_list) > 0:

    st.title(f'NOTEBOOK - {selected_notebook.upper()}')

    notebook = notebook_dict.get(selected_notebook)


    page_section_group_a = notebook.get_page_section(distillation_at=selected_day, 
                                                     group=Group.HEADLIST)
    page_section_group_b = notebook.get_page_section(distillation_at=selected_day, 
                                                     group=Group.B)
    page_section_group_c = notebook.get_page_section(distillation_at=selected_day, 
                                                     group=Group.C)
    page_section_group_d = notebook.get_page_section(distillation_at=selected_day, 
                                                     group=Group.D)

    senteces_a  = None if page_section_group_a is None \
        else page_section_group_a.sentences
    sentences_b = None if page_section_group_b is None \
        else page_section_group_b.sentences
    sentences_c = None if page_section_group_c is None \
        else page_section_group_c.sentences
    sentences_d = None if page_section_group_d is None \
        else page_section_group_d.sentences
    
    columns = [
        "foreign_language",
        "translated_sentence",
        "remembered",
        "mother_tongue"]
    
    dfa = pd.DataFrame(columns=columns) if senteces_a is None \
        else pd.concat([pd.DataFrame(s.data_to_dataframe()) for s in senteces_a])
    dfb = pd.DataFrame(columns=columns) if sentences_b is None \
        else pd.concat([pd.DataFrame(s.data_to_dataframe()) for s in sentences_b])
    dfc = pd.DataFrame(columns=columns) if sentences_c is None \
        else pd.concat([pd.DataFrame(s.data_to_dataframe()) for s in sentences_c])
    dfd = pd.DataFrame(columns=columns) if sentences_d is None \
        else pd.concat([pd.DataFrame(s.data_to_dataframe()) for s in sentences_d])

    dfa['translated_sentence'] = ''
    dfa['remembered'] = False
    
    if not dfb.empty:
        dfb['translated_sentence'] = page_section_group_b.translated_sentences
        dfb['remembered'] = page_section_group_b.memorializeds
    else:
        dfb['translated_sentence'] = ''
        dfb['remembered'] = False
    
    if not dfc.empty:
        dfc['translated_sentence'] = page_section_group_c.translated_sentences
        dfc['remembered'] = page_section_group_c.memorializeds
    else:
        dfc['translated_sentence'] = ''
        dfc['remembered'] = False
    
    if not dfd.empty:
        dfd['translated_sentence'] = page_section_group_d.translated_sentences
        dfd['remembered'] = page_section_group_d.memorializeds
    else:
        dfd['translated_sentence'] = ''
        dfd['remembered'] = False
    

    column_configuration = {
        "foreign_language": st.column_config.TextColumn(
            "Foreign Language", 
            help="Read aloud the sentece or word just once",
            width="medium"
        ),
        "translated_sentence": st.column_config.TextColumn(
            "Translation", 
            help="Write the sentece or word in your mother tongue",
            width="medium"
        ),
        "remembered": st.column_config.CheckboxColumn(
            "You remember?", 
            help="Check the checkbox if you remembered this sentence?",
            width='small'
        ),
    }

    tab1, tab2, tab3, tab4 = st.tabs(['HeadLits/Group A', 'Group B', 'Group C', 'Group D'])

    with tab1:
        col1, col2, col3 = st.columns(3)
        with col1:
            read_aloud_a = st.checkbox('Read aloud', value=True, key='read_aloud_a')
        with col2:
            translate_a = st.checkbox('Translate', key='translate_a')
        with col3:
            distill_a = st.checkbox('Distill', key='distill_a')
        
        placehold_data_edit_headlist = st.empty()

        if read_aloud_a and not translate_a and not distill_a:
            dfa_destilled = placehold_data_edit_headlist.data_editor(
                dfa[['foreign_language']],
                column_config=column_configuration,
                use_container_width=True,
                hide_index=True,
                num_rows="fixed",
                disabled=['foreign_language', 'mother_tongue'],
                key='dt_edit_group_a'
            )
        elif translate_a and not distill_a:
            dfa_destilled = placehold_data_edit_headlist.data_editor(
                dfa[['foreign_language', 'translated_sentence']],
                column_config=column_configuration,
                use_container_width=True,
                hide_index=True,
                num_rows="fixed",
                disabled=['foreign_language', 'mother_tongue'],
                key='dt_edit_group_a'
            )
        elif distill_a:
            dfa_destilled = placehold_data_edit_headlist.data_editor(
                dfa[['remembered', 'foreign_language', 'translated_sentence', 'mother_tongue',]],
                column_config=column_configuration,
                use_container_width=True,
                hide_index=True,
                num_rows="fixed",
                disabled=['foreign_language', 'mother_tongue'],
                key='dt_edit_group_a'
            )
        
        if distill_a and not dfa.empty:
            if st.button('DISTILLATION FINISH HEADLIST', use_container_width=True, type='primary', key='btn_group_a'):
                try:
                    dfa_destilled = dfa_destilled[dfa_destilled['remembered'] == False]
                    print(len(dfa_destilled))
                    build_page_section_with_sentence_list(dataframe=dfa_destilled,
                                                          selected_day=selected_day, 
                                                          notebook=notebook, 
                                                          group=Group.B)                                        
                except Exception as error:
                    placehold_container_msg.error(str(error), icon="🚨")
                    if 'There is already a page'.upper() in str(error).upper():
                        st.error(str(error), icon="🚨")

        if dfa.empty:
            placehold_data_edit_headlist.warning('⚠️There is no a list of expressions to distill on the selected day!')
    
  
    with tab2:
        col1, col2, col3 = st.columns(3)
        with col1:
            read_aloud_b = st.checkbox('Read aloud', value=True, key='read_aloud_b')
        with col2:
            translate_b = st.checkbox('Translate', key='translate_b')
        with col3:
            distill_b = st.checkbox('Distill', key='distill_b')
        
        placehold_data_edit_group_b = st.empty()

        if read_aloud_b and not translate_b and not distill_b:
            dfb_destilled = placehold_data_edit_group_b.data_editor(
                dfa[['foreign_language']],
                column_config=column_configuration,
                use_container_width=True,
                hide_index=True,
                num_rows="fixed",
                disabled=['foreign_language', 'mother_tongue'],
                key='dt_edit_group_b'
            )
        elif translate_b and not distill_b:
            dfb_destilled = placehold_data_edit_group_b.data_editor(
                dfa[['foreign_language', 'translated_sentence']],
                column_config=column_configuration,
                use_container_width=True,
                hide_index=True,
                num_rows="fixed",
                disabled=['foreign_language', 'mother_tongue'],
                key='dt_edit_group_b'
            )
        elif distill_b:
            dfb_destilled = placehold_data_edit_group_b.data_editor(
                dfa[['remembered', 'foreign_language', 'translated_sentence', 'mother_tongue',]],
                column_config=column_configuration,
                use_container_width=True,
                hide_index=True,
                num_rows="fixed",
                disabled=['foreign_language', 'mother_tongue'],
                key='dt_edit_group_b'
            )
        
        if distill_b and not dfb.empty:
            if st.button('DISTILLATION FINISH HEADLIST', use_container_width=True, type='primary', key='btn_group_a'):
                try:
                    dfb_destilled = dfb_destilled[dfb_destilled['remembered'] == False]
                    print(len(dfb_destilled))
                    build_page_section_with_sentence_list(dataframe=dfb_destilled,
                                                          selected_day=selected_day, 
                                                          notebook=notebook, 
                                                          group=Group.C)                                        
                except Exception as error:
                    placehold_container_msg.error(str(error), icon="🚨")
                    if 'There is already a page'.upper() in str(error).upper():
                        st.error(str(error), icon="🚨")

        if dfb.empty:
            placehold_data_edit_headlist.warning('⚠️There is no a list of expressions to distill on the selected day!')
    

    with tab3:
        col1, col2, col3 = st.columns(3)
        with col1:
            read_aloud_c = st.checkbox('Read aloud', value=True, key='read_aloud_c')
        with col2:
            translate_c = st.checkbox('Translate', key='translate_c')
        with col3:
            distill_c = st.checkbox('Distill', key='distill_c')
        
        placehold_data_edit_group_c = st.empty()

        if read_aloud_c and not translate_c and not distill_c:
            dfc_destilled = placehold_data_edit_group_c.data_editor(
                dfa[['foreign_language']],
                column_config=column_configuration,
                use_container_width=True,
                hide_index=True,
                num_rows="fixed",
                disabled=['foreign_language', 'mother_tongue'],
                key='dt_edit_group_c'
            )
        elif translate_c and not distill_c:
            dfc_destilled = placehold_data_edit_group_c.data_editor(
                dfa[['foreign_language', 'translated_sentence']],
                column_config=column_configuration,
                use_container_width=True,
                hide_index=True,
                num_rows="fixed",
                disabled=['foreign_language', 'mother_tongue'],
                key='dt_edit_group_c'
            )
        elif distill_c:
            dfc_destilled = placehold_data_edit_group_c.data_editor(
                dfa[['remembered', 'foreign_language', 'translated_sentence', 'mother_tongue',]],
                column_config=column_configuration,
                use_container_width=True,
                hide_index=True,
                num_rows="fixed",
                disabled=['foreign_language', 'mother_tongue'],
                key='dt_edit_group_c'
            )
        
        if distill_c and not dfc.empty:
            if st.button('DISTILLATION FINISH HEADLIST', use_container_width=True, type='primary', key='btn_group_a'):
                try:
                    dfc_destilled = dfc_destilled[dfc_destilled['remembered'] == False]
                    print(len(dfc_destilled))
                    build_page_section_with_sentence_list(dataframe=dfc_destilled,
                                                          selected_day=selected_day, 
                                                          notebook=notebook, 
                                                          group=Group.D)                                        
                except Exception as error:
                    placehold_container_msg.error(str(error), icon="🚨")
                    if 'There is already a page'.upper() in str(error).upper():
                        st.error(str(error), icon="🚨")

        if dfc.empty:
            placehold_data_edit_headlist.warning('⚠️There is no a list of expressions to distill on the selected day!')
    

    with tab4:
        col1, col2, col3 = st.columns(3)
        with col1:
            read_aloud_d = st.checkbox('Read aloud', value=True, key='read_aloud_d')
        with col2:
            translate_d = st.checkbox('Translate', key='translate_d')
        with col3:
            distill_d = st.checkbox('Distill', key='distill_d')
        
        placehold_data_edit_group_d = st.empty()

        if read_aloud_d and not translate_d and not distill_d:
            dfd_destilled = placehold_data_edit_group_d.data_editor(
                dfa[['foreign_language']],
                column_config=column_configuration,
                use_container_width=True,
                hide_index=True,
                num_rows="fixed",
                disabled=['foreign_language', 'mother_tongue'],
                key='dt_edit_group_d'
            )
        elif translate_d and not distill_d:
            dfd_destilled = placehold_data_edit_group_d.data_editor(
                dfa[['foreign_language', 'translated_sentence']],
                column_config=column_configuration,
                use_container_width=True,
                hide_index=True,
                num_rows="fixed",
                disabled=['foreign_language', 'mother_tongue'],
                key='dt_edit_group_d'
            )
        elif distill_d:
            dfd_destilled = placehold_data_edit_group_d.data_editor(
                dfa[['remembered', 'foreign_language', 'translated_sentence', 'mother_tongue',]],
                column_config=column_configuration,
                use_container_width=True,
                hide_index=True,
                num_rows="fixed",
                disabled=['foreign_language', 'mother_tongue'],
                key='dt_edit_group_d'
            )
        
        if distill_d and not dfd.empty:
            if st.button('DISTILLATION FINISH HEADLIST', use_container_width=True, type='primary', key='btn_group_a'):
                try:
                    dfd_destilled = dfd_destilled[dfd_destilled['remembered'] == False]
                    print(len(dfd_destilled))
                    build_page_section_with_sentence_list(dataframe=dfd_destilled,
                                                          selected_day=selected_day, 
                                                          notebook=notebook, 
                                                          group=Group.NEW_PAGE)                                        
                except Exception as error:
                    placehold_container_msg.error(str(error), icon="🚨")
                    if 'There is already a page'.upper() in str(error).upper():
                        st.error(str(error), icon="🚨")

        if dfd.empty:
            placehold_data_edit_headlist.warning('⚠️There is no a list of expressions to distill on the selected day!')
    
else:
    st.warning('⚠️Attention! There are no notebooks registred!')
    st.markdown('[Create a Notebook](Add%20New%20Notebook)')
