from ibm_platform_services import UserManagementV1
import json

class User:

    def __init__(self, authenticator, account_id: str, ibm_service_url: str = None, **kwargs) -> None:
        self.userManager = UserManagementV1(authenticator=authenticator)
        if (ibm_service_url):
            self.userManager.set_service_url(ibm_service_url)
    
        self.account_id = account_id

        self.ROLE_ID = {'Viewer': 'crn:v1:bluemix:public:iam::::role:Viewer',
        'Administrator': 'crn:v1:bluemix:public:iam::::role:Administrator',
        'Operator': 'crn:v1:bluemix:public:iam::::role:Operator',
        'Editor': 'crn:v1:bluemix:public:iam::::role:Editor'}

    def invite_users_to_cloud(self,users_df, access_group_id):
        users2add_df = users_df[users_df['action'] == 'add']
        
        # ==================================
        # WARNING: This doen't work, getting error 500
        # invite_multiple_users(users2add_df, account_id, access_group_id)
        # ==================================

        # Invite users one by one
        responses = [self.invite_one_user(email, role, access_group_id)
                        for email, role in zip(users2add_df['email'], users2add_df['role'])]
        [print(r) for r in responses]

    def invite_one_user(self, email, role, access_group_id):
        invite_user_model = {
        'email': email,
        'account_role': role
        }

        role_model = {'role_id': self.ROLE_ID[role]}

        attribute_model = {'name': 'accountId', 'value': self.account_id}
        attribute_model2 = {'name': 'resourceGroupId', 'value': '*'}

        resource_model = {'attributes': [attribute_model, attribute_model2]}

        invite_user_iam_policy_model = {
            'type': 'access',
            'roles': [role_model],
            'resources': [resource_model]
        }

        invite_user_response = self.userManager.invite_users(
            account_id=self.account_id,
            users=[invite_user_model],
            iam_policy=[invite_user_iam_policy_model],
            access_groups=[access_group_id]
        ).get_result()

        return json.dumps(invite_user_response, indent=2)


    def iam_policy_model(self, role):
        role_model = {'role_id': self.ROLE_ID[role]}
        attribute_model = {'name': 'accountId', 'value': self.account_id}
        attribute_model2 = {'name': 'resourceGroupId', 'value': '*'}
        resource_model = {'attributes': [attribute_model, attribute_model2]}
        invite_user_iam_policy_model = {
            'type': 'access',
            'roles': [role_model],
            'resources': [resource_model]
        }
        return invite_user_iam_policy_model


    def invite_multiple_users(self,access_group_id, users_df):
        user_model = lambda email, role: {'email':email, 'account_role': role}
        users = [user_model(e,r) for e, r in zip(users_df['email'], users_df['role'])]
        iam_policies = [self.iam_policy_model(role) for role in users_df['role']]

        access_group_ids = [access_group_id for _ in users_df['email']] 

        invite_user_response = self.userManager.user.invite_users(
        account_id=self.account_id,
        users=users,
        iam_policy=iam_policies,
        access_groups=access_group_ids
        ).get_result()

        print(json.dumps(invite_user_response, indent=2))
    
    def removeUser(self, user_id):
        response = self.userManager.remove_user(account_id=self.account_id,iam_id=user_id).get_result()
        return response

