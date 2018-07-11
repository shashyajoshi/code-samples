import googleapiclient.discovery
from oauth2client.client import GoogleCredentials
from pprint import pprint

credentials = GoogleCredentials.get_application_default()
compute_interface = googleapiclient.discovery.build('compute', 'v1', credentials=credentials)
cloud_billing_interface = googleapiclient.discovery.build('cloudbilling', 'v1', credentials=credentials)

#instances_result = compute_interface.instances().list(project=project_id, zone=zone).execute()
billing_result = cloud_billing_interface.billingAccounts().list().execute()

project_result = cloud_billing_interface.billingAccounts().projects().list(name=billing_result["billingAccounts"][0]['name']).execute()

#print project_result
project_list = []
for project_row in project_result["projectBillingInfo"]:
    project_list.append(project_row["projectId"])

#print project_list

for project_id in project_list:
    zone_list = []
    zone_result = compute_interface.zones().list(project=project_id).execute()
    for zone_rows in zone_result['items']:
        zone_list.append(zone_rows['name'])
    for zone_name in zone_list:
        instances_result = compute_interface.instances().list(project=project_id, zone=zone_name).execute()
        if 'items' in instances_result:
            pprint(instances_result["items"])
