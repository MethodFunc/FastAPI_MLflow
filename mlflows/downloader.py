import os
from pathlib import Path
from mlflow.tracking import MlflowClient

MODEL_PATH = 'mlflow_model'

#Tracking Database 와 ArtifactURI입력
# ArtifactURI = sftp 서버
os.environ['MLFLOW_TRACKING_URI'] = 'postgresql+psycopg2://dev:dev1234@localhost:5432/mlflow_test'
os.environ['MLFLOW_ARTIFACT_URI'] = 'sftp://dev:dev1234@localhost:14022/mlflow/'


def download_all_path(output_path=MODEL_PATH):
    client = MlflowClient()
    registered_list = client.list_registered_models()
    model_name_list = [lr.name for lr in registered_list]
    mlflow_run_id_artifacts_name = 'model'

    for model_name in model_name_list:
        filter_string = f"name='{model_name}'"

        for rm in client.search_model_versions(filter_string):
            if rm.current_stage == 'Production':
                deploy_version = rm.version
                run_id = rm.run_id

        dst = Path(f'{output_path}/{model_name}')
        if not dst.exists():
            dst.mkdir(parents=True, exist_ok=True)

        model_uri = client.get_model_version_download_uri(model_name, deploy_version)
        mlflow_run_id = run_id

        client.download_artifacts(mlflow_run_id, mlflow_run_id_artifacts_name, dst_path=dst)


if __name__ == '__main__':
    download_all_path()
