import tensorflow as tf
from tensorflow import keras
from keras.preprocessing.text import Tokenizer
from tensorflow.keras.utils import pad_sequences
import json

class SQLInjectionModel:
    def __init__(self, tokenizer_path='models\sql_injection_tokenizer.json', model_path='models/sql_injection_model.h5'):
        #Load model json
        json_file = open('models/sql_injection_model.json', 'r')
        loaded_model_json = json_file.read()
        json_file.close()
        self.model = keras.models.model_from_json(loaded_model_json)
        # load weights into new model
        self.model.load_weights(model_path)

        # load tokenizer
        self.tokenizer = Tokenizer(num_words=10000, oov_token="<unk>")
        json_file = open(tokenizer_path, 'r')
        json_content = json_file.read()
        tokenizer_json = json.loads(json_content)
        json_file.close()
        self.tokenizer.word_index = tokenizer_json['word_index']
        self.max_len = tokenizer_json['max_len']

    def preprocess_text(self, text):
        sequences = self.tokenizer.texts_to_sequences([text])
        padded_sequences = pad_sequences(sequences, maxlen=self.max_len, padding='post')
        return padded_sequences

    def predict(self, text):
        processed_text = self.preprocess_text(text)
        prediction = self.model.predict(processed_text)[0][0]
        return prediction
    def save_tokenizer(self, tokenizer_path):
        json_obj = {}
        json_obj["word_index"] = self.tokenizer.word_index
        json_obj["max_len"] = self.max_len
        json_content = json.dumps(json_obj)
        with open(tokenizer_path, 'w') as json_file:
           json_file.write(json_content)