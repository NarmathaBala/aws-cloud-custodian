import boto3
from boto3.session import Session
import re
import sys
import wget
import os
import yaml
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

# TODO: pass the properties file as ARGV at runtime?
#### Parse YAML
properties_file = 'config.yml'

with open(properties_file, 'r') as ymlfile:
    cfg = yaml.load(ymlfile)
mugc_script_url = cfg['mugc_script']
masterArn = cfg['master_account_arn']

nonprod_compliance_policies_dir = cfg['nonprod']['compliance_policies_dir']
nonprod_opertional_policies_dir = cfg['nonprod']['opertional_policies_dir']
prod_compliance_policies_dir = cfg['prod']['compliance_policies_dir']
prod_opertional_policies_dir = cfg['prod']['opertional_policies_dir']

mugc_script = wget.download(mugc_script_url)
#####

def policies_list():
    policiesArray = []
    try:
        files = [nonprod_compliance_policies_dir + '/' + 'global', nonprod_compliance_policies_dir + '/' + 'regional', nonprod_opertional_policies_dir + '/' + 'global', nonprod_opertional_policies_dir + '/' + 'regional', prod_compliance_policies_dir + '/' + 'global', prod_compliance_policies_dir + '/' + 'regional', prod_opertional_policies_dir + '/' + 'regional', prod_opertional_policies_dir + '/' + 'global']
        for i in files:
            for file in os.listdir(i):
                if file.endswith(".yml"):
                    updatedName = '-c ' + i + '/' + file
                    policiesArray.append(updatedName)
    except:
        print("no global policies exists..")
        pass
    return policiesArray

def main(arn, session_name):
    """aws sts assume-role --role-arn arn:aws:iam::00000000000000:role/example-role --role-session-name example-role"""
    client = boto3.client('sts')
    account_id = client.get_caller_identity()["Account"]
    response = client.assume_role(RoleArn=arn, RoleSessionName=session_name)
    session = Session(aws_access_key_id=response['Credentials']['AccessKeyId'],
                      aws_secret_access_key=response['Credentials']['SecretAccessKey'],
                      aws_session_token=response['Credentials']['SessionToken'])

    # switch to slave                  
    client = session.client('sts')
    account_id = client.get_caller_identity()["Account"]

    # TODO: do we need to make it loop over or accounts?
    slaveResponse = client.assume_role(RoleArn='arn:aws:iam::XXXXXXXXXXXXXX:role/SlaveCentralAdmin', RoleSessionName='SlaveCentralAdmin')
    slaveSession = Session(aws_access_key_id=slaveResponse['Credentials']['AccessKeyId'],
                    aws_secret_access_key=slaveResponse['Credentials']['SecretAccessKey'],
                    aws_session_token=slaveResponse['Credentials']['SessionToken'])

    os.environ["AWS_ACCESS_KEY_ID"] = slaveResponse['Credentials']['AccessKeyId']
    os.environ["AWS_SECRET_ACCESS_KEY"] = slaveResponse['Credentials']['SecretAccessKey']
    os.environ["AWS_SESSION_TOKEN"] = slaveResponse['Credentials']['SessionToken'] 
    
    print ("slave account: ", account_id)
    client = slaveSession.client('ec2')
    regions = [region['RegionName'] for region in client.describe_regions()['Regions']]
    print("starting cleanup...")
    listOfPolicies =  ' '.join(policies_list())
    for region in regions:
        print("python mugc.py -r %s -c %s" %(region, listOfPolicies))
        os.system("python mugc.py -r %s -c %s" %(region, listOfPolicies))


sessionName = 'master_session'
main(masterArn, sessionName)