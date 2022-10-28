from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.cloud import language_v1
import os.path


def main():
    SCOPES = ['https://www.googleapis.com/auth/contacts.readonly']
    creds = Credentials.from_authorized_user_file('backend/token.json')
    if os.path.exists('backend/token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('LanguageServiceClient', 'v1', credentials=creds)


    client = language_v1.LanguageServiceClient(creds)

    text = "Hello, world! Obama was the President. He is pretty cool."
    document = language_v1.Document(
        content=text, type_=language_v1.Document.Type.PLAIN_TEXT
    )

    request = language_v1.AnalyzeEntitiesRequest(
        document=document,
    )
    response = client.analyze_entities(request=request)

    print(response)

main()