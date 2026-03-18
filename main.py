import boto3
import time
from dotenv import load_dotenv
from utils.file_writer import write_inventory, write_alerts

load_dotenv()

print("🔥 AWS Cloud Security Audit Started...\n")

start = time.time()

session = boto3.Session()

from checks import s3_check, ec2_check, iam_check, rds_check, vpc_check

# 🌍 Region mapping (code → city)
REGION_MAP = {
    "us-east-1": "N. Virginia",
    "us-east-2": "Ohio",
    "us-west-1": "N. California",
    "us-west-2": "Oregon",

    "ap-south-1": "Mumbai",
    "ap-south-2": "Hyderabad",
    "ap-southeast-1": "Singapore",
    "ap-southeast-2": "Sydney",
    "ap-southeast-3": "Jakarta",
    "ap-northeast-1": "Tokyo",
    "ap-northeast-2": "Seoul",
    "ap-northeast-3": "Osaka",

    "eu-west-1": "Ireland",
    "eu-west-2": "London",
    "eu-west-3": "Paris",
    "eu-central-1": "Frankfurt",
    "eu-north-1": "Stockholm",
    "eu-south-1": "Milan",

    "sa-east-1": "São Paulo",
    "ca-central-1": "Canada",
    "me-south-1": "Bahrain",
    "af-south-1": "Cape Town"
}

# Get all regions
ec2 = session.client('ec2', region_name='us-east-1')
regions = [r['RegionName'] for r in ec2.describe_regions()['Regions']]

inventory = []
alerts = []

# 🔁 REGION-WISE SCAN (ONLY REGIONAL SERVICES)
for region in regions:
    print(f"🌍 Scanning Region: {region}")
    regional_session = boto3.Session(region_name=region)

    location = REGION_MAP.get(region, "Unknown")

    # Header
    inventory.append("\n==============================\n")
    inventory.append(f"🌍 REGION: {region} ({location})\n")
    inventory.append("==============================\n")

    alerts.append("\n==============================\n")
    alerts.append(f"🚨 REGION: {region} ({location})\n")
    alerts.append("==============================\n")

    try:
        # ✅ ONLY regional services here
        for check in [ec2_check, vpc_check, rds_check]:
            inv, al = check.run(regional_session)
            inventory += inv
            alerts += al

    except Exception as e:
        alerts.append(f"[ERROR] {region}: {str(e)}\n")

# 🌐 GLOBAL SERVICES (FIXED - NO REGION CONFUSION)
print("\n🌐 Scanning Global Services...\n")

inventory.append("\n==============================\n")
inventory.append("🌐 GLOBAL SERVICES\n")
inventory.append("==============================\n")

alerts.append("\n==============================\n")
alerts.append("🚨 GLOBAL SERVICES\n")
alerts.append("==============================\n")

# Run global checks
for check in [s3_check, iam_check]:
    inv, al = check.run(session)
    inventory += inv
    alerts += al

# Save output
write_inventory(inventory)
write_alerts(alerts)

end = time.time()

print(f"\n✅ Scan Completed in {round(end-start,2)} seconds")


















# import boto3
# import os
# from dotenv import load_dotenv

# load_dotenv()

# print("🔥 Script started...\n")

# session = boto3.Session()

# from checks import s3_check, ec2_check, iam_check, rds_check, vpc_check

# # Get regions
# ec2 = session.client('ec2', region_name='us-east-1')
# regions = [r['RegionName'] for r in ec2.describe_regions()['Regions']]

# inventory = []
# alerts = []

# for region in regions:
#     print(f"🌍 Scanning region: {region}")

#     regional_session = boto3.Session(region_name=region)

#     # 🔥 Add region header in output
#     inventory.append(f"\n==============================\n")
#     inventory.append(f"🌍 REGION: {region}\n")
#     inventory.append(f"==============================\n")

#     alerts.append(f"\n==============================\n")
#     alerts.append(f"🚨 REGION: {region}\n")
#     alerts.append(f"==============================\n")

#     try:
#         inv, al = ec2_check.run(regional_session)
#         inventory += inv
#         alerts += al

#         inv, al = vpc_check.run(regional_session)
#         inventory += inv
#         alerts += al

#         inv, al = rds_check.run(regional_session)
#         inventory += inv
#         alerts += al

#     except Exception as e:
#         print(f"❌ Error in {region}: {e}")

#     print(f"✅ Done: {region}\n")

# # 🌐 Global services
# inventory.append("\n==============================\n🌐 GLOBAL SERVICES\n==============================\n")
# alerts.append("\n==============================\n🚨 GLOBAL SERVICES\n==============================\n")

# inv, al = s3_check.run(session)
# inventory += inv
# alerts += al

# inv, al = iam_check.run(session)
# inventory += inv
# alerts += al

# # Save files
# os.makedirs("output", exist_ok=True)

# with open("output/output.txt", "w") as f:
#     f.writelines(inventory)

# with open("output/output_alerts.txt", "w") as f:
#     f.writelines(alerts)

# print("\n✅ Scan completed!")