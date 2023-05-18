import speech_recognition as sr
import os
from pydub import AudioSegment
from pydub.silence import split_on_silence

r = sr.Recognizer()

def transcribe_large_audio(path):
    sound = AudioSegment.from_wav(path)

    chunks = split_on_silence(sound, min_silence_len=400, silence_thresh=sound.dBFS - 16, keep_silence=100)

    folder_name = "audio-chunks"
    if not os.path.isdir(folder_name):
        os.mkdir(folder_name)

    whole_text = ""
    for i, audio_chunk in enumerate(chunks, start=1):
        chunk_filename = os.path.join(folder_name, f"chunk{i}.wav")
        audio_chunk.export(chunk_filename, format="wav")

        with sr.AudioFile(chunk_filename) as source:
            r.adjust_for_ambient_noise(source, duration=0.5)
            r.dynamic_energy_threshold = True
            audio_listened = r.record(source)
            try:
                text = r.recognize_google(audio_listened)
            except sr.UnknownValueError as e:
                print("Error:", str(e))
            else:
                text = f"{text.capitalize()}. "
                print(chunk_filename, ":", text)
                whole_text += text

    return whole_text


result = transcribe_large_audio('audio1.wav')

print(result)
print(result, file=open('result.txt', 'w'))