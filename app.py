from textblob import TextBlob
import streamlit as st
from googletrans import Translator
import cv2
import numpy as np
import pytesseract
from PIL import Image
from gtts import gTTS
import os
import pandas as pd



st.title('Los caracteres y las emociones')
image = Image.open('emoticones.jpg')
st.image(image)
st.subheader("Por favor ingresa una foto del texto que quieres analizar")

translator = Translator()

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
        elif x <= -0.5:
            st.write( 'Es un sentimiento Negativo 😔')
        else:
            st.write( 'Es un sentimiento Neutral 😐')
