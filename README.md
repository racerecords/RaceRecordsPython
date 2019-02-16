# RaceRecords

This is a project for learning [AWS SAM](https://github.com/awslabs/serverless-application-model) and the surrounding server-less tech stack required to deploy a dynamic website hosted on S3 and Lambda.  This is a focus on back-end technology and DevOps automation. I'm also learning python for the first time while I'm at it.

## Requirements

* [AWS SAM](https://github.com/awslabs/serverless-application-model)
    * AWS CLI already configured with Administrator permission
    * [Python 3 installed](https://www.python.org/downloads/)
    * [Docker installed](https://www.docker.com/community-edition)
    * [Python Virtual Environment](http://docs.python-guide.org/en/latest/dev/virtualenvs/)

## Notes from AWS SAM

### Packaging and deployment

AWS Lambda Python runtime requires a flat folder with all dependencies including the application. SAM will use `CodeUri` property to know where to look up for both application and dependencies:

```yaml
...
    HelloWorldFunction:
        Type: AWS::Serverless::Function
        Properties:
            CodeUri: hello_world/
            ...
```

Firstly, we need a `S3 bucket` where we can upload our Lambda functions packaged as ZIP before we deploy anything - If you don't have a S3 bucket to store code artifacts then this is a good time to create one:

```bash
aws s3 mb s3://BUCKET_NAME
```

Next, run the following command to package our Lambda function to S3:

```bash
sam package \
    --template-file template.yaml \
    --output-template-file packaged.yaml \
    --s3-bucket REPLACE_THIS_WITH_YOUR_S3_BUCKET_NAME
```

Next, the following command will create a Cloudformation Stack and deploy your SAM resources.

```bash
sam deploy \
    --template-file packaged.yaml \
    --stack-name sam-app \
    --capabilities CAPABILITY_IAM
```

> **See [Serverless Application Model (SAM) HOWTO Guide](https://github.com/awslabs/serverless-application-model/blob/master/HOWTO.md) for more details in how to get started.**

After deployment is complete you can run the following command to retrieve the API Gateway Endpoint URL:

```bash
aws cloudformation describe-stacks \
    --stack-name sam-app \
    --query 'Stacks[].Outputs'
``` 

### Testing

We use **Pytest** and **pytest-mock** for testing our code and you can install it using pip: ``pip install pytest pytest-mock`` 

Next, we run `pytest` against our `tests` folder to run our initial unit tests:

```bash
pipenv run pytest tests/ -v
```
**NOTE:** You can find more information about Virtual Environment at [Python Official Docs here](https://docs.python.org/3/tutorial/venv.html). Alternatively, you may want to look at [Pipenv](https://github.com/pypa/pipenv) as the new way of setting up development workflows

### AWS CLI commands

AWS CLI commands to package, deploy and describe outputs defined within the cloudformation stack:

```bash
sam package \
    --template-file template.yaml \
    --output-template-file packaged.yaml \
    --s3-bucket REPLACE_THIS_WITH_YOUR_S3_BUCKET_NAME

sam deploy \
    --template-file packaged.yaml \
    --stack-name sam-app \
    --capabilities CAPABILITY_IAM \
    --parameter-overrides MyParameterSample=MySampleValue

aws cloudformation describe-stacks \
    --stack-name sam-app --query 'Stacks[].Outputs'
```

### Bringing to the next level

Here are a few ideas that you can use to get more acquainted as to how this overall process works:

* Create an additional API resource (e.g. /hello/{proxy+}) and return the name requested through this new path
* Update unit test to capture that
* Package & Deploy

Next, you can use the following resources to know more about beyond hello world samples and how others structure their Serverless applications:

* [AWS Serverless Application Repository](https://aws.amazon.com/serverless/serverlessrepo/)
* [Chalice Python Serverless framework](https://github.com/aws/chalice)
* Sample Python with 3rd party dependencies, pipenv and Makefile: ``sam init --location https://github.com/aws-samples/cookiecutter-aws-sam-python``
