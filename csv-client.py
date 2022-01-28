from cmath import log
import json
from ExceptionResolver import ExceptionResolver
from accessGroupService import AccessGroup
from accessPolicyService import AccessPolicy
from authenticateService import Authenticate
from csvService import Csv
from dotenv import dotenv_values
from gitPushService import GitPush
from userService import User
import time
import sys
from ibm_cloud_sdk_core.api_exception import ApiException

config = dotenv_values(".env")

def invite_users():
   # no access group found, create one and invite all users.
    try:
      users_df = csv.getExcel("Client")
    except ValueError:
      er.raiseError(csv, "Column name error in this excel sheeet. Please provide right column 'Client'", "Error", "Error")
    else:
      user.invite_users_to_cloud(users_df=users_df, access_group_id=ag_id)


if __name__ == '__main__':
  # # instantiate an authenticator, accessgroup
  authenticator = Authenticate(ibm_cloud_iam_api_key=config['IBM_CLOUD_IAM_API_KEY']).get_authenticator()
  user = User(authenticator=authenticator, account_id=config["IBM_CLOUD_ACCOUNT_ID"])
  ag = AccessGroup(authenticator=authenticator, account_id=config["IBM_CLOUD_ACCOUNT_ID"])
  ap = AccessPolicy(authenticator=authenticator)
  csv = Csv(config['PAO'], config['REQUEST_TYPE'], config['URL'])
  gp = GitPush()
  er = ExceptionResolver()

  # # # create an access group if not exist
  # check if an access group is already there
  ag_groups = ag.get_all_access_groups()

  try:
    ag_group_df = csv.getExcel("AccessGroup")
    try:
      ag_group_to_create_name = ag_group_df["access_group_name"][0]
      ag_group_to_create_description = ag_group_df["description"][0]
      if not ag_group_to_create_description:
        ag_group_to_create_description = "Group"
      try:
        ag_id = ag.create_a_access_group(ag_group_to_create_name, ag_group_to_create_description)['id']
      except ApiException as apiException:
        if apiException.code == 409:
          for group in ag_groups["groups"]:
            if group["name"] == ag_group_to_create_name:
              ag_id = group["id"]
          # get all users from that group, and compare if users are in the excel sheet as well, if they are in group
          # and in excel sheet do nothing, if they are not in excel sheet but in group, remove them, if they are in 
          # excel sheet but not in group, invite them
          try:
            users_df = csv.getExcel("Client")
            users2add_df = users_df[users_df['action'] == 'add']['email']
          except ValueError:
            er.raiseError(csv, "Expect Sheet Name {sheetName} which doesn't exist. You will need to create a sheet named {sheetName}".format(sheetName="Client"),"Error","Error")
          else:
            user_to_remove = []
            existing_group_users_id_list = []
            all_users_id_email_dict = dict()
            existing_group_users = ag.get_members(ag_id)["members"]
            for u in existing_group_users:
              existing_group_users_id_list.append(u["iam_id"])

            all_users = user.get_users()["resources"]
            for u in all_users:
              all_users_id_email_dict[u["iam_id"]] = u["user_id"]
            
            for u_iam in existing_group_users_id_list:
              if all_users_id_email_dict[u_iam] not in users2add_df.values:
                user_to_remove.append(u_iam)
            # delete memeber from the group that is not in excel
            for u in user_to_remove:
              ag.delete_member(ag_id, u)
            # for user in all_users["resources"]:
            #   if user
        else:
          er.raiseError(csv, apiException.message, "Error", "Error")  
      else:
          # new access group created, create new policies
          ap.create_policies_for_access_group(ag_id, config["IBM_CLOUD_ACCOUNT_ID"])
    except KeyError:
      er.raiseError(csv, "Column name error in this excel sheeet. Please provide right column 'access_group_name' and 'description'", "Error", "Error")
  except ValueError:
    er.raiseError(csv, "Expect Sheet Name {sheetName} which doesn't exist. You will need to create a sheet named {sheetName}".format(sheetName="AccessGroup"),"Error","Error")

  invite_users()

  # # get currrent state of all users from cloud account
  # # and update to the local xlsx file
  time.sleep(5)
  for u in user.get_users()["resources"]:
    if u["email"] in user.status.keys():
      user.status[u["email"]] = u["state"]
  csv.updateStatusLocalExcel(user.status)
  csv.writeDataframeToExcel(data_frame=csv.data_xls, sheetName="Client")


  # # update excel and push to github
  # gp.push()
  gp.push(login_or_token=config["PAO"])

  # # delete a user, successful response returns null
  # # print(json.dumps(user.remove_user("2e75093df3ef4f8588ce4119ca7fe578"), indent=2))

  # # print(ag.delete_a_access_group(ag_id, force=True))
  




