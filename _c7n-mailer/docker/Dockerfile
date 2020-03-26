FROM python:3.7-slim-stretch

LABEL name="custodian" \
      description="Cloud Management Rules Engine" \
      repository="http://github.com/cloud-custodian/cloud-custodian" \
      homepage="http://github.com/cloud-custodian/cloud-custodian" \
      maintainer="Custodian Community <https://cloudcustodian.io>"

ADD setup.py requirements.txt README.md /src/
ADD c7n /src/c7n/
ADD tools /src/tools/

WORKDIR /src
RUN adduser --disabled-login custodian
RUN apt-get --yes update && apt-get --yes upgrade \
 && apt-get --yes install build-essential \
 && pip3 install -r requirements.txt  . \
 && pip3 install -r tools/c7n_mailer/requirements.txt tools/c7n_mailer 
 
# cleanup
RUN apt-get --yes remove build-essential \
 && apt-get purge --yes --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
 && rm -Rf /var/cache/apt/ \
 && rm -Rf /var/lib/apt/lists/* \
 && rm -Rf /src/ \
 && rm -Rf /root/.cache/

# OKTA cli installation
RUN pip install okta-awscli
RUN touch ~/.okta-aws
RUN echo "[default]" > ~/.okta-aws
RUN echo "base-url = xyz.okta.com" >> ~/.okta-aws

# update image
RUN apt-get update
RUN apt-get install -y \
    vim \
    git

# aws-cli
RUN pip3 install awscli --upgrade --user
RUN export PATH=/root/.local/bin:$PATH
RUN echo "PATH=/root/.local/bin:$PATH" >> /root/.profile
# RUN source ~/.profile 

# git clone cloud-custodian NEED SOME CLEANUP here
WORKDIR /tmp
RUN git clone https://github.com/cloud-custodian/cloud-custodian.git
RUN export AWS_DEFAULT_REGION='us-east-2'


USER root
