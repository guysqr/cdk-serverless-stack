#!/usr/bin/env python3

from aws_cdk import core

from cdk_pipelines.pipelines_stack import PipelineStack
from cdk_pipelines.lambda_stack import LambdaStack
from cdk_pipelines.codecommit_repo_stack import CodecommitRepoStack

app = core.App()

lambda_stack = LambdaStack(app, "LambdaStack")

PipelineStack(app, "PipelineDeployingLambdaStack",
              lambda_code=lambda_stack.lambda_code)

CodecommitRepoStack(app, "RepoStack")

core.Tag.add(lambda_stack, "CreatedBy", "PipelineDeployingLambdaStack")

app.synth()
