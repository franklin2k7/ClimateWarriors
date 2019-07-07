import sys
import csv
import datetime as dt

class Route:

    def __init__(self, route_file):
        print("in route")
        self.title = "Route "#splitext(route_file)[0]""
        self.trackpoints = []
        self.duraion=""
        self._parse_trackpoints(route_file)
        print("end route")

    def _parse_trackpoints(self, route_file):
        print("in trackpoint " ,route_file)
        reader = csv.DictReader(open(route_file))
        for row in reader:
            print(row)
            tm = row["Time"]
            lat = float(row["SLat"])
            lng = float(row["SLan"])
            dlat = float(row["DLat"])
            dlan = float(row["DLan"])
            try:
                alt = float(row["Alt"])
            except IndexError:
                alt = 0.0
            dist = float(row["Dist"])
            self.trackpoints.append((lat, lng, dlat, dlan, alt, tm, dist ))
            self.trackpoints.append((dlat, dlan, lat, lng, alt, tm, dist ))
