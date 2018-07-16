# Author: Shashank Joshi
#
# Refer to the README under code-samples for details
#
# The code is provided on an "AS IS" BASIS, WITHOUT WARRANTIES
# OR CONDITIONS OF ANY KIND, either express or implied.
# See LICENSE under code-samples for more details

"""Example of using gcloud & Python to delete unattached disks based on labels"""

import subprocess
import json
import shlex

# Label key and value to identify the disks and execute the specfied action
# You can get the values from command-line arguments
label_key = "delete-protect"
label_value = "no"

# Execute the gcloud command to get a list of projects
# and load data in JSON format for further processing
project_list_command = "gcloud projects list --format json"
project_output = subprocess.check_output(shlex.split(project_list_command))
project_output_json = json.loads(project_output)

# For each project id in the list, get the disk details
for project_row in project_output_json:
    project_id = project_row["projectId"]
    disk_list_command = "gcloud compute disks list --format json --project "+ project_id
    disk_output_josn = json.loads(subprocess.check_output(shlex.split(disk_list_command)))

    # For every disk in the list check the label key and value and execute specfied action
    for disk_row in disk_output_josn:
        disk_name = disk_row["name"]
        disk_zone = ''.join(disk_row["zone"].split('/')[-1:]) # get the zone name
        if "users" not in disk_row.keys(): # If the disk is not attached
            if "labels" in disk_row.keys() and disk_row["labels"][label_key] == label_value: # Check the label
                print "Disk %s is not attached to any instance and is not labeled for delete protection" % disk_name
                disk_action_command = "gcloud compute disks delete "  \
                    + disk_name + " --zone " + disk_zone + " --project " + project_id
                print "Executing command \"" + disk_action_command + "\"\n"
                # Command below is commented intentionally, ucomment if you really want to delete the unattached disks
                #subprocess.check_output(shlex.split(disk_action_command))
            else:
                print "Disk %s is not attached to any instance and is labeled for delete protection\n" % disk_name
        else:
            print "Disk %s is attached to instance %s\n" % (disk_name, disk_row["users"])
