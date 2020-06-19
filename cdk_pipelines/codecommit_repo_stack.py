from aws_cdk import core

import aws_cdk.aws_codecommit as codecommit
import configparser

#have to add a dummy section header to please configparser
with open('demo-config.ini') as f:
    file_content = '[Default]\n' + f.read()

config = configparser.RawConfigParser()
config.read_string(file_content)

class CodecommitRepoStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # The code that defines your stack goes here
        repo_name = self.node.try_get_context(
            "name") or config["Default"]["name"]
        repo_count = self.node.try_get_context(
            "count") or config["Default"]["count"]

        for i in range(1, int(repo_count)+1):
            codecommit.Repository(self, "Repository" +
                                  str(i),
                                  repository_name=repo_name + '-' +
                                  str(i),
                                  description="Repo number " +
                                  str(i) + " of " +
                                  repo_count
                                  )
