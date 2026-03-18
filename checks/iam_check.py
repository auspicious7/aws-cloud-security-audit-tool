def run(session):
    inventory = ["\n[ IAM DETAILS ]\n"]
    alerts = ["\n[ IAM ALERTS ]\n"]

    iam = session.client('iam')

    # 🔥 Root MFA Check
    try:
        summary = iam.get_account_summary()['SummaryMap']
        if summary.get('AccountMFAEnabled') == 0:
            alerts.append("[CRITICAL] Root account MFA disabled\n")
    except:
        alerts.append("[INFO] Cannot check root MFA (permission issue)\n")

    try:
        users = iam.list_users()['Users']

        if not users:
            inventory.append("No IAM users found\n")

        for user in users:
            username = user['UserName']
            inventory.append(f"User: {username}\n")

            # MFA Check
            try:
                mfa = iam.list_mfa_devices(UserName=username)['MFADevices']
                if not mfa:
                    alerts.append(f"[HIGH] {username} no MFA\n")
            except:
                alerts.append(f"[INFO] Cannot check MFA for {username}\n")

    except:
        alerts.append("[ERROR] Cannot list IAM users\n")

    return inventory, alerts



















# def run(session):
#     inventory = ["\n[ IAM DETAILS ]\n"]
#     alerts = ["\n[ IAM ALERTS ]\n"]

#     iam = session.client('iam')
#     users = iam.list_users()['Users']

#     for user in users:
#         username = user['UserName']
#         inventory.append(f"User: {username}\n")

#         mfa = iam.list_mfa_devices(UserName=username)['MFADevices']
#         if not mfa:
#             alerts.append(f"[!] User {username} has NO MFA\n")

#     return inventory, alerts