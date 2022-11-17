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
from statsmodels.tsa.arima.model import ARIMA

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
        orders = Order.query.order_by(Order.dateCreated.desc()).join(Product.query.filter_by(shop=shop.id)).all()

        data=[]
        for order in orders:
            converted_date = order.dateCreated.strftime('%x')
            data.append([converted_date, order.quantity])

        start = data[-1][0]
        end = data[0][0]

        base = createBaseData(start, end)

        base_df = pd.DataFrame(base, columns=['Date', 'Sales'])
        sales_df = pd.DataFrame(data, columns=['Date', 'Sales'])
        df = pd.concat([base_df, sales_df])
        df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
        df = df.groupby(df.Date.dt.date)['Sales'].mean()
        df = pd.DataFrame({'Date': df.index, 'Sales': df.values})

        now = datetime.now()
        dates_len = len(pd.date_range(start, now))

        if dates_len > 7:
            s = len(df) - 7
            df = df.iloc[s:len(df)]
        else:
            s = len(df) - dates_len
            df = df.iloc[s:len(df)]

        if len(df) <= 3:
            return Response(
                status=200
            )

        df['Time'] = np.arange(len(df.index))

        x = df.loc[:, ['Time']]
        y = df.loc[:, ['Sales']]

        model = LinearRegression()
        model.fit(x, y)

        pred_df = createPredictionData(start=end, index=len(df.index)-1, periods=2)
        pred_x = pred_df.loc[1:, ['Time']]

        predicted = model.predict(pred_x)

        sales = []
        sales_arima = []
        for i, date in enumerate(df['Date']):
            index = df['Date'].index.start + i
            x = date.strftime("%x")
            if i == len(df['Date']) - 1:
                sales.append({'date': x, 'sales': y.loc[index][0], 'predicted': y.loc[index][0]})
            else:
                sales.append({'date': x, 'sales': y.loc[index][0]})
        
        pred_date = [date.strftime("%a") for date in pred_df['Date']]
        predicted = {'predicted': predicted[0][0], 'date': pred_date[1]}
        sales.append(predicted)

        x = df['Sales']
        model = ARIMA(x, order=(0, 0, 1))
        model_fit = model.fit()
        predicted = model_fit.predict(len(x), len(x))

        for i, date in enumerate(df['Date']):
            index = df['Date'].index.start + i
            d = date.strftime("%a %d")
            if i == len(df['Date']) - 1:
                sales_arima.append({'date': "Today", 'sales': x.loc[index], 'predicted': x.loc[index]})
            else:
                sales_arima.append({'date': d, 'sales': x.loc[index]})

        predicted = {'predicted': predicted.values[0], 'date': "Tomorrow"}
        sales_arima.append(predicted)

        return Response(
            status=200,
            data=[sales, sales_arima],
        )

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
#         for order in orders:
#             converted_date = order.dateCreated.strftime('%x')
#             data.append([converted_date, order.quantity])

#         start = '2022-11-14'
#         end = '2022-11-19'
#         base = createBaseData(start, end)
#         base_df = pd.DataFrame(base, columns=['Date', 'Sales'])

#         #data = createSampleData(start, len(base_df), 1000)
#         sales_df = pd.DataFrame(data, columns=['Date', 'Sales'])
        
#         df = pd.concat([base_df, sales_df])
#         df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
#         df = df.groupby(df.Date.dt.date)['Sales'].mean()
#         df = pd.DataFrame({'Date': df.index, 'Sales': df.values})
#         df['Date'] = pd.to_datetime(df['Date'], errors='coerce')

#         x = df['Sales']

#         model = ARIMA(x, order=(0, 0, 1))
#         model_fit = model.fit()
#         predicted = model_fit.predict(len(x), len(x)+1)

#         sales = []
#         for i, date in enumerate(df['Date']):
#             d = date.strftime("%x")
#             if i == len(df['Date']) - 1:
#                 sales.append({'date': d, 'sales': x.loc[i], 'predicted': x.loc[i]})
#             else:
#                 sales.append({'date': d, 'sales': x.loc[i]})
#         pred_df = createPredictionData(start=end, index=len(df.index)-1, periods=1)
#         pred_date = [date.strftime("%x") for date in pred_df['Date']]
#         predicted = {'predicted': predicted.values[0], 'date': pred_date[0]}
#         sales.append(predicted)

#         return Response(
#             status=200,
#             data=sales,
#         )