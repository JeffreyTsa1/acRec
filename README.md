# recAPI
Welcome to pt.2 of AutoCompare, a recommendation system built with Pandas, Scikit-learn, and deployed through Flask. 

This is a slightly older version of the recommendation engine. I've made a few changes since this to the organization of the code, as well as my mathematical model, to eliminate some of the inefficiencies/memory leak and become more accurate.

File Structure:
'engine.py' contains all of the main code.
'wsgi.py' contains the web server gateway interface which forwards requests.
'sampleCarsOutput.json' is a file that contains the json return of the engine running on carID = 1, a Dodge Grand Caravan under the "Cost-effective" combo selection.

Query format:
budget: max budget of cars you would like to look at
combo: type of cars to look at. C = Cost effective cars, U = usable cars, R = reliable cars.
"/get?budget=25000&combo=C", where budget = 25000 and combo = Cost effective cars

Make sure you install all the required dependencies before you run. You can also deploy this project directly to Heroku as through flask.

To run, navigate to this "parent" repository in your terminal and then run the commands in the quotation marks below:
"python3 wsgi.py"

Go to your browser, and add this query string to your link.
"http://127.0.0.1:5000/get?budget=25000&combo=C"


To call my API (It may crash under Heroku H13: Shut down from memory overusage):
"https://carrecommender.herokuapp.com/get?budget=25000&combo=C"


This returns a json with 10 cars that the algorithm thinks would be good recommendations. 