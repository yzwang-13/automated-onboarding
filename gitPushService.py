import base64
from github import Github
from github import InputGitTreeElement
import json
from datetime import datetime

class GitPush:
	def push(self, login_or_token: str, commit_message: str = None):
		commit_message = "test commit from python"
		g = Github(base_url="https://github.ibm.com/api/v3", login_or_token=login_or_token)
		repo = g.get_user().get_repo('holiday-project')
		# A Git reference (git ref) is just a file that contains a Git commit SHA-1 hash. When referring to a Git commit, you can use the Git reference, which is an easy-to-remember name, rather than the hash. 
		master_ref = repo.get_git_ref('heads/master')
		master_sha = master_ref.object.sha
		base_tree = repo.get_git_tree(master_sha)
		element_list = list()
		data = base64.b64encode(open('onboarding_clients_list.xlsx', "rb").read())
		blob = repo.create_git_blob(data.decode("utf-8"), "base64")
		# repo.create_file('onboarding_clients_list.xlsx', "committing files", data, branch="master")
		element = InputGitTreeElement(path='onboarding_clients_list.xlsx', mode='100644', type='blob', sha=blob.sha)
		element_list.append(element)
		tree = repo.create_git_tree(element_list, base_tree)
		parent = repo.get_git_commit(master_sha)
		commit = repo.create_git_commit(datetime.now().strftime("%d/%m/%Y %H:%M:%S"), tree, [parent])
		master_ref.edit(commit.sha)
