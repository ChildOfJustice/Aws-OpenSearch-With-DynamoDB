#!/bin/bash
PackagedCFTemplatePath="PackagedCloudFormationTemplate.yml"
S3BucketName="sardor-test-code"

rm -rf $PackagedCFTemplatePath
aws cloudformation package --template template.yml --s3-bucket $S3BucketName --output-template-file $PackagedCFTemplatePath
aws cloudformation deploy \
 	--template-file $PackagedCFTemplatePath \
 	--stack-name ddb-opensearch-stack \
 	--capabilities CAPABILITY_NAMED_IAM \
 	--region eu-central-1
