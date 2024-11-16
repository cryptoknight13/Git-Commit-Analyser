import requests
from urllib.parse import urlparse

def parse_url(url):
    """
    Parses a GitHub commit URL to extract repo_owner, repo_name, and fix_commit_hash.
    
    :param url: The GitHub commit URL.
    :return: A tuple (repo_owner, repo_name, fix_commit_hash).
    """
    try:
        # Parse the URL
        parsed_url = urlparse(url)
        path_parts = parsed_url.path.strip('/').split('/')
        
        # Validate URL structure
        if len(path_parts) < 4 or path_parts[-2] != "commit":
            print("Invalid GitHub commit URL.")
            return None, None, None
        
        repo_owner = path_parts[0]
        repo_name = path_parts[1]
        fix_commit_hash = path_parts[-1]
        
        return repo_owner, repo_name, fix_commit_hash
    except Exception as e:
        print(f"Exception: {e}")
        return None, None, None

def get_previous_commit(repo_owner, repo_name, fix_commit_hash):
    """
    Finds the commit before the specified fix commit using GitHub API.
    
    :param repo_owner: Owner of the repository (e.g., "u-boot").
    :param repo_name: Name of the repository (e.g., "u-boot").
    :param fix_commit_hash: Hash of the fix commit.
    :return: Commit hash before the fix.
    """
    try:
        # GitHub API URL for commits
        url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/commits"
        
        # Fetch the commit history
        params = {"sha": fix_commit_hash}
        response = requests.get(url, params=params)
        
        if response.status_code != 200:
            print(f"Error: Unable to fetch commits. {response.json()}")
            return None
        
        # Parse JSON response
        commits = response.json()
        if len(commits) < 2:
            print("No previous commit found.")
            return None
        
        # Return the second commit in the list (before the fix commit)
        return commits[1]["sha"]
    
    except Exception as e:
        print(f"Exception: {e}")
        return None

# Main function to integrate both parsing and fetching previous commit
def main():
    # Ask user for the URL
    url = input("Enter the commit URL with fix: ").strip()
    
    # Parse the URL
    repo_owner, repo_name, fix_commit = parse_url(url)
    
    if not repo_owner or not repo_name or not fix_commit:
        print("Failed to parse the URL. Exiting.")
        return
    
    # Get the previous commit
    previous_commit = get_previous_commit(repo_owner, repo_name, fix_commit)
    
    if previous_commit:
        print(f"The commit before the fix is: {previous_commit}")
        print(f"Link to the commit: https://github.com/{repo_owner}/{repo_name}/commit/{previous_commit}")

# Run the main function
if __name__ == "__main__":
    main()
