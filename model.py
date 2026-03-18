import pandas as pd
from sklearn.model_selection import train_test_split
import xgboost as xgb
import numpy as np

pd.set_option('future.no_silent_downcasting', True)
df = pd.read_csv('data_with_address.csv', encoding= 'utf-8')
df = df.dropna(subset=['Area', 'Rooms', 'Location', 'Latitude', 'Metro Proximity'])
print(f"Final data with {len(df)} items")
df.to_csv("final_data.csv", index= False, encoding= 'utf-8')


df = df.drop(columns=["Path", "Currency", "ID", 'address'])
df = df[df["Price"] < df["Price"].quantile(0.99)]
df = df[df["Price"] > df["Price"].quantile(0.01)]

df = pd.get_dummies(df, columns=["Location"])
df["Metro Proximity"] = df["Metro Proximity"].map({"True": 1, "False": 0, True: 1, False: 0})
df['Repaired'] = df['Repaired'].apply(lambda x: 1 if x is True else 0)

X = df.drop(['Price'], axis= 1)
y = np.log1p(df["Price"])
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

model = xgb.XGBRegressor(n_estimators=500,
    learning_rate=0.05,
    max_depth=6,
    subsample=0.8)
model.fit(X_train, y_train)
predictions = np.expm1(model.predict(X_test))
