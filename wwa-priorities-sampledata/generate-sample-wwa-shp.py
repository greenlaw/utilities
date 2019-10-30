#!/usr/bin/env python3
"""
Generate a sample WWA shapefile with at least one of each potential WWA type.

WWA polygons are created as concentric circles over the Contiguous U.S., with
highest-priority WWAs as the innermost circles. This can then be used to
develop symbology and validate precedence, with the target output looking like
a jawbreaker. For an example, see ``wwa_sample_priority.jpg``.

Actual source shapefile containing target schema can be downloaded from:

    https://tgftp.nws.noaa.gov/SL.us008001/DF.sha/DC.cap/DS.WWA/

Possible WWAs are read from ``wwa-types-by-priority.csv``, which was populated
with exact values from:

    https://alerts-v2.weather.gov/events

then sorted (highest-priority first) according to the priorities defined at:

    https://www.weather.gov/help-map
"""
import fiona
from shapely.geometry import mapping, Point

WWA_LIST_CSV = "wwa-types-by-priority.csv"

WWA_SHP_OUT = "wwa_priority_sample.shp"
WWA_SHP_FIELDS = {
    "EXPIRATION": "str:25",
    "SIG": "str:1",
    "WFO": "str:4",
    "MSG_Type": "str:3",
    "PHENOM": "str:2",
    "URL": "str:255",
    "PROD_TYPE": "str:40",
    "ISSUANCE": "str:25",
    "WARNID": "str:31",
    "EVENT": "str:4"
}
WWA_SHP_FIELD_DEFAULTS = {
    "EXPIRATION": "2019-10-30T01:00:00+00:00",
    "SIG": "W",
    "WFO": "KGYX",
    "MSG_Type": "XXX",
    "PHENOM": "XX",
    "URL": "https://alerts-v2.weather.gov/products/NWS-IDP-PROD-3891376-3315413",
    "PROD_TYPE": "",
    "ISSUANCE": "2019-10-29T19:00:00+00:00",
    "WARNID": "O.NEW.KFGZ.FW.W.0009.1572375600",
    "EVENT": "0009"
}

CONUS_CENTROID = Point(-98.5833, 39.8333)

BUFFER_INCREMENT = 0.1

def main():
    wwa_list = []
    with open(WWA_LIST_CSV, "r") as wwa_csv:
        for line in wwa_csv:
            wwa = line.strip()
            if len(wwa) > 0:
                wwa_list.append(wwa)

    schema = {
        "geometry": "Polygon",
        "properties": WWA_SHP_FIELDS
    }
    with fiona.open(WWA_SHP_OUT, "w", "ESRI Shapefile", schema) as shp:
        buffer_size = BUFFER_INCREMENT
        for wwa in wwa_list:
            props = WWA_SHP_FIELD_DEFAULTS
            props["PROD_TYPE"] = wwa
            shp.write({
                "geometry": mapping(CONUS_CENTROID.buffer(buffer_size)),
                "properties": props
            })
            buffer_size += BUFFER_INCREMENT
    
    

if __name__ == "__main__":
    main()

