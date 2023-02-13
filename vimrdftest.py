# %%
import vimrdf

vimrdf = vimrdf.VIMRDF()
vimrdf.load_entries_from_JSON()
#vimrdf.load_kinds()
#vimrdf.load_units()

desc = '''
***********************************************************************************
0: End
1: Given a term, get the subject, then the entry, and display some content
2: Given a term, get the entry and display the definition
3: Given a term, display the list of admitted terms, if present
4. Given an id, display the term
5. Given a term, get the subject, then low-level access and display the definition
6. Given a term, get the entry and display it
11. Given a term, get the list of all superordinates and display their terms
12. Given a term, get the list of all direct subordinates and display their terms
21. Serialize the entries in turtle (default) format
22. Serialize the entries in XML-RDF format
23. Serialize the entries in JSON-LD format
24. Serialize the entries in a turtle-formatted file
***********************************************************************************
'''

the_term = 'quantity dimension'
#the_term = 'measurement unit'
the_ch = 1
the_it = 12

x = -1
while x != 0:
    print(desc)
    x = int(input('--> '))

    if x == 1:
        subject = vimrdf.get_subject_by_term(the_term)
        entry = vimrdf.get_entry_by_subject(subject)
        print(f'{entry[vimrdf.chapter]}.{entry[vimrdf.item]}: {entry[vimrdf.term]}')

    elif x == 2:
        entry = vimrdf.get_entry_by_term(the_term)
        print(entry[vimrdf.definition])

    elif x == 3:
        entry = vimrdf.get_entry_by_term(the_term)
        if vimrdf.admitted_terms in entry:
            print('; '.join([str(term) for term in entry[vimrdf.admitted_terms]]))
        else:
            print('there are no admitted terms')

    elif x == 4:
        #print(vimrdf.get_term_by_id(the_ch, the_it))
        pass

    elif x == 5:
        subject = vimrdf.get_subject_by_term(the_term)
        print(vimrdf.get_graph().value(subject, vimrdf.definition))

    elif x == 6:
        entry = vimrdf.get_entry_by_term(the_term)
        print(vimrdf.to_string(entry))

    elif x == 11:
        subject = vimrdf.get_subject_by_term(the_term)
        #print([vimrdf.get_term_by_subject(e) for e in vimrdf.get_superordinates(subject)])

    elif x == 12:
        subject = vimrdf.get_subject_by_term(the_term)
        #print([vimrdf.get_term_by_subject(e) for e in vimrdf.get_direct_subordinates(subject)])

    elif x == 21:
        print(vimrdf.serialize())

    elif x == 22:
        print(vimrdf.serialize(format='xml'))

    elif x == 23:
        print(vimrdf.serialize(format='json-ld'))

    elif x == 24:
        vimrdf.to_file()
        print('Done: file created')

    print('\n')

print('End...')
