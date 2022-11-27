
import csv, warnings
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn import preprocessing

# gets rid of panda warning
warnings.simplefilter(action='ignore', category=FutureWarning)


def Average(file):
    averageTimes = [0,0,0,0,0,0,0,0,0]

    with open(file, "r") as f:
        file = csv.reader(f)
        next(file) # skips the header
        
        for row in file:
            col = 0
            for time in row:
                sum = 0
                time = time.split(":") # splits the minutes and seconds
                
                # converts the time to seconds and adds it to the list
                sum += (float(time[0]) * 60) + float(time[1])
                averageTimes[col] += sum
                
                col += 1
                
    # finds the average time for each year
    for i in range(len(averageTimes)):
        averageTimes[i] = round(averageTimes[i] / 20, 3)
    
    return averageTimes


def Predict(x, y, years):
    X = x
    Y = y
    
    # creates dataframe
    data = {"Years": Y, "Times": X}
    df = pd.DataFrame(data)
    
    # creates a new column with shifted times, goes 3 years into the past
    df["Shifted"] = df["Times"].shift(-years)
    df.dropna(inplace=True)
    
    # sets up arrays and normalises x
    X = preprocessing.scale(np.array(df.drop(["Shifted"], 1)))
    Y = np.array(df["Shifted"])
    
    # trains the data
    xTrain, xTest, yTrain, yTest= train_test_split(X, Y)
    clf = LinearRegression()
    clf.fit(xTrain, yTrain)
    
    # checks to make sure accuracy is good enough
    accuracy = clf.score(xTest, yTest)
    #if accuracy < 0:
        #return 0
    
    # cuts out the last 3 years, then takes the last 3 of remaining years
    X = X[:-years]
    xNew = X[-years:]
    
    # returns a list of predictions
    prediction = clf.predict(xNew)
    return prediction


def Run():
    # gets the average daya for each track
    monzaData = Average("data/base/MonzaLapTimes.csv")
    silverstoneData = Average("data/base/SilverstoneLapTimes.csv")
    interlagosData = Average("data/base/InterlagosLapTimes.csv")
    
    # predicts new variables
    yearsToPredict = 3
    yearsList = [2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022]
    monzaPredictedData = Predict(monzaData, yearsList, yearsToPredict)
    silverstonePredictedData = Predict(silverstoneData, yearsList, yearsToPredict)
    interlagosPredictedData = Predict(interlagosData, yearsList, yearsToPredict)
    
    # adds predicted variables to lap time array
    for i in range(len(monzaPredictedData)):
        monzaData.append(round(monzaPredictedData[i], 3))
        silverstoneData.append(round(silverstonePredictedData[i], 3))
        interlagosData.append(round(interlagosPredictedData[i], 3))
    
    # adds the track name
    monzaData.insert(0, "Monza")
    silverstoneData.insert(0, "Silverstone")
    interlagosData.insert(0, "Interlagos")

    # stores data in predicted lap times file
    with open("data/LaptimeData.csv", "w", newline="") as f:
        file = csv.writer(f)
        file.writerow(["Track",2014,2015,2016,2017,2018,2019,2020,2021,2022,2023,2024,2025])

        file.writerow(monzaData)
        file.writerow(silverstoneData)
        file.writerow(interlagosData)
    

if __name__ == "__main__":
    Run()
