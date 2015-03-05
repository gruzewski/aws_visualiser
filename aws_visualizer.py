"""
    To do: create an example file of aws_config
"""

# Built-in libraries
import re

# 3rd party imports
from tabulate import tabulate
from boto import ec2, connect_vpc

# Config file imports
import aws_config

# ---------------------   Classes   ----------------------------

class Instance(object):
    """Class to store only certain fields from original EC2 instance class
    Input parameters: boto.ec2.instance
    """
    def __init__(self, instance):
        self.id = str(instance).split(':')[1]
        self.name = instance.tags['Name']
        self.state = instance.state
        self.vpc_id = instance.vpc_id
        self.az = instance.placement
        self.groups = instance.groups
        self.public_dns = instance.public_dns_name
        self.public_ip = instance.ip_address
        self.type = instance.instance_type
        self.private_ip = instance.private_ip_address
        self.platform = instance.platform

    def tuple_info(self):
        table = [(self.name, self.id, self.state, self.vpc_id, self.az, self.platform, self.groups, self.public_dns, self.public_ip, self.type)]
        return table

    def __str__(self):
        table = [(self.name, self.id, self.state, self.vpc_id, self.az, self.platform, self.groups, self.public_dns, self.public_ip, self.type)]
        return tabulate(table, headers=["Name", "Instance ID", "State", "VPC ID", "AZ", "Platform", "Security groups", "Public DNS", "Public IP", "Type"])

# ---------------------   Methods   ----------------------------

def get_regions():
    raw_regions = [str(region).split(':')[1] for region in ec2.regions()]

    regions = list(raw_regions)

    pattern_gov = re.compile("us-gov.*")
    [regions.remove(region) for region in raw_regions if pattern_gov.match(region)]

    return regions

"""def get_ec2_instances(region):

    regions = ec2.regions()
    ec2_instances = dict()

    for region in regions:
        ec2_conn = ec2.connect_to_region(region,
                                                aws_access_key_id=getattr(aws_config, "access_key"),
                                                aws_secret_access_key=getattr(aws_config, "secret_key"))
        if ec2_conn is not None:
            instances = ec2_conn.get_only_instances()

    reservations = ec2_conn.get_all_reservations()
    for reservation in reservations:
        print region+':',reservation.instances

"""

regions = get_regions()

print regions

for region in regions:

    print region
    ec2_conn = ec2.connect_to_region(region,
                                     aws_access_key_id=getattr(aws_config, "access_key"),
                                     aws_secret_access_key=getattr(aws_config, "secret_key"))
   # if ec2_conn is not None:
    instances = ec2_conn.get_only_instances()

    #for instance in instances:
    #    print region+':',instances.instances



ec2_conn = ec2.connect_to_region("us-east-1",
                                       aws_access_key_id=getattr(aws_config, "access_key"),
                                       aws_secret_access_key=getattr(aws_config, "secret_key"))

instances = ec2_conn.get_only_instances()
sec_groups = ec2_conn.get_all_security_groups()




instance_object = Instance(instances[0])
print instance_object.__str__()

#table = [(str(instance).split(':')[1], instance.state, instance.vpc_id, instance.placement) for instance in instances]

#print type (table)
#for instance in instances:
#    print instance.vpc_id

#print tabulate(table, headers=["Instance ID", "State", "VPC ID", "AZ"])



#Connecting to VPC
vpc_conn = connect_vpc(aws_access_key_id=getattr(aws_config, "access_key"),
                            aws_secret_access_key=getattr(aws_config, "secret_key"))
vpcs = vpc_conn.get_all_vpcs()
print vpcs

#for instance in reservations:
#    for instance1 in instance.instances:
#        print str(instance1) + ' - ' + (instance1.state)

