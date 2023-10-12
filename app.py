import streamlit as st
import numpy as np
from PIL import Image
from model_util import recipe_name_generator



st.title('Image to recipe_name')
uploaded_image = st.file_uploader('Upload food images')
col1,col2 = st.columns(2)

if uploaded_image is not None:
    with col1:
        st.image(np.asarray(Image.open(uploaded_image).resize((400,400),Image.Resampling.LANCZOS)))
    recipe_name = recipe_name_generator(uploaded_image)
    with col2:
        st.write(recipe_name)
    