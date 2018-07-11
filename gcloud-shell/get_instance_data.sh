#!/bin/bash
# Shashank Joshi 

#Header row for the output CSV file
echo "project_id,name,labels-app-name,labels-biz-unit,labels-env-name,metadata-server-role,metadata-server-type,metadata-os-image"
# for every project in the list of all projects get the required instance details. 
# in the gcloud output we don't want the header row 
# need to add the project id to the beginning of each row

for project in  $(gcloud projects list --format="value(projectId)")
do
        gcloud compute instances list --format="csv[no-heading](name, labels.app-name, labels.biz-unit, labels.env-name, metadata.items.server-role, metadata.items.server-type, metadata.items.os-image)" --project $project | sed "s/^/$project,/"
done
