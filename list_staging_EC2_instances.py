import boto3

# Any region_name is needed below, otherwise boto3 will error out
ec2Client = boto3.client('ec2', region_name='us-east-1')

# Sorting through all the available regions
regions = [region['RegionName']
           for region in ec2Client.describe_regions()['Regions']]

# Creating the list of instances:
print('Region,Name,ID,State,Launch Time')
for region in regions:
    instancesResource = boto3.resource('ec2', region_name=region)
    instancesAll = instancesResource.instances.all()
    for instance in instancesAll:
        instanceName = list(
            filter(lambda item: item['Key'] == 'Name', instance.tags))

        def keyValFinder(data, value):
            # For any list of dicts composed by Key/Value pairs
            # Return a filtered list with only matching values
            # Or back off with a 'Not Found' unique item
            result = list(filter(lambda item: item['Key'] == value, data))
            if len(result) == 0:
                result = [{'Key': value, 'Value': 'Not found'}]
            return result

        print(region, ',', keyValFinder(instanceName, 'Name'), ',',
              instance.id, ',', instance.state["Name"], ',', instance.launch_time)

#        if len(instanceName) == 0:
#            instanceName = [{'Key': 'Name', 'Value': 'Unnamed!!'}]
#        print(region, ',', instanceName[0]['Value'], ',', instance.id,
#              ',', instance.state["Name"], ',', instance.launch_time)
