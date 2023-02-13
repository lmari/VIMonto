# %%
from rdflib import Graph, Literal
import vimrdf

vimrdf = vimrdf.VIMRDF()
g = vimrdf.get_graph()
vimrdf.load_entries_from_JSON()
#vimrdf.to_file(format='turtle', destination='./quicktest.ttl')

# vimrdf.list_subjects()
# vimrdf.list_terms(lang='it')
# vimrdf.get_subject_by_term('measurement unit')
# vimrdf.get_term_by_subject(vimrdf.get_subject_by_id(1, 7), lang='en')
# vimrdf.get_entry_by_term('unità di misura', lang='it')
# vimrdf.get_local(vimrdf.get_entry_by_id(1, 7)[vimrdf.term], lang='it') # get term by id
# vimrdf.get_superordinate(vimrdf.get_subject_by_term('measurement unit'))
# vimrdf.get_direct_subordinates(vimrdf.get_subject_by_term('reference quantity'))
# vimrdf.get_superordinates(vimrdf.get_subject_by_term('derived unit'))
# vimrdf.to_string(vimrdf.get_entry_by_id(1, 7), lang='en')

# %%
