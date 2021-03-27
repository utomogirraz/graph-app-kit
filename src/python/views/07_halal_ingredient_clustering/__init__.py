import pandas as pd, asyncio, streamlit as st, graphistry, time, os
from components import GraphistrySt, URLParam
from css import all_css
from TigerGraph_helper import tg_helper
from util import getChild


app_id = 'app_07'
logger = getChild(app_id)
urlParams = URLParam(app_id)

# Setup a structure to hold metrics
metrics = {'tigergraph_time': 0, 'graphistry_time': 0,
           'node_cnt': 0, 'edge_cnt': 0, 'prop_cnt': 0}

# Define the name of the view
def info():
    return {
        'id': app_id,
        'name': 'Halal - Ingredient Cluster',
        'tags': ['halal_food', 'tigergraph_halal_food', 'ingredient_cluster']
    }

def run():
    run_all()
 

def custom_css():
    all_css()
    st.markdown(
        """<style>

        </style>""", unsafe_allow_html=True)   
    
def sidebar_area():
    
    st.sidebar.subheader('Select the Number of Cluster')
    clusnumlist = [2, 4]
    clusnum = st.sidebar.selectbox('Number of Cluster', clusnumlist)
    
    conn = tg_helper.connect_to_tigergraph()
    return {'clusnum': clusnum, 'conn': conn}


def plot_url(nodes_df, edges_df):

    logger.info('Starting graphistry plot')
    tic = time.perf_counter()

    # edge weight ( ==> score )
    # edgeInfluence @ https://hub.graphistry.com/docs/api/1/rest/url/#urloptions

    g = graphistry \
        .edges(edges_df) \
        .settings(url_params={'play': 7000, 'dissuadeHubs': True}) \
        .bind(edge_weight=0)      \
        .bind(source='Ingredient', destination='Cluster') \
        .bind(edge_title='', edge_label='') \
        .nodes(nodes_df) \
        .bind(node='Ingredient') \
        .encode_point_color("Cluster", categorical_mapping={"Cluster 1": 'blue',
                                                            "Cluster 2": 'red',
                                                            "Cluster 3": 'green',
                                                            "Cluster 4": 'orange'},
                                    default_mapping='white') \

    # .encode_point_size('', ["blue", "yellow", "red"],  ,as_continuous=True)
    # if not (node_label_col is None):
    #     g = g.bind(point_title=node_label_col)

    # if not (edge_label_col is None):
    #     g = g.bind(edge_title=edge_label_col)

    url = g.plot(render=False, as_files=True)

    toc = time.perf_counter()
    metrics['graphistry_time'] = toc - tic
    logger.info(f'Graphisty Time: {metrics["graphistry_time"]}')
    logger.info('Generated viz, got back urL: %s', url)

    return url



def main_area(clusnum, conn):
    
    st.write(""" # Tigergraph Halal Food """)
    st.write('### Halal Product & Ingredient Link')
    tic = time.perf_counter()
             
    if conn is None:
        logger.error('Cannot run tg demo without creds')
        st.write(RuntimeError('Demo requires a TigerGraph connection. Put creds into left sidebar, or fill in envs/tigergraph.env & restart'))
        return None
    
    file_path = os.path.dirname(os.path.realpath(__file__))
    if (clusnum == 2):
        data = pd.read_csv(os.path.join(file_path, 'klasters3.csv'))
    else:
        data = pd.read_csv(os.path.join(file_path, 'klasters.csv'))
    
    nan_value = float("NaN")
    data.replace("", nan_value, inplace=True)
    data.dropna(subset = ['0'], inplace=True)
    
    cluster_num = []
    for vertex in data['1']:
        if int(vertex)<1:
            cluster_num.append('Cluster {}'.format(int(vertex)+1))
        else:
            cluster_num.append('Cluster {}'.format(int(vertex)))
    
    nodes_df = pd.DataFrame({
            'Ingredient': data['0'],
            'Cluster': cluster_num
            })  
            
    edges_df = nodes_df
    
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
            url = plot_url(nodes_df, edges_df)
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
        
        
        main_area(sidebar_filters['clusnum'], sidebar_filters['conn'])

    except Exception as exn:
        st.write('Error loading dashboard')
        st.write(exn)
