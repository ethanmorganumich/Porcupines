from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.cloud import language_v1
from supabase import create_client
import json
import time

def main():
    client = language_v1.LanguageServiceClient()


    text = "Hello, world! Obama was the President. He is pretty cool. This is a sample"
    document = language_v1.Document(
        content=text, type_=language_v1.Document.Type.PLAIN_TEXT
    )

    request = language_v1.AnalyzeEntitiesRequest(
        document=document,
    )
    response = client.analyze_entities(request=request)

    print(response)

    API_URL = 'https://lwheswmvrtoltfogtrvv.supabase.co'
    API_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imx3aGVzd212cnRvbHRmb2d0cnZ2Iiwicm9sZSI6ImFub24iLCJpYXQiOjE2NjcxNTUxMDgsImV4cCI6MTk4MjczMTEwOH0.2PL2EGizWXNXUh6T_wKuPM1KZrgJ0X41zsWGkR0lgJA'
    supabase = create_client(API_URL, API_KEY)
    currentTime = time.time()
    data = {
        'note_id': 441,
        'deleted': False
    }
    supabase.table('notes').insert(data).execute() # inserting one record

main()
