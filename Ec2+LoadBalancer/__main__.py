import pulumi
import pulumi_aws as aws

''' 
Simple IaC deployment:
3 Ec2 instances across 3 AZ under 1 region + 1 simple ALB to distribute the loads evenly

# Thanks to Beau Carnes and FCA for the intro to Pulumi
'''

ips = []
hostnames = []

#Describe the AMI to use:
ami = aws.ec2.get_ami(
    most_recent=True,
    owners=["137112412989"],
    filters=[aws.GetAmiFilterArgs(name="name", values=["amzn-ami-hvm-*"])]
    )

# Describe VPC and Subnets
vpc = aws.ec2.get_vpc(default=True)
vpc_subnets = aws.ec2.get_subnet_ids(vpc_id=vpc.id)

# Create SGs
group = aws.ec2.SecurityGroup('web-secgrp',
    description='Enable HTTP access',
    ingress=[aws.ec2.SecurityGroupIngressArgs(
        protocol='tcp',
        from_port=80,
        to_port=80,
        cidr_blocks=['0.0.0.0/0'],
    )],
    # For the Load Balancer to work:
    egress=[aws.ec2.SecurityGroupEgressArgs(
        protocol='tcp',
        from_port=80,
        to_port=80,
        cidr_blocks=['0.0.0.0/0']
    )])

# Load Balancer Setup + TG + Listener
lb = aws.lb.LoadBalancer(
    "loadbalancer",
    internal=False,
    security_groups=[group.id],
    subnets=vpc_subnets.ids,
    load_balancer_type="application",
)
target_group = aws.lb.TargetGroup(
    "target-group", port=80, protocol="HTTP", target_type="ip", vpc_id=vpc.id
)
listener = aws.lb.Listener(
    "Listener",
    load_balancer_arn=lb.arn,
    port=80,
    default_actions=[{"type": "forward", "target_group_arn": target_group.arn}]
)

# EC2 Creation
for az in aws.get_availability_zones().names: # AZ described in the pulumi config set command for the previously chosen Region

    server = aws.ec2.Instance(
        f'my-web-server-{az}',
        instance_type="t2.micro",
        security_groups=[group.name],
        ami=ami.id,
        availability_zone=az,
        # Here we could setup a sepparate file with the script and pass it with pulumi's variables
        user_data='''
    #!/bin/bash
    echo \"Hello, World! From: {}\" > index.html
    nohup python -m SimpleHTTPServer 80 &
        '''.format(az),
        tags={
            "Name": 'Web Server',
        }
    )
    ips.append(server.public_ip)
    hostnames.append(server.public_dns)

    attachment = aws.lb.TargetGroupAttachment(f'web-server-{az}',
    target_group_arn=target_group.arn,
    target_id=server.private_ip,
    port=80
    )

pulumi.export("ips", ips)
pulumi.export("Hostnames", hostnames)
pulumi.export("Url", lb.dns_name)