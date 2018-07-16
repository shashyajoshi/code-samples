# Author: Shashank Joshi
#
# Refer to the README under code-samples for details
#
# The code is provided on an "AS IS" BASIS, WITHOUT WARRANTIES
# OR CONDITIONS OF ANY KIND, either express or implied.
# See LICENSE under code-samples for more details

"""Example of using Compute Engine APIs to get instance labels and metadata"""

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

def get_instance_data(compute_client, project_list):
    # Get list & details of all instances for all projects in the project list
    output = []
    for project_id in project_list:
        # First get the list of zones
        zone_list = []
        zone_result = compute_client.zones().list(project=project_id).execute()
        for zone_rows in zone_result['items']:
            zone_list.append(zone_rows['name'])
        for zone_name in zone_list:
            # For every zone for each project, get the instance details
            instances_result = compute_client.instances().list(project=project_id, zone=zone_name).execute()
            if 'items' in instances_result: # Get instance details only when there are instances in the given zone
                for instance_row in instances_result["items"]:
                    output_row = []
                    metadata_dict = {}
                    output_row.append(project_id) # Project ID as the first field
                    output_row.extend([instance_row["name"],instance_row["labels"]["app-name"],instance_row["labels"]["biz-unit"],instance_row["labels"]["env-name"]])
                    # Get nested metadat key-value entries
                    for metadata_entry in instance_row["metadata"]["items"]:
                        metadata_dict[metadata_entry['key']] = metadata_entry['value']
                    output_row.extend([metadata_dict['server-role'], metadata_dict['server-type'], metadata_dict['os-image']])
                    output.append(output_row)
    return output

def write_output(header_row,output):
    # Write CSV format output to stdout
    print header_row
    for row in output:
        print ','.join(row)

def main():
    # Change the header row based on your requirement
    header_row = "project_id,name,labels-app-name,labels-biz-unit,labels-env-name,metadata-server-role,metadata-server-type,metadata-os-image"
    # Use default credentials
    credentials = GoogleCredentials.get_application_default()
    # Build and initialize the API
    compute_client = googleapiclient.discovery.build('compute', 'v1', credentials=credentials)
    cloud_billing_client = googleapiclient.discovery.build('cloudbilling', 'v1', credentials=credentials)

    billing_id = get_billing_id(cloud_billing_client) # get billing id
    project_list = get_project_list(cloud_billing_client,billing_id) # get project list for the given billing id
    output = get_instance_data(compute_client,project_list) # get instance details for the list of projects
    write_output(header_row,output)


if __name__ == "__main__":
    main()
