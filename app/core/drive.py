import os
import aiofiles
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.oauth2 import service_account
from dotenv import load_dotenv

load_dotenv()

SCOPES = ['https://www.googleapis.com/auth/drive']
SERVICE_ACCOUNT_FILE = os.getenv("GOOGLE_SERVICE_ACCOUNT_JSON")
FOLDER_ID = os.getenv("GOOGLE_DRIVE_FOLDER_ID")

def get_drive_service():
    credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES
    )
    return build('drive', 'v3', credentials=credentials)

async def upload_file_to_drive(file) -> str:
    filename = file.filename
    filepath = f"temp/{filename}"

    # Save to disk
    async with aiofiles.open(filepath, 'wb') as out_file:
        content = await file.read()
        await out_file.write(content)

    media = MediaFileUpload(filepath, resumable=True)
    service = get_drive_service()

    file_metadata = {'name': filename, 'parents': [FOLDER_ID]}
    uploaded = service.files().create(
        body=file_metadata,
        media_body=media,
        fields='id'
    ).execute()

    os.remove(filepath)
    return f"https://drive.google.com/uc?id={uploaded['id']}"
