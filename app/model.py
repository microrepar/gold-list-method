import datetime
from enum import Enum
from typing import List



class Notebook:
    def __init__(self, 
                 name              : str=None, *,
                 id_               : int=None,
                 created_at        : 'Date'=None,
                 updated_at        : 'Date'=None,
                 list_size         : int=None,
                 day_range         : int=None,
                 page_section_list : List['PageSection']=[],
                 foreign_idiom     : str=None,
                 mother_idiom      : str=None):
        self.name              = name
        self.id                = id_
        self.created_at        = created_at
        self.updated_at        = updated_at
        self.list_size         = list_size
        self.day_range         = day_range
        self.page_section_list = page_section_list
        self.foreign_idiom     = foreign_idiom
        self.mother_idiom      = mother_idiom

    def data_to_dataframe(self):
        return [
            {
                'id'            : self.id,
                'name'          : self.name,
                'created_at'    : self.created_at,
                'updated_at'    : self.updated_at,
                'list_size'     : self.list_size,
                'day_range'     : self.day_range,
                'foreign_idiom' : self.foreign_idiom,
                'mother_idiom'  : self.mother_idiom,
            }
        ]
    
    def __str__(self) -> str:
        return (f'{self.__class__.__name__}'
                f'('
                    f'id={self.id}, '
                    f'name="{self.name}", '
                    f'list_size={self.list_size}, '
                    f'day_range={self.day_range}, '
                    f'foreign_idiom={self.foreign_idiom}, '
                    f'mother_idiom={self.mother_idiom}'
                ')'
        )
    
    def get_page_section(self, *, distillation_at, group) -> 'PageSection':
        for page_section in self.page_section_list:
            if distillation_at == page_section.distillation_at \
                    and group == page_section.group \
                        and page_section.created_at:
                return page_section
    
    def count_page_section_by_group(self, *, group):
        page_list = list()
        for page_section in self.page_section_list:
            if page_section.group == group and  page_section.created_at:
                page_list.append(page_section)
        return len(page_list)
    

class Sentence:
    def __init__(self,
                 id_              : int=None,
                 created_at       : 'Date'=None,
                 foreign_language : str=None,
                 mother_tongue    : str=None,
                 foreign_idiom    : str=None,
                 mother_idiom     : str=None
                 ):
        self.id               = id_
        self.created_at       = created_at
        self.foreign_language = foreign_language
        self.mother_tongue    = mother_tongue
        self.foreign_idiom    = foreign_idiom
        self.mother_idiom     = mother_idiom
    
    def data_to_dataframe(self):
        return [
            {
                'id'               : self.id,
                'created_at'       : self.created_at,
                'foreign_language' : self.foreign_language,
                'mother_tongue'    : self.mother_tongue,
                'foreign_idiom'    : self.foreign_idiom,
                'mother_idiom'     : self.mother_idiom,
            }
        ]
    
    def __str__(self):
        return (
            f'Sentence('
                f'id_={self.id}, '
                f'created_at={self.created_at}, '
                f'foreign_language={self.foreign_language}, '
                f'mother_tongue={self.mother_tongue} '
            f')'
        )


class Group(Enum):
    HEADLIST = 'A'
    A        = 'A'
    B        = 'B'
    C        = 'C'
    D        = 'D'
    NEW_PAGE = 'NP'


class PageSection:
    def __init__(self, *,
                 id_                  : int=None,
                 section_number       : int=None,
                 page_number          : int=None,
                 group                : Group=None,
                 created_at           : 'Date'=None,
                 created_by           : int=None,
                 distillation_at      : 'Date'=None,
                 distillation_actual  : 'Date'=None,
                 distillated          : bool=False,
                 sentences            : List[Sentence]=[],
                 translated_sentences : List[str]=[],
                 memorializeds        : List[bool]=[],
                 notebook             : int=None):
        self.id                           = id_
        self.section_number               = section_number
        self.page_number                  = page_number
        self.group:Group                  = group
        self.created_at                   = created_at
        self.distillation_at              = distillation_at
        self._distillated                 = distillated
        self.sentences                    = sentences
        self.translated_sentences         = translated_sentences
        self.memorializeds                = memorializeds
        self.notebook                     = notebook
        self._distillation_actual: 'Date' = distillation_actual
        self.set_created_by(created_by)        # section_number from  PageSection
    
    @property
    def distillated(self):
        return bool(self._distillated)

    @distillated.setter
    def distillated(self, value: bool) :
        self._distillated = bool(value)
        if value:
            self._distillation_actual = datetime.datetime.now().date()

    def set_id(self, id_):
        self.id = id_

    def set_created_by(self, page_section: 'PageSection'=None):
        if isinstance(page_section, PageSection):
            self.created_by = page_section
        else:
            self.created_by = None
        
    def __str__(self):
        group = {
            'A'  : 'HeadList',
            'B'  : 'Group B List',
            'C'  : 'Group C List',
            'D'  : 'Group D List',
            'NP' : 'Group NP List'
        }
        notebook_value = self.notebook.name if isinstance(self.notebook, Notebook) else ''
        return (f'{group.get(self.group.value)} of {self.created_at} with '
                f'distillation date of {self.distillation_at} from the {notebook_value} notebook')
        
    def __repr__(self):
        created_by_id = None
        if self.created_by is not None:
            created_by_id = self.created_by.section_number
        notebook_id = None
        if self.notebook is not None:
            notebook_id = self.notebook.id
        return (f'PageSection('
                    # f'id_                = {self.id}, '
                    f'section_number={self.section_number}, '
                    f'page_number={self.page_number}, '
                    f'created_at={self.created_at}, '
                    f'created_by_id={created_by_id}, '
                    f'notebook_id={notebook_id}, '
                    f'group="{self.group}", '
                    f'translated_sentences={self.translated_sentences}, '
                    f'memorializeds={self.memorializeds}, '
                    f'distillation_at={self.distillation_at}, '
                    f'distillated={self.distillated}'
                ')'
        )
    
    def get_distillation_event(self):
        if self.distillated:
            color = {'A'  : '#9B9B9B',
                     'B'  : '#9B9B9B',
                     'H'  : '#9B9B9B',
                     'C'  : '#9B9B9B',
                     'D'  : '#9B9B9B',
                     'NP' : '#9B9B9B'}
        else:
            color = {'A'  : '#FF0000',
                     'B'  : '#00A81D',
                     'C'  : '#002BFF',
                     'D'  : '#B300B7',
                     'NP' : '#000000'}
        sequence = {'A'  : '1st',
                    'B'  : '2nd',
                    'C'  : '3rd',
                    'D'  : '4th',
                    'NP' : '🔁'}
        
        return {
            "title"      : f"{sequence.get(self.group.value, 'Indef')} Distill {self.group.value}" if self.created_at \
                            else f" Add HeadList",
            "color"      : color.get(self.group.value, color['NP']) if self.created_at \
                            else '#DCDCDC',
            "start"      : f"{self.distillation_at}",
            "end"        : f"{self.distillation_at}",
            "resourceId" : f"{self.group.value.lower()}",
        }

    def data_to_dataframe(self):
        created_by = None
        if self.created_by is not None:
            created_by = self.created_by.section_number
        return {    
            'id'                  : [i for i in range(self.id, self.id + len(self.sentences))],
            'section_number'      : [self.section_number for _ in range(len(self.sentences))],
            'page_number'         : [self.page_number for _ in range(len(self.sentences))],
            'group'               : [self.group.value for _ in range(len(self.sentences))],
            'created_at'          : [self.created_at for _ in range(len(self.sentences))],
            'created_by_id'       : [created_by for _ in range(len(self.sentences))],
            'distillation_at'     : [self.distillation_at for _ in range(len(self.sentences))],
            'distillation_actual' : [self._distillation_actual for _ in range(len(self.sentences))],
            'distillated'         : [self._distillated for _ in range(len(self.sentences))],
            'notebook_id'         : [self.notebook.id for _ in range(len(self.sentences))],
            'sentence_id'         : [v.id for v in self.sentences],
            'translated_sentence' : [v for v in self.translated_sentences],
            'memorized'           : [v for v in self.memorializeds],
        }
