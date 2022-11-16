from app import app, db
from flask_login import login_required, current_user
from flask import request
from app.Components.response import Response
from app.models import Order, Shop, Product
from datetime import datetime
import pandas as pd 
import random
from sklearn.linear_model import LinearRegression
import numpy as np
from pmdarima.arima import auto_arima
import pyaf.ForecastEngine as autof

@login_required
@app.route('/api/v1/admin/forecast', methods=['GET'])
def forecast():
    if current_user.userType == 'Buyer':
        return Response(
            status=403,
            message="error",
        )

    if request.method == 'GET':
        shop = Shop.query.filter_by(user=current_user.id).first()
        products = Product.query.filter_by(shop=shop.id).all()
        orders = Order.query.order_by(Order.dateCreated.desc()).join(Product.query.filter_by(shop=shop.id)).all()

        data=[]
        # for order in orders:
        #     converted_date = order.dateCreated.strftime('%x')
        #     data.append([converted_date, order.quantity])

        start = '2021-01-01'
        end = '2022-06-27'
        base = createBaseData(start, end)
        base_df = pd.DataFrame(base, columns=['Date', 'Sales'])

        data = createSampleData(start, len(base_df), 1000)
        sales_df = pd.DataFrame(data, columns=['Date', 'Sales'])
        
        df = pd.concat([base_df, sales_df])
        df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
        df = df.groupby(df.Date.dt.date)['Sales'].mean()
        df = pd.DataFrame({'Date': df.index, 'Sales': df.values})
        df['Time'] = np.arange(len(df.index))
        
        x = df.loc[:, ['Time']]
        y = df.loc[:, ['Sales']]

        model = LinearRegression()
        model.fit(x, y)

        pred_df = createPredictionData(start=end, index=len(df.index)-1)
        pred_x = pred_df.loc[:, ['Time']]
        
        predicted = model.predict(x)

        sales = []
        for i, date in enumerate(df['Date']):
            x = date.strftime("%x")
            sales.append({'date': x, 'sales': y.loc[i][0], 'predicted': predicted[i][0]})


        return Response(
            status=200,
            data=sales,
        )

# @login_required
# @app.route('/api/v1/admin/forecast/arima', methods=['GET'])
# def forecast_arima():
#     if current_user.userType == 'Buyer':
#         return Response(
#             status=403,
#             message="error",
#         )

#     if request.method == 'GET':
#         shop = Shop.query.filter_by(user=current_user.id).first()
#         products = Product.query.filter_by(shop=shop.id).all()
#         orders = Order.query.order_by(Order.dateCreated.desc()).join(Product.query.filter_by(shop=shop.id)).all()

#         data=[]
#         # for order in orders:
#         #     converted_date = order.dateCreated.strftime('%x')
#         #     data.append([converted_date, order.quantity])

#         start = '2021-01-01'
#         end = '2022-06-27'
#         base = createBaseData(start, end)
#         base_df = pd.DataFrame(base, columns=['Date', 'Sales'])

#         data = createSampleData(start, len(base_df), 1000)
#         sales_df = pd.DataFrame(data, columns=['Date', 'Sales'])
        
#         df = pd.concat([base_df, sales_df])
#         df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
#         df = df.groupby(df.Date.dt.date)['Sales'].mean()
#         df = pd.DataFrame({'Date': df.index, 'Sales': df.values})
#         df['Date'] = pd.to_datetime(df['Date'], errors='coerce')

#         train = df[:len(df) - 5]
#         test = df[len(df) - 5:]
        
#         horizon = len(test)

#         lEngine = autof.cForecastEngine()
#         # get the best time series model for test prediction
#         lEngine.train(iInputDS = train, iTime = 'Date', iSignal = 'Sales', iHorizon = horizon)
#         forecast = lEngine.forecast(test, horizon)
#         print(test)
#         print(forecast['Sales_Forecast_Lower_Bound'])
#         print(forecast['Sales_Forecast_Upper_Bound'])

#         # sales = []
#         # for i, date in enumerate(df['Date']):
#         #     x = date.strftime("%x")
#         #     sales.append({'date': x, 'sales': y.loc[i][0], 'predicted': predicted[i][0]})


#         return Response(
#             status=200,
#         )

def createPredictionData(start, index, periods=50):
    dates = pd.date_range(start, periods=periods)

    data = []
    for i, date in enumerate(dates):
        data.append([date, (index + i)])

    df = pd.DataFrame(data, columns=['Date', 'Time'])
    return df

def createBaseData(start, end):
    start = start
    dates = pd.date_range(start, end)
    
    data = []
    for date in dates:
        data.append([date, 0])

    return data

def createSampleData(start, periods, size):
    start = start
    dates = pd.date_range(start, periods=periods)

    data = []
    for i in range(size):
        data.append([random.choice(dates), random.randrange(0, 100)])

    return data

        
