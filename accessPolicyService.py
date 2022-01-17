from ibm_platform_services import IamPolicyManagementV1
from ibm_platform_services.iam_policy_management_v1 import PolicySubject, SubjectAttribute, PolicyRole, ResourceAttribute, ResourceTag, PolicyResource
import json


class AccessPolicy:

    def __init__(self, authenticator, ibm_service_url: str = None,  **kwargs) -> None:
        # Construct the service client.
        self.iamPolicyManager = IamPolicyManagementV1(authenticator=authenticator)
        # Set our custom service URL (optional)
        if (ibm_service_url):
            self.iamPolicyManager.set_service_url(ibm_service_url)

    def create_a_policy_for_access_group(self, access_group_id: str, account_id: str):
        policy_subjects = PolicySubject(attributes=[SubjectAttribute(name='access_group_id', value=access_group_id)])
        # policy_roles = PolicyRole(role_id='crn:v1:bluemix:public:iam::::role:Viewer')
        administrator_role = PolicyRole(role_id='crn:v1:bluemix:public:iam::::role:Administrator')
        manager_role = PolicyRole(role_id='crn:v1:bluemix:public:iam::::serviceRole:Manager')

        # policy_roles = iamPolicyManager.PolicyRole(role_id='crn:v1:bluemix:public:iam::::role:Administrator')
        account_id_resource_attribute = ResourceAttribute(name='accountId', value=account_id)

        service_name_resource_attribute = ResourceAttribute(name='serviceName', value='containers-kubernetes')

        # policy_resource_tag = ResourceTag(name='project', value='prototype')
        policy_resources = PolicyResource(attributes=[account_id_resource_attribute, service_name_resource_attribute])

        policy = self.iamPolicyManager.create_policy(type='access',subjects=[policy_subjects],roles=[administrator_role, manager_role],resources=[policy_resources]
        ).get_result()

        print(json.dumps(policy, indent=2))

    def get_policies(iamPolicyManager: IamPolicyManagementV1, access_group_id: str, account_id: str):
        policy_list = iamPolicyManager.list_policies( account_id=account_id, access_group_id=access_group_id).get_result()
        return policy_list