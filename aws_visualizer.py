__author__ = 'jacek'

"""
    To do: create an example file of aws_config
"""

from tabulate import tabulate

import boto
from boto import ec2
from boto import vpc

import aws_config

class Instance(object):
    """Class to store only certain fields from original EC2 instance class
    Input parameters: boto.ec2.instance
    """
    def __init__(self, instance):
        self.id = str(instance).split(':')[1]
        self.state = instance.state
        self.vpc_id = instance.vpc_id
        self.az = instance.placement

    def __str__(self):
        table = [(self.id, self.state, self.vpc_id, self.az)]
        return tabulate(table, headers=["Instance ID", "State", "VPC ID", "AZ"])


regions = boto.ec2.regions()

ec2_conn = boto.ec2.connect_to_region("us-east-1",
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

"""
#Connecting to VPC
vpc_conn = boto.connect_vpc(aws_access_key_id=access_key,
                            aws_secret_access_key=secret_key)
vpc s = vpc_conn.get_all_vpcs()
print vpcs"""

#for instance in reservations:
#    for instance1 in instance.instances:
#        print str(instance1) + ' - ' + (instance1.state)

