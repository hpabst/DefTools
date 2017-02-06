from apiclient import discovery
from oauth2client import client, tools
from oauth2client.file import Storage
from db.models import Player, Loot, LootAward
from googleapiclient.errors import HttpError
import datetime
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
        requests = []
        sheets_metadata = self.__service.spreadsheets().get(spreadsheetId=self.ss_id).execute()
        sheets = sheets_metadata.get('sheets', '')
        maindata = sheets.pop(0) #Can't delete the last sheet in a spreadsheet, so we leave the last one and clear it instead.
        for sheet in sheets:
            sheet_id = sheet.get("properties").get("sheetId")
            requests.append({
                'deleteSheet':{
                    'sheetId':sheet_id
                }
            })
        requests.append({
            "updateCells":{
                "range":{
                    "sheetId":maindata.get("properties").get("sheetId")
                },
                "fields" : "userEnteredValue"
            }
        })
        body = {
            'requests': requests
        }
        try:
            response = self.__service.spreadsheets().batchUpdate(spreadsheetId=self.ss_id, body=body).execute()
        except HttpError as h:
            raise h
        return

    def __create_summary_sheet(self, session):
        values = []
        data = []
        sheets_metadata = self.__service.spreadsheets().get(spreadsheetId=self.ss_id).execute()
        sheets = sheets_metadata.get('sheets', '')
        maindata = sheets[0]
        maindata_id = maindata.get("properties").get("sheetId")
        all_players = session.query(Player).order_by(Player.name).all()
        values.append(["Player", "Reward", "Reason", "Date", "Replacement1", "Replacement2"])
        data.append({
            'range': 'A1:F1',
            'values': [["Player", "Reward", "Reason", "Date", "Replacement1", "Replacement2"]]
        })
        row_counter = 2
        for player in all_players:
            player_str = "{0}-{1}".format(player.name, player.realm)
            awards = session.query(LootAward).filter(LootAward.player_rel == player).order_by(LootAward.award_date).all()
            for award in awards:
                item = award.item_rel
                replace1 = award.replacement1_rel
                replace2 = award.replacement2_rel
                replace2_str = "None"
                if replace2 is not None: #replacement2 may be null in the DB since it's an optional
                    replace2_str = "=HYPERLINK(\"wowhead.com/item={0}\",\"{1}\")".format(replace2.item_id, replace2.name)
                data.append({
                    'range': 'A{0}:F{0}'.format(row_counter),
                    'values': [[player_str, "=HYPERLINK(\"wowhead.com/item={0}\",\"{1}\")".format(item.item_id, item.name),
                               award.reason, award.award_date.strftime('%m/%d/%Y'),
                               "=HYPERLINK(\"wowhead.com/item={0}\",\"{1}\")".format(replace1.item_id, replace1.name),
                               replace2_str
                               ]]
                })
                row_counter += 1
        body = {
            'valueInputOption': 'USER_ENTERED',
            'data': data
        }
        try:
            result = self.__service.spreadsheets().values().batchUpdate(spreadsheetId=self.ss_id,
                                                                        body=body).execute()
        except HttpError as h:
            raise h
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
            Adapted from google's quickstart guide.
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
        """
            Creates a Sheets API service object.
           Adapted from google's quickstart guide.
        """
        credentials = self.__get_credentials()
        http = credentials.authorize(httplib2.Http())
        discoveryURL = ('https://sheets.googleapis.com/$discovery/rest?'
                        'version=v4')
        service = discovery.build('sheets', 'v4', http=http, discoveryServiceUrl=discoveryURL)
        return service

