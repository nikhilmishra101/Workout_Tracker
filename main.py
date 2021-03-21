import requests
import os
import datetime as dt

APP_ID = os.getenv("APP_ID")
API_KEY = os.getenv("API_KEY")
USER_GENDER = "Male"
USER_AGE = 21
USER_HEIGHT = 186.0
USER_WEIGHT = 70.0
YOUR_TOKEN = os.getenv("YOUR_TOKEN")


url = "https://trackapi.nutritionix.com/v2/natural/exercise"


user_exercise = input("Tell me which exercises you did: ")
today = dt.date.today()

headers = {
    "x-app-id":APP_ID,
    "x-app-key":API_KEY,
    "Content-Type":"application/json"
}

params={
    "query":user_exercise,
    "gender":USER_GENDER,
    "weight_kg":USER_WEIGHT,
    "height_cm":USER_HEIGHT,
    "age":USER_AGE

}


response = requests.post(url=url,json=params,headers=headers)
response.raise_for_status
result = response.json()['exercises']

sheety_url = os.getenv("sheety_url")

for exercise in result:
    workouts = {
        "workout": {
            "date": today.strftime("%d/%m/%Y"),
            "time": dt.datetime.now().strftime("%X"),
            "exercise": exercise["user_input"].title(),
            "duration": exercise['duration_min'],
            "calories": exercise['nf_calories']

        }
    }

bearer_headers = {
    "Authorization":f"Bearer {YOUR_TOKEN}"
}
response_sheet = requests.post(url=sheety_url,json=workouts,headers=bearer_headers)
response_sheet.raise_for_status

print(response_sheet.text)
