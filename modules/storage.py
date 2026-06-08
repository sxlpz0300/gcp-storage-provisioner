from typing import List
import pulumi
import pulumi_gcp as gcp

class MedallionStorage(pulumi.ComponentResource):
    """
    Component resource that provisions multiple Cloud Storage Buckets based on configuration.
    """
    def __init__(self, name: str, project_id: str, region: str, env: str, layers: List[dict], opts: pulumi.ResourceOptions = None):
        super().__init__("custom:gcp:MedallionStorage", name, {}, opts)
        
        self.bucket_outputs = {}
        
        for layer in layers:
            layer_name = layer.get("name")
            storage_class = layer.get("storage_class", "STANDARD")
            versioning_enabled = layer.get("versioning", False)
            
            # Formulating an enterprise-standard, collision-free bucket name
            full_bucket_name = f"{project_id}-{env}-{layer_name}-storage"
            
            bucket = gcp.storage.Bucket(
                f"{name}-{layer_name}-bucket",
                name=full_bucket_name,
                location=region,
                storage_class=storage_class,
                uniform_bucket_level_access=True,
                force_destroy=True,
                versioning=gcp.storage.BucketVersioningArgs(
                    enabled=versioning_enabled
                ),
                opts=pulumi.ResourceOptions(parent=self)
            )
            
            self.bucket_outputs[layer_name] = {
                "name": bucket.name,
                "url": bucket.url
            }
            
        self.register_outputs({"buckets": self.bucket_outputs})