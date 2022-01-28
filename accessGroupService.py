from xmlrpc.client import Boolean
from ibm_platform_services import IamAccessGroupsV2

class AccessGroup:

    def __init__(self, authenticator, account_id, ibm_service_url: str = None, **kwargs) -> None:
        # Construct the service client.
        self.iamAccessGroupV2 = IamAccessGroupsV2(authenticator=authenticator)
        self.account_id = account_id
        # Set our custom service URL (optional)
        if (ibm_service_url):
            self.iamAccessGroupV2.set_service_url(ibm_service_url)
        
    # get all access group based on account id
    def get_all_access_groups(self):
        groups_list = self.iamAccessGroupV2.list_access_groups(self.account_id
        ).get_result()
        return groups_list

    # get all one group based on access group id
    def get_a_access_group(self, access_group_id: str):
        return self.iamAccessGroupV2.get_access_group(access_group_id).get_result()

    # create a access group 
    def create_a_access_group(self, group_name: str, group_description: str):
        group = self.iamAccessGroupV2.create_access_group(
        self.account_id,
        name = group_name,
        description = group_description
        ).get_result()

        return group

    # delete a access group based on access group id
    def delete_a_access_group(self, access_group_id: str, force: Boolean = False):
        response = self.iamAccessGroupV2.delete_access_group(
        access_group_id,
        force=force
        )
        return response

    def get_members(self, access_group_id: str):
        group_members_list = self.iamAccessGroupV2.list_access_group_members(access_group_id=access_group_id).get_result()
        return group_members_list

    def delete_member(self, access_group_id: str, iam_id: str):
        response = self.iamAccessGroupV2.remove_member_from_access_group(
        access_group_id = access_group_id,
        iam_id= iam_id
        )
        return response
