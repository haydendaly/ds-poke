import os
import time

import clip
import joblib
import matplotlib.pyplot as plt
import numpy as np
import torch
from PIL import Image
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC

from ..image import crop_image

WEIGHTS_PATH = "./db/models/label_classifier/"


class LabelClassifier:
    CLIP_PATH = f"{WEIGHTS_PATH}clip_model.pth"
    PREPROCESS_PATH = f"{WEIGHTS_PATH}preprocess.pkl"
    CLASSIFIER_PATH = f"{WEIGHTS_PATH}classifier.joblib"

    def __init__(self, train=False):
        if train:
            self._train()
        else:
            self._load()

    def _preprocess_crop(self, image):
        return crop_image(image, top=0.05, right=0.1, bottom=0.72, left=0.1)

    def _preprocess(self, image):
        preprocessed_image = self._preprocess_clip(self._preprocess_crop(image))
        with torch.no_grad():
            features_tensor = preprocessed_image.flatten()
            features = np.vstack([features_tensor.numpy()])
        return features

    def _train(self):
        base_path = "./db/cgc/labels/"
        front, back = os.listdir(base_path + "front/"), os.listdir(base_path + "back/")
        image_paths = [f"{base_path}front/{img}" for img in front]
        image_paths.extend([f"{base_path}back/{img}" for img in back])
        labels = [0] * len(front)
        labels.extend([1] * len(back))
        images = [self._preprocess_crop(Image.open(path)) for path in image_paths]

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

        # Also tried LogisticRegression, SVC, and GradientBoostingClassifier
        self.clf = LogisticRegression()
        self.clf.fit(X_train, y_train)

        # self.clf = SVC(kernel="linear", probability=True)
        # self.clf.fit(X_train, y_train)

        # self.clf = GradientBoostingClassifier(
        #     n_estimators=100, learning_rate=0.1)
        # self.clf.fit(X_train, y_train, monitor=monitor)

        y_pred = self.clf.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        print("Accuracy:", accuracy)

        for i in range(len(X_test)):
            true_label = y_test[i]
            predicted_label = y_pred[i]
            if true_label != predicted_label:
                print(f"Misidentified Image Index: {i}")
                print(f"True label: {true_label}, Predicted label: {predicted_label}")
                misidentified_image = Image.open(image_paths[i])
                print(image_paths[i])

                plt.imshow(misidentified_image)
                plt.show()

        if accuracy > 0.99:
            if not os.path.exists(WEIGHTS_PATH):
                os.makedirs(WEIGHTS_PATH)
            torch.save(self.clip_model.state_dict(), self.CLIP_PATH)
            joblib.dump(self._preprocess_clip, self.PREPROCESS_PATH)
            joblib.dump(self.clf, self.CLASSIFIER_PATH)
        else:
            raise Exception("Accuracy too low")

    def _load(self):
        self._preprocess_clip = joblib.load(self.PREPROCESS_PATH)
        self.clip_model, self._preprocess_clip = clip.load("ViT-B/32", device="cpu")
        self.clip_model.load_state_dict(torch.load(self.CLIP_PATH))
        self.clip_model.eval()
        self.clf = joblib.load(self.CLASSIFIER_PATH)

    def images_are_inverted(self, image_a, image_b):
        features_a, features_b = self._preprocess(image_a), self._preprocess(image_b)
        prob_a = self.clf.predict_proba(features_a)[0]
        prob_b = self.clf.predict_proba(features_b)[0]
        classified_inverted = prob_a[0] < prob_b[0]
        # TODO: add color check here to verify
        return classified_inverted
