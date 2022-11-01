import pickle
from pathlib import Path

from neuralprophet import NeuralProphet


class NeuralModel(NeuralProphet):
    def save_model(self, path):
        path = Path(path)

        with open(path, 'wb') as f:
            pickle.dump(self.model, f)

    @classmethod
    def load_model(cls, path):
        path = Path(path)

        if not path.exists():
            raise f'{path} is not exist.'

        with open(path, 'rb') as f:
            model = pickle.load(f)

        return model
