from msilib.schema import tables
from operator import index
from unicodedata import decimal
import os
from email import header
from json import load
from operator import index
from unicodedata import decimal
import os
# from __future__ import print_function
import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from pprint import pprint
from googleapiclient import discovery

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

def limpar_celulas(SAMPLE_SPREADSHEET_ID_,SAMPLE_RANGE_NAME_):
	creds = None
	# The file token.json stores the user's access and refresh tokens, and is
	# created automatically when the authorization flow completes for the first
	# time.
	if os.path.exists('token.json'):
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

	# creds = None

	service = discovery.build('sheets', 'v4', credentials=creds)

	# The ID of the spreadsheet to update.
	spreadsheet_id = 'my-spreadsheet-id'  # TODO: Update placeholder value.

	# The A1 notation of the values to clear.
	range_ = 'my-range'  # TODO: Update placeholder value.

	clear_values_request_body = {
		# TODO: Add desired entries to the request body.
	}

	request = service.spreadsheets().values().clear(spreadsheetId=SAMPLE_SPREADSHEET_ID_, range=SAMPLE_RANGE_NAME_, body=clear_values_request_body)
	response = request.execute()

	# TODO: Change code below to process the `response` dict:
	pprint(response)

def update_values(spreadsheet_id, range_name, value_input_option,
                    _values):

    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
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
    
    service = build('sheets', 'v4', credentials=creds)
    # [START sheets_update_values]
    values = [
        [
            # Cell values ...
        ],
        # Additional rows ...
    ]
    # [START_EXCLUDE silent]
    values = _values
    # [END_EXCLUDE]
    body = {
        'values': values
    }
    result = service.spreadsheets().values().update(
        spreadsheetId=spreadsheet_id, range=range_name,
        valueInputOption=value_input_option, body=body).execute()
    print('{0} cells updated.'.format(result.get('updatedCells')))
    # [END sheets_update_values]
    return result

def get_values(spreadsheet_id, range_name):
    """
    Creates the batch_update the user has access to.
    Load pre-authorized user credentials from the environment.
    TODO(developer) - See https://developers.google.com/identity
    for guides on implementing OAuth2 for the application.
        """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
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

    # creds, _ = google.auth.default()
    # pylint: disable=maybe-no-member
    try:
        service = build('sheets', 'v4', credentials=creds)

        result = service.spreadsheets().values().get(
            spreadsheetId=spreadsheet_id, range=range_name).execute()
        rows = result.get('values', [])
        # print(f"{len(rows)} rows retrieved")
        return result["values"]
    except HttpError as error:
        print(f"An error occurred: {error}")
        return error

def ultima_linha(SAMPLE_SPREADSHEET_ID_,SAMPLE_RANGE_NAME_):
	creds = None
	# The file token.json stores the user's access and refresh tokens, and is
	# created automatically when the authorization flow completes for the first
	# time.
	if os.path.exists('token.json'):
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

	# creds = None

	service = discovery.build('sheets', 'v4', credentials=creds)

	# The ID of the spreadsheet to update.
	spreadsheet_id = 'my-spreadsheet-id'  # TODO: Update placeholder value.

	# The A1 notation of the values to clear.
	range_ = 'my-range'  # TODO: Update placeholder value.

	clear_values_request_body = {
		# TODO: Add desired entries to the request body.
	}

	#request = service.spreadsheets().values().clear(spreadsheetId=SAMPLE_SPREADSHEET_ID_, range=SAMPLE_RANGE_NAME_, body=clear_values_request_body)


	# TODO: Change code below to process the `response` dict:
	


	rows = service.spreadsheets().values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID_, range=SAMPLE_RANGE_NAME_).execute().get('values', [])
	#response = rows.execute()
	#pprint(response)
	last_row = rows[-1] if rows else None
	last_row_id = len(rows)
	return (last_row_id + 1)