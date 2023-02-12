# %%
from rdflib import Literal
import vimrdf

vimrdf = vimrdf.VIMRDF()
g = vimrdf.get_graph()
vimrdf.load_entries_from_JSON()
#vimrdf.to_file(format='turtle', destination='./quicktest.ttl')

# vimrdf.list_subjects()
#vimrdf.list_terms(lang='it')
# vimrdf.get_subject_by_term('measurement unit')
#vimrdf.get_term_by_subject(vimrdf.list_subjects()[7], lang='it')




# %%
