# %%
import vimrdf

'''
Having installed rdflib-endpoint
(from PyPI: https://pypi.org/project/rdflib-endpoint
peculiarly, conda does not include it...)
these queries can be executed by running
    rdflib-endpoint serve *.ttl
and then connecting to
    http://localhost:8000
to a YASGUI interface, and by adding
    PREFIX vim: <http://test.vimrdf.org/>
'''

vimrdf = vimrdf.VIMRDF()
vimrdf.load_entries()
vimrdf.load_kinds()
vimrdf.load_units()

g = vimrdf.get_graph()

desc = '''
***********************************************************************************
0: End
1: Get the term given the id (SELECT)
2: Get the term given the id (CONSTRUCT)
3: Get the entry given the id (CONSTRUCT)
4. Get the definition given the term (SELECT)
5. Get the subject given the term (CONSTRUCT)
6. Get all terms given a term fragment (SELECT)
7. Get all unit names (SELECT)
8. Get all unit names (SELECT)
***********************************************************************************
'''

x = -1
while x != 0:
    print(desc)
    x = int(input('--> '))

    if x == 1:   # *** get the term given the id (SELECT) ***
        _ch = 1; _it = 12
        query = f"""
        SELECT ?the_term
        WHERE {{
            ?s vim:term ?the_term ;
            vim:ch {_ch} ;
            vim:it {_it} .
        }} """
        result = list(g.query(query))[0] # actually a dict
        print(str(result.the_term)) # type: ignore

    elif x == 2:   # *** get the term given the id (CONSTRUCT) ***
        _ch = 1; _it = 12
        query = f"""
        CONSTRUCT {{
            ?s vim:term ?term
        }} WHERE {{
            ?s vim:term ?term ;
            vim:ch {_ch} ;
            vim:it {_it} .
        }} """
        result = list(g.query(query))[0] # actually a tuple
        print(str(result[2])) # type: ignore (get the object, i.e. the term)

    elif x == 3:   # *** get the entry given the id (CONSTRUCT) ***
        _ch = 1; _it = 12
        query = f"""
        CONSTRUCT {{
            ?s vim:ch ?ch
        }} WHERE {{
            ?s vim:ch ?ch ;
            vim:ch {_ch} ;
            vim:it {_it} .
        }} """
        result = list(g.query(query))[0] # actually a tuple
        subject = result[0] # type: ignore (get the subbject)
        entry = vimrdf.get_entry_by_subject(subject) # type: ignore
        print(entry[vimrdf.term], entry[vimrdf.definition])

    elif x == 4:   # *** get the definition given the term (SELECT) ***
        _term = 'measurement unit'
        query = f"""
        SELECT ?the_definition
        WHERE {{
            ?s vim:term '{_term}' ;
            vim:definition ?the_definition .
        }} """
        result = list(g.query(query))[0] # actually a dict
        print(str(result.the_definition)) # type: ignore

    elif x == 5:   # *** get the subject given the term (CONSTRUCT) ***
        _term = 'measurement unit'
        query = f"""
        CONSTRUCT {{
            ?s vim:term ?term
        }} WHERE {{
            ?s vim:term ?term ;
            vim:term '{_term}' .
        }} """
        result = list(g.query(query))[0] # actually a tuple
        print(result[0]) # type: ignore

    elif x == 6:   # *** get all terms given a term fragment (SELECT) ***
        _term = 'unit'
        query = f"""
        SELECT ?the_term
        WHERE {{
            ?s vim:term ?the_term .
            FILTER(REGEX(?the_term, '{_term}', 'i')) .
        }} """
        result = list(g.query(query))
        print([str(x.the_term) for x in result]) # type: ignore

    elif x == 7:   # *** get all unit names (SELECT) ***
        query = f"""
        SELECT ?the_unit
        WHERE {{
            ?s a vim:MeasurementUnit ;
            vim:unit_name ?the_unit
        }} """
        result = list(g.query(query))
        print([str(x.the_unit) for x in result]) # type: ignore

    elif x == 8:   # *** get all unit names (SELECT) ***
        query = f"""
        SELECT ?the_unit ?the_kind
        WHERE {{
            ?s1 a vim:MeasurementUnit .
            ?s1 vim:unit_name ?the_unit .
            ?s2 a vim:GeneralQuantity .
            ?s2 vim:kind_name ?the_kind .
            ?s1 vim:unit_kind ?the_kind .
        }} """
        result = list(g.query(query))
        print([(str(x.the_unit), str(x.the_kind)) for x in result]) # type: ignore

    print('\n')

print('End...')


# %%
