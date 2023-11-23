import pandas as pd
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import datetime 
from datetime import date

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

# LOAD DATA HERE. 
data = pd.read_csv('/Users/justinlee/Documents/projport/ml-ai-hack/ao_sightings.csv')

X = data.drop('numSightings', axis=1)
y = data['numSightings']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=1337)

gbr = GradientBoostingRegressor(n_estimators=100, learning_rate=0.1, max_depth=5)

gbr.fit(X_train, y_train)

predictions = gbr.predict(X_test)

mse = mean_squared_error(y_test, predictions)

special_dates = [datetime.date(2023, 1, 1), datetime.date(2023, 12, 25)]  
data = []
for i in range(1, 17):  # Line numbers
    # Generate a random date
    random_date = date.today()
    # Extract day of the week (Monday=1, Sunday=7)
    day_of_week = random_date.isoweekday()

    # Extract week of the year
    week_of_year = random_date.isocalendar()[1]

    # Check if it's a weekend (Saturday or Sunday)
    is_weekend = day_of_week in [6, 7]

    # Check if it's a special date
    is_special_date = random_date in special_dates

    # Append the data
    data.append((i, day_of_week, week_of_year, is_weekend, is_special_date))
daily_predictions = pd.DataFrame(data, columns =['lineNumber', 'dayOfWeek', 'weekOfYear', 'isWeekend', 'isSpecialDate'])

print(f"Mean Squared Error: {mse}")



for i in range(1, 17):
    print(f"Today, the predicted number of sightings on the {train_lines[i]} line is: ", round(gbr.predict(daily_predictions)[i-1], 1))