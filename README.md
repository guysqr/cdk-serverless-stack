# CodePipeline Lambda Deployer

This CDK project sets up a pipeline for deploying an API Gateway fronted Lambda function via CodePipeline. It is linked to a CodeCommit repository which triggers a deployment when changes are committed.

When run, CodePipeline's build stage runs CodeBuild and builds the Lambda function and uses the CDK to build the Lambda/API Gateway deployment stack. Finally CodeDeploy runs a deployment using the CDK-generated CloudFormation to deploy the Lambda code.

[Install the CDK for python before you start.](https://docs.aws.amazon.com/cdk/latest/guide/getting_started.html)

## Configuration

There is a file `demo-config.ini` in the root directory that you should configure first. It contains the following items:

```
project=demoproject
name=demorepo
count=5
```

These are picked up and used in python and shell scripts to make getting set up easier. Note that we need these to be compatible with AWS naming rules so please stick to alphanumerics for the first two and an integer for the last, as per the defaults.

This project is set up like a standard Python project. The initialization
process also creates a virtualenv within this project, stored under the .env
directory. To create the virtualenv it assumes that there is a `python3`
(or `python` for Windows) executable in your path with access to the `venv`
package. If for any reason the automatic creation of the virtualenv fails,
you can create the virtualenv manually.

To manually create a virtualenv on MacOS and Linux:

```
$ python3 -m venv .env
```

After the init process completes and the virtualenv is created, you can use the following
step to activate your virtualenv.

```
$ source .env/bin/activate
```

If you are a Windows platform, you would activate the virtualenv like this:

```
% .env\Scripts\activate.bat
```

Once the virtualenv is activated, you can install the required dependencies.

```
$ pip install -r requirements.txt
```

At this point you can now synthesize the CloudFormation template for this code.

```
$ cdk synth
```

If everything works as expected, you can deploy the stack - note the two context variables name and count that can be used to set the names of the created resources to allow you to match them to the repos you've created in step 1, and control how many instances of the pipelines you want.

```
$ cdk deploy PipelineDeployingLambdaStack -c name=stepfunctions-pipeline-repo -c count=5
```

to deploy it to your account.

To add additional dependencies, for example other CDK libraries, just add
them to your `setup.py` file and rerun the `pip install -r requirements.txt`
command.

## Useful commands

- `cdk ls` list all stacks in the app
- `cdk synth` emits the synthesized CloudFormation template
- `cdk deploy` deploy this stack to your default AWS account/region
- `cdk diff` compare deployed stack with current state
- `cdk docs` open CDK documentation

Enjoy!
