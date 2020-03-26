# there are few files/directories missing from this repo
# you would need to download it form base c7n repo

# Use virtualenv/Docker image to run c7n-mailer

    docker run \
    -v _c7n-mailer/templates:/tmp/templates \
    -v _c7n-mailer/environments:/tmp/environments \
    -v policies:/tmp/policies \
    -it cloudvar/c7n-mailer:latest bash

**AWS path in docker image**

    root/.local/bin/aws

**Install mailer if not installed by default**

    pip3 install c7n-mailer

**Push new templates**

    cp templates/* ./custodian/lib/python3.7/site-packages/c7n_mailer/msg-templates/

**Deploy mailer**

    c7n-mailer --config /tmp/environments/mailer-nonprod.yml --update-lambda

**Test sample policy**

    custodian run -c sample-slack-policy.yml -s /tmp/out

**Test mailer**

    c7n-mailer-replay -c ../environments/mailer-nonprod.yml -t templates/default.html.j2 -p ../sample-sqs-message.json