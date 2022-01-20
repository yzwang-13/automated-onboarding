import json
from accessGroupService import AccessGroup
from accessPolicyService import AccessPolicy
from authenticateService import Authenticate
from csvService import Csv
from dotenv import dotenv_values
from gitPushService import GitPush
from userService import User
import time

config = dotenv_values(".env")

if __name__ == '__main__':
  # # instantiate an authenticator, accessgroup
  authenticator = Authenticate(ibm_cloud_iam_api_key=config['IBM_CLOUD_IAM_API_KEY']).get_authenticator()
  user = User(authenticator=authenticator, account_id=config["IBM_CLOUD_ACCOUNT_ID"])
  ag = AccessGroup(authenticator=authenticator, account_id=config["IBM_CLOUD_ACCOUNT_ID"])
  ap = AccessPolicy(authenticator=authenticator)
  gp = GitPush()

  # # # create an access group
  ag_id = ag.create_a_access_group(config["ACCESS_GROUP_NAME"], "Group for development team automated onboarding")['id']
  # # Create policies for access group
  ap.create_policies_for_access_group(ag_id, config["IBM_CLOUD_ACCOUNT_ID"])

  # print(json.dumps(ap.get_policies(access_group_id="AccessGroupId-32cd9ef9-bf1b-40ea-8bd5-5a79189b22e5", account_id=config["IBM_CLOUD_ACCOUNT_ID"]), indent=2))

  # debug_requests_on()


  # #  add user to access group and send invitation email
  csv = Csv(config['PAO'], config['REQUEST_TYPE'], config['URL'])
  users_df = csv.getClientExcel("Sheet1")
  print(json.dumps(user.invite_users_to_cloud(users_df=users_df, access_group_id=ag_id), indent=2))
  # update local excel file



  # get currrent state of all users from cloud account
  # and update to the local xlsx file
  time.sleep(5)
  for u in user.get_users()["resources"]:
    if u["email"] in user.status.keys():
      user.status[u["email"]] = u["state"]
  csv.updateStatusLocalExcel(user.status)
  csv.writeDataframeToExcel("Sheet1")


  # update excel and push to github
  # gp.push()
  gp.push(login_or_token=config["PAO"])

  # delete a user, successful response returns null
  # print(json.dumps(user.remove_user("2e75093df3ef4f8588ce4119ca7fe578"), indent=2))

  # print(ag.delete_a_access_group(ag_id, force=True))
  




