# Author: Shashank Joshi
#
# Refer to the README under code-samples for details
#
# The code is provided on an "AS IS" BASIS, WITHOUT WARRANTIES
# OR CONDITIONS OF ANY KIND, either express or implied.
# See LICENSE under code-samples for more details

"""Example of using Compute Engine APIs to start & stop instances based on label values"""

import googleapiclient.discovery
from oauth2client.client import GoogleCredentials

def get_billing_id(cloud_billing_client):
    # Get billing account
    billing_result = cloud_billing_client.billingAccounts().list().execute()
    return billing_result["billingAccounts"][0]['name']

def get_project_list(cloud_billing_client,billing_id):
    # Get list of all projects in the billing id
    project_list = []
    project_result = cloud_billing_client.billingAccounts().projects().list(name=billing_id).execute()
    for project_row in project_result["projectBillingInfo"]:
        project_list.append(project_row["projectId"])
    return project_list

def execute_instance_action(compute_client, project_list, instance_action,label_key,label_value):
    # Get list & details of all instances for all projects in the project list
    for project_id in project_list:
        # First need to get the list of zones
        zone_list = []
        zone_result = compute_client.zones().list(project=project_id).execute()
        for zone_rows in zone_result['items']:
            zone_list.append(zone_rows['name'])
        for zone_name in zone_list:
            # For every zone for each project, get the instance details
            instances_result = compute_client.instances().list(project=project_id, zone=zone_name).execute()
            if 'items' in instances_result:
                for instance_row in instances_result["items"]:
                    # For every instance in the list check the label key and value and execute specified action
                    instance_name = ""
                    instance_zone = ""
                    if instance_row["labels"][label_key] == label_value:
                        instance_name = instance_row["name"]
                        instance_zone = zone_name
                        action_api_call = "compute_client.instances()."+instance_action+\
                            "(project=project_id, zone=zone_name, instance=instance_name)"
                        action_result = eval(action_api_call).execute()
                        print action_result

def main():
    # Label key and value to identify instances and execute the specfied action
    # You can get the values from command-line arguments
    label_key = "env-name"
    label_value = "non-prod"
    instance_action = "stop"
    # Use default credentials
    credentials = GoogleCredentials.get_application_default()
    # Build and initialize the API
    compute_client = googleapiclient.discovery.build('compute', 'v1', credentials=credentials)
    cloud_billing_client = googleapiclient.discovery.build('cloudbilling', 'v1', credentials=credentials)

    billing_id = get_billing_id(cloud_billing_client) # get billing id
    project_list = get_project_list(cloud_billing_client,billing_id) # get project list for the given billing id
    # Execute action on instances with the specified label key values
    execute_instance_action(compute_client,project_list,instance_action,label_key,label_value)

if __name__ == "__main__":
    main()
