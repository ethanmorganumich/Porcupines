from django.http import JsonResponse, HttpResponse
from django.db import connection
from django.views.decorators.csrf import csrf_exempt
import json
import uuid
from supabase import create_client
import time

API_URL = 'https://lwheswmvrtoltfogtrvv.supabase.co'
API_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imx3aGVzd212cnRvbHRmb2d0cnZ2Iiwicm9sZSI6ImFub24iLCJpYXQiOjE2NjcxNTUxMDgsImV4cCI6MTk4MjczMTEwOH0.2PL2EGizWXNXUh6T_wKuPM1KZrgJ0X41zsWGkR0lgJA'

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

def notes_post(request):
    supabase = create_client(API_URL, API_KEY)
    json_data = json.loads(request.body)
    note_id = str(uuid.uuid4())
    currentTime = time.time()
    data = {
        'note_id': note_id,
        'content': json_data['context'],
        'deleted': False
    }
    supabase.table('notes').insert(data).execute() # inserting one record

    response = {}
    response['note_id'] = note_id
    return JsonResponse(response)

def notes_get(request):
    supabase = create_client(API_URL, API_KEY)
    t = supabase.table('notes').select('*').execute()
    return JsonResponse(t.data)

def notes_update(request, note_id):
    supabase = create_client(API_URL, API_KEY)
    json_data = json.loads(request.body)
    t = supabase.table('notes').update({'content': json_data['content']}).eq('note_id', note_id).execute()
    return JsonResponse({})

def notes_delete(request, note_id):
    supabase = create_client(API_URL, API_KEY)
    supabase.table('notes').delete().eq('note_id', note_id).execute()
    return JsonResponse({})

