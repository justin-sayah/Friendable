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

    ret = []
    for i in range(4):
        total = 0
        for j in range(3):
            name = 'q' + str(3 * i + j)
            total += value_dict[name]

        
    
