import os
import time

import httplib2
from apiclient import discovery
from googleapiclient.errors import HttpError
from oauth2client import client, tools
from oauth2client.file import Storage

from db.models import Player, LootAward


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
        print("Delete request size: {0}.".format(len(requests)))
        backoff = 2
        while backoff < 256:
            try:
                response = self.__service.spreadsheets().batchUpdate(spreadsheetId=self.ss_id, body=body).execute()
                break
            except HttpError as h:
                time.sleep(backoff)
                backoff = backoff * backoff
                if backoff >= 256:
                    raise h
        return

    def __get__cell_borders_request(self, sheetId, start_row_index = 0, end_row_index = 6,
                                    start_col_index = 0, end_col_index = 6):
        request = {
            "updateBorders":{
                "range":{
                    "sheetId":sheetId,
                    "startRowIndex":start_row_index,
                    "endRowIndex":end_row_index,
                    "startColumnIndex":start_col_index,
                    "endColumnIndex":end_col_index
                },
                "top":{
                    "style":"SOLID",
                    "width":1
                },
                "bottom":{
                    "style": "SOLID",
                    "width": 1
                },
                "left":{
                    "style": "SOLID",
                    "width": 1
                },
                "right":{
                    "style": "SOLID",
                    "width": 1
                },
                "innerHorizontal":{
                    "style": "SOLID",
                    "width": 1
                },
                "innerVertical":{
                    "style": "SOLID",
                    "width": 1
                }
            }
        }
        return request

    def __get_column_width_request(self, sheetId):
        request = {
            "updateDimensionProperties": {
                "range": {
                    "sheetId": sheetId,
                    "dimension": "COLUMNS",
                    "startIndex": 0,
                    "endIndex": 6
                },
                "properties": {
                    "pixelSize": 160
                },
                "fields": "pixelSize"
            }
        }
        return request

    def __get_header_row_style_request(self, sheetId, startIndex = 0, endIndex = 6):
        request = {
            "repeatCell":{
                "range":{
                    "sheetId":sheetId,
                    "startRowIndex":0,
                    "endRowIndex":1,
                    "startColumnIndex":startIndex,
                    "endColumnIndex":endIndex
                },
                "cell":{
                    "userEnteredFormat":{
                        "backgroundColor":{
                            "red":0.0,
                            "green":0.0,
                            "blue":0.0
                        },
                        "horizontalAlignment":"CENTER",
                        "textFormat":{
                            "foregroundColor":{
                                "red":1.0,
                                "green":1.0,
                                "blue":1.0
                            },
                            "fontSize":12,
                            "bold":True
                        }
                    }
                },
                "fields":"userEnteredFormat(backgroundColor, textFormat, horizontalAlignment)"
            }
        }
        return request

    def __create_summary_sheet(self, session):
        style_requests = []
        data = []
        sheets_metadata = self.__service.spreadsheets().get(spreadsheetId=self.ss_id).execute()
        sheets = sheets_metadata.get('sheets', '')
        maindata = sheets[0]
        maindata_id = maindata.get("properties").get("sheetId")
        all_players = session.query(Player).order_by(Player.name).all()
        data.append({
            'range': 'A1:F1',
            'values': [["Player", "Reward", "Reason", "Date", "Replacement1", "Replacement2"]]
        })
        data.append({
            "range":"I1:K1",
            "values":[["Player", "Recent Gear Count (2 Weeks)", "Overall Gear Count"]]
        })
        data_row_counter = 2
        summary_row_counter = 2
        for player in all_players:
            player_str = u"{0}-{1}".format(player.name, player.realm)
            awards = session.query(LootAward).filter(LootAward.player_rel == player).order_by(LootAward.award_date).all()
            for award in awards:
                item = award.item_rel
                replace1 = award.replacement1_rel
                replace2 = award.replacement2_rel
                replace1_str = "None"
                replace2_str = "None"
                if replace1 is not None:
                    replace1_str = u"=HYPERLINK(\"wowhead.com/item={0}\",\"{1}\")".format(replace1.item_id, replace1.name)
                if replace2 is not None: #replacement2 may be null in the DB since it's an optional
                    replace2_str = u"=HYPERLINK(\"wowhead.com/item={0}\",\"{1}\")".format(replace2.item_id, replace2.name)
                data.append({
                    'range': 'A{0}:F{0}'.format(data_row_counter),
                    'values': [[player_str, u"=HYPERLINK(\"wowhead.com/item={0}\",\"{1}\")".format(item.item_id, item.name),
                               award.reason,
                                award.award_date.strftime('%m/%d/%Y'),
                               replace1_str,
                               replace2_str
                               ]]
                })
                data_row_counter += 1
            data.append({
                "range":"I{0}:K{0}".format(summary_row_counter),
                "values":[[player_str,
                           u"=COUNTIFS(A:A, \"={0}\", D:D, \">\"&today()-14)".format(player_str),
                           u"=COUNTIF(A:A, \"={0}\")".format(player_str)
                           ]]
            })
            summary_row_counter += 1
        body = {
            'valueInputOption': 'USER_ENTERED',
            'data': data
        }
        backoff = 2
        while backoff < 256:
            try:
                result = self.__service.spreadsheets().values().batchUpdate(spreadsheetId=self.ss_id,
                                                                            body=body).execute()
                break
            except HttpError as h:
                time.sleep(backoff)
                print("Backoff {0}".format(backoff))
                backoff = backoff * backoff
                if backoff >= 256:
                    raise h
        style_requests.append(self.__get_header_row_style_request(sheetId=maindata_id))
        style_requests.append(self.__get_header_row_style_request(sheetId=maindata_id, startIndex=7, endIndex=11))
        style_requests.append(self.__get_column_width_request(sheetId=maindata_id))
        style_requests.append(self.__get__cell_borders_request(sheetId=maindata_id,
                                                               start_row_index=1,
                                                               end_row_index=data_row_counter-1))
        style_requests.append(self.__get__cell_borders_request(sheetId=maindata_id,
                                                               start_row_index=1,
                                                               end_row_index=summary_row_counter-1,
                                                               start_col_index=8,
                                                               end_col_index=11))
        body = {
            "requests":style_requests
        }
        backoff = 2
        while backoff < 256:
            try:
                result = self.__service.spreadsheets().batchUpdate(spreadsheetId=self.ss_id,
                                                                   body=body).execute()
                break
            except HttpError as h:
                time.sleep(backoff)
                print("Backoff {0}".format(backoff))
                backoff = backoff * backoff
                if backoff >= 256:
                    raise h
        return

    def __create_all_user_sheets(self, session):
        users = session.query(Player).order_by(Player.name).all()
        style_requests = []
        for user in users:
            id = self.__create_user_sheet(session, user)
            time.sleep(0.1)#We delay things because otherwise we get 429 errors from google.
            style_requests.append(self.__get_column_width_request(sheetId=id))
            style_requests.append(self.__get_header_row_style_request(sheetId=id))
        body = {
            "requests":style_requests
        }
        backoff = 2
        while backoff < 256:
            try:
                response = self.__service.spreadsheets().batchUpdate(spreadsheetId=self.ss_id, body=body).execute()
                break
            except HttpError as h:
                time.sleep(backoff)
                print("Backoff {0}".format(backoff))
                backoff = backoff * backoff
                if backoff >= 256:
                    raise h
        return

    def __create_user_sheet(self, session, user):
        sheetName = u"{0}-{1}".format(user.name, user.realm)
        request = []
        request.append({
            "addSheet":{
                "properties":{
                    "title": sheetName
                }
            }
        })

        body = {
            "requests":request
        }
        backoff = 2
        while backoff < 256:
            try:
                response = self.__service.spreadsheets().batchUpdate(spreadsheetId=self.ss_id, body=body).execute()
                break
            except HttpError as h:
                time.sleep(backoff)
                print("Backoff {0}".format(backoff))
                backoff = backoff * backoff
                if backoff >= 256:
                    raise h
        sheetID = response.get("replies")[0].get("addSheet").get("properties").get("sheetId")
        awards = session.query(LootAward).filter(LootAward.player_rel == user).order_by(LootAward.award_date).all()
        row_counter = 2
        player_str = u"{0}-{1}".format(user.name, user.realm)
        data = []
        data.append({
            'range': u'{0}!A1:F1'.format(sheetName),
            'values': [["Player", "Reward", "Reason", "Date", "Replacement1", "Replacement2"]]
        })
        for award in awards:
            item = award.item_rel
            replace1 = award.replacement1_rel
            replace2 = award.replacement2_rel
            replace1_str = "None"
            replace2_str = "None"
            if replace1 is not None:
                replace1_str = u"=HYPERLINK(\"wowhead.com/item={0}\",\"{1}\")".format(replace1.item_id, replace1.name)
            if replace2 is not None:  # replacement2 may be null in the DB since it's an optional
                replace2_str = u"=HYPERLINK(\"wowhead.com/item={0}\",\"{1}\")".format(replace2.item_id, replace2.name)
            data.append({
                'range': u'{0}!A{1}:F{1}'.format(sheetName, row_counter),
                'values': [[player_str, u"=HYPERLINK(\"wowhead.com/item={0}\",\"{1}\")".format(item.item_id, item.name),
                            award.reason, award.award_date.strftime('%m/%d/%Y'),
                            replace1_str,
                            replace2_str
                            ]]
            })
            row_counter += 1
        body = {
            'valueInputOption':'USER_ENTERED',
            'data':data
        }
        backoff = 2
        while backoff < 256:
            try:
                response = self.__service.spreadsheets().values().batchUpdate(spreadsheetId=self.ss_id,
                                                                            body=body).execute()
                break
            except HttpError as h:
                time.sleep(backoff)
                print("Backoff {0}".format(backoff))
                backoff = backoff * backoff
                if backoff >= 256:
                    raise h
        border_request = []
        border_request.append(self.__get__cell_borders_request(sheetId=sheetID,start_row_index=1,
                                                                end_row_index=row_counter-1))
        body = {
            "requests":border_request
        }
        backoff = 2
        while backoff < 256:
            try:
                response = self.__service.spreadsheets().batchUpdate(spreadsheetId=self.ss_id,
                                                                            body=body).execute()
                break
            except HttpError as h:
                time.sleep(backoff)
                print("Backoff {0}".format(backoff))
                backoff = backoff * backoff
                if backoff >= 256:
                    raise h
        return sheetID


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

