bucket=race-records-package
stackName=race-records-b
sam package --template-file template.yaml --output-template-file packaged.yaml --s3-bucket $bucket
sam deploy --template-file packaged.yaml --stack-name $stackName --capabilities CAPABILITY_IAM --region us-east-1
