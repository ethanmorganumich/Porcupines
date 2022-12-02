import json
import uuid
from supabase import create_client
import time
import functions_framework
from google.cloud import language_v1
import requests

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
    elif request.method == "UPDATE":
        return notes_update(request)
    elif request.method == "DELETE":
        return notes_delete(request)


def notes_post(request):
    supabase = create_client(API_URL, API_KEY)
    json_data = request.get_json()
    note_id = str(uuid.uuid4())
    currentTime = time.time()
    if 'title' not in json_data:
        json_data['title'] = "title"

    response = request.json()

    data = {
        'note_id': note_id,
        'content': json_data['content'],
        'deleted': False,
        'title': json_data['title'],
    }
    supabase.table('notes').insert(data).execute()  # inserting one record

    generate_tags(json_data['content'], note_id)

    response = {}
    response['note_id'] = note_id
    return response


def generate_tags(text, note_id):
  # request the url https://us-central1-notesmart.cloudfunctions.net/get_tags and get the response
    request = requests.get(
        "https://us-central1-notesmart.cloudfunctions.net/get_tags", json={"note_text": text})

    if request.ok:
        tags = request.json()
        for tag in tags:
            insert_tag(tag, note_id)
        return tags
    else:
        raise Exception("Error getting tags from cloud function")


def notes_get(request):
    supabase = create_client(API_URL, API_KEY)
    all_notes = supabase.rpc('get_tags_for_notes', {}).execute()
    response = {}
    response['notes'] = []
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
    note_id = request.path[len("/"):]
    supabase = create_client(API_URL, API_KEY)
    json_data = request.get_json()
    data = {}
    if 'title' in json_data:
        data['title'] = json_data['title']
    if 'content' in json_data:
        data['content'] = json_data['content']

    t = supabase.table('notes').update(data).eq('note_id', note_id).execute()
    supabase.table("notes_tags").delete().eq("note_id", note_id).execute()
    generate_tags(json_data['content'], note_id)
    return {}


def notes_delete(request):
    note_id = request.path[len("/"):]
    supabase = create_client(API_URL, API_KEY)
    # only doing soft deletes, not hard deletes
    # supabase.table('notes').delete().eq('note_id', note_id).execute()
    supabase.table('notes').delete().eq('note_id', note_id).execute()
    supabase.table('notes_tags').delete().eq('note_id', note_id).execute()
    return {}


# input: string containing the content
# output: array of dict containing name, salience, type
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
        metadata.append(
          {"name": entity.name, "salience": entity.salience, "type": entity.type_})
    return metadata


def insert_tag(tag, note_id):
    # tag: {"name": tag_name, "salience": salience}
    # note_id: uuid
    supabase = create_client(API_URL, API_KEY)
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
