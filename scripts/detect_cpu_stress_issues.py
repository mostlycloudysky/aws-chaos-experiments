import os
import boto3
import requests
from datetime import datetime, timedelta


def detect_cpu_stress():
    print("Checking CPU stress issues...")
    ec2 = boto3.client("ec2", region_name=os.environ["AWS_REGION"])
    cloud_watch = boto3.client("cloudwatch", region_name=os.environ["AWS_REGION"])

    instance_ids = []
    reservations = ec2.describe_instances()
    for reseveration in reservations["Reservations"]:
        for instance in reseveration["Instances"]:
            instance_ids.append(instance["InstanceId"])

    stressed_instances = []
    for instance_id in instance_ids:
        response = cloud_watch.get_metric_statistics(
            Namespace="AWS/EC2",
            MetricName="CPUUtilization",
            Dimensions=[{"Name": "InstanceId", "Value": instance_id}],
            StartTime=datetime.now() - timedelta(minutes=5),
            EndTime=datetime.now(),
            Period=60,
            Statistics=["Average"],
        )

        if any(dp["Average"] > 80 for dp in response.get("Datapoints", [])):
            stressed_instances.append(instance_id)

        if not stressed_instances:
            print("No CPU stress issues detected.")
            return

        for instance_id in stressed_instances:
            create_github_issue(instance_id)


def create_github_issue(instance_id):
    repo = os.getenv("GITHUB_REPO")
    token = os.getenv("GITHUB_TOKEN")
    url = f"https://api.github.com/repos/{repo}/issues"
    headers = {"Authorization": f"token {token}"}
    issue_title = f"EC2 Instance {instance_id} CPU Stress Detected"
    issue_body = f"The EC2 instance {instance_id} experienced high CPU utilization in the past 15 minutes. Remediation action is required."
    issue = {"title": issue_title, "body": issue_body}
    response = requests.post(url, headers=headers, json=issue)
    if response.status_code == 201:
        print(f"GitHub issue created for instance {instance_id}")
    else:
        print(
            f"Failed to create GitHub issue for instance {instance_id}: {response.text}"
        )


if __name__ == "__main__":
    detect_cpu_stress()
