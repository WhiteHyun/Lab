from datetime import date
from weather import extract_weather
from database import *

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

    """
    데이터베이스 연동 코드
    """
    print(connect_sql.__doc__)  # connect_sql 함수가 무엇을 하는 함수인지 확인함
    cursor, conn = connect_sql()
    if cursor is None:
        print("연동실패")
    else:
        print("연동성공")

    """
    데이터베이스 Execute 코드

    '데이터 조회 SELECT 이용 방법'
    sql = "SELECT * FROM 'TABLE_NAME';"
    cursor.execute(sql)     #sql문을 실행합니다.
    result = cursor.fetchall()  #실행한 결과를 fetchall()을 통해 받아올 수 있습니다.
    
    '데이터 삽입/변경/삭제 이용 방법'
    sql = "INSERT INTO 'TABLE_NAME' (ATTRIBUTES...) VALUES (ATTRIBUTES...);"    #삽입
    sql = "UPDATE 'TABLE_NAME' SET 'FIELD' = 'ATTRIBUTE' WHERE 'FIELD 조건부';"     #변경
    sql = "DELETE FROM 'TABLE_NAME' WHERE 'FIELD 조건부';"  #삭제
    cursor.execute(sql)
    conn.commit()
    """

    # 예시
    sql = "SELECT * FROM 'TABLE_NAME';"
    cursor.execute(sql)
    result = cursor.fetchall()  # fetchall 함수를 통해 결과값을 받아옴
