import uvicorn
from fastapi import FastAPI
from fastapi.responses import HTMLResponse, JSONResponse
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

@app.get('/', response_class=HTMLResponse)
async def home():
    return '<h1>Hello VIMRDF!</h1>Please check <a href="/docs">the API</a>.'

@app.get('/list_terms', response_class=JSONResponse, tags=['List terms'])
async def list_terms():
    return vimrdf.list_terms() # type: ignore

@app.get('/list_ids', response_class=JSONResponse, tags=['List ids'])
async def list_ids():
    return vimrdf.list_ids() # type: ignore

@app.get('/get_entry_by_id', response_class=JSONResponse, tags=['Get entry by id'])
async def get_entry_by_id(chapter, item, lang='en'):
    return vimrdf.get_entry_by_id(int(chapter), int(item), lang=lang, as_string=True, full_URL=True) # type: ignore

if __name__ == '__main__':
    uvicorn.run('vimrdfapi:app', port=8080, reload=True)

