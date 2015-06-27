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
        table = (self.name, self.id, self.state, self.vpc_id, self.az, self.platform, self._get_groups(), self.public_dns, self.public_ip, self.type)
        return table

    def _get_groups(self):
        return [str("%s [%s]" % (sg.name, sg.id)) for sg in self.groups]

    def __str__(self):
        table = [(self.name, self.id, self.state, self.vpc_id, self.az, self.platform, self._get_groups(), self.public_dns, self.public_ip, self.type)]
        return tabulate(table, headers=["Name", "Instance ID", "State", "VPC ID", "AZ", "Platform", "Security groups", "Public DNS", "Public IP", "Type"])

# ---------------------   Methods   ----------------------------

def get_public_regions():
    raw_regions = [str(region).split(':')[1] for region in ec2.regions()]

    regions = list(raw_regions)

    pattern_gov = re.compile("us-gov.*")
    pattern_china = re.compile("cn-*")

    [regions.remove(region) for region in raw_regions if pattern_gov.match(region) or pattern_china.match(region)]

    return regions

def get_ec2_instances():

    regions = get_public_regions()

    ec2_instances = dict()

    for region in regions:

        ec2_conn = ec2.connect_to_region(region,
                                         aws_access_key_id=getattr(aws_config, "access_key"),
                                         aws_secret_access_key=getattr(aws_config, "secret_key"))
        if ec2_conn is not None:
            instances = ec2_conn.get_only_instances()

        ec2_instances[region] = [Instance(instance).tuple_info() for instance in instances]

    return ec2_instances

def print_ec2_instances(instances_list):
    for key, value in instances_list.items():
        if value:
            print(key + ":\n")
            print(tabulate(value, headers=["Name", "Instance ID", "State", "VPC ID", "AZ", "Platform", "Security groups", "Public DNS", "Public IP", "Type"]))
            print("\n")
        else:
            print(key + ": No instances.")

print_ec2_instances(get_ec2_instances())

ec2_conn = ec2.connect_to_region("eu-west-1",
                                 aws_access_key_id=getattr(aws_config, "access_key"),
                                 aws_secret_access_key=getattr(aws_config, "secret_key"))

if ec2_conn is not None:
    sec_groups = ec2_conn.get_all_security_groups()

#[print(sec_group) for sec_group in sec_groups]

for sg in sec_groups:
    print("%s [%s]" % (sg.name, sg.id))
    [print("-- from %s to %s granted for %s" % (rule.from_port, rule.to_port, ",".join([str(ip) for ip in rule.grants]))) for rule in sg.rules]

#Connecting to VPC
#vpc_conn = connect_vpc(aws_access_key_id=getattr(aws_config, "access_key"),
#                            aws_secret_access_key=getattr(aws_config, "secret_key"))
#vpcs = vpc_conn.get_all_vpcs()
#print(vpcs)

