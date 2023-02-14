# %%
from rdflib import Graph, Namespace

sib = Namespace('http://test.sibrochurerdf.org/')

g = Graph()
g.bind('sib', sib, override=True)

g.parse('./SIBrochure.owl')
g.serialize(format='turtle', destination='./SIBrochure.ttl')

# %%
