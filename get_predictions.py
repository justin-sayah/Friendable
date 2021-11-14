import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from joblib import dump, load

def get_prediction(value_dict):
    '''
    Gets a prediction from in house trained kmeans model

    :param value_arr: a dict of values matching the order in fake_people DO NOT PASS A NAME
    '''

    preprocessed = list(value_dict.values())
    preprocessed = preprocessed[2:]
    
    processed = []

    for i in range(3):
        sum = 0
        sum += int(preprocessed[i])
        processed.append(sum/3)
    for i in range(3,6):
        sum = 0
        sum += int(preprocessed[i])
        processed.append(sum/3)
    for i in range(6,9):
        sum = 0
        sum += int(preprocessed[i])
        processed.append(sum/3)
    for i in range(9,12):
        sum = 0
        sum += int(preprocessed[i])
        processed.append(sum/3)

    for i in range(12,18):
        processed.append(int(preprocessed[i]))
    
    #['7', '3', '9', '2', '8', '8', '8', '8', '8', '3', '6', '6', '1', '1', '1', '1', '0', '0']

    kmeans = load('kmeans_model.joblib')
    test = np.array(processed)
    test.reshape(-1,1)
    prediction = kmeans.predict([test])

    return prediction[0]

        

