from supabase import create_client
import functions_framework
from google.cloud import language_v1

API_URL = 'https://lwheswmvrtoltfogtrvv.supabase.co'
API_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imx3aGVzd212cnRvbHRmb2d0cnZ2Iiwicm9sZSI6ImFub24iLCJpYXQiOjE2NjcxNTUxMDgsImV4cCI6MTk4MjczMTEwOH0.2PL2EGizWXNXUh6T_wKuPM1KZrgJ0X41zsWGkR0lgJA'

"""This is following the implementation of https://github.com/ethanmorganumich/Porcupines/wiki/3.-APIs-and-Controller"""
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
    # return notes_get(request)
    if request.method == "GET":
        if len(request.path) != 1:
            return notes_search_by_tag(request=request)
        else:
            # Get all tags
            return get_all_tags()


def notes_search_by_tag(request):
    supabase = create_client(API_URL, API_KEY)
    json_data = request.get_json()
    supabase.auth.api.get_user(jwt=json_data['access_token'])

    tag_id = request.path[len("/"):]
    # Find tag_id from name
    # tag_id = supabase.table('tags').select('tag_id').eq('name', json_data['content']).execute()
    print("tag_id:", tag_id)
    # note_ids = supabase.table('notes_tags').select('note_id').eq('tag_id', tag_id.data[0]['tag_id']).execute()
    note_ids = supabase.table('notes_tags').select('note_id').eq('tag_id', tag_id).execute()
    print("note_ids:", note_ids)
    notes_with_tag = []
    for note_id in note_ids.data:
        one_note = supabase.table('notes').select('content', 'title', 'note_id').eq('note_id', note_id['note_id']).execute()
        notes_with_tag.append(one_note.data[0])
    print({"notes": notes_with_tag})
    return {"notes": notes_with_tag}


def get_all_tags(request):
    supabase = create_client(API_URL, API_KEY)
    json_data = request.get_json()
    supabase.auth.api.get_user(jwt=json_data['access_token'])
    # this code segment gets all notes for that tag
    # ex:
        #   "notes": [
        # {
        #   "content": "Testing from computer.",
        #   "name": "Testing",
        #   "note_id": "bff55320-8275-4a31-8aa9-99f4530578e7",
        #   "salience": 0.722901523113251,
        #   "tag_id": "02200df4-d2ad-48fc-8a95-39d86deefe8e",
        #   "title": "title title man"
        # },
    s = supabase.rpc('get_tags_for_notes', {}).execute()
    return {"notes": s.data}
