import os
import streamlit as st
from PIL import Image
from googletrans import Translator
import time
import glob
from gtts import gTTS
from textblob import TextBlob

st.title('Las palabras y las emociones')
image = Image.open('emoticones.jpg')
st.image(image)
st.subheader("Al ingresar un texto se generará un audio con lo que escribiste y además se analizará el tipo de emoción que se incluye en el texto.")

translator = Translator()
tld="es"

def text_to_speech(text, tld):
    tts = gTTS(text, lang="es", slow=False)
    try:
        my_file_name = text[0:20]
    except:
        my_file_name = "audio"
    tts.save(f"temp/{my_file_name}.mp3")
    return my_file_name, text

text = st.text_input("Ingrese el texto.")

if st.button("Audio"):
    result, output_text = text_to_speech(text, tld)
    audio_file = open(f"temp/{result}.mp3", "rb")
    audio_bytes = audio_file.read()
    st.markdown(f"## Tú audio:")
    st.audio(audio_bytes, format="audio/mp3", start_time=0)

with st.expander('Analizar texto'):

    if text:
        dest_lang = st.selectbox(
            "Selecciona el idioma de destino:",
            ("Inglés", "Español", "Francés", "Alemán", "Italiano", "Portugués", "Ruso", "Chino", "Japonés", "Coreano")
        )
        dest_lang_code = dest_lang.lower()[:2]  # Obtener el código de idioma

        translation = translator.translate(text, dest=dest_lang_code)
        trans_text = translation.text
        blob = TextBlob(trans_text)
        st.write('Texto traducido:', trans_text)
        st.write('Polarity:', round(blob.sentiment.polarity, 2))
        st.write('Subjectivity:', round(blob.sentiment.subjectivity, 2))

        x = round(blob.sentiment.polarity, 2)
        if x >= 0.5:
            st.write('Es un sentimiento Positivo 😊')
            image_feliz = Image.open('feliz.jpg')
            st.image(image_feliz)

        elif x <= -0.5:
            st.write('Es un sentimiento Negativo 😔')
            image_triste = Image.open('triste.jpg')
            st.image(image_triste)

        else:
            st.write('Es un sentimiento Neutral 😐')
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
