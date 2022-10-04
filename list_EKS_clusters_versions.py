import boto3

# Any region_name is needed below, otherwise boto3 will error out
ec2 = boto3.client('ec2', region_name='us-east-1')

# Sorting through all the available regions
regions = [region['RegionName']
           for region in ec2.describe_regions()['Regions']]

# Creating the list of EKS clusters
for region in regions:
    eks = boto3.client('eks', region_name=region)
    cllistraw = eks.list_clusters()
    for cluster in cllistraw['clusters']:
        try:
            cldescrip = eks.describe_cluster(name=cluster)
            clversion = cldescrip['cluster']['version']
            print(cluster, clversion)
        except:
            print(cluster, 'unknown')
