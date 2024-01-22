# aws-metadata-splunk-inputs
Simple python code to enable automated creation of IAM roles and metadata inputs for the Splunk AWS Add-on

Please see [further web documentation](https://docs.splunk.com/Documentation/AddOns/released/AWS/Description) for more information on the Splunk AWS Add-on.

## Overview

This repository contains a the main python file as well as some reference and input files needed to provision the IAM roles and / or metadata inputs specified. The python functions performing the actual IAM role creation / metadata input creation rely on simple web requests using HTTP basic authentication with use of Splunk credentials (with the necessary permissions to create these objects within Splunk Add-on for AWS).

## Structure
```
├── metadata.py                                 # contains python code that can be executed as a script or function
├── api_references                              # contains a comma-separated list of metadata apis to poll, separated by line per service
├── test_inputs                                 # contains a comma-separated list of test inputs for file-based function execution
├── aws_input_file_automation_script.py         # contains python code that can be executed to automatically generate a new inputs file for metadata.py
├── README.md                                   # README documentation (this document)
└── .gitignore                                  # .gitignore ...
```

The 'metadata.py' file contains code to provision the necessary IAM roles and metadata inputs within the Splunk Add-on for AWS. This relies mostly on reading any input files for inputs and also api references to poll.

The 'api_references' file contains a list of metadata endpoints to poll. This is equivalent to the UI tick-box selection available within the Splunk Add-on for AWS. The file is arranged as a comma-separated list of endpoints, with endpoints grouped by AWS service; endpoints for each service are separated by line. Some current defaults are set within this file - these can be modified as suits your needs. Please see the Splunk Add-on for aws metadata inputs configuration UI for further detail on the available api endpoints.

The 'test_inputs' file contains a comma-separated list of test inputs needed to create an IAM role named 'test' with ARN 'arn:aws:iam::123412341234:role/Test_Role'. This IAM role is then used to create a metadata input named 'test' for AWS account ID '123412341234'. This file serves as a guide as to how to structure any files for multiple input creation usage (e.g., creating IAM roles / metadata inputs in bulk for a range of AWS accounts)

The 'aws_input_file_automation_script.py' file contains code to automatically generated a correctly-formatted input file for use with 'metadata.py'. The script relies on [auto_update_aws_config.py] (https://github.com/security-man/auto-update-aws-config) and the necessary access keys and permissions to run this file (see documentation).

## TO-DO: 
Need to update to use environment variables for splunk credentials ...

## Create IAM role and metadata input

1. Clone the repo

2. Edit parameters file for api_references to suit your needs (note, regions are currently hard-coded within metadata.py)

3. If creating a bulk set of IAM roles / metadata inputs, create an input file using the format provided in 'test_inputs'

4. Run the python script / function, using either command-line variables or file-based input:

(Command-line arguments):

        python3 metadata.py -o create -m api_references -n input_name -r role_name -a role_arn

(File-based input):

        python3 metadata.py -o create-bulk -i input_file_name -m api_references  -u splunk_username -p splunk_password

## Using aws_input_file_automation_script.py

1. Modify line 13 to reflect the choice of IAM roles needed for your aws config file (replace 'IAM_ROLE_N' with IAM roles of choice)

        AutoUpdateAWSConfig("<IAM_ROLE_1,IAM_ROLE_2,...,IAM_ROLE_N>")

2. Execute aws_input_file_automation_script.py

3. Use the output file 'metadata_inputs' as an input file for metadata.py:

        python3 metadata.py -o create-bulk -i metadata_inputs -m api_references  -u splunk_username -p splunk_password