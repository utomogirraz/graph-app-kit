import pandas as pd, asyncio, streamlit as st, graphistry, time
from components import GraphistrySt, URLParam
from css import all_css
from TigerGraph_helper import tg_helper
from util import getChild


app_id = 'app_03'
logger = getChild(app_id)
urlParams = URLParam(app_id)

# Setup a structure to hold metrics
metrics = {'tigergraph_time': 0, 'graphistry_time': 0,
           'node_cnt': 0, 'edge_cnt': 0, 'prop_cnt': 0}

# Define the name of the view
def info():
    return {
        'id': app_id,
        'name': 'Halal - Search Product',
        'enabled': True,
        'tags': ['halal_food', 'tigergraph_halal_food', 'search_product']
    }

def run():
    run_all()
 

def custom_css():
    all_css()
    st.markdown(
        """<style>

        </style>""", unsafe_allow_html=True)   
    
def sidebar_area():

    st.sidebar.subheader('Enter the Name of the Product')
    fdnm = st.sidebar.text_input('Food Name', 'nissin')
    fdnm = fdnm.lower()
    
    urlParams.set_field('fdnm', fdnm)
    
    conn = tg_helper.connect_to_tigergraph()
    
    return {'fdnm': fdnm, 'conn': conn}


def main_area(fdnm, conn):

    st.write(""" # Tigergraph Halal Food """)
    st.write('### Search Product')
    tic = time.perf_counter()
             
    if conn is None:
        logger.error('Cannot run tg demo without creds')
        st.write(RuntimeError('Demo requires a TigerGraph connection. Put creds into left sidebar, or fill in envs/tigergraph.env & restart'))
        return None
        
    # Search Product by Name
    
    query = "GetProductByName"
    resultTG = conn.runInstalledQuery(query, params={'foodname': fdnm})
    results = resultTG[0]['@@tupleRecords']
    
    data = pd.DataFrame(results)
    
    data = pd.DataFrame({
            'Food ID': data['id'],
            'Name': data['foodname'],
            'Halal Certifate': data['cert'],
            'Issuing Authority': data['org']
            })
        
    try:
        res = data.values.tolist()
        toc = time.perf_counter()
        logger.info(f'Query Execution: {toc - tic:0.02f} seconds')
        logger.debug('Query Result Count: %s', len(res))
        metrics['tigergraph_time'] = toc - tic

        # Calculate the metrics
        metrics['node_cnt'] = data.size
        metrics['prop_cnt'] = (data.size * data.columns.size)

        if data.size > 0:
#            url = plot_url(nodes_df, edges_df)
            g = graphistry.edges(data).bind(source='Name', destination='Name') \
                .nodes(data).bind(node='Name')
            url = g.plot(render=False, as_files=True)
        else:
            url = ""
    except Exception as e:
        logger.error('oops in TigerGraph', exc_info=True)
        raise e
    logger.info("Finished compute phase")

    try:
        pass

    except RuntimeError as e:
        if str(e) == "There is no current event loop in thread 'ScriptRunner.scriptThread'.":
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)

        else:
            raise e

    except Exception as e:
        logger.error('oops in TigerGraph', exc_info=True)
        raise e

    logger.info('rendering main area, with url: %s', url)
    GraphistrySt().render_url(url)
    
def run_all():
    
    logger.info('run_all')
    custom_css()

    try:

        # Render sidebar, get current settings and TG connection
        sidebar_filters = sidebar_area()

        # Stop if not connected to TG
        if sidebar_filters is None:
            return
        
        
        main_area(sidebar_filters['fdnm'], sidebar_filters['conn'])

    except Exception as exn:
        st.write('Error loading dashboard')
        st.write(exn)
