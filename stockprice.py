import math
import pandas_datareader as web
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential
from keras.layers import Dense,LSTM
import matplotlib.pyplot as plt
plt.style.use('fivethirtyeight')

#Extract the stock of Microsoft
df = web.DataReader('MSFT',data_source='yahoo',start='2010-01-01',end='2020-12-31')
print(df['Close'])

#Visualize the closing price history
plt.figure(figsize=(16,8))
plt.title('Close price history')
plt.plot(df['Close'])
plt.xlabel('Data',fontsize=18)
plt.ylabel('Close Price $',fontsize=18)
plt.show()

print(df.shape)

 #Create new dataframe with close column
 data=df.filter(['Close'])
 #Convert the dataframe numpy
 dataset = data.values
 #no of rows
 training_data_len=math.ceil(len(dataset)*0.8)
 print(training_data_len)
 
 #Scale the data
scaler = MinMaxScaler(feature_range=(0,1))
scaled_data = scaler.fit_transform(dataset)

print(scaled_data)

#Create the training dataset
train_data=scaled_data[0:training_data_len,:]
#Split the data into x_train and y_train
x_train=[]
y_train=[]

for i in range(60,len(train_data)):
  x_train.append(train_data[i-60:i,0])
  y_train.append(train_data[i,0])
  if i<=61:
    print(x_train)
    print(y_train)
    print()
    
x_train,y_train=np.array(x_train),np.array(y_train)

#Reshape the data
x_train=np.reshape(x_train,(x_train.shape[0],x_train.shape[1],1))
print(x_train.shape)

#Build the LSTM model
model = Sequential()
model.add(LSTM(50,return_sequences=True,input_shape=(x_train.shape[1],1)))
model.add(LSTM(50,return_sequences=False))
model.add(Dense(25))
model.add(Dense(1))

#Compile the model
model.compile(optimizer='adam',loss='mean_squared_error')

#Train model
model.fit(x_train,y_train,batch_size=1,epochs=1)

#Create the testing data set
#new array from index 1543 to 2003
test_data =scaled_data[training_data_len-60: , : ]
#Create data set
x_test=[]
y_test=dataset[training_data_len:, : ]
for i in range(60,len(test_data)):
  x_test.append(test_data[i-60:i,0])


#Convert the data to numpy array
x_test=np.array(x_test)

#Reshape
x_test = np.reshape(x_test,(x_test.shape[0],x_test.shape[1],1))

#Get the models predicted price values
predictions = model.predict(x_test)
predictions = scaler.inverse_transform(predictions)

#Get the (RMSE)
rmse = np.sqrt(np.mean(predictions-y_test)**2)
print(rmse)

#Plot the data
train = data[:training_data_len]
valid = data[training_data_len:]
valid['Predictions']=predictions
#Visualize
plt.figure(figsize=(16,8))
plt.title('Model')
plt.xlabel('Date',fontsize=18)
plt.ylabel('Close Price USD',fontsize=18)
plt.plot(train['Close'])
plt.plot(valid[['Close','Predictions']])
plt.legend(['Train','Val','Predictions'],loc='lower right')
plt.show()

print(valid)
