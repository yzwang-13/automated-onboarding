from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from dotenv import dotenv_values

class Authenticate:

    def __init__(self, ibm_cloud_iam_api_key: str) -> None:
        self.ibm_cloud_iam_api_key = ibm_cloud_iam_api_key
    # get an instance of IAMAuthenticator
    def get_authenticator(self) -> IAMAuthenticator:
        authenticator = IAMAuthenticator(self.ibm_cloud_iam_api_key)
        return authenticator