import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/presentations.readonly"]

class GoogleSlidesAPI:
    def __init__(self, PRESENTATION_ID ):
        self.PRESENTATION_ID  = PRESENTATION_ID 

    def getSlides(self):

        creds = None
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists("token.json"):
            creds = Credentials.from_authorized_user_file("token.json", SCOPES)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
                creds = flow.run_local_server(port=0)

            # Save the credentials for the next run
            with open("token.json", "w") as token:
                token.write(creds.to_json())

        try:
            service = build("slides", "v1", credentials=creds)

            presentation = service.presentations().get(presentationId=self.PRESENTATION_ID).execute()
            slides = presentation['slides']
            return slides
            """
            testFile = open("testFile.txt","a")
            testFile.write("////////////////////////////\nNew test:\n\n")
            
            for slide in slides:
                print(slide["slideProperties"]["notesPage"]["pageElements"][1]["shape"]["text"]["textElements"][1]["textRun"]["content"])
                testFile.write(slide["slideProperties"]["notesPage"]["pageElements"][1]["shape"]["text"]["textElements"][1]["textRun"]["content"])
                    
            testFile.close()  
            """          
        except HttpError as err:
            print(err)

#
