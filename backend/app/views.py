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
        tags.append(entity['name'])
        count += 1
    return tags


@csrf_exempt
def notes_post(request):
    supabase = create_client(API_URL, API_KEY)
    json_data = json.loads(request.body)
    note_id = str(uuid.uuid4())
    currentTime = time.time()
    data = {
        'note_id': note_id,
        'content': json_data['content'],
        'deleted': False
    }
    supabase.table('notes').insert(data).execute()  # inserting one record

    response = {}
    response['note_id'] = note_id
    response['tags'] = generate_tags(json_data['content'])
    # need to store tags in database
    return JsonResponse(response)


@csrf_exempt
def notes_get(request):
    supabase = create_client(API_URL, API_KEY)
    t = supabase.table('notes').select('*').execute()
    # should include tags from the tags table
    return JsonResponse({"notes": t.data})


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
    new_tags = generate_tags(json_data['content'])
    # should update tags table as well
    t = supabase.table('notes').update(
        {'content': json_data['content']}).eq('note_id', note_id).execute()
    return JsonResponse({})


@csrf_exempt
def notes_delete(request, note_id):
    supabase = create_client(API_URL, API_KEY)
    supabase.table('notes').delete().eq('note_id', note_id).execute()
    # should also delete tags if no other notes have that tag
    return JsonResponse({})
