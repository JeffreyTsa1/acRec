from flask import Flask
from flask import request
from flask_restful import Resource, Api, reqparse
import json
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer

app = Flask(__name__)
api = Api(app)

## Get API Method
@app.route('/get')
def get():
    ## Takes budget, and combo as input.
    targetPrice = int(request.args.get('budget'))
    combo = request.args.get('combo')
    df = pd.read_csv(r'app/kbbData.csv').dropna()
    print(df)
    if targetPrice < 20000:
        # if combo == "RU":
        # elif combo == "RC":
        # elif combo == "UC":
        if combo == "R":
            # 19990: Civic
            targetID = 7185
        elif combo == "U":
            # 19980: BMW 5-Series
            targetID = 34
        elif combo == "C":
            # 16000: Ford Fiesta, Hyundai
            targetID = 109

    elif targetPrice < 50000:
        # if combo == "RU":
        # elif combo == "RC":
        # elif combo == "UC":
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
            # Cadillac Escalade, 130
            targetID = 1007

    listingCount, featureCount = df.shape
    csvData = df
    features = []
    for index, row in csvData.iterrows():
        ## Append relevant features to the featurelist, for vectorization. Transforms given text into a vector on the basis of frequency of each word.
        features.append("year" + str(row['year']) + " " + str(row['drive']).replace(' ','') + " " + str(row['engine']).replace('-','') + " " + " " + str(row['body']) + " " + str(row['fuelEfficiency']).replace(' ',''))
    
    
    csvData["importantFeatures"] = features
    
    
    vectorizer = CountVectorizer()
    featureMatrix = vectorizer.fit_transform(csvData["importantFeatures"])
    # print(vectorizer.vocabulary_)
    
    ## Create a cosine similarity matrix from the count matrix
    cSim = cosine_similarity(featureMatrix)

    ## Get the shape of similarity matrix
    csShape = cSim.shape

    ## This is the ID of the car the user's recommendations will be based upon.
    targetItemRow = csvData[csvData.id == targetID]
    if len(targetItemRow.index) != 0:
        print(targetItemRow['name'].values[0])
    #List of recommended cars for the similarity score
    scores = list(enumerate(cSim[targetID]))
    # print(targetCarName.values[0])
    minPrice = targetPrice-(targetPrice*0.33)
    #Sort the list
    rankedScores = sorted(scores, key = lambda x:x[1], reverse = True)    
    rankedScores=rankedScores[1:]
    count = 0
    desiredListings = 20
    carList = []
    for item in rankedScores:
        itemID = item[0]
        # print(count)
        itemRow = csvData[csvData.id == itemID]
        if len(itemRow.index) != 0:
            carPrice = csvData[csvData.id == itemID]['price'].values[0]
            carName = csvData[csvData.id == itemID]['name'].values[0]

            if carPrice < targetPrice and carPrice > minPrice:
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