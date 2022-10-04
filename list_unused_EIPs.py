import boto3
from operator import itemgetter

# Any region_name is needed below, otherwise boto3 will error out
ec2 = boto3.client('ec2', region_name='us-east-1')

# Creating the list of available EIPs
EIPresponse = ec2.describe_addresses(
    Filters=[{'Name': 'domain', 'Values': ['vpc']}])

# print(EIPresponse)

freeEIPlist = []
for eip in EIPresponse['Addresses']:
    if 'AssociationId' not in eip and 'Tags' not in eip:
        freeEIPlist.append(eip['PublicIp'])
# print(*freeEIPlist, sep="\n")
# print('Total free EIPs:' + str(len(freeEIPlist)))

usedEIPlist = []
for eip in EIPresponse['Addresses']:
    if 'AssociationId' in eip or 'Tags' in eip:
        item = {
            'Name': next((v['Value'] for v in eip['Tags'] if v['Key'] in 'Name'), '----') if 'Tags' in eip else '----',
            'DC': next((v['Value'] for v in eip['Tags'] if v['Key'] in 'DataCenter'), '----') if 'Tags' in eip else '----',
            'IP': eip['PublicIp']
        }
        usedEIPlist.append(item)

sortedUsedEIPlist = sorted(usedEIPlist, key=itemgetter('Name', 'DC'))
print(*sortedUsedEIPlist, sep="\n")
print('Total used EIPs:' + str(len(usedEIPlist)))

# print('Total EIPs:' + str(len(EIPresponse['Addresses']))
