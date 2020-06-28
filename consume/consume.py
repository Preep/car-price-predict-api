import pika
import json
from pprint import pprint


def callback(channel, deliver, propetries, bytes):
    pprint(json.loads(bytes))


try:
    connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
    channel = connection.channel()
    channel.basic_consume(queue='features',
                          on_message_callback=callback,
                          auto_ack=True)
    print('...Ожидание сообщений, для выхода нажмите CTRL+C')

    channel.start_consuming()
except:
    print('Connection error')
