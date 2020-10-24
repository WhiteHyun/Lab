import requests
from bs4 import BeautifulSoup


# Weather Scraping
def extract_weather() -> (list, list, list, list):
    """
    https://www.weather.go.kr/weather/lifenindustry/sevice_rss.jsp?sido=2800000000&gugun=2818500000&dong=2818582000&x=21&y=3
    https://kocoafab.cc/tutorial/view/595

    <day>: 날짜,    오늘: 0, 내일: 1, 모레: 2
    <temp> 온도
    <tmx> 최고 기온
    <tmn> 최저 기온
    <sky> 하늘 상태
    <pty> 강수 형태
    <pop> 강수 확률
    <ws> 풍속
    <wd> 풍향
    <reh> 습도
    <r12> 12시간 강수량
    <s12> 12시간 신적설
    <r06> 6시간 강수량
    <s06> 6시간 신적설

    Return:
        weather_data (doubled list): 리스트내부의 리스트 마다 각 날짜별 데이터들을 가지고있습니다.
    """
    URL = "http://www.kma.go.kr/wid/queryDFSRSS.jsp?zone=2818582000"
    SEQ_NUM = 17
    weather_result = requests.get(URL)
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
        weather_data[n].append(data_list[n].find("day").string)
        weather_data[n].append(data_list[n].find("hour").string)
        weather_data[n].append(data_list[n].find("temp").string)
        weather_data[n].append(data_list[n].find("reh").string)

    

    return weather_data
