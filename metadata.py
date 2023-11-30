import time
import requests
from requests.auth import HTTPBasicAuth
import csv
import sys, getopt

# IAM role creation
"""
Example usage:
create_new_iam_role('test_role','123456781234','username','password')
"""
def create_new_iam_role(iam_role_name,iam_role_arn,username,password):
    url_iam_role = 'https://ccs.splunkcloud.com:8089/servicesNS/nobody/Splunk_TA_aws/splunk_ta_aws_iam_roles'
    iam_role_data = {'name':iam_role_name,'arn':iam_role_arn}
    iam_role_request = requests.post(url_iam_role, data = iam_role_data, auth = HTTPBasicAuth(username, password), headers={'Connection':'close'})
    print('')
    print(iam_role_request)
    print('')
    print("New IAM role '" + iam_role_name + "' created")

# IAM role deletion
"""
Example usage:
delete_iam_role('test_role','username','password')
"""
def delete_iam_role(iam_role_name,username,password):
    url_iam_role = 'https://ccs.splunkcloud.com:8089/servicesNS/nobody/Splunk_TA_aws/splunk_ta_aws_iam_roles/' + iam_role_name
    iam_role_request = requests.delete(url_iam_role, auth = HTTPBasicAuth(username, password), headers={'Connection':'close'})
    print('')
    print(iam_role_request)
    print('')
    print("Existing IAM role '" + iam_role_name + "' deleted")

# IAM role bulk creation
"""
Example usage:
create_iam_roles_from_file('filename','username','password')
"""
def create_iam_roles_from_file(iam_role_names_file,username,password):
    with open(iam_role_names_file, newline='') as splunk_input:
        splunk_input_reader = csv.DictReader(splunk_input, delimiter=',')
        input_name = []
        account_id = []
        role_name = []
        role_arn = []
        for row in splunk_input_reader:
            input_name.append(row['Input Name'])
            account_id.append(row['Account ID'])
            role_name.append(row['Role Name'])
            role_arn.append(row['Role ARN'])
        for i in range(len(role_name)):
            create_new_iam_role(role_name[i],role_arn[i],username,password)

# IAM role bulk delete
"""
Example usage:
delete_iam_roles_from_file('filename','username','password')
"""
def delete_iam_roles_from_file(iam_role_names_file,username,password):
    with open(iam_role_names_file, newline='') as splunk_input:
        splunk_input_reader = csv.DictReader(splunk_input, delimiter=',')
        input_name = []
        account_id = []
        role_name = []
        role_arn = []
        for row in splunk_input_reader:
            input_name.append(row['Input Name'])
            account_id.append(row['Account ID'])
            role_name.append(row['Role Name'])
            role_arn.append(row['Role ARN'])
        for i in range(len(role_name)):
            delete_iam_role(role_name[i],username,password)

# Metadata input creation
"""
Example usage:
create_new_metadata_input('test_input','test_role','username','password')
"""
def create_new_metadata_input(metadata_input_name,iam_role_name,api_references_inputs,username,password):
    api_references_reader = open(api_references_inputs,'r')
    api_references_lines = api_references_reader.readlines()
    counter = 0
    api_references = ''
    for row in api_references_lines:
        if counter > 0:
            api_references = row.strip() + ',' + api_references
        else:
            api_references = row.strip() + api_references
        counter = counter + 1
    print(api_references)
    metadata_data = {
        'name':metadata_input_name,
        'account':'splunk_access',
        'aws_iam_role':iam_role_name,
        'regions':'eu-west-2,eu-west-1,us-east-1',
        'apis':api_references,
        'sourcetype':'aws:metadata',
        'index':'aws-operations',
        'retry_max_attempts':5
    }
    url_metadata = 'https://ccs.splunkcloud.com:8089/servicesNS/nobody/Splunk_TA_aws/splunk_ta_aws_aws_metadata'
    metadata_request = requests.post(url_metadata, data = metadata_data, auth = HTTPBasicAuth(username, password), headers={'Connection':'close'})
    print('')
    print(metadata_request)
    print('')
    print("New Metadata input '" + metadata_input_name + "' created")

# Metadata input deletion
"""
Example usage:
delete_metadata_input('test_input','username','password')
"""
def delete_metadata_input(metadata_input_name,username,password):
    url_metadata = 'https://ccs.splunkcloud.com:8089/servicesNS/nobody/Splunk_TA_aws/splunk_ta_aws_aws_metadata/' + metadata_input_name
    metadata_request = requests.delete(url_metadata, auth = HTTPBasicAuth(username, password), headers={'Connection':'close'})
    print('')
    print(metadata_request)
    print('')
    print("Existing Metadata input '" + metadata_input_name + "' deleted")

# Metadata bulk create from file
"""
Example usage:
create_metadata_inputs('filename','username','password')
"""
def create_metadata_inputs_from_file(metadata_input_names_file,api_references_inputs,username,password):
    with open(metadata_input_names_file, newline='') as splunk_input:
        splunk_input_reader = csv.DictReader(splunk_input, delimiter=',')
        input_name = []
        account_id = []
        role_name = []
        role_arn = []
        for row in splunk_input_reader:
            input_name.append(row['Input Name'])
            account_id.append(row['Account ID'])
            role_name.append(row['Role Name'])
            role_arn.append(row['Role ARN'])
        if len(input_name) > 1:
            for i in range(len(input_name)):
                create_new_metadata_input(input_name[i],role_name[i],api_references_inputs,username,password)
                # print("Having a quick sleep for " + str(3600/len(input_name)) + " seconds")
                # time.sleep(3600/len(input_name))
                print("Having a quick sleep for " + str(5) + " seconds")
                time.sleep(5)
        else:
            create_new_metadata_input(input_name[0],role_name[0],api_references_inputs,username,password)

# Metadata bulk delete from file
"""
Example usage:
delete_metadata_inputs('filename','username','password')
"""
def delete_metadata_inputs_from_file(metadata_input_names_file,username,password):
    with open(metadata_input_names_file, newline='') as splunk_input:
        splunk_input_reader = csv.DictReader(splunk_input, delimiter=',')
        input_name = []
        account_id = []
        role_name = []
        role_arn = []
        for row in splunk_input_reader:
            input_name.append(row['Input Name'])
            account_id.append(row['Account ID'])
            role_name.append(row['Role Name'])
            role_arn.append(row['Role ARN'])
        for i in range(len(input_name)):
            delete_metadata_input(input_name[i],username,password)

def main(argv):
    operation = ''
    input_file = ''
    input_name = ''
    role_name = ''
    role_arn = ''
    account_id = ''
    splunk_user = ''
    splunk_password = ''
    opts, args = getopt.getopt(argv,"ho:i:m:n:r:a:u:p:",["operation=","inputfile=","apireferences=","inputname=","rolename=","rolearn=","splunkuser=","splunkpassword="])
    for opt, arg in opts:
        if opt == '-h':
            print ('test.py -o <operation> -i <inputfile> -m <apireferences> -n <inputname> -r <rolename> -a <rolearn> -u <splunkuser> -p <splunkpassword>')
            sys.exit()
        elif opt in ("-o", "--operation"):
            operation = arg
        elif opt in ("-i", "--inputfile"):
            input_file = arg
        elif opt in ("-m", "--apireferences"):
            api_references = arg
        elif opt in ("-n", "--inputname"):
            input_name = arg
        elif opt in ("-r", "--rolename"):
            role_name = arg
        elif opt in ("-a", "--rolearn"):
            role_arn = arg
            role_elements = role_arn.split(":")
            account_id = role_elements[4]
        elif opt in ("-u", "--splunkuser"):
            splunk_user = arg
        elif opt in ("-p", "--splunkpassword"):
            splunk_password = arg
    if operation == "create":
        create_new_iam_role(role_name,account_id,splunk_user,splunk_password)
        create_new_metadata_input(input_name,role_name,api_references,splunk_user,splunk_password)
    elif operation == "create-bulk":
        create_iam_roles_from_file(input_file,splunk_user,splunk_password)
        create_metadata_inputs_from_file(input_file,api_references,splunk_user,splunk_password)
    elif operation == "delete":
        delete_metadata_input(input_name,splunk_user,splunk_password)
        delete_iam_role(role_name,splunk_user,splunk_password)
    elif operation == "delete-bulk":
        delete_iam_roles_from_file(input_file,splunk_user,splunk_password)
        delete_metadata_inputs_from_file(input_file,splunk_user,splunk_password)
    elif operation == "update":
        delete_iam_role(role_name,splunk_user,splunk_password)
        create_new_iam_role(role_name,role_arn,splunk_user,splunk_password)
        delete_metadata_input(input_name,splunk_user,splunk_password)
        create_new_metadata_input(input_name,role_name,api_references,splunk_user,splunk_password)
    elif operation == "update-bulk":
        delete_iam_roles_from_file(input_file,splunk_user,splunk_password)
        delete_metadata_inputs_from_file(input_file,splunk_user,splunk_password)
        create_iam_roles_from_file(input_file,splunk_user,splunk_password)
        create_metadata_inputs_from_file(input_file,api_references,splunk_user,splunk_password)

if __name__ == "__main__":
   main(sys.argv[1:])