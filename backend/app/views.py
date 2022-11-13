from django.http import JsonResponse, HttpResponse
from django.db import connection
from django.views.decorators.csrf import csrf_exempt
import json
import uuid
from supabase import create_client
import time
import requests

API_URL = 'https://lwheswmvrtoltfogtrvv.supabase.co'
API_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imx3aGVzd212cnRvbHRmb2d0cnZ2Iiwicm9sZSI6ImFub24iLCJpYXQiOjE2NjcxNTUxMDgsImV4cCI6MTk4MjczMTEwOH0.2PL2EGizWXNXUh6T_wKuPM1KZrgJ0X41zsWGkR0lgJA'

GOOGLE_API_KEY = "AIzaSyDYIhhUkPaSShIvqXprmycYyRyGfRxSrHs"
GOOGLE_LANG_BASE_URL = "https://language.googleapis.com/v1/documents:analyzeEntities"


# TEST_API_URL = "https://vsrtlryzcqlqltbxviqd.supabase.co"
# TEST_API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InZzcnRscnl6Y3FscWx0Ynh2aXFkIiwicm9sZSI6ImFub24iLCJpYXQiOjE2NjgzMTE1NjUsImV4cCI6MTk4Mzg4NzU2NX0.G5AhSqn_dH7I9bA12u-ZC5HQTOpHzfnMMeGAdvgoXHA"


@csrf_exempt
# @api_view(['GET', 'POST', 'DELETE', 'UPDATE'])
def notes(request):
    if request.method == 'POST':
        return notes_post(request)
    elif request.method == 'GET':
        return notes_get(request)
    elif request.method == 'UPDATE':
        return notes_update(request)
    elif request.method == 'DELETE':
        return notes_delete(request)

    cursor = connection.cursor()
    cursor.execute(
        'SELECT username, message, time FROM chatts ORDER BY time DESC;')
    rows = cursor.fetchall()

    response = {}
    response['chatts'] = rows
    return JsonResponse(response)


def generate_tags(text) -> list:
    body = {
        "document": {
            "content": text,
            "type": "PLAIN_TEXT"
        },
        "encodingType": "UTF8"
    }
    res = requests.post(GOOGLE_LANG_BASE_URL + "?key=" +
                        GOOGLE_API_KEY, json=body)

    count = 0
    tags = []
    for entity in res.json()['entities']:
        if count > 5:
            break
        tags.append({"name": entity['name'], "salience": entity['salience']})
        count += 1

    print(tags)
    return tags


def insert_tag(tag, note_id):
    # tag: {"name": tag_name, "salience": salience}
    # note_id: uuid
    supabase = create_client(API_URL, API_KEY)
    current_tag = supabase.table("tags").select(
        "*").eq("name", tag['name']).execute()
    print("CURRENT TAG")
    print(current_tag)
    if current_tag.data == []:
        print("INSERTING TAG")
        tag_id = str(uuid.uuid4())
        supabase.table("tags").insert(
            {"name": tag['name'], "tag_id": tag_id}).execute()
        supabase.table("notes_tags").insert(
            {"tag_id": tag_id, "note_id": note_id, "salience": tag['salience']}).execute()
    else:
        supabase.table("notes_tags").insert(
            {"note_id": note_id, "tag_id": current_tag.data[0]["tag_id"], "salience": tag["salience"]}).execute()


@csrf_exempt
def notes_post(request):
    supabase = create_client(API_URL, API_KEY)
    json_data = json.loads(request.body)
    note_id = str(uuid.uuid4())
    data = {
        'note_id': note_id,
        'content': json_data['content'],
        'deleted': False
    }
    response = {}
    response['tags'] = generate_tags(json_data['content'])
    supabase.table('notes').insert(
        data).execute()  # inserting one record
    response['note_id'] = note_id
    for tag in response['tags']:
        insert_tag(tag, note_id)

    return JsonResponse(response)


@csrf_exempt
def notes_get(request):
    supabase = create_client(API_URL, API_KEY)
    all_notes = supabase.rpc('get_tags_for_notes', {}).execute()
    return JsonResponse({"notes": all_notes.data})


@csrf_exempt
def note_action(request, note_id):
    if request.method == 'UPDATE':
        return notes_update(request, note_id)
    elif request.method == 'DELETE':
        return notes_delete(request, note_id)


@csrf_exempt
def notes_update(request, note_id):
    supabase = create_client(API_URL, API_KEY)
    json_data = json.loads(request.body)
    t = supabase.table('notes').update(
        {'content': json_data['content']}).eq('note_id', note_id).execute()
    supabase.table("notes_tags").delete().eq("note_id", note_id).execute()
    tags = generate_tags(json_data['content'])
    for tag in tags:
        insert_tag(tag, note_id)
    return JsonResponse({})


@csrf_exempt
def notes_delete(request, note_id):
    supabase = create_client(API_URL, API_KEY)
    # supabase.table('notes').delete().eq('note_id', note_id).execute()
    # supabase.table("notes_tags").delete().eq("note_id", note_id).execute()
    supabase.table('notes').update(
        {'deleted': True}).eq('note_id', note_id).execute()
    supabase.table('notes_tags').update(
        {'deleted': True}).eq('note_id', note_id).execute()
    # TODO: delete tags if no other notes have that tag
    return JsonResponse({})


@csrf_exempt
def notes_test(request):
    body = {
        "document": {
            "content": "Ethan is a student at the University of Michigan. He is going to go hard for Halloween.",
            "type": "PLAIN_TEXT"
        },
        "encodingType": "UTF8"
    }
    res = requests.post(GOOGLE_LANG_BASE_URL + "?key=" +
                        GOOGLE_API_KEY, json=body)
    print(json.dumps(res.json(), indent=2))

    return JsonResponse(res.json())
