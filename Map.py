import math
import matplotlib.pyplot as plt
from io import BytesIO
import sys


class Map:
    def __init__(self, points):
        """
        Instantiate an Map object with route corodinates added to the Map object
        :param points: a list of tuples contains latitude and longitude of a route
        """
        print(points)
        print(type(points))
        
        self._points = points
        print(self._points)
        print(type(self._points))
        #firstco = ["{{lat: {lat}, lng: {lng}}}".format(lat=x, lng=y ) for x, y, *other in self._points]
        #secondco = firstco.join(",\n".join(["{{lat: {lat}, lng: {lng}}}".format(lat=a, lng=b ) for *other, a, b in self._points]))
        self.google_coordinates = ",\n".join(["{{lat: {lat}, lng: {lng}}}".format(lat=x, lng=y) for x, y, *rest in self._points])
##        firstco=""
##        # getting length of list 
##        length = len(self._points)
##        print(self._points[0][0])
##        a = self._points[0][0]
##        print(a)
##        b = self._points[0][1]
##        c = self._points[0][2]
##        d = self._points[0][3]
##        firstco.join(["{{lat: {lat}, lng: {lng}}}".format(lat=a, lng=b ) ]).join(",\n")
##        print(firstco)
##        #firstco.join(["{{lat: {lat}, lng: {lng}}}".format(lat=self._points[0][2], lng=self._points[0][3] ) ])
##        #print(firstco)             
                             
            
           
            
        #self.google_coordinates = firstco
        #",\n".join(["{{lat: {lat}, lng: {lng}}}".format(lat=x, lng=y ) for x, y, *other in self._points].)
        #.join(["{{lat: {lat}, lng: {lng}}}".format(dlat=x, dlan=y) for x, y in self._points])
        print(self.google_coordinates )
        
    @property
    def zoom(self):
        
        """
        Algorithm to derive zoom from a route. For details please see
        - https://developers.google.com/maps/documentation/javascript/maptypes#WorldCoordinates
        - http://stackoverflow.com/questions/6048975/google-maps-v3-how-to-calculate-the-zoom-level-for-a-given-bounds
        :return: zoom value 0 - 21 based on the how widely spread of the route coordinates
        """
        min_zoom = 14
        
        return min_zoom

    @property
    def center(self):
        """
        Calculate the center of the current map object (19.7514798, 75.7138884)
        :return: (center_lat, center_lng) latitude, longitude represents the center of the map object
        """
        center_lat =  18.5204303#19.7514798 #self._points[0][0]#(max((x[0] for x in self._points[0])) + min((x[0] for x in self._points[0]))) / 2
        center_lng =  73.8567437#75.7138884 #self._points[0][1]#(max((x[1] for x in self._points[0])) + min((x[1] for x in self._points[0]))) / 2
        return center_lat, center_lng

    @property
    def altitude_svg(self):
        """
        Create an svg data object using matplotlib for altitude chart that can be injected into html template
        :return: altitude_svg; svg data for altitude chart
        """
        altitudes = self._points[0][4]
        distances = self._points[0][5]
        plt.figure(figsize=(12, 1.5))
        plt.ylabel('Altitude(m)')
        plt.tight_layout()
        plt.plot(distances, altitudes)
        svg_file = BytesIO()
        plt.savefig(svg_file, format='svg')     # save the file to io.BytesIO
        svg_file.seek(0)
        altitude_svg = svg_file.getvalue().decode() # retreive the saved data
        altitude_svg = '<svg' + altitude_svg.split('<svg')[1]   # strip the xml header
        return altitude_svg

    @staticmethod
    def _lat_rad(lat):
        """
        Helper function for calculating latitude spread across the map
        """
        sinus = math.sin(math.radians(lat + math.pi / 180))
        rad_2 = math.log((1 + sinus) / (1 - sinus)) / 2
        return max(min(rad_2, math.pi), -math.pi) / 2
