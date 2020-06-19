#!/usr/bin/env python3

from aws_cdk import core

from cdk_pipelines.pipelines_stack import PipelineStack
from cdk_pipelines.lambda_stack import LambdaStack
from cdk_pipelines.codecommit_repo_stack import CodecommitRepoStack

import configparser

# have to add a dummy section header to please configparser
with open('demo-config.ini') as f:
    file_content = '[Default]\n' + f.read()

config = configparser.RawConfigParser()
config.read_string(file_content)

app = core.App()

lambda_stack = LambdaStack(app, "LambdaStack", config)

PipelineStack(app, "PipelineDeployingLambdaStack", config,
              lambda_code=lambda_stack.lambda_code)

CodecommitRepoStack(app, "RepoStack", config)

core.Tag.add(lambda_stack, "CreatedBy", "PipelineDeployingLambdaStack")

app.synth()
