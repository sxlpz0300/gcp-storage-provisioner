import pulumi
import pytest

class MyMocks(pulumi.runtime.Mocks):
    def new_resource(self, args: pulumi.runtime.MockResourceArgs):
        outputs = args.inputs
        if args.typ == "gcp:storage/bucket:Bucket":
            outputs = {**args.inputs, "url": f"gs://{args.inputs.get('name')}"}
        if args.typ == "gcp:composer/environment:Environment":
            outputs = {**args.inputs, "config": {"airflow_uri": "https://airflow.gcp.url"}}
        return [args.name + "_id", outputs]

    def call(self, args: pulumi.runtime.MockCallArgs):
        return {}

@pytest.fixture(scope="module")
def setup_pulumi_mocks():
    pulumi.runtime.set_mocks(
        MyMocks(),
        project="gcp-platform-orchestrator",
        stack="dev",
        preview=False
    )