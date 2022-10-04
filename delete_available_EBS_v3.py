import datetime
import boto3

# Defining the variable for the current date and time
now = datetime.datetime.now()

# Any region_name is needed below, otherwise boto3 will error out
ec2 = boto3.client('ec2', region_name='us-east-1')
regions = [region['RegionName'] for region in ec2.describe_regions()['Regions']]

# Creating the list of available EBS volumes and deleting them
listOut = []
for region in regions:
    try:
        ec2Each = boto3.resource('ec2', region_name=region)
        volumes = ec2Each.volumes.filter(Filters=[{'Name': 'status', 'Values': ['available']}])
        for vol in volumes:
            listOut.append([region, vol.id, str(vol.size) + " GiB"])
            try:
                vol.delete(DryRun=True)
            except:
                print ("Exception found, skipping...")
    except:
        print ("No volumes found, skipping...")

# Adding the list created above to the HTML table below
new_list = listOut

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
    <font size=+1><i>These are the available EBS volumes DELETED in QA environments today.</i></font>
<br>
<br>
    <font size=+2>Deleted available EBS volumes in QA environments</font>
<br>
<br>
    <table>\n
      <tr>
        <th>Region</th>
        <th>Vol ID</th>
        <th>Size</th>
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
display = open("DeletedAvailableEBS.html", 'w')
display.write(result_string)
display.close()
