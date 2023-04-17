# Grondwater minimal example

Instructions:

**First Insert the SAS token in grondwater_minimal.py**
```
pip install virtualenv
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
python grondwater_minimal.py  
```
Should result in:
```
(2098, 2942)
{'driver': 'GTiff', 'dtype': 'uint8', 'nodata': None, 'width': 2942, 'height': 2098, 'count': 1, 'crs': CRS.from_epsg(28992), 'transform': Affine(25.0, 0.0, 183525.0,
       0.0, -25.0, 479450.0)}
```
