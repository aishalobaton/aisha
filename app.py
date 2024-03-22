import os
import streamlit as st
from PIL import Image
from googletrans import Translator
import time
import glob
from gtts import gTTS

st.title('Las palabras y las emociones')
image = Image.open('emoticones.jpg')
st.image(image)
st.subheader("Al ingresar un texto se generará un audio con lo que escribiste y además se analizará el tipo de emoción que se incluye en el texto.")

translator = Translator()
try:
    os.mkdir("temp")
except:
    pass

text = st.text_input("Ingrese el texto.")

# Selección del idioma de traducción
languages = {
    "es": "Español",
    "en": "Inglés",
    "fr": "Francés",
    "de": "Alemán",
    "it": "Italiano",
    "ja": "Japonés",
    "ko": "Coreano",
    "zh-cn": "Chino Simplificado",
    "ru": "Ruso",
}
input_language = st.selectbox("Seleccione el idioma de entrada:", list(languages.values()))
output_language = st.selectbox("Seleccione el idioma de salida:", list(languages.values()))

def text_to_speech(text, input_language, output_language):
    translation = translator.translate(text, src=input_language, dest=output_language)
    trans_text = translation.text
    tts = gTTS(trans_text, lang=output_language, slow=False)
    try:
        my_file_name = text[0:20]
    except:
        my_file_name = "audio"
    tts.save(f"temp/{my_file_name}.mp3")
    return my_file_name, trans_text

if st.button("Audio"):
    result, output_text = text_to_speech(text, input_language[:2], output_language[:2])
    audio_file = open(f"temp/{result}.mp3", "rb")
    audio_bytes = audio_file.read()
    st.markdown(f"## Tú audio:")
    st.audio(audio_bytes, format="audio/mp3", start_time=0)

with st.expander('Analizar texto'):
    if text:
        translation = translator.translate(text, src=input_language[:2], dest="en")
        trans_text = translation.text
        blob = TextBlob(trans_text)
        st.write('Polaridad: ', round(blob.sentiment.polarity,2))
        st.write('Subjetividad: ', round(blob.sentiment.subjectivity,2))
        x=round(blob.sentiment.polarity,2)
        if x >= 0.5:
            st.write( 'Es un sentimiento Positivo 😊')
            image_feliz = Image.open('feliz.jpg')
            st.image(image_feliz)

        elif x <= -0.5:
            st.write( 'Es un sentimiento Negativo 😔')
            image_triste = Image.open('triste.jpg')
            st.image(image_triste)

        else:
            st.write( 'Es un sentimiento Neutral 😐')
            image_neutro = Image.open('neutro.jpg')
            st.image(image_neutro)

def remove_files(n):
    mp3_files = glob.glob("temp/*mp3")
    if len(mp3_files) != 0:
        now = time.time()
        n_days = n * 86400
        for f in mp3_files:
            if os.stat(f).st_mtime < now - n_days:
                os.remove(f)
                print("Deleted ", f)

remove_files(7)
