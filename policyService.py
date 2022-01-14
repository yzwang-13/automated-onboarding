from ibm_platform_services import IamPolicyManagementV1
from ibm_platform_services.iam_policy_management_v1 import PolicySubject, SubjectAttribute, PolicyRole, ResourceAttribute, ResourceTag, PolicyResource

class Policy:

    def __init__(self, authenticator, access_group_id: str, ibm_service_url: str = None,  **kwargs) -> None:
        # Construct the service client.
        self.iamPolicyManager = IamPolicyManagementV1(authenticator=authenticator)
        # Set our custom service URL (optional)
        if (ibm_service_url):
            self.iamPolicyManager.set_service_url(ibm_service_url)

    def create_a_policy_for_access_group(self):
        # access_group_id = "AccessGroupId-580954bc-0d22-4ed5-8983-bc4c7a34a0b5"

        policy_subjects = PolicySubject(attributes=[SubjectAttribute(name='access_group_id', value=self.access_group_id)])
        # policy_roles = PolicyRole(role_id='crn:v1:bluemix:public:iam::::role:Viewer')
        administrator_role = PolicyRole(role_id='crn:v1:bluemix:public:iam::::role:Administrator')
        manager_role = PolicyRole(role_id='crn:v1:bluemix:public:iam::::serviceRole:Manager')

        # policy_roles = iamPolicyManager.PolicyRole(role_id='crn:v1:bluemix:public:iam::::role:Administrator')
        account_id_resource_attribute = ResourceAttribute(name='accountId', value=config["IBM_CLOUD_ACCOUNT_ID"])

        service_name_resource_attribute = ResourceAttribute(name='serviceName', value='containers-kubernetes')

        # policy_resource_tag = ResourceTag(name='project', value='prototype')
        policy_resources = PolicyResource(attributes=[account_id_resource_attribute, service_name_resource_attribute])

        policy = iamPolicyManager.create_policy(type='access',subjects=[policy_subjects],roles=[administrator_role, manager_role],resources=[policy_resources]
        ).get_result()

        print(json.dumps(policy, indent=2))

    def get_policies(iamPolicyManager: IamPolicyManagementV1, access_group_id: str):
        policy_list = iamPolicyManager.list_policies( account_id=config["IBM_CLOUD_ACCOUNT_ID"], access_group_id="AccessGroupId-32cd9ef9-bf1b-40ea-8bd5-5a79189b22e5").get_result()
        return policy_list