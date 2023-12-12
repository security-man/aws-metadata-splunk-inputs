from auto_update_aws_config import AutoUpdateAWSConfig
import os

# Open file to read AWS config
f0 = open(os.path.expanduser('~/.aws/config'), 'r')
f0_lines = []
with f0 as file:
    f0_lines = f0.readlines()
f0_lines = [x.strip() for x in f0_lines]
f0.close()

# Run auto update script to update AWS config
AutoUpdateAWSConfig("<IAM_ROLE_1,IAM_ROLE_2,...,IAM_ROLE_N>")

# Open file again to read updated AWS config
f1 = open(os.path.expanduser('~/.aws/config'), 'r')
f1_lines = []
with f1 as file:
    f1_lines = f1.readlines()
f1_lines = [x.strip() for x in f1_lines]
f1.close()

# Find differences between f1 and f0 files
fdelta = list(set(f1_lines).difference(f0_lines))

# Write differences to metadata inputs file
fmetadata = open(os.path.expanduser('metadata_inputs'), 'w')
fmetadata.write("Input Name,Account ID,Role Name,Role ARN\n")

roles = []
role_arns = []
account_ids = []
input_names = []
for line in fdelta:
    if line.split()[0] == "role_arn":
        role = line.split("/")[1]
        if "RO" in role:
            role_arn = (line.split("=")[1]).lstrip()
            account_id = line.split(":")[4]
            roles.append(role)
            role_arns.append(role_arn)
            account_ids.append(account_id)
    if line.split()[0] == "role_session_name":
        name = line.split("=")[1].lstrip()
        input_names.append(name)

for i in range(len(roles)):
    fmetadata.write(input_names[i]+",")
    fmetadata.write(account_ids[i]+",")
    fmetadata.write(input_names[i]+",")
    fmetadata.write(role_arns[i]+"\n")

fmetadata.close()