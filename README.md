
# Pybahn

A Python library to query Deutsche Bahn journey, departure, and arrival data using the (unofficial) API.

## 📚 Table of Contents

- [📦 Installation](#-installation)
- [🛠️ Usage](#️-usage)
  - [🔧 Initialize PyBahn](#-initialize-pybahn)
  - [🔍 Search Stations](#-search-stations)
  - [📍 Get a Single Station](#-get-a-single-station)
  - [🗺️ Nearby Stations](#-nearby-stations)
  - [🚉 Departures](#-departures)
  - [🚉 Arrivals](#-arrivals)
  - [🚆 Journeys](#-journeys)
  - [🎯 Filter Departures/Arrivals](#-filter-departuresarrivals)
  - [🎯 Filter Journeys](#-filter-journeys)
  - [🚆 Stopovers](#-stopovers)
- [⚠️ License](#-license)
- [⚠️ Disclaimer](#️-disclaimer)



## 📦 Installation

```bash
pip install pybahn
```
    
## 🛠️ Usage

### 🔧 Initialize PyBahn

```python
from pybahn import PyBahn

bahn = PyBahn("your_app")
```


### 🔍 Search Station

```python
stations = bahn.stations("Berlin")

print(stations[0].name)
```

### 📍 Get a Single Station

```python
station = bahn.station("Munich")
```

### 🗺️ Nearby Stations

```python
stations = bahn.nearby(latitude=00.00000, longitude=00.0000)
```

### 🚉 Departures

```python
departures = bahn.departures("8000105")  # Berlin Hbf

print(departures[0].lineName)
```

#### or

```python
station = bahn.station("Munich")

departures = bahn.departures(station)

print(departures[0].lineName)
```

### 🚉 Arrivals

```python
arrivals = bahn.arrivals("8000105")  # Berlin Hbf

print(arrivals[0].lineName)
```

#### or

```python
station = bahn.station("Munich")

arrivals = bahn.arrivals(station)

print(arrivals[0].lineName)
```


### 🚆 Journeys

``` python

station1 = bahn.station("Frankfurt")

station2 = bahn.station("Berlin")

journeys = bahn.journeys(station1.lid, stat2.lid)

print(journeys[0].arrival_name)
```

#### or 

```python
station1 = bahn.station("Frankfurt")

station2 = bahn.station("Berlin")

journeys = bahn.journeys(station1, station2)

print(journeys[0].arrival_name)
```


### 🎯 Filter Departures/Arrivals

```python
from pybahn.structs import Products
from datetime import datetime

station1 = bahn.station("Frankfurt")

station2 = bahn.station("Berlin")

time = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")

journeys = bahn.journeys(departure = station1, 
                      destination = station2, 
                      time = time,
                      products = [Products.EC_IC, Products.SBAHN],
                      only_d_ticket = True)

print(journeys[0].changes_amont)
```


### 🎯 Filter Journeys

```python
from pybahn.structs import Products


station1 = bahn.station("Frankfurt")

station2 = bahn.station("Berlin")

journeys = bahn.journeys(station1.lid, station2.lid, products=Products.REGIONALS)

print(journeys[0].changes_amont)
```

#### or

```python
from pybahn.structs import Products


station1 = bahn.station("Frankfurt")

station2 = bahn.station("Berlin")

journeys = bahn.journeys(departure=station2, 
                           destination=station1, 
                           products=[Products.EC_IC, Products.REGIONAL])

print(journeys[0].changes_amont)
```

### 🚆 Stopovers

```python
from datetime import datetime


station1 = bahn.station("kassel")

station2 = bahn.station("Berlin")

stopo = bahn.station("frankfurt")
stopo.stopover_time = 5


time = datetime.strptime("2025-05-23T21:40:00", "%Y-%m-%dT%H:%M:%S")
time = time.strftime("%Y-%m-%dT%H:%M:%S")


journeys = bahn.journeys(departure=station1, destination=station2, stopovers=[stopo], time=time)


print(journeys)
```

## 📄 License

[MIT License](https://choosealicense.com/licenses/mit/)

## ⚠️ Disclaimer

This library (`pybahn`) is an **unofficial** wrapper around Deutsche Bahn’s internal web APIs, discovered via publicly accessible browser traffic.

- It is **not affiliated with or endorsed by Deutsche Bahn**.
- It uses **undocumented and unsupported endpoints**, which may break or change without notice.
- Use this library **at your own risk**.
- Please respect Deutsche Bahn’s terms of use and avoid abusive behavior.
