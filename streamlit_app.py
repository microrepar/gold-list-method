import datetime

import pandas as pd
import streamlit as st
from st_pages import Page, Section, add_page_title, show_pages

from app.core.dao_parquet import NotebookDAO, PageSectionDAO
from app.model import Group, Notebook, PageSection
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

page_section_dao = PageSectionDAO()
notebook_dao = NotebookDAO()
notebooks_list = notebook_dao.get_all()
notebook_dict = {n.name: n for n in notebooks_list}

if len(notebooks_list) > 0:
    selected_notebook = st.sidebar.selectbox('**NOTEBOOK:**', [n.name for n in notebooks_list])

    notebook: Notebook = notebook_dict.get(selected_notebook)

    st.title(f'NOTEBOOK - {notebook.name.upper()}')
    col_group_1, col_group_2, col_group_3, col_group_4 = st.sidebar.columns(4)
    
    st.sidebar.divider()

    selected_day = st.sidebar.date_input('**LIST OF THE DAY:**', datetime.datetime.now().date(), format='DD/MM/YYYY')

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


    if page_section_group_a:
        dfa['translated_sentence'] = page_section_group_a.translated_sentences
        dfa['remembered'] = page_section_group_a.memorializeds
    else:
        dfa['translated_sentence'] = ''
        dfa['remembered'] = False        
    
    if page_section_group_b:
        dfb['translated_sentence'] = page_section_group_b.translated_sentences
        dfb['remembered'] = page_section_group_b.memorializeds
    else:
        dfb['translated_sentence'] = ''
        dfb['remembered'] = False
    
    if page_section_group_c:
        dfc['translated_sentence'] = page_section_group_c.translated_sentences
        dfc['remembered'] = page_section_group_c.memorializeds
    else:
        dfc['translated_sentence'] = ''
        dfc['remembered'] = False
    
    if page_section_group_d:
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

    btn_update_a = False
    btn_record_b = False
    btn_record_c = False
    btn_record_d = False

    tab1, tab2, tab3, tab4 = st.tabs(['HeadLits/Group A', 'Group B', 'Group C', 'Group D'])


    with tab1:
        col1, col2, col3 = st.columns(3)
        with col1:
            read_aloud_a = st.checkbox('Read aloud', value=True, key='read_aloud_a', disabled=True)
        with col2:
            translate_a = st.checkbox('Translate', value=True, key='translate_a', disabled=True)
        with col3:
            distill_a = st.checkbox('Distill', key='distill_a',
                                    value=True if page_section_group_a and page_section_group_a.distillated else False,
                                    disabled=True if page_section_group_a and page_section_group_a.distillated else False)
        
        placehold_data_edit_headlist = st.empty()
        with placehold_data_edit_headlist:
            placehold_container_dt_edit_headlist = st.container()

        
        if read_aloud_a and not translate_a and not distill_a:
            dfa_destilled = placehold_container_dt_edit_headlist.data_editor(
                dfa[['foreign_language']],
                column_config=column_configuration,
                use_container_width=True,
                hide_index=True,
                num_rows="fixed",
                disabled=['foreign_language', 'mother_tongue'],
                key='dt_edit_group_a'
            )
        elif translate_a and not distill_a:
            dfa_destilled = placehold_container_dt_edit_headlist.data_editor(
                dfa[['foreign_language', 'translated_sentence']],
                column_config=column_configuration,
                use_container_width=True,
                hide_index=True,
                num_rows="fixed",
                disabled=['foreign_language'] if page_section_group_a and not page_section_group_a.distillated \
                    else ['translated_sentence', 'foreign_language'],
                key='dt_edit_group_a'
            )
            btn_update_a = placehold_container_dt_edit_headlist.button('RECORD TRANSLATION', use_container_width=True, type='primary', key='btn_record_group_a')
        elif distill_a:
            dfa_destilled = placehold_container_dt_edit_headlist.data_editor(
                dfa[['remembered', 'foreign_language', 'translated_sentence', 'mother_tongue',]],
                column_config=column_configuration,
                use_container_width=True,
                hide_index=True,
                num_rows="fixed",
                disabled=['foreign_language', 'mother_tongue', 'translated_sentence'] \
                                if not page_section_group_a.distillated \
                                else ['foreign_language', 'mother_tongue', 'translated_sentence', 'remembered'],
                key='dt_edit_group_a'
            )
        
        if btn_update_a:
            dfa_destilled['remembered'] = False
            page_section_update_a: PageSection = build_page_section_with_sentence_list(dataframe=dfa_destilled,
                                                        selected_day=page_section_group_a.created_at.date(), 
                                                        notebook=notebook, 
                                                        group=page_section_group_a.group,
                                                        persit=False)
            page_section_update_a.page_number = page_section_group_a.page_number
            try:
                page_section_dao.update(page_section_update_a)
            except Exception as error:
                    placehold_container_msg.error(str(error), icon="🚨")
                    if 'There is already a page'.upper() in str(error).upper():
                        st.error(str(error), icon="🚨")

        if distill_a and not dfa.empty:
            if placehold_container_dt_edit_headlist.button('DISTILLATION FINISH HEADLIST', 
                                                           use_container_width=True, 
                                                           type='primary', 
                                                           key='btn_group_a',
                                                           disabled=True if page_section_group_a.distillated else False):
                try:
                    page_section_update_a: PageSection = build_page_section_with_sentence_list(dataframe=dfa_destilled,
                                                          selected_day=page_section_group_a.created_at.date(), 
                                                          notebook=notebook, 
                                                          group=page_section_group_a.group,
                                                          persit=False)
                    page_section_update_a.page_number = page_section_group_a.page_number
                    page_section_update_a.distillated = True
                    page_section_dao.update(page_section_update_a)
                    
                    dfa_base = dfa_destilled[dfa_destilled['remembered'] == False].copy()
                    dfa_base['translated_sentence'] = ''
                    page_section_after_a = build_page_section_with_sentence_list(dataframe=dfa_base,
                                                          selected_day=selected_day, 
                                                          notebook=notebook, 
                                                          group=Group.B)
                    
                    placehold_data_edit_headlist.success(f'{page_section_after_a} was inserted success!')
                except Exception as error:
                    placehold_container_msg.error(str(error), icon="🚨")
                    if 'There is already a page'.upper() in str(error).upper():
                        st.error(str(error), icon="🚨")

        if dfa.empty:
            placehold_data_edit_headlist.warning('⚠️There is no a list of expressions in "Group A" to distill on the selected day!')
    
  

    with tab2:
        col1, col2, col3 = st.columns(3)
        with col1:
            read_aloud_b = st.checkbox('Read aloud', value=True, key='read_aloud_b', disabled=True)
        with col2:
            translate_b = st.checkbox('Translate', value=True, key='translate_b', disabled=True)
        with col3:
            distill_b = st.checkbox('Distill', key='distill_b')
        
        placehold_data_edit_group_b = st.empty()
        with placehold_data_edit_group_b:
            placehold_container_dt_edit_group_b = st.container()


        if read_aloud_b and not translate_b and not distill_b:
            dfb_destilled = placehold_container_dt_edit_group_b.data_editor(
                dfb[['foreign_language']],
                column_config=column_configuration,
                use_container_width=True,
                hide_index=True,
                num_rows="fixed",
                disabled=['foreign_language', 'mother_tongue'],
                key='dt_edit_group_b'
            )
        elif translate_b and not distill_b:
            dfb_destilled = placehold_container_dt_edit_group_b.data_editor(
                dfb[['foreign_language', 'translated_sentence']],
                column_config=column_configuration,
                use_container_width=True,
                hide_index=True,
                num_rows="fixed",
                disabled=['foreign_language', 'mother_tongue'],
                key='dt_edit_group_b'
            )
        elif distill_b:
            dfb_destilled = placehold_container_dt_edit_group_b.data_editor(
                dfb[['remembered', 'foreign_language', 'translated_sentence', 'mother_tongue',]],
                column_config=column_configuration,
                use_container_width=True,
                hide_index=True,
                num_rows="fixed",
                disabled=['foreign_language', 'mother_tongue'],
                key='dt_edit_group_b'
            )
        
        if distill_b and not dfb.empty:
            if placehold_container_dt_edit_group_b.button('DISTILLATION FINISH HEADLIST', use_container_width=True, type='primary', key='btn_group_a'):
                try:
                    dfb_destilled = dfb_destilled[dfb_destilled['remembered'] == False]
                    page_section_after_b = build_page_section_with_sentence_list(dataframe=dfb_destilled,
                                                          selected_day=selected_day, 
                                                          notebook=notebook, 
                                                          group=Group.C)
                    placehold_data_edit_group_b.success(f'{page_section_after_b} was inserted success!')
                except Exception as error:
                    placehold_container_msg.error(str(error), icon="🚨")
                    if 'There is already a page'.upper() in str(error).upper():
                        st.error(str(error), icon="🚨")

        if dfb.empty:
            placehold_data_edit_group_b.warning('⚠️There is no a list of expressions in "Group B" to distill on the selected day!')
    



    with tab3:
        col1, col2, col3 = st.columns(3)
        with col1:
            read_aloud_c = st.checkbox('Read aloud', value=True, key='read_aloud_c', disabled=True)
        with col2:
            translate_c = st.checkbox('Translate', value=True, key='translate_c', disabled=True)
        with col3:
            distill_c = st.checkbox('Distill', key='distill_c')
        
        placehold_data_edit_group_c = st.empty()
        with placehold_data_edit_group_c:
            placehold_container_dt_edit_group_c = st.container()

        if read_aloud_c and not translate_c and not distill_c:
            dfc_destilled = placehold_container_dt_edit_group_c.data_editor(
                dfc[['foreign_language']],
                column_config=column_configuration,
                use_container_width=True,
                hide_index=True,
                num_rows="fixed",
                disabled=['foreign_language', 'mother_tongue'],
                key='dt_edit_group_c'
            )
        elif translate_c and not distill_c:
            dfc_destilled = placehold_container_dt_edit_group_c.data_editor(
                dfc[['foreign_language', 'translated_sentence']],
                column_config=column_configuration,
                use_container_width=True,
                hide_index=True,
                num_rows="fixed",
                disabled=['foreign_language', 'mother_tongue'],
                key='dt_edit_group_c'
            )
        elif distill_c:
            dfc_destilled = placehold_container_dt_edit_group_c.data_editor(
                dfc[['remembered', 'foreign_language', 'translated_sentence', 'mother_tongue',]],
                column_config=column_configuration,
                use_container_width=True,
                hide_index=True,
                num_rows="fixed",
                disabled=['foreign_language', 'mother_tongue'],
                key='dt_edit_group_c'
            )
        
        if distill_c and not dfc.empty:
            if placehold_container_dt_edit_group_c.button('DISTILLATION FINISH HEADLIST', use_container_width=True, type='primary', key='btn_group_a'):
                try:
                    dfc_destilled = dfc_destilled[dfc_destilled['remembered'] == False]
                    print(len(dfc_destilled))
                    page_section_after_c = build_page_section_with_sentence_list(dataframe=dfc_destilled,
                                                          selected_day=selected_day, 
                                                          notebook=notebook, 
                                                          group=Group.D)
                    placehold_data_edit_group_c.success(f'{page_section_after_c} was inserted success!')
                except Exception as error:
                    placehold_container_msg.error(str(error), icon="🚨")
                    if 'There is already a page'.upper() in str(error).upper():
                        st.error(str(error), icon="🚨")

        if dfc.empty:
            placehold_data_edit_group_c.warning('⚠️There is no a list of expressions in "Group C" to distill on the selected day!')
    

    

    with tab4:
        col1, col2, col3 = st.columns(3)
        with col1:
            read_aloud_d = st.checkbox('Read aloud', value=True, key='read_aloud_d', disabled=True)
        with col2:
            translate_d = st.checkbox('Translate', value=True, key='translate_d', disabled=True)
        with col3:
            distill_d = st.checkbox('Distill', key='distill_d')
        
        placehold_data_edit_group_d = st.empty()
        with placehold_data_edit_group_d:
            placehold_container_dt_edit_group_d = st.container()

        if read_aloud_d and not translate_d and not distill_d:
            dfd_destilled = placehold_container_dt_edit_group_d.data_editor(
                dfd[['foreign_language']],
                column_config=column_configuration,
                use_container_width=True,
                hide_index=True,
                num_rows="fixed",
                disabled=['foreign_language', 'mother_tongue'],
                key='dt_edit_group_d'
            )
        elif translate_d and not distill_d:
            dfd_destilled = placehold_container_dt_edit_group_d.data_editor(
                dfd[['foreign_language', 'translated_sentence']],
                column_config=column_configuration,
                use_container_width=True,
                hide_index=True,
                num_rows="fixed",
                disabled=['foreign_language', 'mother_tongue'],
                key='dt_edit_group_d'
            )
        elif distill_d:
            dfd_destilled = placehold_container_dt_edit_group_d.data_editor(
                dfd[['remembered', 'foreign_language', 'translated_sentence', 'mother_tongue',]],
                column_config=column_configuration,
                use_container_width=True,
                hide_index=True,
                num_rows="fixed",
                disabled=['foreign_language', 'mother_tongue'],
                key='dt_edit_group_d'
            )
        
        if distill_d and not dfd.empty:
            if placehold_container_dt_edit_group_d.button('DISTILLATION FINISH HEADLIST', use_container_width=True, type='primary', key='btn_group_a'):
                try:
                    dfd_destilled = dfd_destilled[dfd_destilled['remembered'] == False]
                    print(len(dfd_destilled))
                    page_section_after_d = build_page_section_with_sentence_list(dataframe=dfd_destilled,
                                                          selected_day=selected_day, 
                                                          notebook=notebook, 
                                                          group=Group.NEW_PAGE)
                    placehold_data_edit_group_d.success(f'{page_section_after_d} was inserted success!')
                except Exception as error:
                    placehold_container_msg.error(str(error), icon="🚨")
                    if 'There is already a page'.upper() in str(error).upper():
                        st.error(str(error), icon="🚨")

        if dfd.empty:
            placehold_data_edit_group_d.warning('⚠️There is no a list of expressions in "Group D" to distill on the selected day!')
    
    notebooks_list = notebook_dao.get_all()
    notebook_dict = {n.name: n for n in notebooks_list}

    notebook = notebook_dict.get(selected_notebook)

    col_group_1.markdown(f'Group A: {notebook.count_page_section_by_group(group=Group.A):0>6}')
    col_group_2.markdown(f'Group B: {notebook.count_page_section_by_group(group=Group.B):0>6}')
    col_group_3.markdown(f'Group C: {notebook.count_page_section_by_group(group=Group.C):0>6}')
    col_group_4.markdown(f'Group D: {notebook.count_page_section_by_group(group=Group.D):0>6}')

else:
    st.warning('⚠️Attention! There are no notebooks registred!')
    st.markdown('[Create a Notebook](Add%20New%20Notebook)')
