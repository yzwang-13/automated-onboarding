from ibm_platform_services import IamAccessGroupsV2

class AccessGroup:

    def __init__(self, authenticator, ibm_service_url: str = None, **kwargs) -> None:
        # Construct the service client.
        self.iamAccessGroupV2 = IamAccessGroupsV2(authenticator=authenticator)
        # Set our custom service URL (optional)
        if (ibm_service_url):
            self.iamAccessGroupV2.set_service_url(ibm_service_url)
        
    # get all access group based on account id
    def get_all_access_groups(self, account_id: str):
        groups_list = self.iam_access_group_service.list_access_groups(account_id
        ).get_result()
        return groups_list

    # get all one group based on access group id
    def get_a_access_group(self, access_group_id: str):
        return self.iam_access_group_service.get_access_group(access_group_id).get_result()

    # create a access group 
    def create_a_access_group(self, account_id: str, group_name: str, group_description: str):
        group = self.iam_access_group_service.create_access_group(
        account_id,
        name = group_name,
        description = group_description
        ).get_result()

        return group

    # delete a access group based on access group id
    def delete_a_access_group(self, access_group_id: str):
        response = self.iam_access_group_service.delete_access_group(
        access_group_id
        )
        return response
