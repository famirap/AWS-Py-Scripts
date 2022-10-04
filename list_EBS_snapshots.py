import boto3

# Any region_name is needed below, otherwise boto3 will error out
ec2Client = boto3.client('ec2', region_name='us-east-1')

# Sorting through all the available regions
regions = [region['RegionName']
           for region in ec2Client.describe_regions()['Regions']]

# Creating the list of snapshots
for region in regions:
    snapshotsResource = boto3.resource('ec2', region_name=region)
    snapshotsClient = boto3.client('ec2', region_name=region)
    snapshotsList = snapshotsResource.snapshots.filter(
        OwnerIds=['810465967144'])
    for snapshot in snapshotsList:
        if snapshot.volume_id == 'vol-ffffffff':
            snapshotsDesc = snapshotsClient.describe_snapshots(
                SnapshotIds=[snapshot.id])
            snapshotSize = snapshotsDesc['Snapshots'][0]['VolumeSize']
            print(
                f'{region} -- {snapshot.id} -- {snapshotSize} GiB')
