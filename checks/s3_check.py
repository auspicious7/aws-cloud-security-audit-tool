def run(session):
    inventory = ["\n[ S3 DETAILS ]\n"]
    alerts = ["\n[ S3 ALERTS ]\n"]

    s3 = session.client('s3')

    try:
        buckets = s3.list_buckets()['Buckets']

        if not buckets:
            inventory.append("No S3 buckets found\n")

        for b in buckets:
            name = b['Name']

            # 📍 Get bucket region (important fix)
            try:
                location = s3.get_bucket_location(Bucket=name)['LocationConstraint']
            except:
                location = "unknown"

            inventory.append(f"Bucket: {name} | Region: {location}\n")

            # 🚨 Public Access Block
            try:
                pab = s3.get_public_access_block(Bucket=name)
                if not all(pab['PublicAccessBlockConfiguration'].values()):
                    alerts.append(f"[HIGH] {name} Public Access Block disabled\n")
            except:
                alerts.append(f"[HIGH] {name} no Public Access Block\n")

            # 🚨 ACL Public
            acl = s3.get_bucket_acl(Bucket=name)
            for g in acl['Grants']:
                if "AllUsers" in str(g):
                    alerts.append(f"[HIGH] {name} PUBLIC via ACL\n")

            # 🔐 Encryption
            try:
                s3.get_bucket_encryption(Bucket=name)
            except:
                alerts.append(f"[MEDIUM] {name} no encryption\n")

            # 🧾 Logging
            try:
                log = s3.get_bucket_logging(Bucket=name)
                if 'LoggingEnabled' not in log:
                    alerts.append(f"[MEDIUM] {name} logging disabled\n")
            except:
                pass

    except Exception as e:
        alerts.append(f"[ERROR] S3: {str(e)}\n")

    return inventory, alerts



















