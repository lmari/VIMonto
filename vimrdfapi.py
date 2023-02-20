import uvicorn
from fastapi import FastAPI
from fastapi.responses import Response
import json
from dict2xml import dict2xml
import vimrdf

vimrdf = vimrdf.VIMRDF()
vimrdf.load_entries_from_JSON()

tags_metadata = [
    {"name": "VIMRDF", "description": "A sample app to deal with the content of the International Vocabulary of Metrology (VIM) as an RDF ontology."},
    {"name": "List terms", "description": "Return a dictionary with the list of all terms." },
    {"name": "List ids", "description": "Return a dictionary with the list of all ids (chapter.item)." },
    {"name": "Get entry by id", "description": "Return a dictionary with the entry with the given id (chapter.item)." },
]

app = FastAPI(openapi_tags=tags_metadata)   # call it with http://localhost:8080/docs for Swagger


def format_chooser(res, format):
    if format == 'xml':
        x = '''<?xml version="1.0" encoding="utf-8"?>
            <vim
                xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
                xmlns:rdfs="http://www.w3.org/2000/01/rdf-schema#"
                xmlns:vim="http://test.vimrdf.org/">
        '''
        x += dict2xml(res, indent ="   ") + '</vim>'
        return Response(content=x, media_type='application/xml')
    return Response(content=json.dumps(res), media_type='application/json')


@app.get('/')
async def home():
    return Response(content='<h1>Hello VIMRDF!</h1>Please check <a href="/docs">the API</a>.', media_type='text/html')


@app.get('/list_terms', tags=['List terms'])
async def list_terms(format='json', lang='en'):
    return format_chooser(vimrdf.list_terms(lang=lang), format)


@app.get('/list_ids', tags=['List ids'])
async def list_ids(format='json'):
    return format_chooser(vimrdf.list_ids(), format)


@app.get('/get_entry_by_id', tags=['Get entry by id'])
async def get_entry_by_id(chapter=1, item=1, format='json', lang='en'):
    return format_chooser(vimrdf.get_entry_by_id(int(chapter), int(item), lang=lang, as_string=True, full_URL=False), format)


if __name__ == '__main__':
    uvicorn.run('vimrdfapi:app', port=8080, reload=True)
