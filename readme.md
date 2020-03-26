# AWS Cloud Custodian (c7n)

**Why we chose c7n**

Cloud Custodian is an open source tool to bring automated governance, security, compliance, and cost optimization to cloud environments. 

Cloud Custodian has following key features:

- Ensure real-time compliance.

- Manage costs by setting up off-hours to turn off resources.

- Multi-cloud support e.g. AWS, GCP, Azure.


**c7n-mailer**

Its used to send outbound mail delivery.

The _c7n-mailer directory structure:
```
- Dockerfile
- environment/accounts.yml (used for c7n-org deployment)
- environment/mailer.yml (used to specify mailer properties like SQS, SMTP details)
```

**templates**

left it blank intentionally, you can create your own template or use default.


**support directory contains**

some handy script that I used to debug the deployment and extra stuff
