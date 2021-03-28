import pandas as pd, asyncio, streamlit as st, graphistry, time, os
from components import GraphistrySt, URLParam
from css import all_css
from TigerGraph_helper import tg_helper
from util import getChild
from PIL import Image


app_id = 'app_00'
logger = getChild(app_id)
urlParams = URLParam(app_id)

# Setup a structure to hold metrics
metrics = {'tigergraph_time': 0, 'graphistry_time': 0,
           'node_cnt': 0, 'edge_cnt': 0, 'prop_cnt': 0}

# Define the name of the view
def info():
    return {
        'id': app_id,
        'name': 'Linked Open Data (LOD) Halal',
        'enabled': True,
        'tags': ['halal_food', 'tigergraph_halal_food', 'linked_open_data']
    }

def run():
    run_all()
 

def custom_css():
    all_css()
    st.markdown(
        """<style>

        </style>""", unsafe_allow_html=True)   
    

def main_area():
    
    st.write(""" # Linked Open Data Halal """)
    st.write('')
    st.write('Linked Open Data system for halal products (LODHalal) proposed a halal \
             food vocabulary that is enhanced from two food existing vocabularies. \
             Furthermore, it provides two interfaces: a web application and an Android \
             application that are able to search a food product and predict a halal \
             status of an uncertified-halal product.')
    
    st.write('')
    st.subheader('Features')
    st.write('**1 - Halal Certified Food** : Shows all of the halal certified product in the dataset.')
    st.write('**2 - Top Ingredients & Manufacturers** : Shows the most used ingredients in halal \
             products and the manufacturers that produce halal product the most.')
    st.write('**3 - Search Product** : Search product that contains the input word.')
    st.write('**4 - Similar Product** : Search product with similar ingredients.')
    st.write('**5 - Product & Manufacture Link** : Shows the link between products and its manufacturers.')
    st.write('**6 - Product & Ingredient Link** : Shows the link between products and its ingredients.')
    st.write('**7 - Ingredient Cluster** : Shows the cluster of product\'s ingredients.')
    
    
    st.write('')
    st.subheader('Source Code')
    st.markdown("""The source code of this project can be found at \
                <a href="https://github.com/utomogirraz/graph-app-kit" \
                target="_blank">https://github.com/utomogirraz/graph-app-kit</a>.""", \
                unsafe_allow_html=True)

    st.write('')
    st.subheader('Developers')
    st.write('- Nur Aini Rakhmawati, Ph.D.')
    st.write('- Dr. Rarasmaya Indraswari')
    st.write('- Irfan Rifqi Susetyo')
    st.write('- Girraz Karyo Utomo')
    st.write('')
    st.write('Data Acquisition and Information Dissemination Laboratory (Lab ADDI)')
    st.write('Department of Information Systems')
    st.write('Faculty of Intelligent Electrical and Informatics Technology')
    st.write('Institut Teknologi Sepuluh Nopember (ITS) - Surabaya, Indonesia')
    
    file_path = os.path.dirname(os.path.realpath(__file__))
    parent_path = os.path.abspath(os.path.join(file_path, os.path.pardir))
    logo_its = Image.open(os.path.join(parent_path, 'logo.jpeg'))
    st.image(logo_its, caption=None, width=800, use_column_width='True', clamp=False, channels='RGB', output_format='auto')
    
def run_all():
    
    logger.info('run_all')
    custom_css()

    try:        
        main_area()

    except Exception as exn:
        st.write('Error loading dashboard')
        st.write(exn)
