import vimrdf

vimrdf = vimrdf.VIMRDF()

#vimrdf.load_entries_from_JSON()
#vimrdf.to_file(format='turtle', destination='./quicktest.ttl')

vimrdf.load_entries_from_TTL(data_file='./quicktest.ttl')
vimrdf.to_file(format='turtle', destination='./quicktest2.ttl')
