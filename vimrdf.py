# %%
from rdflib import Graph, URIRef, Literal # see https://rdflib.readthedocs.io/en/stable
from rdflib.namespace._RDF import RDF
from rdflib.namespace._RDFS import RDFS
import json

class VIMRDF:
    def __init__(self, namespace:str='http://test.vimrdf.org/', prefix:str='vim', logging:bool=True):
        self.namespace = namespace
        self.logging = logging
        self._g = Graph()                               # a triple store as the main data structure
        self._g.bind(prefix, namespace)
        self._entries = {}                              # a dictionary of URIRefs as the front-end data structure

        VIMEntity = self.set_URI('VIMEntity')           # the top entity of the VIM ontology
        self._g.add((VIMEntity, RDF.type, RDFS.Class))
        self._g.add((VIMEntity, RDFS.subClassOf, RDFS.Resource))
        self._entries['VIMEntity'] = VIMEntity

        self.chapter = self.set_URI('chapter')          # the properties of the entries (*to be completed*)
        self._g.add((self.chapter, RDF.type, RDF.Property))
        self._g.add((self.chapter, RDFS.label, Literal('The id of the chapter in which the entry is included')))
        self._g.add((self.chapter, RDFS.domain, VIMEntity))
        self._g.add((self.chapter, RDFS.range, RDFS.Literal))

        self.item = self.set_URI('item')
        self._g.add((self.item, RDF.type, RDF.Property))
        self._g.add((self.item, RDFS.label, Literal('The id of the entry in the chapter')))
        self._g.add((self.item, RDFS.domain, VIMEntity))
        self._g.add((self.item, RDFS.range, RDFS.Literal))

        self.term = self.set_URI('term')
        self._g.add((self.term, RDF.type, RDF.Property))
        self._g.add((self.term, RDFS.label, Literal('The dictionary of the first / preferred term of the entry for each language')))
        self._g.add((self.term, RDFS.domain, VIMEntity))
        self._g.add((self.term, RDFS.range, RDFS.Literal))

        self.admitted_terms = self.set_URI('admitted_terms')
        self._g.add((self.admitted_terms, RDF.type, RDF.Property))
        self._g.add((self.admitted_terms, RDFS.label, Literal('The optional dictionary of the list of zero or more admitted terms of the entry for each language')))
        self._g.add((self.admitted_terms, RDFS.domain, VIMEntity))
        self._g.add((self.admitted_terms, RDFS.range, RDF.Seq))

        self.definition = self.set_URI('definition')
        self._g.add((self.definition, RDF.type, RDF.Property))
        self._g.add((self.definition, RDFS.label, Literal('The dictionary of the definition of the entry for each language')))
        self._g.add((self.definition, RDFS.domain, VIMEntity))
        self._g.add((self.definition, RDFS.range, RDFS.Literal))

        self._g.add((VIMEntity, self.chapter, Literal(0)))
        self._g.add((VIMEntity, self.item, Literal(0)))
        self._g.add((VIMEntity, self.term, Literal('VIM Entity')))
        self._g.add((VIMEntity, self.definition, Literal('(primitive)')))

        self.init_graph()


    def set_URI(self, name:str) -> URIRef:
        ''' Utility method. '''
        return URIRef(self.namespace + name)


    def log(self, text:str):
        ''' Utility method. '''
        if(self.logging): print(text)


    def get_graph(self):
        ''' Utility method (it should not be needed). '''
        return self._g


    def init_graph(self):
        ''' Populate the db with some primitives. '''
        VIMEntity = self.set_URI('VIMEntity')
        self._g.add((VIMEntity, RDF.type, RDFS.Class))
        self._g.add((VIMEntity, RDFS.subClassOf, RDFS.Resource))
        self._g.add((VIMEntity, self.chapter, Literal(0)))
        self._g.add((VIMEntity, self.definition, Literal('(primitive)', lang='en')))
        self._entries['VIMEntity'] = VIMEntity

        GeneralProperty = self.set_URI('GeneralProperty')
        self._g.add((GeneralProperty, RDF.type, RDFS.Class))
        self._g.add((GeneralProperty, RDFS.subClassOf, VIMEntity))
        self._g.add((GeneralProperty, self.chapter, Literal(0)))
        self._g.add((GeneralProperty, self.definition, Literal('(primitive)', lang='en')))
        self._entries['GeneralProperty'] = GeneralProperty

        IndividualProperty = self.set_URI('IndividualProperty')
        self._g.add((IndividualProperty, RDF.type, RDFS.Class))
        self._g.add((IndividualProperty, RDFS.subClassOf, VIMEntity))
        self._g.add((IndividualProperty, self.chapter, Literal(0)))
        self._g.add((IndividualProperty, self.definition, Literal('(primitive)', lang='en')))
        self._entries['IndividualProperty'] = IndividualProperty


    def load_entries_from_JSON(self, data_file:str='./vimrdf.json'):
        ''' [ok] Populate the db from the specified JSON file. '''
        data = json.load(open(data_file))
        for x in data:
            a = self.set_URI(x['class'])
            self._entries[x['class']] = a
            self._g.add((a, RDF.type, RDFS.Class))
            self._g.add((a, RDFS.subClassOf, self._entries[x['superclass']]))
            self._g.add((a, self.chapter, Literal(x['chapter'])))
            self._g.add((a, self.item, Literal(x['item'])))
            for lang in x['term'].keys():
                self._g.add((a, self.term, Literal(x['term'][lang], lang=lang))) 
            if 'admitted_terms' in x:
                for lang in x['admitted_terms'].keys():
                    for i, adm_term in enumerate(x['admitted_terms'][lang]):
                        self._g.add((a, self.admitted_terms, Literal(adm_term, lang=lang)))
            for lang in x['definition'].keys():
                self._g.add((a, self.definition, Literal(x['definition'][lang], lang=lang)))
        self.log('VIM RDF: json loaded.\n')


    def load_entries_from_TTL(self, data_file:str='./vimrdf.ttl'):
        ''' [ok] Populate the db from the specified TTL file. '''
        self._g.parse(data_file)
        self.log('VIM RDF: ttl loaded.\n')


    def load_kinds(self, data_file:str='./vimkinds.json'):
        ''' Sample loader of kind instances. '''
        entity = self.get_subject_by_term('quantity <general>')
        self.kind_name = self.set_URI('kind_name')
        self.kind_symbol = self.set_URI('kind_symbol')
        data = json.load(open(data_file))
        for x in data:
            a = self.set_URI(x['kind'])
            self._g.add((a, RDF.type, entity))
            self._g.add((a, self.kind_name, Literal(x['kind'])))
            self._g.add((a, self.kind_symbol, Literal(x['symbol'])))
        self.log('VIM RDF kinds: json loaded.\n')


    def load_units(self, data_file:str='./vimunits.json'):
        ''' Sample loader of unit instances. '''
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
        self.log('VIM RDF units: json loaded.\n')


    def list_subjects(self):
        ''' [ok] Return the list of URIRefs of all subjects. '''
        return list(self._g.subjects(self.term, unique=True))


    def list_terms(self, lang:str='en'):
        ''' [ok] Return the list of all terms as strings of the given language. '''
        res = []
        for subject in self.list_subjects():
            objects = self._g.objects(subject, self.term)
            for object in objects:
                if object.language == lang: # type: ignore
                    res.append(str(object))
        return res


    def get_subject_by_term(self, term:str, lang:str='en') -> URIRef:
        ''' [ok] Return the URIRef of the subject with the given term in the given language,
            or None if the term is not found. '''
        x = list(self._g.subjects(self.term, Literal(term, lang=lang)))
        if len(x) == 0: return None # type: ignore
        return x[0] # type: ignore


    def get_term_by_subject(self, subject:URIRef, lang:str='en') -> str:
        ''' [ok] Return the term in the given language of the subject with the given URIRef,
            or an empty string if the subject is not found. '''
        objects = self._g.objects(subject, self.term)
        for object in objects:
            if object.language == lang: # type: ignore
                return str(object)
        return ''


    def get_term_by_id(self, _ch:int, _it:int) -> str:
        ''' Return the term of the given chapter and item. '''
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
            and return them as a dictionary {predicate: object}. '''
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
            and return them as a dictionary {predicate: object}. '''
        subject = self.get_subject_by_term(_term)
        if subject is None: return {}
        return self.get_entry_by_subject(subject)


    def get_superordinate(self, _subject:URIRef) -> URIRef:
        ''' Return the URIRef superordinate of the given URIRef. '''
        return self._g.value(_subject, RDFS.subClassOf) # type: ignore


    def get_superordinates(self, _subject:URIRef) -> list:
        ''' Return the sorted list of the URIRefs superordinate of the given URIRef. '''
        res = []
        sup = self.get_superordinate(_subject)
        while int(self._g.value(sup, self.chapter)) != 0: # type: ignore
            res.append(sup)
            sup = self.get_superordinate(sup)
        return res


    def get_direct_subordinates(self, _subject:URIRef) -> list:
        ''' Return the list of the URIRef direct subordinates of the given URIRef. '''
        return list(self._g.subjects(RDFS.subClassOf, _subject))


    def to_string(self, _entry:dict) -> str:
        ''' Return a formatted string with the content of the given entry. '''
        t = ' (' + '; '.join([str(term) for term in _entry[self.admitted_terms]]) + ')' if self.admitted_terms in _entry else ''
        return f'{_entry[self.chapter]}.{_entry[self.item]} {_entry[self.term]}{t}: {_entry[self.definition]}'


    def to_file(self, format:str='turtle', destination:str='./vimrdf.ttl'):
        self._g.serialize(format=format, destination=destination)
        self.log('Done: file created')


    def serialize(self, format:str='turtle') -> str:
        return self._g.serialize(format=format)


# %%
