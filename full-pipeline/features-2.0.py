import datetime 
from datetime import date
from joblib import load
import pandas as pd

gbr = load('grad-boost-trained-model.joblib')
train_lines = {1: 'alamein', 2: 'belgrave', 3: 'craigieburn', 4: 'cranbourne', 5: 'frankston', 6: 'glen_waverley', 7: 'hurstbridge', 8: 'lilydale', 9: 'mernda', 10: 'pakenham', 11: 'sandringham', 12: 'stony_point', 13: 'sunbury', 14: 'upfield', 15: 'werribee', 16: 'williamstown'}
def getAnnoyanceScore(trainLine): 
    """
    Takes trainLine (1-16)
    Returns current annoyance score (date/time)
    Annoyance score calculated from: 
        - Recorded foot traffic data from Google Maps 
        - Reddit threads 
        - Predicted AO sightings (gradient boosting) scraped from Private Facebook Groups
        - https://philipmallis.com/blog/2019/02/21/which-are-the-least-and-most-used-stations-in-victoria/
        - https://www.timeout.com/melbourne/blog/melbournes-train-lines-definitively-ranked-from-best-to-worst-011917
    """
    special_dates = [datetime.date(2023, 1, 1), datetime.date(2023, 12, 25)]  
    data = []
    random_date = date.today()

    # Extract day of the week (Monday=1, Sunday=7)
    day_of_week = random_date.isoweekday()
    # Extract week of the year
    week_of_year = random_date.isocalendar()[1]
    # Check if it's a weekend (Saturday or Sunday)
    is_weekend = day_of_week in [6, 7]
    # Check if it's a special date
    is_special_date = random_date in special_dates

    data.append((trainLine, day_of_week, week_of_year, is_weekend, is_special_date))
    daily_predictions = pd.DataFrame(data, columns =['lineNumber', 'dayOfWeek', 'weekOfYear', 'isWeekend', 'isSpecialDate'])

    #print(f"Mean Squared Error: {mse}")

    a_score = round(gbr.predict(daily_predictions)[0], 1)
        
    #a_score = 0.33 * () + 0.33 * () + 0.34 * ()

    return a_score


print(getAnnoyanceScore(3))

