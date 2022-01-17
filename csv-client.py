from calendar import c
from email.policy import Policy
import requests
import pandas as pd
import io
import os
import json
from accessGroupService import AccessGroup
from accessPolicyService import AccessPolicy
from authenticateService import Authenticate
from csvService import Csv
from dotenv import dotenv_values
from ibm_platform_services import IamAccessGroupsV2, UserManagementV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from userService import User

config = dotenv_values(".env")

if __name__ == '__main__':

  # # instantiate an authenticator, accessgroup
  authenticator = Authenticate(ibm_cloud_iam_api_key=config['IBM_CLOUD_IAM_API_KEY']).get_authenticator()
  user = User(authenticator=authenticator, account_id=config["IBM_CLOUD_ACCOUNT_ID"])
  ag = AccessGroup(authenticator=authenticator, account_id=config["IBM_CLOUD_ACCOUNT_ID"])
  ap = AccessPolicy(authenticator=authenticator)
  # create an access group
  ag_id = ag.create_a_access_group("test", "this is a test group")['id']
  # Create a policy
  ap.create_a_policy_for_access_group(ag_id, config["IBM_CLOUD_ACCOUNT_ID"])








  #  add user to access group
  csv = Csv(config['PAO'], config['REQUEST_TYPE'], config['URL'])
  users_df = csv.getClientExcel()
  print(json.dumps(user.invite_users_to_cloud(users_df=users_df, access_group_id=ag_id), indent=2))

  # delete a user, successful response returns null
  # print(json.dumps(user.removeUser("2e75093df3ef4f8588ce4119ca7fe578"), indent=2))
  




