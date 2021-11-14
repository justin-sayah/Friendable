import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from joblib import dump, load

def get_prediction(value_arr):
    '''
    Gets a prediction from in house trained kmeans model

    :param value_arr: an array of values matching the order in fake_people DO NOT PASS A NAME
    '''
    kmeans = load('kmeans_model.joblib')
    test = np.array(value_arr)
    test.reshape(-1,1)
    prediction = kmeans.predict([test])
    return prediction[0]

def process_data(value_dict):
    '''
    takes in a dictionary of values and returns an array ready to get passed to get_prediction

    I know I need to average
    '''
    # {('number', '9788065553'), ('name', 'Conor Walsh'), ('q1', '7'), ('q2', '3'), ('q3', '9'), 
    # ('q4', '2'), ('q5', '8'), ('q6', '8'), ('q7', '8'), ('q8', '8'), ('q9', '8'), ('q10', '3'), 
    # ('q11', '6'), ('q12', '6'), ('13', '1'), ('14', '1'), ('15', '1'), ('16', '1'), ('17', '0'), ('18', '0')}

    preprocessed = list(value_dict.values())
    preprocessed = preprocessed[2:]
    print(preprocessed)

        

