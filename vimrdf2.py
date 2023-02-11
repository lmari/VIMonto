# %%
from rdflib import Graph, URIRef, Literal
from rdflib.namespace._RDF import RDF
from rdflib.namespace._RDFS import RDFS
import json

class VIMRDF:
    def __init__(self, namespace:str='http://test.vimrdf.org/', prefix:str='vim'):
        self.namespace = namespace
        self._g = Graph()                               # a triple store as the main data structure
        self._g.bind(prefix, namespace)
        self._entries = {}                              # a dictionary of URIRefs as the front-end data structure

        VIMEntity = self.set_URI('VIMEntity')           # the top entity
        self._g.add((VIMEntity, RDF.type, RDFS.Class))
        self._g.add((VIMEntity, RDFS.subClassOf, RDFS.Resource))
        self._entries['VIMEntity'] = VIMEntity

        self.ch = self.set_URI('ch')                    # the properties of the entries (*to be completed*)
        self._g.add((self.ch, RDF.type, RDF.Property))
        self._g.add((self.ch, RDFS.label, Literal('The id of the chapter in which the entry is included')))
        self._g.add((self.ch, RDFS.domain, VIMEntity))
        self._g.add((self.ch, RDFS.range, RDFS.Literal))

        self.it = self.set_URI('it')
        self._g.add((self.it, RDF.type, RDF.Property))
        self._g.add((self.it, RDFS.label, Literal('The id of the entry in the chapter')))
        self._g.add((self.it, RDFS.domain, VIMEntity))
        self._g.add((self.it, RDFS.range, RDFS.Literal))

        self.term = self.set_URI('term')
        self._g.add((self.term, RDF.type, RDF.Property))
        self._g.add((self.term, RDFS.label, Literal('The preferred term of the entry')))
        self._g.add((self.term, RDFS.domain, VIMEntity))
        self._g.add((self.term, RDFS.range, RDFS.Literal))

        self.admitted_terms = self.set_URI('admitted_terms')
        self._g.add((self.admitted_terms, RDF.type, RDF.Property))
        self._g.add((self.admitted_terms, RDFS.label, Literal('The list of zero or more admitted terms of the entry')))
        self._g.add((self.admitted_terms, RDFS.domain, VIMEntity))
        self._g.add((self.admitted_terms, RDFS.range, RDF.Seq))

        self.definition = self.set_URI('definition')
        self._g.add((self.definition, RDF.type, RDF.Property))
        self._g.add((self.definition, RDFS.label, Literal('The definition of the entry')))
        self._g.add((self.definition, RDFS.domain, VIMEntity))
        self._g.add((self.definition, RDFS.range, RDFS.Literal))

        self._g.add((VIMEntity, self.ch, Literal(0)))
        self._g.add((VIMEntity, self.it, Literal(0)))
        self._g.add((VIMEntity, self.term, Literal('VIM Entity')))
        self._g.add((VIMEntity, self.definition, Literal('(primitive)')))

        self.init_graph()


    def set_URI(self, name: str) -> URIRef:
        ''' Utility method '''
        return URIRef(self.namespace + name)


    def init_graph(self):
        ''' Populate both the graph and the dictionary with some primitives '''
        VIMEntity = self.set_URI('VIMEntity')
        self._g.add((VIMEntity, RDF.type, RDFS.Class))
        self._g.add((VIMEntity, RDFS.subClassOf, RDFS.Resource))
        self._g.add((VIMEntity, self.ch, Literal(0)))
        self._g.add((VIMEntity, self.definition, Literal('(primitive)')))
        self._entries['VIMEntity'] = VIMEntity

        GeneralProperty = self.set_URI('GeneralProperty')
        self._g.add((GeneralProperty, RDF.type, RDFS.Class))
        self._g.add((GeneralProperty, RDFS.subClassOf, VIMEntity))
        self._g.add((GeneralProperty, self.ch, Literal(0)))
        self._g.add((GeneralProperty, self.definition, Literal('(primitive)')))
        self._entries['GeneralProperty'] = GeneralProperty

        IndividualProperty = self.set_URI('IndividualProperty')
        self._g.add((IndividualProperty, RDF.type, RDFS.Class))
        self._g.add((IndividualProperty, RDFS.subClassOf, VIMEntity))
        self._g.add((IndividualProperty, self.ch, Literal(0)))
        self._g.add((IndividualProperty, self.definition, Literal('(primitive)')))
        self._entries['IndividualProperty'] = IndividualProperty


    def load_entries(self, data_file:str='./vimrdf.json'):
        ''' Populate both the graph and the dictionary from a JSON file '''
        data = json.load(open(data_file))
        for x in data:
            a = self.set_URI(x['class'])
            self._entries[x['class']] = a
            self._g.add((a, RDF.type, RDFS.Class))
            self._g.add((a, RDFS.subClassOf, self._entries[x['sclass']]))
            self._g.add((a, self.ch, Literal(x['ch'])))
            self._g.add((a, self.it, Literal(x['it'])))
            self._g.add((a, self.term, Literal(x['term'])))
            if 'admitted_terms' in x:
                for i, adm_term in enumerate(x['admitted_terms']):
                    self._g.add((a, self.admitted_terms, Literal(adm_term)))
            self._g.add((a, self.definition, Literal(x['definition'])))
        print('VIM RDF: json loaded.\n')


    def load_kinds(self, data_file:str='./vimkinds.json'):
        ''' Sample loader of kind instances '''
        entity = self.get_subject_by_term('quantity <general>')
        self.kind_name = self.set_URI('kind_name')
        self.kind_symbol = self.set_URI('kind_symbol')
        data = json.load(open(data_file))
        for x in data:
            a = self.set_URI(x['kind'])
            self._g.add((a, RDF.type, entity))
            self._g.add((a, self.kind_name, Literal(x['kind'])))
            self._g.add((a, self.kind_symbol, Literal(x['symbol'])))
        print('VIM RDF kinds: json loaded.\n')


    def load_units(self, data_file:str='./vimunits.json'):
        ''' Sample loader of unit instances '''
        entity = self.get_subject_by_term('measurement unit')
        self.unit_name = self.set_URI('unit_name')
        self.unit_symbol = self.set_URI('unit_symbol')
        self.unit_kind = self.set_URI('unit_kind')
        data = json.load(open(data_file))
        for x in data:
            a = self.set_URI(x['unit'])
            self._g.add((a, RDF.type, entity))
            self._g.add((a, self.unit_name, Literal(x['unit'])))
            self._g.add((a, self.unit_symbol, Literal(x['symbol'])))
            self._g.add((a, self.unit_kind, Literal(x['kind'])))
        print('VIM RDF units: json loaded.\n')


    def get_subject_by_term(self, _term:str) -> URIRef:
        ''' Return the URIRef with the given term '''
        x = list(self._g.subjects(self.term, Literal(_term)))
        if len(x) != 1: return None # type: ignore
        return x[0] # type: ignore


    def get_term_by_subject(self, _subject:URIRef) -> str:
        ''' Return the term of the given URIRef '''
        return str(self._g.value(_subject, self.term))


    def get_term_by_id(self, _ch:int, _it:int) -> str:
        ''' Return the term of the given chapter and item '''
        query = f"""
            SELECT ?term
            WHERE {{
                ?s vim:term ?term .
                ?s vim:ch {_ch} .
                ?s vim:it {_it} .
            }} """
        result = self._g.query(query)
        if len(result) != 1: return ''
        return str(list(result)[0].term) # type: ignore


    def get_entry_by_subject(self, _subject:URIRef) -> dict:
        ''' Read all triples with the given subject
            and return them as a dictionary {predicate: object} '''
        #return dict(self._g.predicate_objects(_subject))
        temp = list(self._g.predicate_objects(_subject))
        entry = {}
        for item in temp:
            if item[0] not in entry:
                entry[item[0]] = item[1]
            elif type(entry[item[0]]) != list:
                entry[item[0]] = [entry[item[0]], item[1]]
            else:
                entry[item[0]].append(item[1])
        return entry


    def get_entry_by_term(self, _term:str) -> dict:
        ''' Read all triples whose subject has the given term
            and return them as a dictionary {predicate: object} '''
        subject = self.get_subject_by_term(_term)
        if subject is None: return {}
        return self.get_entry_by_subject(subject)


    def get_superordinate(self, _subject:URIRef) -> URIRef:
        ''' Return the URIRef superordinate of the given URIRef '''
        return self._g.value(_subject, RDFS.subClassOf) # type: ignore


    def get_superordinates(self, _subject:URIRef) -> list:
        ''' Return the sorted list of the URIRefs superordinate of the given URIRef '''
        res = []
        sup = self.get_superordinate(_subject)
        while int(self._g.value(sup, self.ch)) != 0: # type: ignore
            res.append(sup)
            sup = self.get_superordinate(sup)
        return res


    def get_direct_subordinates(self, _subject:URIRef) -> list:
        ''' Return the list of the URIRef direct subordinates of the given URIRef '''
        return list(self._g.subjects(RDFS.subClassOf, _subject))


    def to_string(self, _entry:dict) -> str:
        ''' Return a formatted string with the content of the given entry '''
        t = ' (' + '; '.join([str(term) for term in _entry[self.admitted_terms]]) + ')' if self.admitted_terms in _entry else ''
        return f'{_entry[self.ch]}.{_entry[self.it]} {_entry[self.term]}{t}: {_entry[self.definition]}'


    def get_graph(self):
        ''' Utility method (it should not be needed) '''
        return self._g


    def to_file(self, format:str='turtle', destination:str='./vimrdf.ttl'):
        self._g.serialize(format=format, destination=destination)


    def serialize(self, format:str='turtle') -> str:
        return self._g.serialize(format=format)

# %%
