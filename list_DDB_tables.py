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

# Creating the list of DDB tables
for region in regions:
    cloudwatch = boto3.client('cloudwatch', region_name=region)
    dynamodb = boto3.client('dynamodb', region_name=region)
    tname = dynamodb.list_tables()
    for table in tname['TableNames']:
        tnamestr = str(table)
        tdescrip = dynamodb.describe_table(TableName=tnamestr)
        tsize = tdescrip['Table']['TableSizeBytes']

# Getting the consumed RCUs and WCUs per table
        metric_result_crcu = cloudwatch.get_metric_statistics(Period=sampleInterval, StartTime=startUtc, EndTime=nowUtc,
            MetricName='ConsumedReadCapacityUnits', Namespace='AWS/DynamoDB', Statistics=['Sum'],
            Dimensions=[{'Name': 'TableName', 'Value': str(table)}])
        metric_result_cwcu = cloudwatch.get_metric_statistics(Period=sampleInterval, StartTime=startUtc, EndTime=nowUtc,
            MetricName='ConsumedWriteCapacityUnits', Namespace='AWS/DynamoDB', Statistics=['Sum'],
            Dimensions=[{'Name': 'TableName', 'Value': str(table)}])

# Getting the sum of RCUs and WCUs
        count_rcu = sum(map(lambda x: float(x['Sum']), metric_result_crcu['Datapoints']))
        count_wcu = sum(map(lambda x: float(x['Sum']), metric_result_cwcu['Datapoints']))
        sumwcurcu = (int(count_rcu) + int(count_wcu))

# Output is optional, but a nice to have
#        output = {
#            'Region': region,
#            'Table Name': tnamestr,
#            'Table Size': tsize
#        }

# Use only one of the following sections at a time, comment the rest

# List only the empty DBs
        print ('The following DBs are empty')
        if tsize == 0:
            print (region, tnamestr)

# List empty tables with no RCUs and no WCUs
#        print ('The following DBs are empty AND have no consumed RCUs/WCUs')
#        if tsize == 0:
#            if sumwcurcu == 0:
#                print(region, tnamestr)

# List non-empty tables with no RCUs and no WCUs
#        print ('The following DBs are NOT empty AND have no consumed RCUs/WCUs')
#        if tsize != 0:
#            if sumwcurcu == 0:
#                print(region, tnamestr)

# List non-empty tables with consumed RCUs and no WCUs
#        print ('The following DBs are NOT empty AND DO have consumed RCUs/WCUs')
#        if tsize != 0:
#            if sumwcurcu != 0:
#                print(region, tnamestr)
