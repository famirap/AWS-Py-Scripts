import datetime
import boto3
import json

# Defining the variable for the current date and time
now = datetime.datetime.now()

# Any region_name is needed below, otherwise boto3 will error out
ec2 = boto3.client('ec2', region_name='us-east-1')

# Sorting through all the available regions
regions = [region['RegionName'] for region in ec2.describe_regions()['Regions']]

# Set the new retention policy to be applied
retention_days = 7

# Creating the list of log groups with NO retention policy and applying the new policy
logGroupsList = []
for region in regions:
  logGroups = boto3.client('logs', region_name=region)
  response = logGroups.describe_log_groups()
  nextToken = response.get('nextToken',None)
  retention = response['logGroups']
  while (nextToken is not None):
    response = logGroups.describe_log_groups(nextToken=nextToken)
    nextToken = response.get('nextToken', None)
    retention = retention + response['logGroups']
    for group in retention:
      if 'retentionInDays' not in group.keys():
        logGroupsList.append([region, group['logGroupName']])
        setretention = logGroups.put_retention_policy(logGroupName=group['logGroupName'],retentionInDays=retention_days)
      else:
        continue

# Adding the list created above to the HTML table below
new_list = logGroupsList

# HTML to be included in the email
result_string = """<HTML>
<head>
<style>
table, th, td {border: 1px solid black; border-collapse: collapse;}
th, td {padding: 10px;}
tr:nth-child(even) {background-color: #D3D3D3;}
</style>
</head>
<body>
  <font size=+1><i>These were the log groups found with NO retention policy and were set with a 1 week retention</i></font>
    <br>
    <br>
        <font size=+2>Log groups in QA environments</font>
    <br>
    <br>
        <table>\n
          <tr>
            <th>Region</th>
            <th>Log Group Name</th>
          </tr>"""

# Defining the HTML table
for i in new_list:
  result_string += "<tr>\n"
  for j in i:
    result_string += "<td>%s</td>" %j
  result_string += "\n</tr>\n"
result_string += """
</table>
<br>
    <p>Current Date and Time is (UTC):  <% datetime %></p>
</body>
</HTML>"""

# Inserting the current date and time in the email
replacements = {'<% datetime %>': str(now.strftime("%Y-%m-%d %H:%M:%S"))}
for key in replacements:
  result_string = result_string.replace(key, replacements[key])

# Output the resulting HTML to a file
display = open("LGsWithNoRetentionPolicy.html", 'w')
display.write(result_string)
display.close()
