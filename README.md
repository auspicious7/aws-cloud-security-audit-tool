## 🏗️ Architecture Overview

```mermaid
flowchart TD

%% Styles
classDef aws fill:#FF9900,stroke:#232F3E,color:#fff
classDef service fill:#1f77b4,stroke:#0d3b66,color:#fff
classDef output fill:#2ca02c,stroke:#145a32,color:#fff
classDef alert fill:#d62728,stroke:#7b241c,color:#fff

%% Nodes
A[AWS Account (Target)]:::aws --> B[Boto3 Session]:::service

%% Services
subgraph Security Checks
C[EC2 Check]:::service
D[S3 Check]:::service
E[IAM Check]:::service
F[RDS Check]:::service
G[VPC Check]:::service
end

B --> C
B --> D
B --> E
B --> F
B --> G

%% Outputs
C --> H[Inventory Data]:::output
D --> H
E --> H
F --> H
G --> H

C --> I[Security Alerts]:::alert
D --> I
E --> I
F --> I
G --> I

H --> J[output.txt]:::output
I --> K[output_alerts.txt]:::alert

This tool uses a Boto3 session to connect to an AWS account and perform security checks across multiple services.  
Each service module analyzes configurations and returns:

- Inventory data (resources information)
- Alerts (security misconfigurations)

Finally, all results are aggregated and written into structured output reports.



# 🔐 AWS Cloud Security Audit Tool

A Python-based **AWS Cloud Security Audit Tool** designed to identify misconfigurations and potential security risks across AWS services.

This tool performs a **comprehensive security audit of your AWS environment**.
Currently, it focuses on **core and critical AWS services**, but it is designed to be extended to cover more services in the future.

---

## 🚀 What This Tool Does

* 🌍 Performs **multi-region scanning**
* 🔐 Audits important AWS services like:

  * EC2 (Public access, IMDSv2, Encryption)
  * S3 (Public access, Encryption, Logging)
  * IAM (MFA, Access keys, User security)
  * RDS (Public DB, Encryption)
  * VPC (Basic configuration checks)
* 🌐 Handles both **global (IAM, S3)** and **regional services**
* 📄 Generates **two separate reports**:

  * Full AWS inventory
  * Security findings (alerts)

---

## 📂 Output Files

After running the tool, you will find results inside the `output/` folder:

* `output.txt` → Contains **complete AWS inventory details**
* `output_alerts.txt` → Contains **all detected security issues**

---

## ⚙️ Setup & Installation

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/your-username/aws-cloud-security-audit-tool.git
cd aws-cloud-security-audit-tool
```

---

### 2️⃣ Create Virtual Environment

```bash
python -m venv venv
```

Activate it:

* Linux / Mac:

```bash
source venv/bin/activate
```

* Windows:

```bash
venv\Scripts\activate
```

---

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

### 4️⃣ Configure AWS Credentials

Create a `.env` file and add your AWS credentials:

```env
AWS_ACCESS_KEY_ID=your_access_key
AWS_SECRET_ACCESS_KEY=your_secret_key
```

👉 Make sure:

* IAM user has **required read permissions**
* (EC2, S3, IAM, RDS, VPC, CloudTrail, etc.)

---

### 5️⃣ Run the Tool

```bash
python main.py
```

---

### 6️⃣ Check Results

Go to the `output/` folder:

* 📄 `output.txt` → Full AWS audit data
* 🚨 `output_alerts.txt` → Security findings

---

## 🎯 Note

This tool is built with a **cloud security mindset**, focusing on identifying real-world misconfigurations used in **security audits and penetration testing**.

---

## ⚡ Future Improvements

* Add more AWS services (Lambda, CloudFront, EKS, etc.)
* Severity-based alert classification
* HTML dashboard reporting

---

## 👨‍💻 Author

Built by Gulshan Kumar 🚀
