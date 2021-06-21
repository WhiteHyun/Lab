
# Weather Scraping


def extract_weather(is_local=False):
    """크롤링할 예보를 선택할 시 그에 해당하는 함수를 리턴합니다.

    Parameter
    ---------

    `is_local` (bool)
        - True: 동네예보
        - False: 중기예보

    Returns
    -------
    (url, SEQ_NUM=17) -> list: 동네예보 함수
    (url) -> list: 중기예보 함수
    """
    if is_local:
        return __extract_weather_local
    else:
        return __extract_weather_mid_term


def __extract_weather_local(url, SEQ_NUM=17) -> list:
    """
    Explanation
    ----
    분석할 기상청 주소: https://www.weather.go.kr/weather/lifenindustry/sevice_rss.jsp?sido=2800000000&gugun=2818500000&dong=2818582000&x=21&y=3

    참고한 사이트: https://kocoafab.cc/tutorial/view/595

    동네예보를 크롤링하여 값을 가져오는 함수입니다.
    중기예보와는 양식이 틀리오니 적절하게 사용하시길 바랍니다.

    Tags
    -----

    `<day>`: 날짜
        - 오늘: 0
        - 내일: 1
        - 모레: 2

    `<temp>`: 온도

    `<tmx>`: 최고 기온

    `<tmn>`: 최저 기온

    `<sky>`: 하늘 상태

    `<pty>`: 강수 형태

    `<pop>`: 강수 확률

    `<ws>`: 풍속

    `<wd>`: 풍향

    `<reh>`: 습도

    `<r12>`: 12시간 강수량

    `<s12>`: 12시간 신적설

    `<r06>`: 6시간 강수량

    `<s06>`: 6시간 신적설

    Return
    -------

    weather_data (list-dict): 리스트내부의 리스트 마다 각 날짜별 데이터들을 딕셔너리 형태로 가지고있습니다.

    """
    import requests
    from bs4 import BeautifulSoup

    weather_result = requests.get(url)
    weather_soup = BeautifulSoup(weather_result.text, "html.parser")
    data_list = []
    # 시간에 따른 기상 데이터들을 리스트에 저장
    for i in range(SEQ_NUM):
        temp = weather_soup.find("data", {"seq": i})
        if temp is not None:
            data_list.append(temp)

    data_length = len(data_list)
    weather_data = [[] for i in range(len(data_list))]

    for n in range(data_length):
        # 각 데이터들을 참조하여 날짜, 시간, 온도, 습도 순서로 추가
        weather_data[n].append(data_list[n].find("day").string)
        weather_data[n].append(data_list[n].find("hour").string)
        weather_data[n].append(data_list[n].find("temp").string)
        weather_data[n].append(data_list[n].find("reh").string)

    return weather_data


def __extract_weather_mid_term(url) -> list:
    """

    Explanation
    ----
    분석할 기상청 주소: https://www.weather.go.kr/weather/lifenindustry/sevice_rss.jsp?sido=2800000000&gugun=2818500000&dong=2818582000&x=21&y=3

    참고한 사이트: https://kocoafab.cc/tutorial/view/595

    중기예보를 크롤링하여 값을 가져오는 함수입니다.
    동네예보와는 양식이 틀리오니 적절하게 사용하시길 바랍니다.

    Tags
    -----

    `<mode>`: 예보날짜
        - A01: 전일 예보
        - A02: 오전, 오후 구분 예보

    `<tmEf>`: 시간(yyyy-mm-dd 00:00)

    `<wf>`: 날씨예보

    `<tmn>`: 최저온도

    `<tmx>`: 최고온도

    `<rnSt>`: 강수확률

    Return
    -------

    weather_data (list-dict): 리스트내부의 리스트 마다 각 날짜별 데이터들을 딕셔너리 형태로 가지고있습니다.

    """
    import requests
    from bs4 import BeautifulSoup

    # 크롤링할 url 주소
    weather_result = requests.get(url)
    weather_soup = BeautifulSoup(weather_result.text, "html.parser")

    weather_data = []
    # 각 location을 반복
    for location_data in weather_soup.findAll("location", {"wl_ver": 3}):
        city = location_data.find("city")   # location의 지역 이름

        # 한 location의 여러 데이터들 반복하여 값을 넣음
        for data in location_data.findAll("data"):
            dictionary = {}
            dictionary["city"] = city.string
            dictionary["mode"] = data.find("mode").string
            dictionary["tmef"] = data.find("tmef").string
            dictionary["wf"] = data.find("wf").string
            dictionary["tmn"] = data.find("tmn").string
            dictionary["tmx"] = data.find("tmx").string
            dictionary["rnst"] = data.find("rnst").string
            weather_data.append(dictionary)

    return weather_data


if __name__ == "__main__":
    from util import *
    weather_value = extract_weather()(
        "http://www.weather.go.kr/weather/forecast/mid-term-rss3.jsp?stnId=108")
    print(convert_to_csv(weather_value))
