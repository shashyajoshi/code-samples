#!/bin/bash
# Shashank Joshi 

#Header row for the output CSV file
echo "project_id,instance_name,license"
# for every project in the list of all projects get the required instance details. 
# in the gcloud output we don't want the header row 
# need to add the project id to the beginning of each row

for project in  $(gcloud projects list --format="value(projectId)")
do
        gcloud compute instances list --format="csv[no-heading](name,disks.licenses.basename())" --project $project | sed s/\']]//g | sed "s/^/$project,/"
done
