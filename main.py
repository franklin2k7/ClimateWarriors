from flask import Flask, render_template, request
import googlemaps
from datetime import datetime
import csv
from Route import Route
from Map import Map


app = Flask(__name__, template_folder='templates')
duration =""
COEmmision=""
mT=""
 # name of csv file
filename = "maps_records.csv"

with open('apikey.txt') as f:
    api_key = f.readline()
    f.close()

gmaps_key = googlemaps.Client(key=api_key)


@app.route('/')
def home():
    return render_template("home.html")


@app.route('/result', methods=['GET','POST'], strict_slashes=False)
def index():

    context = {
            "key": api_key,
            "title": "Map Demo"
        }
    startLocation = request.form['startLoc']
    endLocation = request.form['endLoc']
    mT = str(request.form.get('_mode'))
    print(str(mT))
    duration = _create_update_CSVFile(startLocation, endLocation)
    rout = Route(filename)
    maps = Map(rout.trackpoints)
  
   
    if "fourWheel" in mT:
        COEmmision = (((rout.trackpoints[0][6])/17) * 2.31)
    elif "TwoWheel" in mT:
        COEmmision = (((rout.trackpoints[0][6])/55) * 2.31)
    else:
        COEmmision = "Yiiykkss !! you made it to 0 "
            
        
    #duration = get_duration
    #route = Route()
    result = {'Start ':startLocation,'Destination ': endLocation, 'Distace ': rout.trackpoints[0][6], 'Duration ': duration, 'Fuel ': "Petrol", "Carbon Emmision ": COEmmision}
    return render_template("template.html", map=maps, context=context, result=result)


def _create_update_CSVFile(sLoc, dLoc):
    print("start csv file filling")
    geocode_result_source = gmaps_key.geocode(sLoc)
    sloc_lat = geocode_result_source[0]["geometry"]["location"]["lat"]
    sloc_lan = geocode_result_source[0]["geometry"]["location"]["lng"]
    startlocCrd = (sloc_lat, sloc_lan)
    print(sLoc, startlocCrd)
     
    geocode_result_destination = gmaps_key.geocode(dLoc)
    deLoc_lat = geocode_result_destination[0]["geometry"]["location"]["lat"]
    deloc_lan = geocode_result_destination[0]["geometry"]["location"]["lng"]
    destlocCrd = (deLoc_lat, deloc_lan)
    print(dLoc, destlocCrd)
    #mT = request.form.get("_mode")
    #print("mt>> ",mT)
    print(destlocCrd)
    

    mydist = gmaps_key.distance_matrix(startlocCrd, destlocCrd)
    
    print(mydist)
    distance = mydist["rows"][0]["elements"][0]["distance"]["text"]
    #dist = ''.join(i for i in distance if i.isdigit())
    dist = distance.split()[0]
    duration = mydist["rows"][0]["elements"][0]["duration"]["text"]
    time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # field names 
    fields = ['Time', 'SLat', 'SLan', 'DLat', 'DLan', 'Alt', 'Dist', 'TranMode']
    rows = [[time, sloc_lat, sloc_lan, deLoc_lat, deloc_lan, '0.0', dist, mT]]

    
   

    

    # writing to csv file
    with open(filename, 'w') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(fields)
        csvwriter.writerows(rows)

    return duration


if __name__ == '__main__':
    app.run(debug=True)
