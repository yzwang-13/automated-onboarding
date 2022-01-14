import requests
import pandas as pd
import io
import os
import json
from authenticateService import Authenticate
from dotenv import dotenv_values

config = dotenv_values(".env")

# make request to github enterprise repo to fetch client onboarding list
def getClientExcel():
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

  # Todo:
  # Call invite users here according to the user email data here


if __name__ == '__main__':

  Authenticate()
  # print(json.dumps(get_a_access_group(iam_access_group_service, "AccessGroupId-PublicAccess"), indent=2))
  # print(json.dumps(get_all_access_groups(iam_access_group_service, config["IBM_CLOUD_ACCOUNT_ID"]), indent=2))
  # print(json.dumps(create_a_access_group(iam_access_group_service, config["IBM_CLOUD_ACCOUNT_ID"], 'clients_access_group', "This is a access group for our clients"), indent=2))
  
  response_dict = create_a_access_group(iam_access_group_service, config["IBM_CLOUD_ACCOUNT_ID"], 'policy_test_group', "This is a group for testing policies")
  # print(response_dict['id'])

  # print(delete_a_access_group(iam_access_group_service, "AccessGroupId-55aa1eb5-1a81-4da7-b6b8-15cecc898d29"))

  # print(json.dumps(get_policies(get_iamPolicyManager_instance(), "AccessGroupId-580954bc-0d22-4ed5-8983-bc4c7a34a0b5"), indent=2))

  # print(create_a_policy_for_access_group(get_iamPolicyManager_instance()))




