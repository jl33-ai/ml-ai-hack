from datetime import date
from datetime import datetime
from joblib import load
import pandas as pd
import json

with open('full-pipeline/train_lines_data.json', 'r') as fp:
    line_busy_data = json.load(fp)

gbr = load('full-pipeline/grad-boost-trained-model.joblib')
weekday_dict = ['a_mon', 'b_tue', 'c_wed', 'd_thu', 'e_fri', 'f_sat', 'g_sun']
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
    special_dates = [date(2023, 1, 1), date(2023, 12, 25)]  
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

    pred_sightings = round(gbr.predict(daily_predictions)[0], 1)
    #print("Model Score:", a_score)

    # need current hour [0-23]
    # need train line 
    # need day of week 

    curr_day = weekday_dict[date.today().weekday()]
    raw_curr_hour = int(datetime.now().strftime("%H"))
    curr_hour = (raw_curr_hour+24-3) % 24
    #print(trainLine, curr_day, curr_hour)

    line_busy = line_busy_data[trainLine-1][curr_day][curr_hour] / 1.5
    weighted = 0.25 * (pred_sightings) + 0.75 * (line_busy)

    return f"The calculated annoyance score along the {train_lines[trainLine]} line at hour {raw_curr_hour} is {round(weighted, 2)} out of 10"

for i in range(1, 17):  
    print(getAnnoyanceScore(i))