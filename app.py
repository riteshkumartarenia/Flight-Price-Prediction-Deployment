import pandas as pd
import pickle
import sklearn
from flask import Flask, render_template, request
from flask_cors import cross_origin

app = Flask(__name__)
model = pickle.load(open('model.pkl','rb'))

@app.route('/')
@cross_origin()
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST','GET'])
@cross_origin()
def predict():
    if request.method =='POST':

        #Date
        date_dep = request.form['Dep_Time']
        Journey_day = int(pd.to_datetime(date_dep, format="%Y/%m/%dT%H:%M").day)
        Journey_month = int(pd.to_datetime(date_dep, format = "%Y/%m/%dT%H:%M").month)

        #Departure Time
        dep_hour = int(pd.to_datetime(date_dep, format="%Y/%m/%dT%H:%M").hour)
        dep_min = int(pd.to_datetime(date_dep,format="%Y/%m/%dT%H:%M").minute)
#-----------------------------------------------------------------------------------------------------------------------#
        #Arrival Time
        date_arr = request.form['Arrival_Time']
        arr_hour = int(pd.to_datetime(date_arr,format="%Y/%m/%dT%H:%M").hour)
        arr_min = int(pd.to_datetime(date_arr, format="%Y/%m/%dT%H:%M").minute)
#-----------------------------------------------------------------------------------------------------------------------#
        # Duration
        dur_hour = abs(arr_hour-dep_hour)
        dur_min = abs(arr_min-dep_min)
#-----------------------------------------------------------------------------------------------------------------------#
        #Airline
        airline = request.form['airline']
        if (airline == 'Jet Airways'):
            airline = 4
        elif (airline == 'Indigo'):
            airline = 3
        elif (airline=='Air India'):
            airline = 1
        elif (airline == 'Multiple_carriers'):
            airline = 6
        elif (airline == 'SpiceJet'):
            airline = 8
        elif (airline=='Vistara'):
            airline = 10
        elif (airline=='GoAir'):
            airline = 2
        elif (airline=='Multiple_carriers_Premium_economy'):
            airline = 7
        elif (airline == 'Jet_Airways_Business'):
            airline = 5
        elif (airline=='Vistara_Premium_economy'):
            airline = 11
        elif (airline=='Trujet'):
            airline = 9
        else:
            airline = 0

#-----------------------------------------------------------------------------------------------------------------------#
        # Total Stopage
        total_stops = int(request.form['stops'])
#-----------------------------------------------------------------------------------------------------------------------#


        #Source
        s = request.form['Source']
        if s=='Delhi':
            source=2
        elif s=='Kolkata':
            source=3
        elif s=='Mumbai':
            source=4
        elif s=='Chennai':
            source=1
        else:
            source = 0

#-----------------------------------------------------------------------------------------------------------------------#
        # Destination
        dest=request.form['Destination']
        if dest=='Cochin':
            dest=1
        elif dest=='Delhi':
            dest=2
        elif dest=='New Delhi':
            dest=5
        elif dest=='Hyderabad':
            dest=3
        elif dest=='Kolkata':
            dest=4
        else:
            dest = 0

#-----------------------------------------------------------------------------------------------------------------------#

        prediction = model.predict([[
            airline,
            source,
            dest,
            total_stops,
            Journey_day,
            Journey_month,
            dep_hour,
            dep_min,
            arr_hour,
            arr_min,
            dur_hour,
            dur_min
        ]])

        output=round(prediction[0],2)
        return render_template('index.html', prediction_text='Your Flight Price is Rs.{}'.format(output))



if __name__ =='__main__':
    app.run(debug=True)