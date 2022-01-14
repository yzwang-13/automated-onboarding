import requests
import pandas as pd
import io
import os
import json
from dotenv import dotenv_values
from ibm_platform_services import IamAccessGroupsV2
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

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


# get all access group based on account id
def get_all_access_groups(iam_access_group_service: IamAccessGroupsV2, account_id: str):
  groups_list = iam_access_group_service.list_access_groups(
    account_id
  ).get_result()
  return groups_list

# get all one group based on access group id
def get_a_access_group(iam_access_group_service: IamAccessGroupsV2, access_group_id: str):
  return iam_access_group_service.get_access_group(access_group_id).get_result()

# create a access group 
def create_a_access_group(iam_access_group_service: IamAccessGroupsV2, account_id: str, group_name: str, group_description: str):
  group = iam_access_group_service.create_access_group(
  account_id,
  name = group_name,
  description = group_description
  ).get_result()

  return group

# delete a access group based on access group id
def delete_a_access_group(iam_access_group_service: IamAccessGroupsV2, access_group_id: str):
  response = iam_access_group_service.delete_access_group(
  access_group_id
  )
  return response

# get an instance of IAMAuthenticator
def authenticate() -> IAMAuthenticator:
  # Create an IAM authenticator.
  authenticator = IAMAuthenticator(config["IBM_CLOUD_IAM_API_KEY"])
  # Construct the service client.
  iamAccessGroupV2 = IamAccessGroupsV2(authenticator=authenticator)
  # Set our custom service URL (optional)
  iamAccessGroupV2.set_service_url('https://iam.cloud.ibm.com')
  return iamAccessGroupV2


if __name__ == '__main__':
  iam_access_group_service = authenticate()

  # print(json.dumps(get_a_access_group(iam_access_group_service, "AccessGroupId-PublicAccess"), indent=2))
  # print(json.dumps(get_all_access_groups(iam_access_group_service, config["IBM_CLOUD_ACCOUNT_ID"]), indent=2))
  # print(json.dumps(create_a_access_group(iam_access_group_service, config["IBM_CLOUD_ACCOUNT_ID"], 'clients_access_group', "This is a access group for our clients"), indent=2))
  
  response_dict = create_a_access_group(iam_access_group_service, config["IBM_CLOUD_ACCOUNT_ID"], 'clients_access_group', "This is a access group for our clients")
  print(response_dict['id'])
  # print(type(response_dict))

  # print(delete_a_access_group(iam_access_group_service, "AccessGroupId-55aa1eb5-1a81-4da7-b6b8-15cecc898d29"))




