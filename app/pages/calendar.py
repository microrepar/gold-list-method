import datetime

import streamlit as st
from st_pages import add_page_title
from streamlit_calendar import calendar

from app.core.dao_parquet import NotebookDAO, PageSectionDAO
from app.model import Notebook

st.set_page_config(layout='wide')

placehold_container_msg = st.container()
placehold_container_msg.empty()

add_page_title()  # Optional method to add title and icon to current page


def on_change_notebook():
    st.session_state.flag_alter_calendar = not st.session_state.flag_alter_calendar


if 'flag_alter_calendar' not in st.session_state:
    st.session_state.flag_alter_calendar = True

page_section_dao = PageSectionDAO()
notebook_dao = NotebookDAO()
notebooks_list = notebook_dao.get_all()
notebook_dict = {n.name: n for n in notebooks_list}

if len(notebooks_list) > 0:
    selected_notebook = st.sidebar.selectbox('**NOTEBOOK:**', 
                                             [n.name for n in notebooks_list], 
                                             on_change=on_change_notebook,                                             
                                             key='select_notebook')

    notebook: Notebook = notebook_dict.get(selected_notebook)

    st.title(f'NOTEBOOK - {notebook.name.upper()}')

    col_group_1, col_group_2, col_group_3, col_group_4 = st.sidebar.columns(4
                                                                            )
    st.sidebar.markdown("[Add New Headlist](Add%20New%20HeadList)")
    st.sidebar.markdown("[Distillation](Distillation)")

    st.sidebar.divider()

    mode = 'daygrid'

    events = [ps.get_distillation_event() for ps in notebook.page_section_list]
    calendar_resources = [
        {"id": "a", "building": "Building A", "title": "Group A"},
        {"id": "b", "building": "Building A", "title": "Group B"},
        {"id": "c", "building": "Building B", "title": "Group C"},
        {"id": "d", "building": "Building B", "title": "Group D"},
    ]

    calendar_options = {
        "editable": "true",
        "navLinks": "true",
        "resources": calendar_resources,
    }

    calendar_options = {
        **calendar_options,
        "headerToolbar": {
            "left": "today prev,next",
            "center": "title",
            "right": "dayGridDay,dayGridWeek,dayGridMonth",
        },
        "initialDate": f"{datetime.datetime.now().date()}",
        "initialView": "dayGridMonth",
    }

    

    if st.session_state.flag_alter_calendar:
        state = calendar(
            events=events,
            options=calendar_options,
            key=mode+'1',
        )
    else:     
        state = calendar(
            events=events,
            options=calendar_options,
            key=mode+'2',
        )

    # state = calendar(
    #     events=st.session_state.get("events", events),
    #     options=calendar_options,
    #     key=mode,
    # )

    # if state.get("eventsSet") is not None:
    #     st.session_state["events"] = state["eventsSet"]
    
    # st.write(state)

    # st.markdown("## API reference")
    
    # st.help(calendar) 
else:
    st.warning('⚠️Attention! There are no notebooks registred!')
    st.markdown('[Create a Notebook](Add%20New%20Notebook)')