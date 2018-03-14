# Smart-Lighting-System
## Accounts

### Setup
- Create a project in Google Developers Console with the required Google account and enable the Gmail API [here](https://console.developers.google.com/start/api?id=gmail)

- Add Credentials in the Credentials Tab and select OAuth 2.0 client ID.

- Select the application type Other and create .

- Add homepage URL like `http://localhost:8000` for testing.

- Download JSON file as given to the right of the Client ID.

- Rename as client_secret.json and move to this send_mail subdirectory.

- Install the Google Client Library
`sudo pip3 install --upgrade google-api-python-client`

- Run `python3 custom.py` in the send_mail directory to login with the used account for the first time.

### Usage
- Once the Google account is setup, run the server ( `python3 manage.py runserver 8000` ) normally.
- Edit send_mail/mail_info.py.
