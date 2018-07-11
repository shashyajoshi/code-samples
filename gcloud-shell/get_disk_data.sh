#!/bin/bash
# Shashank Joshi 

#Header row for the output CSV format
echo "project_id,disk_name,user"
# for every project in the list of all projects get the required details. 
# in the gcloud output we don't want the header row 
# need to add the project id to the beginning of each row

for project in  $(gcloud projects list --format="value(projectId)")
do
        gcloud compute disks list --format="csv[no-heading](name,users.basename())" --project $project | sed s/\']//g | sed "s/^/$project,/"
done
