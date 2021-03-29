#!/usr/bin/env python
# coding: utf-8

# In[1]:


import graphistry
import pandas as pd
import numpy as np
import requests


# In[2]:


graphistry.register(api=3, protocol="https", server="hub.graphistry.com", username="Girraz", password="Girraz281199")


# In[3]:


import pyTigerGraph as tg

TG_HOST = "https://halal.i.tgcloud.io"
TG_USERNAME= "tigergraph"
TG_PASSWORD="syahnaz"
TG_GRAPH ="halal"
TG_SECRET= "gh9urnvt8aa0hk2tppic1r9vck0jmumj"

conn = tg.TigerGraphConnection(host=TG_HOST, graphname=TG_GRAPH, username=TG_USERNAME, password=TG_PASSWORD)

print(conn.getToken(TG_SECRET, "1000000")) #uses a lifetime of 1,000,000 seconds


# In[ ]:


query = "ProductManufactureLink"
resultTG = conn.runInstalledQuery(query)
results = resultTG[0]['@@tupleRecords']
ProdMan = pd.DataFrame(results)


# In[ ]:





# In[ ]:


get_ipython().run_line_magic('matplotlib', 'inline')
from sklearn.manifold import TSNE
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns
from node2vec import Node2Vec
sns.set_style('whitegrid')
import pandas as pd
import warnings


# In[ ]:


ProdMan.head(10)


# In[ ]:


ProdMan['src']= ProdMan['src'].str.replace(' ', '_')
ProdMan['dest']= ProdMan['dest'].str.replace(' ', '_')


# In[ ]:


g_data = nx.from_pandas_edgelist(ProdMan, source='src',target='dest')


# In[ ]:


#Manufacture
man = ProdMan[['src','dest']].dropna(axis = 0,how = 'any')
man.head()


# In[ ]:


mylist = man.values.tolist()
mylist


# In[ ]:


g_data.add_edges_from(mylist,weight=1,label="Manufacture")


# In[ ]:


labels = [i for i in dict(g_data.nodes).keys()]
labels = {i:i for i in dict(g_data.nodes).keys()}
labels


# In[ ]:


node2vec = Node2Vec(g_data, dimensions=100, walk_length=16, num_walks=5)


# In[ ]:


n2w_model = node2vec.fit(window=7, min_count=1)


# In[ ]:


model = node2vec.fit(window=10,min_count=1)


# In[ ]:


nodeFood =[x for x in ProdMan.src]
nodeFood


# In[ ]:


embeddings = np.array([model.wv[x] for x in nodeFood])
embeddings


# In[ ]:


tsne = TSNE(n_components=2, random_state=7, perplexity=15)
embeddings_2d = tsne.fit_transform(embeddings)


# In[ ]:


import streamlit as st
figure = plt.figure()

ax = figure.add_subplot(111)

ax.scatter(embeddings_2d[:, 0], embeddings_2d[:, 1])
st.write(figure)


# In[ ]:


model.save


# In[ ]:


model.wv.save_word2vec_format('foodmanufacture.emb')


# In[ ]:


words = list(model.wv.vocab)
print(words)


# In[ ]:


model.wv.save_word2vec_format('foodmanufacture.emb','vocab.txt')


# In[ ]:





# In[33]:





# In[34]:





# In[ ]:




