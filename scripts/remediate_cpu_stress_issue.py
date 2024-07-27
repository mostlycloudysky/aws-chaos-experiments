import os
import boto3
import requests
import re


def parse_body(issue_body):
    match = re.search(r"EC2 instance (\bi-\w+\b)", issue_body)
    if match:
        return match.group(1)
    else:
        raise ValueError("Instance ID not found in issue body")


def reopen_issue():
    repo = os.getenv("GITHUB_REPO")
    issue_number = os.getenv("GITHUB_ISSUE_NUMBER")
    token = os.getenv("GITHUB_TOKEN")
    url = f"https://api.github.com/repos/{repo}/issues/{issue_number}"
    headers = {"Authorization": f"token {token}"}
    data = {"state": "open"}

    response = requests.patch(url, headers=headers, json=data)
    if response.status_code == 200:
        print(f"Issue #{issue_number} reopened successfully.")
    else:
        print(f"Failed to reopen issue #{issue_number}: {response.text}")


def remediate_cpu_stress_issue():
    issue_body = os.getenv("ISSUE_BODY")
    try:
        instance_id = parse_body(issue_body)
        print(f"Instance ID to remediate {instance_id}")

        # Run the SSM document on that

    except Exception as e:
        print(f"Error during remediation {e}")
        reopen_issue()


if __name__ == "__main__":
    remediate_cpu_stress_issue()
