#!/usr/bin/env python
#Created Volodymyr Yampolskyi
import boto3
import requests
import os
import datetime
import time

ec2 = boto3.resource('ec2')
client = boto3.client('ec2')
curent_date = datetime.date.today()
subdom = 'abc'
my_aws_id = 'XXXXXXXXXXXX'

#Check state via domain name
for i in subdom:
    hostname = i + '.for-task.pp.ua'
    response = os.system("ping -c 1 " + hostname)
    if response == 0:
        print hostname, 'is up!'
    else:
        print hostname, 'is down!'
        continue
    response = requests.get('http://' + hostname)
    print 'http://', hostname , response



#Get instance id with state "Stopped"
for instance in ec2.instances.all():
    state_code = instance.state
    if state_code['Code'] == 80:
        in_id = [instance.id]
#Create image
        response = client.create_image(InstanceId=instance.id, Name=curent_date.strftime('%Y-%m-%d'))
#Terminate instance
        response = ec2.instances.filter(InstanceIds=in_id).terminate()

#Clean up AMIs older than 7 days
ami_list = client.describe_images(Filters = [{'Name':'owner-id', 'Values' : ['725114873331']}])
for i in range(0, len(ami_list)-1):
    temp_image = ami_list['Images']
    ts=temp_image[i]['CreationDate']

#Not beautiful but work, parsing Date
    s = ts[0:10]
    s = s.split('-')
    creation_date = datetime.date(int(s[0]),int(s[1]),int(s[2]))
    if creation_date < (curent_date - datetime.timedelta(days=7)):
#Deregister image
       response = client.deregister_image(ImageId=temp_image[0]['ImageId'])


#Print finaly output
for instance in ec2.instances.all():
    state = instance.state
    print instance, 'State', state['Name']
