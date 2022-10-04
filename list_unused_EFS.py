from datetime import datetime, timedelta
import boto3

# Defining the variable for the current date and time
now = datetime.now()

# Defining the period to poll data for
nowUtc = datetime.utcnow()
startUtc = nowUtc - timedelta(days=30)

# Defining the sample interval for cloudwatch, set to 4hrs
sampleInterval = 60*60*4

# Any region_name is needed below, otherwise boto3 will error out
ec2 = boto3.client('ec2', region_name='us-east-1')

# Sorting through all the available regions
regions = [region['RegionName'] for region in ec2.describe_regions()['Regions']]

# Creating the list of EFS
for region in regions:
    cloudwatch = boto3.client('cloudwatch', region_name=region)
    efsclient = boto3.client('efs', region_name=region)
    efslist = efsclient.describe_file_systems(MaxItems=123)
    for efs in efslist['FileSystems']:
        if efs.get('Name') is not None:
            efsname = efs['Name']
        efsfsid = efs['FileSystemId']
        efssize = efs['SizeInBytes']['Value']
        efssizeMB = "{:.2f}".format(int(efssize)/(1024*1024))

# Getting the IOPS and connections per EFS
        metric_result_iops = cloudwatch.get_metric_statistics(Period=sampleInterval, StartTime=startUtc, EndTime=nowUtc,
            MetricName='TotalIOBytes', Namespace='AWS/EFS', Statistics=['Sum'],
            Dimensions=[{'Name': 'FileSystemId', 'Value': efsfsid}])
        metric_result_clconn = cloudwatch.get_metric_statistics(Period=sampleInterval, StartTime=startUtc, EndTime=nowUtc,
            MetricName='ClientConnections', Namespace='AWS/EFS', Statistics=['Sum'],
            Dimensions=[{'Name': 'FileSystemId', 'Value': efsfsid}])

# Getting the count of IOPS and connections
        count_iops = sum(map(lambda x: float(x['Sum']), metric_result_iops['Datapoints']))
        count_clconn = sum(map(lambda x: float(x['Sum']), metric_result_clconn['Datapoints']))

# List the EFS items, change the conditionals as needed
        if efssize != 0:
            if count_iops == 0:
                if count_clconn == 0:
                    print(region)
                    print('Name:', efsname, '---', 'ID:', efsfsid, '---', 'Size (MBs):', efssizeMB)