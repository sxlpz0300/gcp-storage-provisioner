import pytest
import pulumi

# Import local modules to test their logic structures
from modules import MedallionStorage

@pulumi.runtime.test
def test_medallion_storage_bucket_naming(setup_pulumi_mocks):
    """Validates that bucket names adhere to the deployment naming standards without collisions."""
    mock_layers = [{"name": "bronze", "storage_class": "STANDARD", "versioning": True}]
    
    storage = MedallionStorage(
        name="test-lake",
        project_id="test-project",
        region="us-central1",
        env="dev",
        layers=mock_layers
    )

    def check_bucket_name(args):
        bucket_name = args[0]
        assert bucket_name == "test-project-dev-bronze-storage", f"Standard naming convention violated: {bucket_name}"

    return pulumi.Output.all(storage.bucket_outputs["bronze"]["name"]).apply(check_bucket_name)