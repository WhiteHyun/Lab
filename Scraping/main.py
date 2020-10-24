from datetime import date
from weather import extract_weather
from database import connect_sql

DAY = 0
HOUR = 1
TEMPERATURE = 2
HUMIDITY = 3

if __name__ == "__main__":
    weather_data = extract_weather()
    today = date.today()
    time = ""
    for i in range(len(weather_data)):
        if weather_data[i][DAY] == "0":
            time = f"{today.year}년 {today.month}월 {today.day}일"
        elif weather_data[i][DAY] == "1":
            time = f"{today.year}년 {today.month}월 {today.day+1}일"
        elif weather_data[i][DAY] == "2":
            time = f"{today.year}년 {today.month}월 {today.day+2}일"
        print(f"""
        ================================
        날짜: {time} {weather_data[i][HOUR]}시
        온도: {weather_data[i][TEMPERATURE]}
        습도: {weather_data[i][HUMIDITY]}
        ================================
        """)

    cursor = connect_sql()
    if cursor is None:
        print("연동실패")
    else:
        print("연동성공")
