import pandas as pd, asyncio, streamlit as st, graphistry, time
from components import GraphistrySt, URLParam
from css import all_css
from TigerGraph_helper import tg_helper
from util import getChild


app_id = 'app_01'
logger = getChild(app_id)
urlParams = URLParam(app_id)

# Setup a structure to hold metrics
metrics = {'tigergraph_time': 0, 'graphistry_time': 0,
           'node_cnt': 0, 'edge_cnt': 0, 'prop_cnt': 0}

# Define the name of the view
def info():
    return {
        'id': app_id,
        'name': 'Halal - Certified Food',
        'enabled': True,
        'tags': ['halal_food', 'tigergraph_halal_food', 'halal_certified']
    }

def run():
    run_all()
 

def custom_css():
    all_css()
    st.markdown(
        """<style>

        </style>""", unsafe_allow_html=True)   
    
def sidebar_area():
    
    conn = tg_helper.connect_to_tigergraph()
    return {'conn': conn}


def main_area(ingnum, conn):
    
    st.write(""" # Tigergraph Halal Food """)
    st.write('### Halal Certified Food')
    tic = time.perf_counter()
             
    if conn is None:
        logger.error('Cannot run tg demo without creds')
        st.write(RuntimeError('Demo requires a TigerGraph connection. Put creds into left sidebar, or fill in envs/tigergraph.env & restart'))
        return None
        
    # Get Top 10 Ingredients
    
    query = "GetHalalProduct"
    resultTG = conn.runInstalledQuery(query)
    results = resultTG[0]['Product']
    
    atttoping = []
    for vertex in results:
        atttoping.append(vertex['attributes'])
    
    data = pd.DataFrame(atttoping)
        
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
            g = graphistry.edges(data).bind(source='food_name', destination='food_name')
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
        
        
        main_area(5, sidebar_filters['conn'])

    except Exception as exn:
        st.write('Error loading dashboard')
        st.write(exn)
