from utils import check_valid_request, Merge
from google.cloud import language_v1
from supabase import create_client
from dotenv import load_dotenv
import functions_framework
import os

load_dotenv()
API_URL = os.getenv("API_URL")
API_KEY = os.getenv("API_KEY")
SECRET = os.getenv("SECRET")

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

    # ---- Start Check valid request ----
    tokens = check_valid_request(request)
    if(type(tokens) is Exception):
        return tokens
    # ---- End Check Valid Request ----

    # return notes_get(request)
    if request.method == "GET":
        if len(request.path) != 1:
            return Merge(notes_search_by_tag(request), tokens)
        else:
            # Get all tags
            return Merge(get_all_tags(), tokens)


def notes_search_by_tag(request):
    supabase = create_client(API_URL, API_KEY)

    tag_id = request.path[len("/"):]
    # Find tag_id from name
    note_ids = supabase.table('notes_tags').select('note_id').eq('tag_id', tag_id).execute()
    
    notes_with_tag = []
    for note_id in note_ids.data:
        one_note = supabase.table('notes').select('content', 'title', 'note_id').eq('note_id', note_id['note_id']).execute()
        notes_with_tag.append(one_note.data[0])
    return {"notes": notes_with_tag}


def get_all_tags():
    supabase = create_client(API_URL, API_KEY)
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
    res = supabase.rpc('get_tags_for_notes', {}).execute()
    return {"notes": res.data}
