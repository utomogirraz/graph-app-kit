import pandas as pd, asyncio, streamlit as st, graphistry, time
from components import GraphistrySt, URLParam
from css import all_css
from TigerGraph_helper import tg_helper
from util import getChild


app_id = 'app_04'
logger = getChild(app_id)
urlParams = URLParam(app_id)

# Setup a structure to hold metrics
metrics = {'tigergraph_time': 0, 'graphistry_time': 0,
           'node_cnt': 0, 'edge_cnt': 0, 'prop_cnt': 0}

# Define the name of the view
def info():
    return {
        'id': app_id,
        'name': 'Halal - Similar Product',
        'enabled': True,
        'tags': ['halal_food', 'tigergraph_halal_food', 'similar_product']
    }

def run():
    run_all()
 

def custom_css():
    all_css()
    st.markdown(
        """<style>

        </style>""", unsafe_allow_html=True)   
    
def sidebar_area():
    
    st.sidebar.subheader('Search the Most Similar Product')
    toplist = [i for i in range(1, 21)]
    top = st.sidebar.selectbox('The Number of Most Similar Product', toplist)
    
    selectlist = ['Based on Product ID', 'Based on 10 Similar Product Name']
    options = list(range(len(selectlist)))
    selectval = st.sidebar.selectbox('Input Selection Method', options,
                                  format_func=lambda x: selectlist[x])
    
    urlParams.set_field('top', top)
    urlParams.set_field('selval', selectval)
    
    if(selectval == 0):
        st.sidebar.subheader('Using Product ID as Input')
        selstr = st.sidebar.text_input('Product ID', '32366')
        selstr = selstr.lower()
        
    elif(selectval == 1):
        st.sidebar.subheader('Using Similar Name as Input')
        selstr = st.sidebar.text_input('Food Name', 'indomie')
        selstr = selstr.lower()
    
    urlParams.set_field('selstr', selstr)
    
    conn = tg_helper.connect_to_tigergraph()
    
    return {'top': top, 'selval': selectval, 'selstr': selstr, 'conn': conn}


def plot_url(nodes_df, edges_df):

    logger.info('Starting graphistry plot')
    tic = time.perf_counter()
    
    g = graphistry \
        .edges(edges_df) \
        .settings(url_params={'play': 7000, 'dissuadeHubs': True}) \
        .bind(edge_weight=1)      \
        .bind(source='from_id', destination='to_id') \
        .bind(edge_title='', edge_label='') \
        .nodes(nodes_df) \
        .bind(node='Food ID')
        

    # .encode_point_size('', ["blue", "yellow", "red"],  ,as_continuous=True)
#    if not (node_label_col is None):
#        g = g.bind(point_title=node_label_col)

    # if not (edge_label_col is None):
    #     g = g.bind(edge_title=edge_label_col)

    url = g.plot(render=False, as_files=True)

    toc = time.perf_counter()
    metrics['graphistry_time'] = toc - tic
    logger.info(f'Graphisty Time: {metrics["graphistry_time"]}')
    logger.info('Generated viz, got back urL: %s', url)

    return url



def main_area(top, selval, selstr, conn):
    
#    logger.debug('rendering main area, with url: %s', url)
#    GraphistrySt().render_url(url)
    
    st.write(""" # Tigergraph Halal Food """)
    st.write('### Similar Product')
    tic = time.perf_counter()
             
    if conn is None:
        logger.error('Cannot run tg demo without creds')
        st.write(RuntimeError('Demo requires a TigerGraph connection. Put creds into left sidebar, or fill in envs/tigergraph.env & restart'))
        return None
    
    new_from_id = []
    new_foodname = []
    new_cert = []
    new_org = []
    new_to_id = []
    
    if selval == 0:
        # Get Similar Product
        
        error = 0
        try:
            query2 = "GetSimilarProduct"
            resultTG2 = conn.runInstalledQuery(query2, params={'ids': selstr, 'top': top})
            results2 = resultTG2[0]['SIMILAR_Product']
            
        except Exception as e:
                print(e)
                error = 1
        
        if error == 1:
            new_from_id.append(selstr)
            new_foodname.append('')
            new_cert.append('')
            new_org.append('')
            new_to_id.append(selstr)
        else:
            dataawal = pd.DataFrame(results2)
            dataname = []
            for dataattr in dataawal['attributes']:
                name = dataattr.get('Subjects.food_name')
                dataname.append(name)
            
            i=0
            for product in results2:
                new_from_id.append(selstr)
                new_foodname.append(dataname[i])
                new_cert.append('')
                new_org.append('')
                new_to_id.append(product['v_id'])
                i += 1
                
    elif selval == 1:
    
        # Search Product by Name
        
        query = "GetProductByName"
        resultTG = conn.runInstalledQuery(query, params={'foodname': selstr})
        results = resultTG[0]['@@tupleRecords']
        results = results[0:10]
        
        # Get Similar Product
        
        
        for product in results:
            error = 0
            try:   
                query2 = "GetSimilarProduct"
                resultTG2 = conn.runInstalledQuery(query2, params={'ids': product['id'], 'top': top})
                results2 = resultTG2[0]['SIMILAR_Product']
                    
            except Exception as e:
                print(e)
                error = 1
                
            if error == 1:
                new_from_id.append(product['id'])
                new_foodname.append(product['foodname'])
                new_cert.append(product['cert'])
                new_org.append(product['org'])
                new_to_id.append(product['id'])
            else:
                for simproduct in results2:
                    new_from_id.append(product['id'])
                    new_foodname.append(product['foodname'])
                    new_cert.append(product['cert'])
                    new_org.append(product['org'])
                    new_to_id.append(simproduct['v_id'])
            
    nodes_from_df = pd.DataFrame({
            'Food ID': [int (i) for i in new_from_id],
            'Name': new_foodname,
            'Halal Certifate': new_cert,
            'Issuing Authority': new_org
            })
    
    nodes_to_df = pd.DataFrame({
            'Food ID': [int (i) for i in new_to_id],
            'Name': '',
            'Halal Certifate': '',
            'Issuing Authority': ''
            })
    
    nodes_df = nodes_from_df.append(nodes_to_df)
        
    edges_df = pd.DataFrame({
            'from_id': [int (i) for i in new_from_id],
            'to_id': [int (i) for i in new_to_id]
            })
        
    nodes_df = nodes_df.drop_duplicates(subset='Food ID')
    edges_df = edges_df.drop_duplicates()
        
    try:
        res = nodes_df.values.tolist()
        toc = time.perf_counter()
        logger.info(f'Query Execution: {toc - tic:0.02f} seconds')
        logger.debug('Query Result Count: %s', len(res))
        metrics['tigergraph_time'] = toc - tic

        # Calculate the metrics
        metrics['node_cnt'] = nodes_df.size
        metrics['prop_cnt'] = (nodes_df.size * nodes_df.columns.size) + \
                                (edges_df.size * edges_df.columns.size)

        if nodes_df.size > 0:
            url = plot_url(nodes_df, edges_df)
#            g = graphistry.edges(edges_df).bind(source='from_id', destination='to_id')
#            url = g.plot(render=False, as_files=True)
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
        
        main_area(sidebar_filters['top'], sidebar_filters['selval'], \
                  sidebar_filters['selstr'], sidebar_filters['conn'])

    except Exception as exn:
        st.write('Error loading dashboard')
        st.write(exn)
