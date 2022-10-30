from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.cloud import language_v1


def main():
    client = language_v1.LanguageServiceClient()


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