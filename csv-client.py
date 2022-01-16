import requests
import pandas as pd
import io
import os
import json
from authenticateService import Authenticate
from dotenv import dotenv_values
from ibm_platform_services import IamAccessGroupsV2, UserManagementV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

config = dotenv_values(".env")

ROLE_ID = {'Viewer': 'crn:v1:bluemix:public:iam::::role:Viewer',
  'Administrator': 'crn:v1:bluemix:public:iam::::role:Administrator',
  'Operator': 'crn:v1:bluemix:public:iam::::role:Operator',
  'Editor': 'crn:v1:bluemix:public:iam::::role:Editor'}

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
  # print (data_xls.head())
  return data_xls

# get an instance of IAMAuthenticator
def authenticate() -> IAMAuthenticator:
  # Create an IAM authenticator.
  authenticator = IAMAuthenticator(config["IBM_CLOUD_IAM_API_KEY"])
  # Construct the service client.
  iamAccessGroupV2 = IamAccessGroupsV2(authenticator=authenticator)
  # Set our custom service URL (optional)
  iamAccessGroupV2.set_service_url('https://iam.cloud.ibm.com')
  return iamAccessGroupV2


def get_userManager() -> UserManagementV1:
  authenticator = IAMAuthenticator(config["IBM_CLOUD_IAM_API_KEY"])
  # Construct the service client.
  userManager = UserManagementV1(authenticator=authenticator)
  # Set our custom service URL (optional)
  userManager.set_service_url(config["IBM_SERVICE_URL"])
  return userManager

def invite_one_user(email, role, account_id, user_management_admin_service, access_group_id):
  invite_user_model = {
  'email': email,
  'account_role': role
  }

  role_model = {'role_id': ROLE_ID[role]}

  attribute_model = {'name': 'accountId', 'value': account_id}
  attribute_model2 = {'name': 'resourceGroupId', 'value': '*'}

  resource_model = {'attributes': [attribute_model, attribute_model2]}

  invite_user_iam_policy_model = {
    'type': 'access',
    'roles': [role_model],
    'resources': [resource_model]
  }

  invite_user_response = user_management_admin_service.invite_users(
    account_id=account_id,
    users=[invite_user_model],
    iam_policy=[invite_user_iam_policy_model],
    access_groups=[access_group_id]
  ).get_result()

  return json.dumps(invite_user_response, indent=2)


def invite_multiple_users(users_df, account_id, access_group_id):
  user_model = lambda email, role: {'email':email, 'account_role': role}
  users = [user_model(e,r) for e, r in zip(users_df['email'], users_df['role'])]
  iam_policies = [iam_policy_model(role) for role in users_df['role']]

  access_group_ids = [access_group_id for _ in users_df['email']] 

  user_management_admin_service = get_userManager()

  invite_user_response = user_management_admin_service.invite_users(
  account_id=account_id,
  users=users,
  iam_policy=iam_policies,
  access_groups=access_group_ids
  ).get_result()

  print(json.dumps(invite_user_response, indent=2))


def iam_policy_model(role):
  role_model = {'role_id': ROLE_ID[role]}
  attribute_model = {'name': 'accountId', 'value': account_id}
  attribute_model2 = {'name': 'resourceGroupId', 'value': '*'}
  resource_model = {'attributes': [attribute_model, attribute_model2]}
  invite_user_iam_policy_model = {
    'type': 'access',
    'roles': [role_model],
    'resources': [resource_model]
  }
  return invite_user_iam_policy_model


def invite_users_to_cloud(users_df, account_id, access_group_id):
  users2add_df = users_df[users_df['action'] == 'add']
  
  # ==================================
  # WARNING: This doen't work, getting error 500
  # invite_multiple_users(users2add_df, account_id, access_group_id)
  # ==================================

  # Invite users one by one
  user_management_admin_service = get_userManager()
  responses = [invite_one_user(email, role, account_id, user_management_admin_service, access_group_id)
                for email, role in zip(users2add_df['email'], users2add_df['role'])]
  [print(r) for r in responses]


if __name__ == '__main__':
  
  # response_dict = create_a_access_group(iam_access_group_service, config["IBM_CLOUD_ACCOUNT_ID"], 'policy_test_group', "This is a group for testing policies")

  users_df = getClientExcel()
  account_id = config["IBM_CLOUD_ACCOUNT_ID"]
  access_group_id = 'AccessGroupId-580954bc-0d22-4ed5-8983-bc4c7a34a0b5'
  invite_users_to_cloud(users_df, account_id, access_group_id)




