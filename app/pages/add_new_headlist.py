import datetime

import pandas as pd
import streamlit as st
from st_pages import add_page_title

from app.core.dao_parquet import NotebookDAO, PageSectionDAO, SentenceDAO
from app.core.service import build_page_section_with_sentence_list
from app.model import Group, Notebook

st.set_page_config(layout='wide')

placehold_container_msg = st.container()
placehold_container_msg.empty()

# Either this or add_indentation() MUST be called on each page in your
# app to add indendation in the sidebar
add_page_title()  # Optional method to add title and icon to current page

sentences_dao = SentenceDAO()
page_section_dao = PageSectionDAO()
notebook_dao = NotebookDAO()

if 'notebook_list' not in st.session_state:
    st.session_state.notebook_list = notebook_dao.get_all(Notebook())
    

def on_change_session_state_notebook_list(on_change=None, *args, **kwargs):
    del st.session_state['notebook_list']
    if on_change is None:
        st.experimental_rerun()


notebooks_list = st.session_state.notebook_list

notebook_dict = {n.name: n for n in notebooks_list}

if len(notebooks_list) > 0:
    selected_notebook = st.sidebar.selectbox('**NOTEBOOK:**', 
                                             notebook_dict.keys(),
                                             on_change=on_change_session_state_notebook_list,
                                             args=('onchange',))
    
    notebook: Notebook = notebook_dict.get(selected_notebook)


    if notebook.count_page_section_by_group(group=Group.A) == 0 \
            and len(notebook.page_section_list) > 0:
        on_change_session_state_notebook_list()
    
    st.title(f'NOTEBOOK - {notebook.name.upper()}')
    col_group_1, col_group_2, col_group_3, col_group_4 = st.sidebar.columns(4)

    st.sidebar.divider()

    selected_day = st.sidebar.date_input('**LIST OF THE DAY:**', datetime.datetime.now().date(), format='DD/MM/YYYY')
    
    page_section_dict = {p.created_at: p for p in notebook.page_section_list}
    selected_page_section_day = page_section_dict.get(selected_day)

    sentences_txt = [("I love learning new languages.", "Eu adoro aprender novos idiomas."), ("She enjoys reading books in her free time.", "Ela gosta de ler livros nas horas vagas."), ("They went to the beach last weekend.", "Eles foram à praia no fim de semana passado."), ("I'm going to the grocery store to buy some groceries.", "Vou à mercearia comprar mantimentos."), ("He is a talented musician who plays the guitar beautifully.", "Ele é um músico talentoso que toca violão lindamente."), ("She usually takes a walk in the park after dinner.", "Normalmente, ela dá uma caminhada no parque depois do jantar."), ("I can't wait to see you again.", "Mal posso esperar para te ver de novo."), ("My favorite movie is a classic from the 80s.", "Meu filme favorito é um clássico dos anos 80."), ("They are planning a family vacation to Europe next summer.", "Eles estão planejando uma viagem em família para a Europa no próximo verão."), ("The weather is very hot today.", "O clima está muito quente hoje."), ("I need to study for my exams this weekend.", "Preciso estudar para as provas neste fim de semana."), ("She's a great cook and makes delicious meals.", "Ela é uma ótima cozinheira e faz refeições deliciosas."), ("He's always telling funny jokes that make everyone laugh.", "Ele está sempre contando piadas engraçadas que fazem todos rirem."), ("I enjoy going for a run in the morning.", "Gosto de sair para correr de manhã."), ("They are planning a surprise party for her birthday.", "Eles estão planejando uma festa surpresa para o aniversário dela."), ("She wants to travel the world and explore different cultures.", "Ela quer viajar pelo mundo e explorar diferentes culturas."), ("I have a lot of work to do this week.", "Tenho muito trabalho para fazer esta semana."), ("We had a great time at the concert last night.", "Nos divertimos muito no show de ontem à noite."), ("He's an excellent student and always gets good grades.", "Ele é um ótimo aluno e sempre tira boas notas."), ("They are going to visit their grandparents during the holidays.", "Eles vão visitar os avós durante as férias.")]
    new_data_add = []
    for i in range(1, notebook.list_size + 1 ):
        new_data_add.append(
            {
                "foreign_language": sentences_txt[i-1][0],
                "mother_tongue": sentences_txt[i-1][1],
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

    st.markdown('**Add new HeadList**')

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

    if selected_page_section_day is not None:
        placehold_sentences_sheet.warning(f'⚠️There is already a page for the group {selected_page_section_day.group.value} and selected day {selected_page_section_day.created_at}!')
        
    if placehold_btn_insert.button('INSERT NEW LIST', 
                                   type='primary', 
                                   disabled=False if selected_page_section_day is None else True, 
                                   use_container_width=True):
        try:
            page_section = build_page_section_with_sentence_list(dataframe=df_result,
                                                                selected_day=selected_day,
                                                                notebook=notebook,
                                                                group=Group.HEADLIST,
                                                                persit=False)            
            page_section = page_section_dao.insert(page_section)
            placehold_sentences_sheet.success(f'{page_section} was inserted successfully!')
            
            notebook.page_section_list.append(page_section)

            page_section_clone = page_section.clone()
            page_section_clone.distillation_at = datetime.datetime.strptime(str(selected_day), '%Y-%m-%d').date()


            page_section_dao.insert(page_section_clone)
        
            st.toast('Page section was inserted successfully.')
            placehold_btn_insert.empty()

            
        except Exception as error:
            st.toast('Something went wrong!')
            placehold_container_msg.error(str(error), icon="🚨")
            if 'There is already a page'.upper() in str(error).upper():
                placehold_page_exists.error(str(error), icon="🚨")


    qty_group_a = notebook.count_page_section_by_group(group=Group.A)
    qty_group_b = notebook.count_page_section_by_group(group=Group.B)
    qty_group_c = notebook.count_page_section_by_group(group=Group.C)
    qty_group_d = notebook.count_page_section_by_group(group=Group.D)
    
    col_group_1.markdown(f'**GroupA:** {qty_group_a:0>7}')
    col_group_2.markdown(f'**GroupB:** {qty_group_b:0>7}')
    col_group_3.markdown(f'**GroupC:** {qty_group_c:0>7}')
    col_group_4.markdown(f'**GroupD:** {qty_group_d:0>7}')

else:
    st.warning('⚠️Attention! There are no notebooks registred!')
    st.markdown('[Create a Notebook](Add%20Notebook)')



# st.divider()
# # The directory containing this file
# import os.path
# from pathlib import Path
# HERE = os.path.abspath(os.path.dirname(__file__))
# sentence_file = Path(HERE).parent.parent / 'data_base' / 'sentence.parquet'
# page_section_file = Path(HERE).parent.parent / 'data_base' / 'page_section.parquet'
# df_page = pd.read_parquet(page_section_file)
# df_sentence = pd.read_parquet(sentence_file)
# st.markdown('PAGE SECTIONS')
# st.dataframe(df_page, hide_index=True, use_container_width=True)
# st.divider()
# st.markdown('SENTENCES')
# st.dataframe(df_sentence, hide_index=True, use_container_width=True)