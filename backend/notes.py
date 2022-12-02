import uuid, time, os, functions_framework 
from utils import check_valid_request, Merge
from supabase import create_client, Client
from google.cloud import language_v1
from dotenv import load_dotenv

load_dotenv()
API_URL = os.getenv("API_URL")
API_KEY = os.getenv("API_KEY")
SECRET = os.getenv("SECRET")

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
    
    # ---- Start Check valid request ----
    tokens = check_valid_request(request)
    if(type(tokens) is Exception):
        return tokens
    # ---- End Check Valid Request ----

    if request.method == "GET":
        return Merge(notes_get(), tokens)
    elif request.method == "POST":
        if len(request.path) == 1:
            return Merge(notes_post(request), tokens)
        else:
            return Merge(notes_update(request), tokens)
    elif request.method == "UPDATE":
        return Merge(notes_update(request), tokens)
    elif request.method == "DELETE":
        return Merge(notes_delete(request), tokens)

# Make sure this inserts a user_notes entry
def notes_post(request):
    supabase = create_client(API_URL, API_KEY)

    json_data = request.get_json()
    if 'title' not in json_data:
        json_data['title'] = "title"

    # ---- Start NLP API ----
    document = language_v1.Document(
        content=json_data['content'], type_=language_v1.Document.Type.PLAIN_TEXT
    )

    request = language_v1.AnalyzeEntitiesRequest(
        document=document,
    )
    nlp_client = language_v1.LanguageServiceClient()

    response = nlp_client.analyze_entities(request=request)
    # ---- End NLP Api ----

    note_id = str(uuid.uuid4())
    data = {
        'note_id': note_id,
        'content': json_data['content'],
        'deleted': False,
        'title': json_data['title'],
    }

    supabase.table('notes').insert(data).execute()  # inserting one record

    for entity in response.entities:
        insert_tag(entity, note_id, supabase)

    response = {
        'note_id': note_id,
    }
    return response

# Refactor to only pull down notes of user
def notes_get():
    supabase = create_client(API_URL, API_KEY)
    
    all_notes = supabase.rpc('get_tags_for_notes', {}).execute()
    response = {
        'notes': []
    }

    note_id_hash = {}
    for note in all_notes.data:
        if note['note_id'] not in note_id_hash:
            note_id_hash[note['note_id']] = {
                'note_id': note['note_id'],
                'content': note['content'],
                'title': note['title'],
                'tags': [{"tag_id": note["tag_id"], "name": note["name"], "salience": note["salience"]}]
            }
        else:
            note_id_hash[note['note_id']]['tags'].append(
                {"tag_id": note["tag_id"], "name": note["name"], "salience": note["salience"]})

    for note in note_id_hash:
        response['notes'].append(note_id_hash[note])
    return response


def notes_update(request):
    supabase = create_client(API_URL, API_KEY)
    
    json_data = request.get_json()
    data = {}
    if 'title' in json_data:
        data['title'] = json_data['title']
    if 'content' in json_data:
        data['content'] = json_data['content']

    note_id = request.path[len("/"):]
    supabase.table('notes').update(data).eq('note_id', note_id).execute()
    supabase.table("notes_tags").delete().eq("note_id", note_id).execute()

    request = language_v1.AnalyzeEntitiesRequest(
        document=language_v1.Document(
            content=json_data['content'], type_=language_v1.Document.Type.PLAIN_TEXT
        )
    )
    nlp_client = language_v1.LanguageServiceClient()

    response = nlp_client.analyze_entities(request=request)
    for tag in response.entities:
        insert_tag(tag, note_id, supabase)

    response = {
        'note_id': note_id,
    }
    return response


def notes_delete(request):
    supabase = create_client(API_URL, API_KEY)
    note_id = request.path[len("/"):]

    # only doing soft deletes, not hard deletes
    supabase.table('notes').delete().eq('note_id', note_id).execute()
    supabase.table('notes_tags').delete().eq('note_id', note_id).execute()
    
    response = {
        'note_id': note_id,
    }
    return response

# input: string containing the content
# output: array of dict containing name, salience, type
def gcp_nlp_api(text):
    client = language_v1.LanguageServiceClient()

    request = language_v1.AnalyzeEntitiesRequest(
        document=language_v1.Document(
            content=text, type_=language_v1.Document.Type.PLAIN_TEXT
        )
    )
    response = client.analyze_entities(request=request)

    metadata = []
    for entity in response.entities:
        metadata.append({"name": entity.name, "salience": entity.salience, "type":entity.type_})
    return metadata

# tag: {"name": tag_name, "salience": salience}
# note_id: uuid
def insert_tag(tag, note_id, supabase: Client):

    
    current_tag = supabase.table("tags").select(
        "*").eq("name", tag.name).execute()
    print("CURRENT TAG: ", current_tag)
    if current_tag.data == []:
        print("INSERTING TAG")
        tag_id = str(uuid.uuid4())
        supabase.table("tags").insert(
            {"name": tag.name, "tag_id": tag_id}).execute()
        supabase.table("notes_tags").insert(
            {"tag_id": tag_id, "note_id": note_id, "salience": tag.salience}).execute()
    else:
        supabase.table("notes_tags").insert(
            {"note_id": note_id, "tag_id": current_tag.data[0]["tag_id"], "salience": tag.salience}).execute()