import numpy as np
from sklearn.datasets import load_diabetes
import pika
import json


X, y = load_diabetes(return_X_y=True)

while True:
    try:
        random_row = np.random.randint(0, X.shape[0]-1)

        connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
        channel = connection.channel()
        channel.queue_declare(queue='features')
        channel.basic_publish(exchange='',
                              routing_key='features',
                              body=json.dumps({
                                            'features': list(X[random_row]),
                                            'y_true': float(y[random_row])
                                              }))

        # print(json.dumps(list(X[random_row])))
        print('Message sent')
        connection.close()
    except:
        print('Connection error')
