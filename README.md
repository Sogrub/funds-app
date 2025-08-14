# Funds App - Deployment on AWS with CloudFormation

This repository contains the **AWS CloudFormation template** to deploy the `funds-app` application on an EC2 instance with FastAPI and systemd.  

It also includes a step-by-step guide to manually deploy the infrastructure using the AWS console.

---

## Prerequisites

Before deploying the infrastructure, make sure you have:

- An active AWS account.
- A Key Pair in your desired region (to access the EC2 instance via SSH).
- Internet connection and sufficient permissions to create EC2, Security Groups, and CloudFormation stacks.
- Optional: AWS CLI configured if you prefer using it instead of the web console.

---

## Manual Deployment Steps

1. **Access CloudFormation**

   - Go to the [AWS Console](https://aws.amazon.com/console/).
   - Search for **CloudFormation** and click **Create stack** → **With new resources (standard)**.

2. **Upload the Template**

   - Select **Upload a template file**.
   - Click **Choose file** and select `cloudformation.yaml` from this repository.
   - Click **Next**.

3. **Configure the Stack**

   - Enter a name for your stack, e.g., `funds-app-stack`.
   - Fill in any required template parameters, for example:
     - `KeyName`: your AWS Key Pair.
   - Click **Next**.

4. **Configure Additional Options (Optional)**

   - Add tags, permissions, or policies if desired.
   - Click **Next**.

5. **Review and Create Stack**

   - Review all details to ensure everything is correct.
   - Check the acknowledgment box if necessary (**I acknowledge that AWS CloudFormation might create IAM resources**).
   - Click **Create stack**.

6. **Wait for Stack Creation**

   - CloudFormation will start creating resources.  
   - You can monitor progress in the **Events** tab.  
   - Once the status changes to **CREATE_COMPLETE**, your infrastructure is ready.

7. **Access the Application**

   - Get the **public IP** of the EC2 instance (from the Outputs tab or EC2 console).  
   - Open a browser and navigate to:

     ```
     http://<EC2_PUBLIC_IP>:8000/docs
     ```

   - You can access the FastAPI documentation at `/docs` or Redoc at `/redoc`.

---

## Security and Best Practices

- **Do not commit secrets or keys** to the repository.  
  - The template uses environment variables for AWS keys. Use **Secrets Manager** or **Parameter Store**.
- Configure the **Security Group** to restrict access only to necessary IPs in production.
- Check the systemd service logs on the EC2 instance:

  ```bash
  sudo journalctl -u fundsapp -f
  ```

### To stop the service:
  ```bash
  sudo systemctl stop fundsapp
  ```

### To restart the service:
  ```bash
  sudo systemctl restart fundsapp
  ```