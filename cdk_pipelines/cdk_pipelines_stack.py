from aws_cdk import (core, aws_codebuild as codebuild,
                     aws_codecommit as codecommit,
                     aws_codepipeline as codepipeline,
                     aws_codepipeline_actions as codepipeline_actions,
                     aws_lambda as lambda_, aws_s3 as s3)


class PipelineStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, *,
                 lambda_code: lambda_.CfnParametersCode = None, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        code = codecommit.Repository.from_repository_name(self, "ImportedRepo",
                                                          "pipeline-stack")

        cdk_build = codebuild.PipelineProject(self, "CdkBuild",
                                              build_spec=codebuild.BuildSpec.from_object(dict(
                                                  version="0.2",
                                                  phases=dict(
                                                      install=dict(
                                                          commands=[
                                                              "npm install -g aws-cdk",
                                                              "python -m ensurepip --upgrade",
                                                              "python -m pip install --upgrade pip",
                                                              "python -m pip install --upgrade virtualenv",
                                                              "virtualenv .env",
                                                              ". .env/bin/activate",
                                                              "pip install -r requirements.txt",
                                                              "pip install aws_cdk.aws_codedeploy aws_cdk.aws_lambda aws_cdk.aws_codebuild aws_cdk.aws_codepipeline",
                                                              "pip install aws_cdk.aws_codecommit aws_cdk.aws_codepipeline_actions aws_cdk.aws_s3"]),
                                                      build=dict(commands=[
                                                          "cdk synth PipelineDeployingLambdaStack"])),
                                                  artifacts={
                                                      "base-directory": "cdk.out",
                                                      "files": [
                                                          "LambdaStack.template.json"]},
                                                  environment=dict(buildImage=codebuild.LinuxBuildImage.STANDARD_2_0))))

        lambda_build = codebuild.PipelineProject(self, 'LambdaBuild',
                                                 build_spec=codebuild.BuildSpec.from_object(dict(
                                                     version="0.2",
                                                     phases=dict(
                                                         install=dict(
                                                             commands=[
                                                                 "cd lambda",
                                                                 "npm install"]),
                                                         build=dict(
                                                             commands="npm run build")),
                                                     artifacts={
                                                         "base-directory": "lambda",
                                                         "files": [
                                                             "index.js",
                                                             "node_modules/**/*"]},
                                                     environment=dict(buildImage=codebuild.LinuxBuildImage.STANDARD_2_0))))

        source_output = codepipeline.Artifact()
        cdk_build_output = codepipeline.Artifact("CdkBuildOutput")
        lambda_build_output = codepipeline.Artifact("LambdaBuildOutput")

        lambda_location = lambda_build_output.s3_location

        codepipeline.Pipeline(self, "Pipeline",
                              stages=[
                                  codepipeline.StageProps(stage_name="Source",
                                                          actions=[
                                                              codepipeline_actions.CodeCommitSourceAction(
                                                                  action_name="CodeCommit_Source",
                                                                  repository=code,
                                                                  output=source_output)]),
                                  codepipeline.StageProps(stage_name="Build",
                                                          actions=[
                                                              codepipeline_actions.CodeBuildAction(
                                                                  action_name="Lambda_Build",
                                                                  project=lambda_build,
                                                                  input=source_output,
                                                                  outputs=[lambda_build_output]),
                                                              codepipeline_actions.CodeBuildAction(
                                                                  action_name="CDK_Build",
                                                                  project=cdk_build,
                                                                  input=source_output,
                                                                  outputs=[cdk_build_output])]),
                                  codepipeline.StageProps(stage_name="Deploy",
                                                          actions=[
                                                              codepipeline_actions.CloudFormationCreateUpdateStackAction(
                                                                  action_name="Lambda_CFN_Deploy",
                                                                  template_path=cdk_build_output.at_path(
                                                                      "LambdaStack.template.json"),
                                                                  stack_name="LambdaDeploymentStack",
                                                                  admin_permissions=True,
                                                                  parameter_overrides=dict(
                                                                      lambda_code.assign(
                                                                          bucket_name=lambda_location.bucket_name,
                                                                          object_key=lambda_location.object_key,
                                                                          object_version=lambda_location.object_version)),
                                                                  extra_inputs=[lambda_build_output])])
                              ]
                              )
