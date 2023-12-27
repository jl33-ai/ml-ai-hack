import pandas as pd
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from joblib import dump

"""
NOTE: THIS IS STRICTLY A PREDICTIVE TOOL
WE DO NOT CONDONE FARE EVADING 
PART OF A LARGE SUITE OF JOURNEY PREDICTIONS, FOR THOSE WHO MAY FIND IT ANXIOUS

"""

reversed_train_lines = {
    'alamein': 1,
    'belgrave': 2,
    'craigieburn': 3,
    'cranbourne': 4,
    'frankston': 5,
    'glen_waverley': 6,
    'hurstbridge': 7,
    'lilydale': 8,
    'mernda': 9,
    'pakenham': 10,
    'sandringham': 11,
    'stony_point': 12,
    'sunbury': 13,
    'upfield': 14,
    'werribee': 15,
    'williamstown': 16
}

train_lines = {number : line for line, number in reversed_train_lines.items()}
print(train_lines)

# LOAD DATA HERE. 
data = pd.read_csv('/Users/justinlee/Documents/projport/ml-ai-hack/full-pipeline/ao_sightings.csv')

X = data.drop('numSightings', axis=1)
y = data['numSightings']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=1337)

gbr = GradientBoostingRegressor(n_estimators=100, learning_rate=0.1, max_depth=5)

gbr.fit(X_train, y_train)

predictions = gbr.predict(X_test)

mse = mean_squared_error(y_test, predictions)

dump(gbr, 'grad-boost-trained-model.joblib')