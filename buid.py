import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split

train = pd.read_csv('deploy_df.csv')
#print(train.head(3))

x = train.drop(['Unnamed: 0','Price'],axis=1)
y = train[['Price']]
print(x.head(2))
print(y.head(2))

x_train, x_test, y_train, y_test = train_test_split(x,y,test_size=0.3, random_state=10)

from sklearn.ensemble import RandomForestRegressor
model_rfr = RandomForestRegressor()
model_rfr.fit(x_train,y_train)
y_predict=model_rfr.predict(x_test)

# save model
import pickle
pickle.dump(model_rfr, open('model.pkl','wb'))
model = pickle.load(open('model.pkl','rb'))
print('Final Output:',y_predict)