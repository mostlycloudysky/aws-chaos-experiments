import os
import boto3
import re


def start_instance(instance_id):
    ec2 = boto3.client("ec2", region_name=os.getenv("AWS_REGION"))
    response = ec2.start_instances(InstanceIds=[instance_id])
    print(f"Starting instance {instance_id}: {response}")


def parse_issue_body(issue_body):
    # Use regex to extract instance ID from the issue body
    match = re.search(r"EC2 instance (\bi-\w+\b)", issue_body)
    if match:
        return match.group(1)
    else:
        raise ValueError("Instance ID not found in issue body...")


def remediate():
    issue_body = os.getenv("ISSUE_BODY")
    try:
        instance_id = parse_issue_body(issue_body)
        print(f"Instance ID to remediate: {instance_id}")
        start_instance(instance_id)
    except Exception as e:
        print(f"Error during remediation: {e}")


if __name__ == "__main__":
    remediate()
