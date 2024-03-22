from textblob import TextBlob
import pandas as pd
import streamlit as st
from PIL import Image
from googletrans import Translator
import os
import time
import glob
from gtts import gTTS


st.title('Los caracteres y las emociones')
image = Image.open('emoticones.jpg')
st.image(image)
st.subheader("Por favor ingresa una foto del texto que quieres analizar")

translator = Translator()
tld="es"

def generar_audio():
 if x >= 0.5:
  texto_audio = "Yupi, tu texto feliz"
  tts = gTTS(text=texto_audio, lang='es')
  tts.save("feliz.mp3")
  os.system("mpg123 feliz.mp3")
 elif x <= -0.5:
  texto_audio = "Que mal, tu texto es triste"
  tts = gTTS(text=texto_audio, lang='es')
  tts.save("triste.mp3")
  os.system("mpg123 triste.mp3")
 else:
  texto_audio = "Tu texto es neutral"
  tts = gTTS(text=texto_audio, lang='es')
  tts.save("neutro.mp3")
  os.system("mpg123 neutro.mp3")


    
with st.expander('Analizar texto'):
    text = st.text_input('Escribe por favor: ')
    if text:

        translation = translator.translate(text, src="es", dest="en")
        trans_text = translation.text
        blob = TextBlob(trans_text)
        st.write('Polarity: ', round(blob.sentiment.polarity,2))
        st.write('Subjectivity: ', round(blob.sentiment.subjectivity,2))
        x=round(blob.sentiment.polarity,2)
        if x >= 0.5:
            st.write( 'Es un sentimiento Positivo 😊')
            generar_audio()

        elif x <= -0.5:
            st.write( 'Es un sentimiento Negativo 😔')
            generar_audio()

        else:
            st.write( 'Es un sentimiento Neutral 😐')
            generar_audio()

