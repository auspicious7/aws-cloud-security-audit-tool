def run(session):
    inventory = ["\n[ RDS DETAILS ]\n"]
    alerts = ["\n[ RDS ALERTS ]\n"]

    rds = session.client('rds')

    try:
        dbs = rds.describe_db_instances()['DBInstances']

        if not dbs:
            inventory.append("No RDS instances found\n")

        for db in dbs:
            name = db['DBInstanceIdentifier']
            public = db['PubliclyAccessible']
            encrypted = db['StorageEncrypted']

            inventory.append(f"DB: {name} | Public: {public}\n")

            if public:
                alerts.append(f"[HIGH] {name} is public\n")

            if not encrypted:
                alerts.append(f"[HIGH] {name} not encrypted\n")

    except Exception as e:
        alerts.append(f"[ERROR] RDS: {str(e)}\n")

    return inventory, alerts





















# def run(session):
#     inventory = ["\n[ RDS DETAILS ]\n"]
#     alerts = ["\n[ RDS ALERTS ]\n"]

#     rds = session.client('rds')
#     dbs = rds.describe_db_instances()['DBInstances']

#     for db in dbs:
#         name = db['DBInstanceIdentifier']
#         public = db['PubliclyAccessible']

#         inventory.append(f"DB: {name} | Public: {public}\n")

#         if public:
#             alerts.append(f"[!] RDS {name} is PUBLIC\n")

#     return inventory, alerts