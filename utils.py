from google.cloud import speech_v1p1beta1
from google.cloud.speech_v1p1beta1 import enums
from google.cloud import storage
import random
import string
import json
from moviepy.editor import *
from summarize_abstract import summarize_title
from summarize_wybiorcze import summarize
import sqlite3


def transcribe(storage_uri):
    """
    Performs synchronous speech recognition on an audio file

    Args:
      storage_uri URI for audio file in Cloud Storage, e.g. gs://[BUCKET]/[FILE]
    """

    client = speech_v1p1beta1.SpeechClient()

    # storage_uri = 'gs://cloud-samples-data/speech/brooklyn_bridge.mp3'

    # The language of the supplied audio
    language_code = "en-US"

    # Sample rate in Hertz of the audio data sent
    sample_rate_hertz = 44100

    enable_word_time_offsets = True

    enable_automatic_punctuation = True

    # Encoding of audio data sent. This sample sets this explicitly.
    # This field is optional for FLAC and WAV audio formats.
    encoding = enums.RecognitionConfig.AudioEncoding.MP3
    config = {
        "language_code": language_code,
        "sample_rate_hertz": sample_rate_hertz,
        "encoding": encoding,
        "enable_word_time_offsets": enable_word_time_offsets,
        "enable_automatic_punctuation": enable_automatic_punctuation
    }
    audio = {"uri": storage_uri}

    plaintext = ""
    sentences = []

    operation = client.long_running_recognize(config, audio)

    print(u"Waiting for operation to complete...")
    response = operation.result()

    for result in response.results:
        # First alternative is the most probable result
        alternative = result.alternatives[0]
        string = alternative.transcript.replace('!', '.')
        string = string.replace('?', '.')
        plaintext += string + ' '
        tab = string.split('. ')

        n=0
        for elem in tab[:-1]:
            sentences.append(
            (elem+'.', alternative.words[n].start_time.seconds))
            words = elem.split()
            n += len(words)

        sentences.append(
            (tab[-1], alternative.words[n].start_time.seconds))

    print(u"Transcribed")
    return (plaintext, sentences)


# wrzucanie plików do cloud storage.
def upload_blob(source_file_name):
    """Uploads a file to the bucket."""
    bucket_name = "alamakota1"
    # source_file_name = "local/path/to/file"
    destination_blob_name = ''.join(
        random.choices(
            string.ascii_uppercase +
            string.digits,
            k=5))

    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    print("uploading")
    blob.upload_from_filename(source_file_name)
    link = f"gs://alamakota1/{destination_blob_name}"
    print("uploaded")

    return link


# extracts .mp3 file from video and returns it's relative path
def extract_audio(source_file_name):
    print("extracting")
    video = VideoFileClip(source_file_name)
    audio = video.audio
    path = 'static/audio/' + \
        ''.join(random.choices(string.ascii_uppercase + string.digits, k=5)) + '.mp3'
    audio.write_audiofile(path)
    print("extracted")
    return path


def test(res):
    print(res[0])
    print("------------------------------------------")
    print(res[1])

def handle_video(video_id):
    filepath = 'static/vid/'+video_id+'.mp4'
    print("Uploaded: " + filepath)
    #to trwa długo, więc jeśli chcecie testować to sobie zapiszcie wartosci
    (plaintext, sentences_timestamps) = transcribe(upload_blob(extract_audio(filepath)))

    print(sentences_timestamps)
    print(plaintext)

    print(u"Abs sum in progress")
    title=summarize_title(plaintext)
    print(u"Abs sum done")

    print(u"Selective sum in progress")
    summary_sentences = summarize(plaintext) #zwraca tablice zdań
    print(u"Selective sum done")
    summary = []
    next_sentence = 0

    print(u"Magia Maksa 1")
    for sentence in summary_sentences:
        while next_sentence < len(sentences_timestamps) and sentences_timestamps[next_sentence][0] != sentence:
            print('not', sentence, sentences_timestamps[next_sentence][0])
            next_sentence += 1
        if next_sentence >= len(sentences_timestamps):
            summary.append((sentence, sentences_timestamps[-1][1]))
        else:
            summary.append((sentence, sentences_timestamps[next_sentence][1]))

    print(u"Magia Maksa 2")
    transcript = []
    for (sentence, timestamp) in sentences_timestamps:
        while len(transcript) <= timestamp // 60:
            transcript.append('')
        transcript[-1] += sentence 

    summary_json = json.dumps(summary)
    transcript_json = json.dumps(transcript)
    
    print(sentences_timestamps)
    print(summary)
    print(transcript)

    print(u"Baza danych")

    db = sqlite3.connect("kotki.db")
    cursor = db.cursor()
    cursor.execute(
        '''INSERT INTO videos(title,id, summary,transcript) VALUES(?,?,?,?)''', (title, video_id, summary_json, transcript_json))
    db.commit()
    db.close()

def load_data(video_id):
    filepath = 'vid/'+video_id+'.mp4'
    db = sqlite3.connect("kotki.db")
    cursor = db.cursor()
    cursor.execute(
        '''SELECT title, summary, transcript FROM videos WHERE id=?''', (video_id,))
    ret = cursor.fetchone()
    return (filepath, ret[0], ret[1], ret[2]) #(path, title, summary, transcript)


# example
#upload_blob(extract_audio("vid/A2G1Z.mp4"))
