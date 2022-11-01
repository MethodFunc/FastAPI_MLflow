import mlflow
from mlflow.tracking import MlflowClient


def model_register(model_name, artifact_uri, run_id):
    client = MlflowClient()
    try:
        client.create_registered_model(model_name)
    except mlflow.exceptions.MlflowException:
        print(f'{model_name} is exists')

    client.create_model_version(
        name=model_name,
        source=f"{artifact_uri}/{run_id}/artifacts/model",
        run_id=run_id,
        description=f'{model_name}',
        tags={
        }
    )

    filter_string = f"name='{model_name}'"

    model_version = client.search_model_versions(filter_string)
    current_version = len(model_version)
    for i in range(len(model_version)):
        if model_version[i].current_stage == 'Production':
            client.transition_model_version_stage(
                name=model_name,
                version=model_version[i].version,
                stage='None'
            )

    client.transition_model_version_stage(
        name=model_name,
        version=current_version,
        stage='Production'
    )
