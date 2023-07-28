import boto3
import paramiko
import time

# AWS credentials and EC2 instance configuration
aws_access_key_id = 'YOUR_AWS_ACCESS_KEY'
aws_secret_access_key = 'YOUR_AWS_SECRET_KEY'
region_name = 'us-west-2'
key_pair_name = 'your_key_pair_name'
security_group_name = 'your_security_group_name'
instance_type = 't2.micro'
ami_id = 'your_ami_id'
flask_app_local_path = '/path/to/your/flask_app'
flask_app_remote_path = '/home/ec2-user/flask_app'

# Initialize Boto3 clients
ec2 = boto3.client('ec2', region_name=region_name)
ec2_resource = boto3.resource('ec2', region_name=region_name)
ec2_ssh = paramiko.SSHClient()
ec2_ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

# Create a new EC2 instance
response = ec2.run_instances(
    ImageId=ami_id,
    InstanceType=instance_type,
    MinCount=1,
    MaxCount=1,
    KeyName=key_pair_name,
    SecurityGroups=[security_group_name],
    UserData=f'''#!/bin/bash
                yum update -y
                yum install python3 -y
                yum install python3-pip -y
                pip3 install gunicorn
                mkdir -p {flask_app_remote_path}
                '''
)

instance_id = response['Instances'][0]['InstanceId']
print(f"EC2 instance with ID {instance_id} is being created. Waiting for it to be running...")

# Wait for the instance to be running
waiter = ec2.get_waiter('instance_running')
waiter.wait(InstanceIds=[instance_id])

# Get the public IP address of the instance
instance = ec2_resource.Instance(instance_id)
public_ip = instance.public_ip_address

# Upload the Flask application to the instance using SCP
ssh_key_path = '/path/to/your/key.pem'
ssh_username = 'ec2-user'
ssh_client = paramiko.SSHClient()
ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh_client.connect(public_ip, username=ssh_username, key_filename=ssh_key_path)

scp_client = ssh_client.open_sftp()
scp_client.put(flask_app_local_path, f"{flask_app_remote_path}/app.py")
scp_client.close()
ssh_client.close()

print("Flask application uploaded to the EC2 instance.")

# SSH into the instance and deploy the Flask app with Gunicorn
ssh_client = paramiko.SSHClient()
ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh_client.connect(public_ip, username=ssh_username, key_filename=ssh_key_path)

# Install required Python packages using pip
stdin, stdout, stderr = ssh_client.exec_command(f"cd {flask_app_remote_path} && pip3 install -r requirements.txt")
print(stdout.read().decode('utf-8'))
print(stderr.read().decode('utf-8'))

# Start the Flask app using Gunicorn
stdin, stdout, stderr = ssh_client.exec_command(f"cd {flask_app_remote_path} && gunicorn app:app -b 0.0.0.0:8000 &")
print("Flask application is now running on port 8000.")

# Close the SSH connection
ssh_client.close()
