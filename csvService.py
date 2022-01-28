from ast import ExceptHandler
from fileinput import filename
import sys
import requests
import pandas as pd

from ExceptionResolver import ExceptionResolver

class Csv:

    def __init__(self, PAO: str, requestType: str, url: str, fileName: str = 'onboarding_clients_list.xlsx') -> None:
        self.PAO = PAO
        self.requestType = requestType
        self.url = url
        self.fileName = fileName
        self.data_xls = None

    # make request to github enterprise repo to fetch client onboarding list
    # and put them into an excel sheet before load into dataframe
    # currently only deal with sheet1 in excel
    def getExcel(self, sheetName):
        headers = {
            'Authorization': 'token {token}'.format(token = self.PAO),
            'Accept': self.requestType
        }
        response = requests.request("GET", self.url, headers=headers)

        # load binary to a new excel file
        newFile = open(self.fileName, "wb")
        newFile.write(response.content)

        # read client list data into pandas

        # data_xls = pd.read_excel(self.fileName, dtype=str, index_col=None, engine='openpyxl')
        data_xls = pd.read_excel(self.fileName, sheetName, dtype=str, index_col=None, engine='openpyxl')
        self.data_xls = data_xls
        return data_xls

    def updateStatusLocalExcel(self, index):
        for key, value in index.items():
            # print(key, value)
            # self.data_xls.at[key, 'status'] = value
            self.data_xls.loc[self.data_xls.email == key, 'status'] = value
        print(self.data_xls)
    
    def createExceptionLocalExcel(self, message, sheetName, columnName):
        print(columnName)
        print(sheetName)
        print(message)
        exception_frame = pd.DataFrame({columnName: {0: message}})
        self.writeDataframeToExcel(data_frame=exception_frame, sheetName=sheetName)


    def writeDataframeToExcel(self, data_frame, sheetName):
        with pd.ExcelWriter(self.fileName, mode='a',if_sheet_exists="replace") as writer:
            print("writing....")
            data_frame.to_excel(writer, sheet_name=sheetName, index=False)



