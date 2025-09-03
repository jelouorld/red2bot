
import os 
import operator 

import boto3


import iface
import impl
import mock

# envs:
# local -> local > 
# cloud -> manual invoke 
# cloud -> scheduled <(special case) manual 
# LOCAL, MANUAL_INVOKE, SCHEDULED 


ddbr = boto3.resource("dynamodb")
ddbt = ddbr.Table("products")

dependencies: dict[str, dict] = {
    "LOCAL_DRY_RUN": {
        "datasource": mock.products,
        "destination": mock.dump_stdout 
    }, 
    "LOCAL": {
        "datasource": mock.products,
        "destination": impl.dynamodb
    },
    "CLI_INVOKE": {
        "datasource": mock.products,
        "destination": impl.dynamodb
    },
    "PROD": {
        "datasource": impl.products,
        "destination": impl.dynamodb
    }
}


def resolve(datasource: iface.DataSource, destination: iface.DataDestination) -> None:
    # TODO: improve it with pipeline architecture if that makes sense.
    for product in datasource:
        destination.push(product)

def lambda_entrypoint(event, context):
    deps: dict = dependencies[os.environ.get("FETCHER_ENV")]

    result = resolve(**{
        name: operator.call(dependency) 
        for name, dependency in deps.items()
    })

    return {"statusCode": 200, "body": result}

if __name__ == "__main__":
    # enbles local run
    lambda_entrypoint(None, None) 