import boto3

# Any region_name is needed below, otherwise boto3 will error out
ec2 = boto3.client('ec2', region_name='us-east-1')

# Sorting through all the available regions
regions = [region['RegionName']
           for region in ec2.describe_regions()['Regions']]

# List of addons to create and verify
addonsList = ['coredns', 'kube-proxy', 'vpc-cni']

# Generic function to describe an addon and return standardized structure


def describe(addon, cluster, eks):
    struct = {
        'addonName': 'addon',
        'status': 'failed',
        'addonVersion': '',
    }
    try:
        # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/eks.html#EKS.Client.describe_addon
        details = eks.describe_addon(clusterName=cluster, addonName=addon)
        struct['status'] = details['addon']['status']
        struct['addonVersion'] = details['addon']['addonVersion']
    except:
        print('Failed querying Addon: ', addon, ' for Cluster: ', cluster)
    return struct

# Generic function to create an addon, returns true, does not raise


def create(addon, cluster, eks):
    try:
        # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/eks.html#EKS.Client.create_addon
        eks.create_addon(clusterName=cluster, addonName=addon)
    except:
        print('Failed creating Addon:', addon, ' for Cluster: ', cluster)
    return


# For each region
for region in regions:
    # Create the list of EKS clusters
    eks = boto3.client('eks', region_name=region)
    cllistraw = eks.list_clusters()
    # For each cluster
    for cluster in cllistraw['clusters']:
        # First, create (or attempt to create) all addons
        for item in addonsList:
            # Call create function with params
            create(item, cluster, eks)

        # Then, query details
        for item in addonsList:
            # Call describe function with params, receive data into variable
            describeData = describe(item, cluster, eks)
            print(cluster, describeData['addonName'],
                  describeData['status'], describeData['addonVersion'])

        print(cluster, 'Done!')
