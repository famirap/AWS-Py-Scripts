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
        # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/eks.html#EKS.Client.create_addon
        try:
            addcoredns = eks.create_addon(
                clusterName=cluster, addonName='coredns')
            addkubeproxy = eks.create_addon(
                clusterName=cluster, addonName='kube-proxy')
            addvpccni = eks.create_addon(
                clusterName=cluster, addonName='vpc-cni')
            # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/eks.html#EKS.Client.list_addons
            listaddons = eks.list_addons(clusterName=cluster)
            print(cluster)
            for addon in listaddons:
                try:
                    # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/eks.html#EKS.Client.describe_addon
                    addondesc = eks.describe_addon(
                        clusterName=cluster, addonName=addon)
                    print(addondesc['addon']['addonName'], addondesc['addon']
                          ['status'], addondesc['addon']['addonVersion'])
                except:
                    print('Missing addons!')
            print('Done!')
        except:
            print(cluster, 'Errors!')
