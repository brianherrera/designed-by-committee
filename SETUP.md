# Setup Guide

This guide walks through setting up **Designed by Committee** after cloning the repository.
It covers required AWS permissions, local credentials, and installation steps.

## Prerequisites

Before you begin, ensure you have the following:

- **Python 3.10 or higher**
- **An AWS account with credentials configured with permission to invoke Bedrock models**

Designed by Committee relies on Amazon Bedrock for model execution via the
Strands Agents framework.

**Note:** This project uses Amazon Bedrock models that are available via **on-demand usage** only.
No provisioned throughput, reservations, or custom model configuration is required.

The specific models used by each committee member are defined in
[`committee_members.py`](src/dbc/committee/committee_members.py).

## 1. Configure AWS Permissions

Designed by Committee requires permission to invoke Bedrock foundation models.

Create an IAM user or role with the following policy attached:

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "bedrock:InvokeModel",
                "bedrock:InvokeModelWithResponseStream"
            ],
            "Resource": "*"
        }
    ]
}
```

**Notes:**

* This policy is intentionally minimal and scoped only to model invocation.

## 2. Configure AWS Credentials

Designed by Committee uses the standard AWS credential resolution chain.

You must provide credentials with permission to invoke Amazon Bedrock models.
How those credentials are supplied is up to you.

### Supported Credential Methods

Any of the following approaches will work:

#### Option 1: AWS CLI

```bash
aws configure
```

You will be prompted for:

* AWS Access Key ID
* AWS Secret Access Key
* Default region name (for example: `us-west-2`)
* Default output format (for example: `json`)

#### Option 2: Environment Variables

```bash
export AWS_ACCESS_KEY_ID=...
export AWS_SECRET_ACCESS_KEY=...
export AWS_DEFAULT_REGION=us-west-2
```

#### Option 3: IAM Role (for EC2 or other AWS-managed environments)

If running in an environment with an attached IAM role, no local credential configuration is required.

**Note:**

- Only the **default credential chain** is supported.
- Named AWS profiles are not yet supported.

## 3. Clone the Repository

```bash
git clone https://github.com/brianherrera/designed-by-committee.git
cd designed-by-committee
```

## 4. Install the Package

Using a virtual environment is strongly recommended.

```bash
# Create a virtual environment
python -m venv .venv

# Activate the virtual environment
# Linux / macOS
source .venv/bin/activate

# Windows
.venv\Scripts\activate

# Install the package
pip install .
```

This installs the `dbc` command-line interface into your active environment.

## 5. Verify the Installation

Run a simple kickoff command to confirm everything is working:

```bash
dbc kickoff "Design a web app to visualize server utilization"
```

If setup is successful, the committee will begin a multi-round discussion using
Amazon Bedrock models.

## Troubleshooting

If you encounter issues:

* Ensure credentials are configured for the default AWS profile
* Double-check that your virtual environment is active

You are now ready to bring the committee into session.
