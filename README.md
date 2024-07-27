# AWS-CHAOS-EXPERIMENTS


```sh
aws cloudwatch put-metric-alarm \
    --alarm-name NetworkInAlarm \
    --alarm-description "Alarm when NetworkIn is below 1000 bytes" \
    --metric-name NetworkIn \
    --namespace AWS/EC2 \
    --statistic Average \
    --period 300 \
    --threshold 1000 \
    --comparison-operator LessThanThreshold \
    --dimensions Name=InstanceId,Value=i-0470acf2fbe9a1c2f \
    --evaluation-periods 1 \
    --alarm-actions arn:aws:sns:us-east-1:273509275056:actions-sns


```


 
