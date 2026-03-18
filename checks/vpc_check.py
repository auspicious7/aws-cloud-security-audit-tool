def run(session):
    inventory = ["\n[ VPC DETAILS ]\n"]
    alerts = ["\n[ VPC ALERTS ]\n"]

    ec2 = session.client('ec2')

    try:
        vpcs = ec2.describe_vpcs()['Vpcs']

        if not vpcs:
            inventory.append("No VPCs found\n")

        for vpc in vpcs:
            vpc_id = vpc['VpcId']
            inventory.append(f"VPC: {vpc_id}\n")

            # 🚨 Flow Logs Check
            logs = ec2.describe_flow_logs(
                Filters=[{"Name": "resource-id", "Values": [vpc_id]}]
            )

            if not logs['FlowLogs']:
                alerts.append(f"[MEDIUM] {vpc_id} no flow logs\n")

    except Exception as e:
        alerts.append(f"[ERROR] VPC: {str(e)}\n")

    return inventory, alerts



















# def run(session):
#     inventory = ["\n[ VPC DETAILS ]\n"]
#     alerts = []

#     ec2 = session.client('ec2')
#     vpcs = ec2.describe_vpcs()['Vpcs']

#     for vpc in vpcs:
#         vpc_id = vpc['VpcId']
#         cidr = vpc['CidrBlock']

#         inventory.append(f"VPC: {vpc_id} | CIDR: {cidr}\n")

#     return inventory, alerts