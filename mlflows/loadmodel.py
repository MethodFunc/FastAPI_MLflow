import mlflow.pyfunc


def load_model(model_name):
    MODEL_PATH = 'mlflow_model'
    model = mlflow.pyfunc.load_model(f'{MODEL_PATH}/{model_name}/model')

    return model
