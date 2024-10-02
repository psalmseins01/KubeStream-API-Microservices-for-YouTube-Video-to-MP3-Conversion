import os, pika, sys, time
from pymongo import MongoClient
import gridfs
from convert import to_mp3


def main():
    client = MongoClient("host.minikube.internal", 27017)
    videos_db = client.videos
    mp3s_db = client.mp3s

    # Creating gridfs instance
    video_fs = gridfs.GridFS(videos_db)
    mp3s_fs = gridfs.GridFS(mp3s_db)

    # Creating rabbitmq connection
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host="rabbitmq")
    )
    channel = connection.channel()
    
    def callback(ch, method, properties, body):
        err = to_mp3.start(body, video_fs, mp3s_fs, ch)
        # keep messages on the queue if not processed
        if err:
            # delivery tag uniquely identifies the delivery on a channel
            ch.basic_nack(delivery_tag=method.delivery_tag)
        else:
            ch.basic_nack(delivery_tag=method.delivery_tag)

    channel.basic_consume(
        queue=os.environ.get("VIDEO_QUEUE"), on_message_callback=callback
    )

    print("Waiting for messages. Press CTRL+C to exit")

    # Start the listener
    channel.start_consuming()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Interrupted")
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
