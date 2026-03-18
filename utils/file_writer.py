import os

os.makedirs("output", exist_ok=True)

def write_inventory(data):
    with open("output/output.txt", "w") as f:
        f.write("===== CLOUD INVENTORY REPORT =====\n\n")
        for line in data:
            f.write(line)
        f.write("\n===== END =====\n")


def write_alerts(data):
    with open("output/alerts.txt", "w") as f:
        f.write("===== SECURITY ALERTS =====\n\n")
        for line in data:
            f.write(line)
        f.write("\n===== END =====\n")














