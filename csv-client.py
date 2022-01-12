import requests
import pandas as pd
import io
import os
from dotenv import dotenv_values

config = dotenv_values(".env")


# url = os.getenv(URL)
# token = os,getenv(PAO)
# requestType = os.getenv(REQUEST_TYPE)

# make request to github enterprise repo to fetch client onboarding list
headers = {
  'Authorization': 'token {token}'.format(token = config["PAO"]),
  'Accept': config["REQUEST_TYPE"]
}
response = requests.request("GET", config["URL"], headers=headers)
# print(response.content)

# load binary to a new excel file
newFile = open("onboarding_clients_list.xlsx", "wb")
newFile.write(response.content)

# read client list data into pandas
data_xls = pd.read_excel('onboarding_clients_list.xlsx', 'Sheet1', dtype=str, index_col=None)
print (data_xls.head())




