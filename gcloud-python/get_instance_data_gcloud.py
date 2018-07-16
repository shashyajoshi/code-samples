# Author: Shashank Joshi
#
# Refer to the README under code-samples for details
#
# The code is provided on an "AS IS" BASIS, WITHOUT WARRANTIES
# OR CONDITIONS OF ANY KIND, either express or implied.
# See LICENSE under code-samples for more details

"""Example of using gcloud & Python to get instance labels and metadata"""

import subprocess
import json
import shlex

output = []
output_row = []
# Change the header row based on your requirement
header_row = "project_id,name,labels-app-name,labels-biz-unit,labels-env-name,metadata-server-role,metadata-server-type,metadata-os-image"

# Execute the gcloud command to get a list of projects
# and load data in JSON format for further processing
project_list_command = "gcloud projects list --format json"
project_output = subprocess.check_output(shlex.split(project_list_command))
project_output_json = json.loads(project_output)

# For each project id in the list, get the instance details
for project_row in project_output_json:
    instance_list_command = "gcloud compute instances list --format json --project "+ project_row["projectId"]
    instance_output_josn = json.loads(subprocess.check_output(shlex.split(instance_list_command)))
    # For every instance in the list get the labels and metadata as required
    for instance_row in instance_output_josn:
        output_row = []
        metadata_dict = {}
        output_row.append(project_row["projectId"]) # Add project id to the begining of the output row
        output_row.extend([instance_row["name"],instance_row["labels"]["app-name"],instance_row["labels"]["biz-unit"],instance_row["labels"]["env-name"]])
        for metadata_entry in instance_row["metadata"]["items"]: # Metadata is nested field so would need further processing
            metadata_dict[metadata_entry['key']] = metadata_entry['value']
        output_row.extend([metadata_dict['server-role'], metadata_dict['server-type'], metadata_dict['os-image']])
        output.append(output_row)

# Print the header row and the instance data rows to stdout
print header_row
for row in output:
    print ','.join(row)
