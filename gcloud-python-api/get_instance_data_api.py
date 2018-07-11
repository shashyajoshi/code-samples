import googleapiclient.discovery
from oauth2client.client import GoogleCredentials
from pprint import pprint

output = []
output_row = []
project_list = []

header_row = "project_id,name,labels-app-name,labels-biz-unit,labels-env-name,metadata-server-role,metadata-server-type,metadata-os-image"

credentials = GoogleCredentials.get_application_default()
compute_interface = googleapiclient.discovery.build('compute', 'v1', credentials=credentials)
cloud_billing_interface = googleapiclient.discovery.build('cloudbilling', 'v1', credentials=credentials)

billing_result = cloud_billing_interface.billingAccounts().list().execute()

project_result = cloud_billing_interface.billingAccounts().projects().list(name=billing_result["billingAccounts"][0]['name']).execute()

for project_row in project_result["projectBillingInfo"]:
    project_list.append(project_row["projectId"])

for project_id in project_list:
    zone_list = []
    zone_result = compute_interface.zones().list(project=project_id).execute()
    for zone_rows in zone_result['items']:
        zone_list.append(zone_rows['name'])
    for zone_name in zone_list:
        instances_result = compute_interface.instances().list(project=project_id, zone=zone_name).execute()
        if 'items' in instances_result:
            #pprint(instances_result["items"])
            for instance_row in instances_result["items"]:
                output_row = []
                metadata_dict = {}
                output_row.append(project_id)
                output_row.extend([instance_row["name"],instance_row["labels"]["app-name"],instance_row["labels"]["biz-unit"],instance_row["labels"]["env-name"]])
                for metadata_entry in instance_row["metadata"]["items"]:
                    metadata_dict[metadata_entry['key']] = metadata_entry['value']
                output_row.extend([metadata_dict['server-role'], metadata_dict['server-type'], metadata_dict['os-image']])
                output.append(output_row)

print header_row

for row in output:
    print ','.join(row)
