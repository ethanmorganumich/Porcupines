from supabase import create_client
import functions_framework
from google.cloud import language_v1
import json


API_URL = 'https://lwheswmvrtoltfogtrvv.supabase.co'
API_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imx3aGVzd212cnRvbHRmb2d0cnZ2Iiwicm9sZSI6ImFub24iLCJpYXQiOjE2NjcxNTUxMDgsImV4cCI6MTk4MjczMTEwOH0.2PL2EGizWXNXUh6T_wKuPM1KZrgJ0X41zsWGkR0lgJA'

@functions_framework.http
def authentication_request(request):
    if request.method == 'POST':
        return user_post(request)
    elif request.method == 'GET':
        return user_get(request)

def user_post(request):
    supabase = create_client(API_URL, API_KEY)
    json_data = request.get_json()
    res = supabase.auth.sign_up(email=json_data['email'], password=json_data['password'])
    return ({
        "user_id": res.id
    })

def user_get(request):
    supabase = create_client(API_URL, API_KEY)
    json_data = request.get_json() 
    res = supabase.auth.sign_in(email=json_data['email'], password=json_data['password'])
    return ({
        "token": res.access_token,
        "refresh_token": res.refresh_token,
        "user_id": res.user.id,
        "email": res.user.email
    })

# a1251f20-3a24-4fbc-b23e-8f38e2c2e64c

