## Local setup
- Run `pip install -r requirements.txt` to set up dependencies
- Create GCloud service account to access Google Drive, download the JSON file.
- Create .env file with:
    ```
    GOOGLE_PROJECT_ID=project_id
    DRIVE_PROJECT_ID=private_key
    DRIVE_CRED_PASSWORD=private_key
    DRIVE_CRED_USERNAME=client_email
    DRIVE_KEY_ID=private_key_id
    DRIVE_CLIENT_ID=client_id
    ```
- Share the Google Drive folder with the service account email
