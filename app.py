from textblob import TextBlob
import pandas as pd
import streamlit as st
from PIL import Image
from googletrans import Translator
import os
import time
import glob
import os
from gtts import gTTS


st.title('Los caracteres y las emociones')
image = Image.open('emoticones.jpg')
st.image(image)
st.subheader("Por favor ingresa una foto del texto que quieres analizar")

translator = Translator()
tld="es"

try:
    os.mkdir("temp")
except:
    pass


text = st.text_input("Ingrese el texto.")

tld="es"

def text_to_speech(text, tld):
    
    tts = gTTS(text,"es", tld, slow=False)
    try:
        my_file_name = text[0:20]
    except:
        my_file_name = "audio"
    tts.save(f"temp/{my_file_name}.mp3")
    return my_file_name, text


#display_output_text = st.checkbox("Verifica el texto")

if st.button("convertir"):
    result, output_text = text_to_speech(text, tld)
    audio_file = open(f"temp/{result}.mp3", "rb")
    audio_bytes = audio_file.read()
    st.markdown(f"## Tú audio:")
    st.audio(audio_bytes, format="audio/mp3", start_time=0)

    #if display_output_text:
    st.markdown(f"## Texto en audio:")
    st.write(f" {output_text}")

    
with st.expander('Analizar texto'):

    if text:

        translation = translator.translate(text, src="es", dest="en")
        trans_text = translation.text
        blob = TextBlob(trans_text)
        st.write('Polarity: ', round(blob.sentiment.polarity,2))
        st.write('Subjectivity: ', round(blob.sentiment.subjectivity,2))
        x=round(blob.sentiment.polarity,2)
        if x >= 0.5:
            st.write( 'Es un sentimiento Positivo 😊')
            audio_feliz()

        elif x <= -0.5:
            st.write( 'Es un sentimiento Negativo 😔')
            audio_triste()

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
