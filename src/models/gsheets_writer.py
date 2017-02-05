from apiclient import discovery
from oauth2client import client, tools
from oauth2client.file import Storage
from db.models import Player
import httplib2
import os


class GSheetsWriter:

    def __init__(self, spreadsheet_id):
        self.ss_id = spreadsheet_id
        self.__service = self.__get_service()
        return

    def update_loot_spreadsheet(self, session):
        self.__clear_existing_spreadsheet(session)
        self.__create_summary_sheet(session)
        self.__create_all_user_sheets(session)
        return

    def __clear_existing_spreadsheet(self, session):
        sheets_metadata = self.__service.spreadsheets().get(spreadsheetId=self.ss_id).execute()
        sheets = sheets_metadata.get('sheets', '')
        return

    def __create_summary_sheet(self, session):
        return

    def __create_all_user_sheets(self, session):
        users = session.query(Player).order_by(Player.name).all()
        for user in users:
            self.__create_user_sheet(session, user)
        return

    def __create_user_sheet(self, session, user):
        return


    def __get_credentials(self):
        """Gets valid user credentials from storage.

            If nothing has been stored, or if the stored credentials are invalid,
            the OAuth2 flow is completed to obtain the new credentials.

            Returns:
                Credentials, the obtained credential.
        """

        # If modifying these scopes, delete your previously saved credentials
        # at ~/.credentials/sheets.googleapis.com-python-quickstart.json
        SCOPE = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive.readonly"]
        CLIENT_ID = 'client_secret.json'
        APPLICATION_NAME = 'DefTools'
        try:
            import argparse
            flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
        except ImportError:
            flags = None
        home_dir = os.path.expanduser('~')
        credential_dir = os.path.join(home_dir, '.credentials')
        if not os.path.exists(credential_dir):
            os.makedirs(credential_dir)
        credential_path = os.path.join(credential_dir, 'sheets.googleapis.com-deftools.json')
        store = Storage(credential_path)
        credentials = store.get()
        if not credentials or credentials.invalid:
            flow = client.flow_from_clientsecrets(CLIENT_ID, SCOPE)
            flow.user_agent = APPLICATION_NAME
            if flags:
                credentials = tools.run_flow(flow, store, flags)
            else:
                credentials = tools.run(flow, store)
            print('Storing credentials to ' + credential_path)
        return credentials

    def __get_service(self):
        """Shows basic usage of the Sheets API.

            Creates a Sheets API service object and prints the names and majors of
            students in a sample spreadsheet:
            https://docs.google.com/spreadsheets/d/1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms/edit
        """
        credentials = self.__get_credentials()
        http = credentials.authorize(httplib2.Http())
        discoveryURL = ('https://sheets.googleapis.com/$discovery/rest?'
                        'version=v4')
        service = discovery.build('sheets', 'v4', http=http, discoveryServiceUrl=discoveryURL)
        return service

