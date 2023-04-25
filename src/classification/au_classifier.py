import os
import time

import clip
import joblib
import numpy as np
import torch
from PIL import Image
# gradientboosting
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split

from src.shared.image import crop_image, display_image
from src.shared.storage import Database, ImageStorage

WEIGHTS_PATH = "./db/local/models/au_classifier"


class AUClassifier:
    # CLIP_PATH = f"{WEIGHTS_PATH}/clip_model.pth"
    PREPROCESS_PATH = f"{WEIGHTS_PATH}/preprocess.pkl"
    CLASSIFIER_PATH = f"{WEIGHTS_PATH}/classifier.joblib"

    def __init__(self, train=False):
        if train:
            self._train()
        else:
            self._load()

    def _preprocess_crop(self, image):
        return crop_image(image, 0.95, 0.1, 0.02, 0.6)

    def _preprocess(self, image):
        preprocessed_image = self._preprocess_clip(self._preprocess_crop(image))
        with torch.no_grad():
            features_tensor = preprocessed_image.flatten()
            features = np.vstack([features_tensor.numpy()])
        return features

    def _train(self):
        local_path = "./db/shared/jpg"
        shared_path = "pkmncards/sets-eng/base"
        image_storage = ImageStorage(shared_path, db=Database.SHARED)

        keys = list(image_storage.get_all_keys())
        # randomize order
        np.random.shuffle(keys)

        paths = [f"{local_path}/{shared_path}/{key}.jpg" for key in keys]
        labels = [1 if key[-1] == "t" else 0 for key in keys]

        images = [self._preprocess_crop(Image.open(path)) for path in paths]

        self.clip_model, self._preprocess_clip = clip.load("ViT-B/32", device="cpu")
        self.clip_model.eval()

        with torch.no_grad():
            features_tensors = [
                self._preprocess_clip(image).flatten() for image in images
            ]
            features = np.vstack([tensor.numpy() for tensor in features_tensors])

        assert len(features) == len(labels)
        X_train, X_test, y_train, y_test = train_test_split(
            features, labels, test_size=0.1
        )

        def monitor(iteration, estimator, args):
            if iteration == 0:
                monitor.start_time = time.time()
            elif iteration % 10 == 0:
                elapsed_time = time.time() - monitor.start_time
                remaining_time = (
                    elapsed_time
                    / (iteration + 1)
                    * (estimator.n_estimators - iteration - 1)
                )
                print(
                    f"Iteration: {iteration + 1}, Remaining Time: {remaining_time:.2f} seconds"
                )

        # self.clf = LogisticRegression()
        # self.clf.fit(X_train, y_train)

        self.clf = GradientBoostingClassifier(n_estimators=10, learning_rate=0.1)
        self.clf.fit(X_train, y_train, monitor=monitor)

        y_pred = self.clf.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        print("Accuracy:", accuracy)

        for i in range(len(X_test)):
            true_label = y_test[i]
            predicted_label = y_pred[i]
            if true_label != predicted_label:
                print(f"Misidentified Image Index: {i}")
                print(f"True label: {true_label}, Predicted label: {predicted_label}")

                misidentified_image = Image.open(paths[i])
                print(paths[i])
                display_image(misidentified_image)

        if accuracy > 0.9:
            if not os.path.exists(WEIGHTS_PATH):
                os.makedirs(WEIGHTS_PATH)
            joblib.dump(self._preprocess_clip, self.PREPROCESS_PATH)
            joblib.dump(self.clf, self.CLASSIFIER_PATH)
        else:
            raise Exception("Accuracy too low")

    def _load(self):
        self._preprocess_clip = joblib.load(self.PREPROCESS_PATH)
        self.clf = joblib.load(self.CLASSIFIER_PATH)

    def is_au(self, image):
        features = self._preprocess(image)
        prob = self.clf.predict_proba(features)[0]
        return prob[0] > prob[1]


def main():
    classifier = AUClassifier(train=True)
