# Linked Open Data Halal Visualization

## What is LODHalal?

Linked Open Data system for halal products (LODHalal) proposed a halal food vocabulary that is enhanced from two food existing vocabularies. Furthermore, it provides two interfaces: a web application and an Android application that are able to search a food product and predict a halal status of an uncertified-halal product.

## Dataset
See [DATASET.md](DATASET.md) for more dataset information

## Query Set

The installed queris at TGCloud can be found at [query](query) directory
The following line codes is an example for calling one of the query using [pytigergraph](https://pypi.org/project/pyTigerGraph/).

```python
params = {"foodname":"indomie"} #query's arguments
queryName = "GetProductByName"
preInstalledResult = conn.runInstalledQuery(queryName, params) 
print(preInstalledResult)
```
## Visualization



## Teams

Department of Information Systems, Insitut Teknologi Sepuluh Nopember Surabaya, Indonesia

* Nur Aini Rakhmawati, PhD
* Dr. Rarasmaya Indraswari
* Irfan Rifqi Susetyo
* Girraz Karyo Utomo


