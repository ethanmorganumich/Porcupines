import json
import uuid
from supabase import create_client
import time
import functions_framework
from google.cloud import language_v1

API_URL = 'https://lwheswmvrtoltfogtrvv.supabase.co'
API_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imx3aGVzd212cnRvbHRmb2d0cnZ2Iiwicm9sZSI6ImFub24iLCJpYXQiOjE2NjcxNTUxMDgsImV4cCI6MTk4MjczMTEwOH0.2PL2EGizWXNXUh6T_wKuPM1KZrgJ0X41zsWGkR0lgJA'

@functions_framework.http
def notes_request(request):
    """Responds to any HTTP request.
    Args:
        request (flask.Request): HTTP request object.
    Returns:
        The response text or any set of values that can be turned into a
        Response object using
        `make_response <http://flask.pocoo.org/docs/1.0/api/#flask.Flask.make_response>`.
    """
    # print(vars(request))
    # print(request.method)
    if request.method == "GET":
        return notes_get(request)
    elif request.method == "POST":
        if len(request.path) == 1:
            return notes_post(request)
        else:
            return notes_update(request)
    # elif request.method == "UPDATE":
    #     return notes_update(request)
    elif request.method == "DELETE":
        return notes_delete(request)


def notes_post(request):
    supabase = create_client(API_URL, API_KEY)
    json_data = request.get_json()
    note_id = str(uuid.uuid4())
    currentTime = time.time()
    if 'title' not in json_data:
        json_data['title'] = "title"

    metadata = gcp_nlp_api(json_data["content"])

    data = {
        'note_id': note_id,
        'content': json_data['content'],
        'deleted': False,
        'title': json_data['title'],
        'metadata': metadata
    }
    supabase.table('notes').insert(data).execute() # inserting one record

    response = {}
    response['note_id'] = note_id
    return response

def notes_get(request):
    supabase = create_client(API_URL, API_KEY)
    t = supabase.table('notes').select('*').execute()
    return {"notes": t.data}


def notes_update(request):
    # print(request.path[7:])
    # print(vars(request))
    # print(type(request.url))
    note_id = request.path[len("/"):]
    supabase = create_client(API_URL, API_KEY)
    json_data = request.get_json()
    data = {}
    if 'title' in json_data:
        data['title'] = json_data['title']
    if 'content' in json_data:
        data['content'] = json_data['content']

    
    t = supabase.table('notes').update(data).eq('note_id', note_id).execute()

    return {}

def notes_delete(request):
    note_id = request.path[len("/"):]
    supabase = create_client(API_URL, API_KEY)
    supabase.table('notes').delete().eq('note_id', note_id).execute()
    return {}


def notes_search_by_tag(request):
    supabase = create_client(API_URL, API_KEY)
    json_data = json.loads(request.body)

    tag_id = supabase.table('tags').select('tag_id').eq('name', json_data['content']).execute()
    note_ids = supabase.table('notes_tags').select('note_id').eq('tag_id', tag_id.data[0]['tag_id']).execute()
    notes_with_tag = []
    for note_id in note_ids.data:
        one_note = supabase.table('notes').select('*').eq('note_id', note_id['note_id']).execute()
        notes_with_tag.append(one_note.data)
    return {"notes": notes_with_tag}

# @csrf_exempt
# def notes_search_by_content(request):
#     supabase = create_client(API_URL, API_KEY)
#     json_data = json.loads(request.body)

#     #find all notes with the requested content
#     notes = supabase.table('notes').select('*')..filter('content', 'textSearch', '(json_data['content'])').execute()
#     return JsonResponse({"notes": notes.data})



# input: string containing the content
# output: array of dict containing name, saleince, type
def gcp_nlp_api(text):
    client = language_v1.LanguageServiceClient()

    document = language_v1.Document(
        content=text, type_=language_v1.Document.Type.PLAIN_TEXT
    )

    request = language_v1.AnalyzeEntitiesRequest(
        document=document,
    )
    response = client.analyze_entities(request=request)

    metadata = []
    for entity in response.entities:
        metadata.append({"name": entity.name, "saleince": entity.salience, "type":entity.type_})
    return metadata
