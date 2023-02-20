# %%
from rdflib import Graph, Namespace

sib = Namespace('http://test.sibrochurerdf.org/')

g = Graph()
g.bind('sib', sib, override=True)

g.parse('./***.owl') # name of the file with data about units and/or kinds
g.serialize(format='turtle', destination='./***.ttl')

# %%
