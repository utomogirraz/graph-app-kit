# Linked Open Data Halal Visualization

## What is LODHalal?

Linked Open Data system for halal products (LODHalal) proposed a halal food vocabulary that is enhanced from two food existing vocabularies. Furthermore, it provides two interfaces: a web application and an Android application that are able to search a food product and predict a halal status of an uncertified-halal product.

## Dataset
See [DATASET.md](DATASET.md) for more dataset information

## Query Set

The installed queris at TGCloud can be found at [query](query) directory.
The following line codes is an example for calling one of the queries using [pytigergraph](https://pypi.org/project/pyTigerGraph/).

```python
params = {"foodname":"indomie"} #query's arguments
queryName = "GetProductByName"
preInstalledResult = conn.runInstalledQuery(queryName, params) 
print(preInstalledResult)
```

## Setting Connection to TGCloud and Graphistry

Connection with TGCloud can be established by entering the TGCloud host info on `/src/python/envs/tigergraph.env` while connection with Graphistry can be established by entering Graphistry account information on `/src/python/envs/graphistry.env`.

## Visualization

To create a new visualization, go to `/src/python/views` and create a new folder.

## Teams

Department of Information Systems, Insitut Teknologi Sepuluh Nopember Surabaya, Indonesia

* Nur Aini Rakhmawati, PhD
* Dr. Rarasmaya Indraswari
* Irfan Rifqi Susetyo
* Girraz Karyo Utomo


