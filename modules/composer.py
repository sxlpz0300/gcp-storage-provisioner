import pulumi
import pulumi_gcp as gcp

class OrchestratorComposer(pulumi.ComponentResource):
    """
    Component resource to provision a GCP Cloud Composer environment with specific PyPI packages.
    """
    def __init__(self, name: str, project_id: str, region: str, env: str, config: dict, opts: pulumi.ResourceOptions = None):
        super().__init__("custom:gcp:OrchestratorComposer", name, {}, opts)
        
        env_name = f"{env}-{config.get('name', 'orchestrator')}-env"
        pypi_packages = config.get("pypi_packages", {})
        
        composer_env = gcp.composer.Environment(
            f"{name}-env",
            name=env_name,
            region=region,
            config=gcp.composer.EnvironmentConfigArgs(
                software_config=gcp.composer.EnvironmentConfigSoftwareConfigArgs(
                    image_version=config.get("image_version"),
                    pypi_packages=pypi_packages
                ),
                environment_size=config.get("environment_size", "ENVIRONMENT_SIZE_SMALL")
            ),
            opts=pulumi.ResourceOptions(parent=self)
        )
        
        self.composer_name = composer_env.name
        self.airflow_uri = composer_env.config.airflow_uri
        
        self.register_outputs({
            "composer_name": self.composer_name,
            "airflow_uri": self.airflow_uri
        })