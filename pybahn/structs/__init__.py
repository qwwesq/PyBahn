from enum import StrEnum, Enum


class Filter(StrEnum):
    """
    Args:
        IC: - IC(intercity), EC(eurocity).
        FLX: - means trains like NJ, FLX, RJ etc.
        S: - S-Bahn(city train).
        U: - U-Bahn(underground).

    
    ``Example of use``::
    
        from pybahn import PyBahn
        from pybahn.structs import Filter

        client = PyBahn(__name__)

        station = client.station("Frankfurt")
        departures = client.departures(id=station.id, filters=[Filter.TRAM])

        print(departures[0].canceled)
    ..
    """
    ICE = "&filterTransports=HIGH_SPEED_TRAIN"
    IC = "&filterTransports=INTERCITY_TRAIN"
    FLX = "&filterTransports=INTER_REGIONAL_TRAIN"
    RB_RE = "&filterTransports=REGIONAL_TRAIN"
    S = "&filterTransports=CITY_TRAIN"
    U = "&filterTransports=SUBWAY"
    BUS = "&filterTransports=BUS"
    TRAM = "&filterTransports=TRAM"

class Products(Enum):
    """
    ``Example of use``::
    
        from pybahn import PyBahn
        from pybahn.structs import Products

        client = PyBahn(__name__)

        station1 = client.station("Frankfurt")

        station2 = client.station("Berlin")
        
        journeys = client.journeys(station1, station2, products=[Products.REGIONAL])

        print(journeys[0])
    ..
    """
    ICE = "ICE"
    EC_IC = "EC_IC"
    IR = "IR"
    REGIONAL = "REGIONAL"
    SBAHN = "SBAHN"
    UBAHN = "UBAHN"
    BUS = "BUS"
    TRAM = "TRAM"
    RUF = "ANRUFPFLICHTIG"
    
    REGIONALS = ["REGIONAL", "SBAHN", "UBAHN", "BUS", "TRAM", "ANRUFPFLICHTIG"]
    ALL = ["ICE", "EC_IC", "IR", "REGIONAL", "SBAHN", "UBAHN", "BUS", "TRAM", 'ANRUFPFLICHTIG']

