from aws_cdk import core, aws_codedeploy as codedeploy, aws_apigateway as apigateway, aws_lambda as lambda_
import random
import string
randomness = ''.join(random.choice(string.ascii_uppercase +
                                   string.ascii_lowercase + string.digits) for _ in range(8))


class LambdaStack(core.Stack):
    def __init__(self, app: core.App, id: str, config, **kwargs):
        super().__init__(app, id, **kwargs)

        self.lambda_code = lambda_.Code.from_cfn_parameters()

        func = lambda_.Function(self, "Lambda",
                                function_name=config["Default"]["project"] +
                                "-lambda-"+randomness,
                                code=self.lambda_code,
                                handler="index.handler",
                                runtime=lambda_.Runtime.NODEJS_12_X,
                                tracing=lambda_.Tracing.ACTIVE
                                )

        api = apigateway.RestApi(self, "lambda-service",
                                 rest_api_name="stepfunctions-demo-api-"+randomness,
                                 description="This service serves the lambda.",
                                 deploy_options={
                                     "logging_level": apigateway.MethodLoggingLevel.INFO,
                                     "tracing_enabled": True
                                 })

        get_lambda_integration = apigateway.LambdaIntegration(func,
                                                              request_templates={"text/html": '{ "statusCode": "200" }'})

        api.root.add_method("GET", get_lambda_integration)   # GET /

        version = func.latest_version
        alias = lambda_.Alias(self, "LambdaAlias",
                              alias_name="Prod", version=version)

        codedeploy.LambdaDeploymentGroup(self, "DeploymentGroup",
                                         alias=alias,
                                         deployment_config=codedeploy.LambdaDeploymentConfig.LINEAR_10_PERCENT_EVERY_1_MINUTE
                                         )
