from datetime import date
from weather import extract_weather
from database import connect_sql

DAY = 0
HOUR = 1
TEMPERATURE = 2
HUMIDITY = 3
TODAY = "0"

if __name__ == "__main__":
    weather_data = extract_weather()
    data_length = len(weather_data)
    today = date.today()
    time = ""
    for i in range(data_length):
        if weather_data[i][DAY] != TODAY:  # 내일이나 모레의 값은 사용하지 않으므로 continue로 다음 인덱스로 넘어감
            continue
        else:
            # 데이터베이스에 DATE값을 넣기위해 날짜 사이에 형식을 '-' 로 채움
            time = f"{today.year}-{today.month}-{today.day}"
            weather_data[i][DAY] = time
        print(f"""
        ================================
        날짜: {weather_data[i][DAY]} {weather_data[i][HOUR]}시
        온도: {weather_data[i][TEMPERATURE]}
        습도: {weather_data[i][HUMIDITY]}
        ================================
        """)

    cursor = connect_sql()
    if cursor is None:
        print("연동실패")
    else:
        print("연동성공")
