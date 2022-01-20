from email import policy
from ibm_platform_services import IamPolicyManagementV1
from ibm_platform_services.iam_policy_management_v1 import PolicySubject, SubjectAttribute, PolicyRole, ResourceAttribute, ResourceTag, PolicyResource
import json


class AccessPolicy:
    def __init__(self, authenticator, ibm_service_url: str = None,  **kwargs) -> None:
        self.iamPolicyManager = IamPolicyManagementV1(authenticator=authenticator)
        if (ibm_service_url):
            self.iamPolicyManager.set_service_url(ibm_service_url)
        self.policies = {
        "containers-kubernetes": {"name": "serviceName", "roles" : [PolicyRole(role_id='crn:v1:bluemix:public:iam::::role:Administrator'), PolicyRole(role_id='crn:v1:bluemix:public:iam::::serviceRole:Manager')]},
        "service": {"name": "serviceType","roles" : [PolicyRole(role_id='crn:v1:bluemix:public:iam::::role:Administrator'), PolicyRole(role_id='crn:v1:bluemix:public:iam::::serviceRole:Manager')]},
        "is": {"name": "serviceName", "roles" : [PolicyRole(role_id='crn:v1:bluemix:public:iam::::role:Administrator'), PolicyRole(role_id='crn:v1:bluemix:public:is::::serviceRole:VirtualServerConsoleAdmin')]},
        "platform_service": {"name": "serviceType",  "roles": [PolicyRole(role_id='crn:v1:bluemix:public:iam::::role:Administrator')]}
    }

    def create_policies_for_access_group(self, access_group_id: str, account_id: str):
        for key, item in self.policies.items():
            self.create_a_policy_for_access_group(access_group_id, account_id, item["name"], key, item["roles"])
        

    def create_a_policy_for_access_group(self, access_group_id: str, account_id: str, name: str, value: str, roles: list):
        policy_subjects = PolicySubject(attributes=[SubjectAttribute(name='access_group_id', value=access_group_id)])
        account_id_resource_attribute = ResourceAttribute(name='accountId', value=account_id)
        service_name_resource_attribute = ResourceAttribute(name=name, value=value)
        policy_resources = PolicyResource(attributes=[account_id_resource_attribute, service_name_resource_attribute])
        policy = self.iamPolicyManager.create_policy(type='access',subjects=[policy_subjects],roles=roles,resources=[policy_resources]
        ).get_result()
        print(json.dumps(policy, indent=2))

    def get_policies(self, access_group_id: str, account_id: str):
        policy_list = self.iamPolicyManager.list_policies( account_id=account_id, access_group_id=access_group_id).get_result()
        return policy_list