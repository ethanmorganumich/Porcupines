from supabase import create_client
import functions_framework
from google.cloud import language_v1
import json


API_URL = 'https://lwheswmvrtoltfogtrvv.supabase.co'
API_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imx3aGVzd212cnRvbHRmb2d0cnZ2Iiwicm9sZSI6ImFub24iLCJpYXQiOjE2NjcxNTUxMDgsImV4cCI6MTk4MjczMTEwOH0.2PL2EGizWXNXUh6T_wKuPM1KZrgJ0X41zsWGkR0lgJA'


"""
    This is following the implementation of https://github.com/ethanmorganumich/Porcupines/wiki/3.-APIs-and-Controller
"""

@functions_framework.http
def tags_request(request):
    """Responds to any HTTP request.
    Args:
        request (flask.Request): HTTP request object.
    Returns:
        The response text or any set of values that can be turned into a
        Response object using
        `make_response <http://flask.pocoo.org/docs/1.0/api/#flask.Flask.make_response>`.
    """
    if request.method == "GET" or request.method == "POST":
        print(request.get_json())
        if not request.get_json():
            print("no request json")
            # get all tags from the database
            supabase = create_client(API_URL, API_KEY)
            supabase.rpc('get_tags_for_notes')
        else:
            print("request json")
            return notes_search_by_tag(request)



def notes_search_by_tag(request):
    supabase = create_client(API_URL, API_KEY)
    json_data = request.get_json()
    # json_data = {"content": "02200df4-d2ad-48fc-8a95-39d86deefe8e"}
    tag_id = supabase.table('tags').select('tag_id').eq('name', json_data['content']).execute()
    print("tag_id:", tag_id)
    note_ids = supabase.table('notes_tags').select('note_id').eq('tag_id', tag_id.data[0]['tag_id']).execute()
    print("note_ids:", note_ids)
    notes_with_tag = []
    for note_id in note_ids.data:
        one_note = supabase.table('notes').select('*').eq('note_id', note_id['note_id']).execute()
        notes_with_tag.append(one_note.data)
    print({"notes": notes_with_tag})
    return {"notes": notes_with_tag}


