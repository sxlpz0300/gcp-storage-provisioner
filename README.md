# GCP Medallion & Orchestration Provisioner

Enterprise-ready infrastructure platform code to provision data engineering assets using Pulumi Cloud and Python.

## Prerequisites
- Active `gcloud` session with appropriate IAM impersonation roles.
- Python 3.10+ installed.

## Setup Instructions

1. **Rebuild Environment and Dependencies:**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

2. Run Unit Tests:
Validate naming conventions and structural parameters before communicating with the Cloud Provider API:
   ```bash
   $ pytest tests/
   ```

3. Deploy to Target Project Environment:
Ensure the identity impersonation is configured and deploy directly to your Pulumi Cloud Console Stack:

   # Establish the bypass bridge for ADC & Impersonation
   ```sh
   $ cp ~/.config/gcloud/legacy_credentials/*/adc.json ~/.config/gcloud/application_default_credentials.json 2>/dev/null
   
   # Set the environment variable to impersonate the deployment account
   $ export GOOGLE_IMPERSONATE_SERVICE_ACCOUNT="pulumi-local-deployer@your-gcp-project-id.iam.gserviceaccount.com"
   
   # Deploy using dev configuration file mapping
   $ pulumi login
   $ pulumi stack init dev
   $ pulumi up
   ```
   
-------------------------------------------------------------------------------
Outputs and Verification
-------------------------------------------------------------------------------
Once the deployment completes successfully, Pulumi Cloud will display the 
following structured metadata outputs:

- deployed_environment: The specific runtime context (e.g., "dev").
- storage_buckets: A dynamic map containing the absolute names and "gs://" 
  URLs for the bronze, silver, and gold storage layers.
- composer_env_name: The resource name of the active Cloud Composer cluster.
- airflow_ui_url: The direct secure web link to access the Airflow DAG 
  orchestration interface.