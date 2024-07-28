# AWS-CHAOS-EXPERIMENTS

This repository demonstrates chaos engineering practices using AWS Fault Injection Simulator (FIS), Systems Manager and GitHub Actions Workflow. It includes scenarios for CPU stress, network latency, and stopping EC2 instances. The workflows automate detection and remediation of issues using AWS Systems Manager (SSM).

## Prerequisites

- An EC2 instance running Windows with the `SSM agent` installed and configured.
- AWS CLI configured with appropriate permissions.
- CloudWatch Alarms set up for CPUUtilization, NetworkIn, and NetworkOut.

## Setup

1. AWS IAM Roles and Policies
Ensure the following IAM roles and policies are set up:

   - IAM Role for FIS: Attach the AWS managed policy AWSFISServiceRolePolicy to this role.
   - IAM Role for SSM: Attach the AWS managed policy AmazonSSMFullAccess to this role.
  
2. CloudWatch Alarms
Create CloudWatch Alarms for monitoring `CPUUtilization`, `NetworkIn`, and `NetworkOut`.

```sh
aws cloudwatch put-metric-alarm --alarm-name CPUUtilizationAlarm --alarm-description "Alarm when CPU exceeds 80%" --metric-name CPUUtilization --namespace AWS/EC2 --statistic Average --period 60 --threshold 80 --comparison-operator GreaterThanOrEqualToThreshold --dimensions Name=InstanceId,Value=<YourInstanceId> --evaluation-periods 1 --alarm-actions <YourSNSTopicARN>

aws cloudwatch put-metric-alarm --alarm-name NetworkInAlarm --alarm-description "Alarm when NetworkIn is below 1000 bytes for 1 data point within 1 minute" --metric-name NetworkIn --namespace AWS/EC2 --statistic Average --period 60 --threshold 1000 --comparison-operator LessThanThreshold --dimensions Name=InstanceId,Value=<YourInstanceId> --evaluation-periods 1 --alarm-actions <YourSNSTopicARN>

aws cloudwatch put-metric-alarm --alarm-name NetworkOutAlarm --alarm-description "Alarm when NetworkOut is below 1000 bytes for 1 data point within 1 minute" --metric-name NetworkOut --namespace AWS/EC2 --statistic Average --period 60 --threshold 1000 --comparison-operator LessThanThreshold --dimensions Name=InstanceId,Value=<YourInstanceId> --evaluation-periods 1 --alarm-actions <YourSNSTopicARN>

```

## AWS Fault Injection Simulator (FIS) Experiements

### CPU Stress

Refer the following FIS template to simulate stress on `EC2 Windows Instances`.
 - [Inject CPU Stress](https://github.com/mostlycloudysky/aws-chaos-experiments/blob/master/fis-templates/inject-cpu-stress.json)
 - [Actions workflow to Inject CPU Stress](https://github.com/mostlycloudysky/aws-chaos-experiments/blob/master/.github/workflows/inject-cpu-stress.yml)
 - [Detect CPU Stress Script](https://github.com/mostlycloudysky/aws-chaos-experiments/blob/master/scripts/detect_cpu_stress_issues.py)
 - [Remediate CPU Stress Script](https://github.com/mostlycloudysky/aws-chaos-experiments/blob/master/scripts/remediate_cpu_stress_issue.py)
 - [Actions Workflow Remediate CPU Stress](https://github.com/mostlycloudysky/aws-chaos-experiments/blob/master/.github/workflows/remediate-cpu-stress.yml)
 
