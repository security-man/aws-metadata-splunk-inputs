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

for line in fdelta:
    name = f1_lines[f1_lines.index(line)+2].split("=")
    account_ids = line.split(":")
    roles = account_ids[5].split("/")
    if "RO" in roles[1]:
        fmetadata.write(name[1]+",")
        fmetadata.write(account_ids[4]+",")
        fmetadata.write(roles[1]+",")
        fmetadata.write(line+"\n")