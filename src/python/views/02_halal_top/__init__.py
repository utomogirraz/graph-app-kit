import pandas as pd, streamlit as st
from components import GraphistrySt, URLParam
from css import all_css
from TigerGraph_helper import tg_helper
import plotly.express as px
from util import getChild


app_id = 'app_02'
logger = getChild(app_id)
urlParams = URLParam(app_id)

# Define the name of the view
def info():
    return {
        'id': app_id,
        'name': 'Halal - Top Ingredients & Manufactures',
        'tags': ['halal_food', 'tigergraph_halal_food', 'top_ingredients', 'top_manufactures']
    }

def run():
    run_all()
 

def custom_css():
    all_css()
    st.markdown(
        """<style>

        </style>""", unsafe_allow_html=True)   
    
def sidebar_area():

    st.sidebar.subheader('Select the Number of Top Halal Ingredients')
    ingnumlist = [i for i in range(1, 50)]
    ingnum = st.sidebar.selectbox('Number of Top Ingredients', ingnumlist)
    
    st.sidebar.subheader('Select the Number of Top Halal Manufactures')
    mannumlist = [i for i in range(1, 50)]
    mannum = st.sidebar.selectbox('Number of Top Manufactures', mannumlist)
    
    urlParams.set_field('ingnum', ingnum)
    urlParams.set_field('mannum', mannum)
    
    conn = tg_helper.connect_to_tigergraph()
    
    return {'ingnum': ingnum, 'mannum': mannum, 'conn': conn}

def main_area(ingnum, mannum, conn):
    
#    logger.debug('rendering main area, with url: %s', url)
#    GraphistrySt().render_url(url)
    
    st.write(""" # Tigergraph Halal Food """)
    st.write('### Top Ingredients & Top Manufactures')
    
    if conn is None:
        logger.error('Cannot run tg demo without creds')
        st.write(RuntimeError('Demo requires a TigerGraph connection. Put creds into left sidebar, or fill in envs/tigergraph.env & restart'))
        return None
        
    # Get Top 10 Ingredients
    
    query = "GetTopIngredient"
    resultTG = conn.runInstalledQuery(query, params={'num':ingnum})
    results = resultTG[0]['Ing']
    
    atttoping = []
    for vertex in results:
        atttoping.append(vertex['attributes'])
    
    datatoping = pd.DataFrame(atttoping)
    bartoping = px.bar(datatoping, x=datatoping['name'], y=datatoping['@productNum'],
                 labels={'name': 'Ingredient Name',
                         '@productNum': 'Amount of Products Using Ingredient'},
                 title="Top {} Halal Ingredients".format(ingnum), barmode='group')
    
    st.plotly_chart(bartoping, use_container_width=True)
    
    # Get Top 10 Manufacturers
    
    query = "GetTopHalalManufactures"
    resultTG = conn.runInstalledQuery(query, params={'num':mannum})
    results = resultTG[0]['Man']
    
    atttopman = []
    for vertex in results:
        atttopman.append(vertex['attributes'])
    
    datatopman = pd.DataFrame(atttopman)
    bartopman = px.bar(datatopman, x=datatopman['manufacture_name'], y=datatopman['@productNum'],
                 labels={'manufacture_name': 'Name of Manufacturer',
                         '@productNum': 'Amount of Halal Product'},
                 title="Top {} Halal Manufactures".format(mannum), barmode='group')
    
    st.plotly_chart(bartopman, use_container_width=True)


def run_all():
    
    logger.info('run_all')
    custom_css()

    try:

        # Render sidebar, get current settings and TG connection
        sidebar_filters = sidebar_area()

        # Stop if not connected to TG
        if sidebar_filters is None:
            return
        
        main_area(sidebar_filters['ingnum'], sidebar_filters['mannum'], sidebar_filters['conn'])

    except Exception as exn:
        st.write('Error loading dashboard')
        st.write(exn)
