from supabase import create_client
from urllib.parse import urlparse
from dotenv import load_dotenv
import functions_framework, os, re

load_dotenv()
API_URL = os.getenv("API_URL")
API_KEY = os.getenv("API_KEY")

@functions_framework.http
def authentication_request(request):
    if request.method == 'POST':
        return user_post(request)
    elif request.method == 'GET':
        return user_get(request)

def user_post(request):
    supabase = create_client(API_URL, API_KEY)
    json_data = request.get_json()
    
    res = supabase.auth.sign_up(
        email=json_data['email'], 
        password=json_data['password']
    )
    
    return ({
        "user_id": res.id,
    })

def user_get(request):
    supabase = create_client(API_URL, API_KEY)

    json_data = re.split(';|=', urlparse(request.path).params)
    
    res = supabase.auth.sign_in(
        email=json_data[1], 
        password=json_data[3]
    )
    
    return ({
        "access_token": res.access_token,
        "refresh_token": res.refresh_token,
        "user_id": res.user.id,
    })
