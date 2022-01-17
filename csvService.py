import requests
import pandas as pd

class Csv:

    def __init__(self, PAO: str, requestType: str, url: str) -> None:
        self.PAO = PAO
        self.requestType = requestType
        self.url = url

    # make request to github enterprise repo to fetch client onboarding list
    # and put them into an excel sheet before load into dataframe
    # currently only deal with sheet1 in excel
    def getClientExcel(self):
        headers = {
            'Authorization': 'token {token}'.format(token = self.PAO),
            'Accept': self.requestType
        }
        response = requests.request("GET", self.url, headers=headers)

        # load binary to a new excel file
        newFile = open("onboarding_clients_list.xlsx", "wb")
        newFile.write(response.content)

        # read client list data into pandas
        data_xls = pd.read_excel('onboarding_clients_list.xlsx', 'Sheet1', dtype=str, index_col=None, engine='openpyxl')
        # print (data_xls.head())
        self.data_xls = data_xls
        return data_xls