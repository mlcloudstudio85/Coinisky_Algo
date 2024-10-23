import requests
import logging
import json, os
import subprocess
import zipfile  
from config import *
from requests.auth import HTTPBasicAuth 


# Logging Configuration
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_pull_request_files_bitbucket(repo_owner, repo_slug, pr_id):  
    try:
        url = f'{Configuration.BITBUCKET_API_URL}/rest/api/latest/projects/{repo_owner}/repos/{repo_slug}/pull-requests/{pr_id}/changes?start=0&limit=5000'
        response = requests.get(url, auth=HTTPBasicAuth(Configuration.BITBUCKET_GENERIC_USERNAME, Configuration.BITBUCKET_GENERIC_PASSWORD),verify=False) 
        response.raise_for_status()  
        return response.json()  
    except Exception as e:
        logger.error("An error occurred while reading PULL request files: " + str(e))  

def get_pull_request_files_github(repo_owner, repo_slug, pr_id, github_auth_token):  
    try:
        url = f'{Configuration.GITHUB_API_URL}/repos/{repo_owner}/{repo_slug}/pulls/{pr_id}/files'
        headers = {'Authorization': f'Bearer {github_auth_token}'} 
        response = requests.get(url, headers=headers,verify=False)  
        response.raise_for_status()  
        return response.json()  
    except Exception as e:
        logger.error("An error occurred while reading PULL request files: " + str(e))  
        raise e

def github_clone_to_local_with_commands(repo_owner, repo_slug, branch_name, local_dir, github_auth_token):  
    try:  
        # Clone the repository using the git clone command  
        url = f'{Configuration.GITHUB_API_URL}/{repo_owner}/{repo_slug}.git'  
        cmd = ['git', 'clone', '-b', branch_name, url, local_dir]  
        env = {'GIT_TERMINAL_PROMPT': '0', 'GIT_ASKPASS': '/bin/echo'}  
        subprocess.check_call(cmd, env=env)  
  
        print(f'Repository {repo_slug} cloned to {local_dir}')  
        return local_dir  
    except Exception as e:  
        print("An error occurred while cloning github repo to local: " + str(e))

def create_github_clone_to_local(repo_owner, repo_slug, branch_name, local_dir, github_auth_token):  
    try:
        url = f'{Configuration.GITHUB_API_URL}/repos/{repo_owner}/{repo_slug}/zipball/{branch_name}'  
        headers = {'Authorization': f'Bearer {github_auth_token}'}  
        response = requests.get(url, headers=headers,verify=False) 
        if not os.path.exists(local_dir):  
            os.makedirs(local_dir)  
            logger.info(f"Directory created at {local_dir}")  

        # Save the ZIP file to the local directory  
        zip_file_path = os.path.join(local_dir, f'{repo_slug}.zip')  
        with open(zip_file_path, 'wb') as f:  
            f.write(response.content) 

         # Extract the ZIP file to a temporary directory  
        temp_dir = os.path.join(local_dir, 'temp')  
        with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:  
            zip_ref.extractall(temp_dir)  
 
        # Move the contents of the first directory to the desired location  
        first_dir = os.listdir(temp_dir)[0]  
        src_dir = os.path.join(temp_dir, first_dir)  
        dst_dir = os.path.join(local_dir, repo_slug)  
        os.rename(src_dir, dst_dir)  

        # Remove the ZIP file  
        os.rmdir(temp_dir)  
        os.remove(zip_file_path)  

        logger.info(f'Repository {repo_slug} cloned to {dst_dir}')    
        return dst_dir 
    except Exception as e:
        logger.error("An error occurred while cloning github repo to local: " + str(e))  

def get_branch_name_bitbucket(repo_owner, repo_slug, pr_id): 
    try:
        url = f'{Configuration.BITBUCKET_API_URL}/rest/api/latest/projects/{repo_owner}/repos/{repo_slug}/pull-requests/{pr_id}'  
        response = requests.get(url, auth=HTTPBasicAuth(Configuration.BITBUCKET_GENERIC_USERNAME, Configuration.BITBUCKET_GENERIC_PASSWORD),verify=False)
        data = json.loads(response.content) 
        # Get the branch name from the pull request data    
        branch_name = data['fromRef']['displayId']    
        # Print the branch name    
        logger.info("BRANCH: " + str(branch_name)) 
        return str(branch_name)
    except Exception as e:
        logger.error(f"An error occurred while reading branch name from Pull Request: " + str(e)) 

def get_branch_name_github(repo_owner, repo_slug, pr_id, github_auth_token) :  
    try:  
        url = f'{Configuration.GITHUB_API_URL}/repos/{repo_owner}/{repo_slug}/pulls/{pr_id}'  
        headers = {'Authorization': f'Bearer {github_auth_token}'}  
        response = requests.get(url, headers=headers,verify=False)  
        data = json.loads(response.content)  
        # Get the branch name from the pull request data  
        branch_name = data['head']['ref']  
        # Print the branch name  
        logger.info("Referring Branch: " + str(branch_name))  
        return str(branch_name)  
    except Exception as e:  
        logger.error(f"An error occurred while reading branch name from Pull Request: " + str(e)) 
        raise e

def create_pull_request_github(repo_owner, repo_slug, base_branch_name, pr_title, pr_body, github_auth_token):  
    try:
        url = f'{Configuration.GITHUB_API_URL}/repos/{repo_owner}/{repo_slug}/pulls'

        headers = {'Authorization': f'Bearer {github_auth_token}', 
        'Accept': 'application/vnd.github.v3+json'} 
        # Define the request body  
        data = {  
                'title': pr_title,  
                'body': pr_body,  
                'head': base_branch_name,  
                'base': base_branch_name  
                }  

        # Send the POST request to create the pull request  
        response = requests.post(url, headers=headers, data=json.dumps(data),verify=False) 
        # Print the response status code and content  
        logger.info("PR request handled with status code: " + response.status_code)  
        logger.info("PR request created with content: " + response.content) 
        return response.json()  
    except Exception as e:
        logger.error("An error occurred while creating new PR : " + str(e)) 
        raise e

def create_commit_github(repo_owner, repo_slug, commit_message, file_path, commit_content, pr_id, github_auth_token):  
    try:
        url = f'{Configuration.GITHUB_API_URL}/repos/{repo_owner}/{repo_slug}/pulls/{pr_id}/commits'

        headers = {'Authorization': f'Bearer {github_auth_token}', 
        'Accept': 'application/vnd.github.v3+json'} 
        # Define the request body  
        data = {  
                'message': commit_message,  
                'content': commit_content  
                }  
                
        testcases_file = split_string(split_string(file_path,'/')[1], '.')[0] + "Test." +split_string(split_string(file_path,'/')[1], '.')[1] 
        final_file_path = split_string(file_path,'/')[0] +  testcases_file
        file = {'file': open(final_file_path, 'rb')}  

        # Send the POST request to create the new commit  
        response = requests.post(url, headers=headers, data=json.dumps(data), files=file,verify=False) 
        # Print the response status code and content  
        logger.info("New Commit request handled with status code: " + response.status_code)  
        logger.info("New Commit created with info: " + response.content) 
    except Exception as e:
        logger.error("An error occurred while creating new commit : " + str(e)) 
        raise e

def list_all_files_github(repo_owner, repo_slug, head_branch_name, github_auth_token):
    try:
        # Set the API endpoint and repository name  
        url = f'{Configuration.GITHUB_API_URL}/repos/{repo_owner}/{repo_slug}/git/trees/{head_branch_name}?recursive=1'  
        headers = {'Authorization': f'Bearer {github_auth_token}', 
            'Accept': 'application/vnd.github.v3+json'} 
    
        # Send a GET request to the API endpoint  
        response = requests.get(url, headers=headers,verify=False) 
    
        # Check if the request was successful  
        if response.status_code == 200:  
            # Parse the response JSON and get the list of files  
            files = response.json()["tree"]  
        else:  
            logger.error(f"Error getting files from Github: {response.text}")
        return files
    except Exception as e:
        logger.error()
# Function to read a file and handle exceptions
def read_file(file_name):
    try:
        with open(file_name, "r") as file:
            data = file.read()
            if data:
                logger.info(f"Successfully read file: {file_name}")
                return data
            else:
                logger.warning(f"File is empty: {file_name}")
                return None
    except FileNotFoundError:
        logger.error(f"File '{file_name}' not found")

def is_not_empty_string(s):  
    """  
    Returns True if the given string is not empty, False otherwise.  
    """  
    return isinstance(s, str) and bool(s.strip())  

def split_string(s, delimiter):  
    """  
    Splits the given string into two strings based on the last occurrence of the given delimiter.  
    Returns a tuple containing the two resulting strings.  
    """  
    index = s.rfind(delimiter)  
    if index == -1:  
        return s, ""  
    else:  
        return s[:index], s[index+1:]