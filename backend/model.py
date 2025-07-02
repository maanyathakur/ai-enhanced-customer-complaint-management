import tensorflow as tf
import numpy as np
# from tensorflow import keras
from keras.models import load_model
from dotenv import load_dotenv
import os
import requests

load_dotenv()



class Review:
    def __init__(self):
        self.model = load_model('reviewsmodel.h5')
        self.ai21apikey = os.getenv('AI21_API_KEY')


    def _make_embedding_(self,text):

        url = "https://api.ai21.com/studio/v1/embed"
        payload = { "texts": [f"{text}"] }
        headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "Authorization": f"BEARER {self.ai21apikey}"
        }
        response = requests.post(url, json=payload, headers=headers)
        embd=response.json()['results'][0]['embedding']
        return embd

    
    def predict(self, text):
        # Preprocess the text
        maps={0:'A',1:'B',2:'C',3:'D',4:'E'}
        embd = self._make_embedding_(text)
        # Make a prediction
        prediction = self.model.predict(np.array([embd]))[0].argmax()
        # rating = maps[prediction]
        return prediction
    
if __name__=='__main__':
    review = Review()
    text = "slight flickering screen."
    print(review.predict(text)) # Output: E
    text = "MY drill machine i scompletely broken i cannot use it please replce it as soon as possible"
    print(review.predict(text)) # Output: Apip install --upgrade tensorflow