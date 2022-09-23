# Grindery Ping Connector

firebaseCloudMessaging driver for Grindery Nexus


## [CDS Link](https://github.com/grindery-io/grindery-nexus-schema-v2/blob/master/cds/web2/firebaseCloudMessagingConnector.json)


## Development locally

Steps:

    1. Clone/pull/download this repository
    2. Create a virtualenv with virtualenv env and install dependencies with pip install -r requirements.txt
    3. Configure your .env variables
        You need to set following variables, also you can get the values from https://console.cloud.google.com/iam-admin/serviceaccounts?authuser=0&project=grindery-ping
        project_id, private_key_id, private_key, client_email, client_id, auth_uri, token_uri, auth_provider_x509_cert_url, client_x509_cert_url



## Deployment
Google Cloud will deploy any changes in the `main`, `staging` branch automatically







