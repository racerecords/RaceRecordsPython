#!/bin/bash
aws cloudformation package --region us-east-1 --template template.yaml --s3-bucket aws-codestar-us-east-1-249502774627-race-records-pipe --output-template template-export.yml
