from django.http import JsonResponse, HttpResponse
from django.db import connection
from django.views.decorators.csrf import csrf_exempt
import json
import uuid
from supabase import create_client
import time

API_URL = 'https://lwheswmvrtoltfogtrvv.supabase.co'
API_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imx3aGVzd212cnRvbHRmb2d0cnZ2Iiwicm9sZSI6ImFub24iLCJpYXQiOjE2NjcxNTUxMDgsImV4cCI6MTk4MjczMTEwOH0.2PL2EGizWXNXUh6T_wKuPM1KZrgJ0X41zsWGkR0lgJA'

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
    cursor.execute('SELECT username, message, time FROM chatts ORDER BY time DESC;')
    rows = cursor.fetchall()

    response = {}
    response['chatts'] = rows
    return JsonResponse(response)

@csrf_exempt
def notes_post(request):
    supabase = create_client(API_URL, API_KEY)
    json_data = json.loads(request.body)
    note_id = str(uuid.uuid4())
    currentTime = time.time()
    if 'title' not in json_data:
        json_data['title'] = "title"

    data = {
        'note_id': note_id,
        'content': json_data['content'],
        'deleted': False,
        'title': json_data['title']
    }
    supabase.table('notes').insert(data).execute() # inserting one record

    response = {}
    response['note_id'] = note_id
    return JsonResponse(response)

@csrf_exempt
def notes_get(request):
    supabase = create_client(API_URL, API_KEY)
    t = supabase.table('notes').select('*').execute()
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
    data = {}
    if 'title' in json_data:
        data['title'] = json_data['title']
    if 'content' in json_data:
        data['content'] = json_data['content']

    t = supabase.table('notes').update(data).eq('note_id', note_id).execute()
    return JsonResponse({})

@csrf_exempt
def notes_delete(request, note_id):
    supabase = create_client(API_URL, API_KEY)
    supabase.table('notes').delete().eq('note_id', note_id).execute()
    return JsonResponse({})

# a1251f20-3a24-4fbc-b23e-8f38e2c2e64c