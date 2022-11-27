
import csv
import streamlit as st
import matplotlib.pyplot as plt
from matplotlib import style


def Graph(x1, x2, x3, y, predicting):
    # graph showing past data
    fig = plt.figure()
    
    # applies style to figure
    style.use("ggplot")
    fig.set_figheight(3)
    
    # sets up layout
    plt.margins(0,0)
    ax = plt.axes([0,0,1,1])
    plt.xlim(0,8)
    
    # plots the 3 different sets of data
    defaultXTicks = range(len(x1))
    plt.plot(defaultXTicks, x1, linewidth=2, color="red", label="Monza", marker='.', markersize=10)
    plt.plot(defaultXTicks, x2, linewidth=2, color="xkcd:sky blue", label="Silverstone", marker='.', markersize=10)
    plt.plot(defaultXTicks, x3, linewidth=2, color="green", label="Interlagos", marker='.', markersize=10)
    
    plt.xticks(defaultXTicks, y, fontsize=7.5)
    plt.ylim(69, 103)
    
    # special instructions for predictions
    if predicting:
        plt.xlim(0,11)
        
        ax.grid(zorder=0)
        ax.bar(9.5, 120, width=3, align='center', color='black', alpha=0.1)
    
    # labels
    plt.title("Average Lap Time", fontsize=10, fontweight="bold")
    plt.xlabel("Year", fontsize=10, fontweight="bold")
    plt.ylabel("Lap Time (seconds)", fontsize=10, fontweight="bold")
    plt.legend(loc="upper right")
    
    return fig


def Run():
    # loads in data
    monzaPredictedData = []
    silverstonePredictedData = []
    interlagosPredictedData = []
    
    with open("data/LaptimeData.csv", "r") as f:
        file = csv.reader(f)
        next(file) # skips the header
        
        for row in file:
            col = 0
            for time in row:
                # checks to see if column is pointing to track name
                if col != 0:
                    if row[0] == "Monza":
                        monzaPredictedData.append(float(time))
                    elif row[0] == "Silverstone":
                       silverstonePredictedData.append(float(time))
                    elif row[0] == "Interlagos":
                        interlagosPredictedData.append(float(time))
                col += 1
    
    # seperates predicted data to only show past data
    monzaAverageTimes = monzaPredictedData[:len(monzaPredictedData) - 3]
    silverstoneAverageTimes = silverstonePredictedData[:len(silverstonePredictedData) - 3]
    interlagosAverageTimes = interlagosPredictedData[:len(interlagosPredictedData) - 3]
    
    
    # title
    st.write("""
            # F1 V6-Era Laptime Analysis
            """)


    # graph showing past data
    st.write("""
                #### Past Years
            """)

    yearsList = [2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022]

    graph1 = Graph(monzaAverageTimes, silverstoneAverageTimes, interlagosAverageTimes, yearsList, False)
    st.pyplot(graph1)


    # graph showing predicted outcomes 
    st.write("""
                #### Forecast
            """)

    yearsList = [2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025]

    graph2 = Graph(monzaPredictedData, silverstonePredictedData, interlagosPredictedData, yearsList, True)
    st.pyplot(graph2)

    st.caption("""
            (Predictions located in the greyed zone)
            """)


if __name__ == "__main__":
    Run()
