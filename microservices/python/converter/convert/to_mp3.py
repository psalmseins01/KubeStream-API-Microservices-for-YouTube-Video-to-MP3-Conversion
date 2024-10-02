import pika, os, tempfile, json
from bson.objectid import ObjectId
import moviepy.editor


def start(message, video_fs, mp3_fs, channel):
    # Deserializing the message
    message = json.loads(message)

    tf = tempfile.NamedTemporaryFile()

    out = video_fs.get(ObjectId(message["video_fid"]))

    # Read the bytes from the file and write to the tempfile
    tf.write(out.read())

    # Create audio from the tempfile having the video

    audio = moviepy.editor.VideoFileClip(tf.name).audio
    tf.close()

    # Write the audio to a file
    tf_path = tempfile.gettempdir() + f"/{message['video_fid']}.mp3"
    audio.write_audiofile(tf_path)

    f = open(tf_path, "rb")
    data = f.read()
    fid = mp3_fs.put(data)
    f.close()
    os.remove(tf_path)

    message["mp3_fid"] = str(fid)

    try:
        channel.basic_publish(
            exchange="",
            routing_key=os.environ.get("MP3_QUEUE"),
            body=json.dumps(message),
            properties=pika.BasicProperties(
                delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
            ),
        )
    except Exception as err:
        mp3_fs.delete(fid)
        return "failed to publish message"

