# Author: Shashank Joshi
#
# Refer to the README under code-samples for details
#
# The code is provided on an "AS IS" BASIS, WITHOUT WARRANTIES
# OR CONDITIONS OF ANY KIND, either express or implied.
# See LICENSE under code-samples for more details

"""Example of using gcloud & Python to start & stop instances based on label values"""

import subprocess
import json
import shlex

# Label key and value to identify instances and execute the specfied action
# You can get the values from command-line arguments
label_key = "env-name"
label_value = "non-prod"
instance_action = "stop"
# Execute the gcloud command to get a list of projects
# and load data in JSON format for further processing
project_list_command = "gcloud projects list --format json"
project_output = subprocess.check_output(shlex.split(project_list_command))
project_output_json = json.loads(project_output)

# For each project id in the list, get the instance details
for project_row in project_output_json:
    project_id = project_row["projectId"]
    instance_list_command = "gcloud compute instances list --format json --project "+ project_id
    instance_output_josn = json.loads(subprocess.check_output(shlex.split(instance_list_command)))

    # For every instance in the list check the label key and value and execute specified action
    for instance_row in instance_output_josn:
        instance_name = ""
        instance_zone = ""
        if instance_row["labels"][label_key] == label_value:
            instance_name = instance_row["name"]
            instance_zone = ''.join(instance_row["zone"].split('/')[-1:])
            instance_action_command = "gcloud compute instances " + instance_action + " " \
                + instance_name + " --zone " + instance_zone + " --project " + project_id
            print "Executing command \"" + instance_action_command + "\""
            subprocess.check_output(shlex.split(instance_action_command))
