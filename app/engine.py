## Probably why I have a memory leak.
from flask import Flask
from flask import request
from flask_restful import Resource, Api, reqparse
import json
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer
from flask_cors import CORS
## Imports End


## sample link for /GET
# https://carrecommender.herokuapp.com/get?budget=25000&combo=C
# /get?budget=25000&combo=C
# Where budget is the max value the user is willing to spend, and combo is the 


## Basic CORS auth, I will later specify the specific domain of the server my react app is hosted on (Heroku) for safety. 
app = Flask(__name__)
CORS(app)
api = Api(app)

## Get API Method
@app.route('/get')
def get():
    ## Takes budget, and combo as input.
    targetPrice = int(request.args.get('budget'))
    combo = request.args.get('combo')
    s = request.args.get('s')
    
    ## Yes, I would absolutely love to have this directly read from Postgresql, but Heroku doesn't allow me to do this for free, apparently?
    ## Reading from a csv is slower and contributes to my main memory leak issue, but it works.
    df = pd.read_csv(r'app/kbbData.csv').dropna()

    ## Makes recommendations based on each price limit. Currently this is just my hardcoded value, tailored to my biases. 
    ## Current Gold standards for each price range. This will become input values of Player 2, the knowledgable archetype recommending cars.
    if targetPrice < 20000:
        ## We should recommend a reliable car
        if combo == "R":
            # 19990: Civic
            targetID = 7185
        ## We should recommend a usable car
        elif combo == "U":
            # 19980: BMW 5-Series
            targetID = 34
        elif combo == "C":
            # 16000: Ford Fiesta, Hyundai
            targetID = 109

    elif targetPrice < 50000:
        if combo == "R":
            # 54990: Lexus LX570
            targetID = 1362
        elif combo == "U":
            # 55590: BMW M3
            targetID = 1366
        elif combo == "C":
            # Silverado 1500
            targetID = 1116
    elif targetPrice < 100000:
        # if combo == "RU":
        # elif combo == "RC":
        # elif combo == "UC":
        if combo == "R":
            # 88899 Porsche Cayenne
            targetID = 1043
        elif combo == "U":
            # Borsche Turbo
            targetID = 507
        elif combo == "C":
            # 130000 Cadillac Escalade
            ## Rethink how to evaluate this metric better at a higher price point.
            targetID = 1007

    # listingCount, featureCount = df.shape
    csvData = df
    features = []
    for index, row in csvData.iterrows():
        ## Append relevant features to the featurelist, for vectorization. Transforms given text into a vector on the basis of frequency of each word.
        ## Basic text cleaning is done so that the vectorizer is extracting and counting unique tokens for features, rather than incrementing on tokens like "4" from "4-wheel-drive" or "4" from "4-cylinder Turbo". 
        features.append("year" + str(row['year']) + " " + str(row['drive']).replace(' ','') + " " + str(row['engine']).replace('-','') + " " + " " + str(row['body']) + " " + str(row['fuelEfficiency']).replace(' ',''))
    
    ## This column contains a long string with important descriptions about each of the used cars and their specific attributes. It will be parsed by the vectorizer to find other similar cars for recommendation.
    csvData["importantFeatures"] = features
    
    ## CountVectorizer for finding similar car listings.
    vectorizer = CountVectorizer()
    featureMatrix = vectorizer.fit_transform(csvData["importantFeatures"])
    # print(vectorizer.vocabulary_)
    
    ## Create a cosine similarity matrix from the count matrix
    cSim = cosine_similarity(featureMatrix)

    ## Get the shape of similarity matrix
    # csShape = cSim.shape

    ## This is the ID of the car the user's recommendations will be based upon.
    # targetItemRow = csvData[csvData.id == targetID]
    # if len(targetItemRow.index) != 0:
        # print(targetItemRow['name'].values[0])
        
    ## List of scores to evaluate
    scores = list(enumerate(cSim[targetID]))
    # print(targetCarName.values[0])
    ## lower bound is currently set to 5k under. Thinking about adding some functionalities to recommend users cheaper/pricier cars.  
    minPrice = targetPrice-5000
    
    rankedScores = sorted(scores, key = lambda x:x[1], reverse = True)    
    rankedScores=rankedScores[1:]
    count = 0
    desiredListings = 10
    carList = []
    for item in rankedScores:
        itemID = item[0]
        # print(count)
        itemRow = csvData[csvData.id == itemID]
        if len(itemRow.index) != 0:
            carPrice = csvData[csvData.id == itemID]['price'].values[0]
            # carName = csvData[csvData.id == itemID]['name'].values[0]

            if carPrice > minPrice and carPrice < targetPrice:
                ## Pandas dataframe to_dict. orient by records removes Pandas' horrible formatting tendencies.
                js = itemRow.to_dict(orient='records')
                carList.append(js[0])
                count += 1
            # print(f'car: {carName}, price: {carPrice}')
        if count > desiredListings:
            break
    # print(combo)
    # print(carList[0])
    # return carList
    return json.dumps(carList)

# if __name__ == "__main__":
#     app.run()heroku