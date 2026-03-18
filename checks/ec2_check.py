def run(session):
    inventory = ["\n[ EC2 DETAILS ]\n"]
    alerts = ["\n[ EC2 ALERTS ]\n"]

    ec2 = session.client('ec2')

    try:
        instances = ec2.describe_instances()

        if not instances['Reservations']:
            inventory.append("No EC2 instances found\n")

        for res in instances['Reservations']:
            for inst in res['Instances']:
                instance_id = inst['InstanceId']
                public_ip = inst.get('PublicIpAddress', 'N/A')

                inventory.append(f"Instance: {instance_id} | Public IP: {public_ip}\n")

                # 🚨 Public Exposure
                if public_ip != 'N/A':
                    alerts.append(f"[MEDIUM] EC2 {instance_id} is publicly accessible\n")

                # 🔥 SSRF Protection (IMDSv2)
                if inst.get('MetadataOptions', {}).get('HttpTokens') != 'required':
                    alerts.append(f"[HIGH] EC2 {instance_id} not enforcing IMDSv2 (SSRF risk)\n")

                # 🔐 EBS Encryption
                for dev in inst.get('BlockDeviceMappings', []):
                    if not dev.get('Ebs', {}).get('Encrypted'):
                        alerts.append(f"[HIGH] EC2 {instance_id} has unencrypted EBS\n")

    except Exception as e:
        alerts.append(f"[ERROR] EC2: {str(e)}\n")

    return inventory, alerts





















# def run(session):
#     inventory = ["\n[ EC2 DETAILS ]\n"]
#     alerts = ["\n[ EC2 ALERTS ]\n"]

#     ec2 = session.client('ec2')
#     instances = ec2.describe_instances()

#     for res in instances['Reservations']:
#         for inst in res['Instances']:
#             instance_id = inst['InstanceId']
#             state = inst['State']['Name']
#             public_ip = inst.get('PublicIpAddress', 'N/A')

#             inventory.append(f"Instance: {instance_id} | State: {state} | Public IP: {public_ip}\n")

#     # Security group check
#     groups = ec2.describe_security_groups()['SecurityGroups']

#     for group in groups:
#         for perm in group['IpPermissions']:
#             for ip in perm.get('IpRanges', []):
#                 if ip.get('CidrIp') == '0.0.0.0/0':
#                     alerts.append(f"[!] SG {group['GroupId']} open to world\n")

#     return inventory, alerts