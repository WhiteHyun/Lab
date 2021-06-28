import numpy as np
import pandas as pd
POINT_LENGTH = 0.2  # 사용자 기점 반경 거리 (km 단위)
CRIME_TIME = 0
CRIME_TYPE = 1
LATITUDE = 2  # 위도
LONGITUDE = 3  # 경도
VIOLENT_CRIME = 1


def get_distance(x: float, y: float, crime_x: float, crime_y: float) -> float:
    """
    자신의 위치와 범죄 발생 지역 위치의 거리를 하버사인 공식을 이용하여 보다 정확한 거리를 계산 후 반환합니다.
    Params:
        x (float): 자신의 좌표 중 위도를 나타냅니다.
        y (float): 자신의 좌표 중 경도를 나타냅니다.
        crime_x (float): 범죄 발생지역의 위도를 나타냅니다.
        crime_y (float): 범죄 발생지역의 경도를 나타냅니다.
    Return:
        distnace (float): 자신의 위치와 범죄 발생 지역 위치의 거리를 계산한 값입니다.
    """
    def degree2radius(degree): return degree * (np.pi/180)
    EARTH_RADIUS = 6371  # 지구의 반경 (단위: km)
    d_longitude = degree2radius(np.abs(crime_x-x))
    d_latitude = degree2radius(np.abs(crime_y-y))
    sqroot = np.sqrt(np.sin(d_latitude/2)*np.sin(d_latitude/2)+np.cos(degree2radius(x)) *
                     np.cos(degree2radius(crime_x)) *
                     np.sin(d_longitude/2)*np.sin(d_longitude/2))
    distance = 2 * EARTH_RADIUS * np.arcsin(sqroot)
    return distance


def is_crime_near_occured(x: float, y: float, crime_x: float, crime_y: float) -> bool:
    """
    자신의 위치 주변에 범죄가 발생되었는지를 확인해주는 함수입니다.
    사용자 중심 반경 값에 의존합니다.
    """
    length = get_distance(x, y, crime_x, crime_y)  # 거리 계산
    if length <= POINT_LENGTH:
        return True
    else:
        return False


def search_CRIME(x, y):
    df = pd.read_csv("C:/Users/Human/Desktop/sample_data.csv",
                     encoding="EUC-KR")  # 사용자에 따라 경로 재지정 필요
    my_pos_x, my_pos_y = x, y
    crime = df[["시간", "강력범죄", "위도", "경도"]]
    del_list = []
    for i in crime.index:
        crime_data: list = list(crime.iloc[i, :])
        if is_crime_near_occured(my_pos_x, my_pos_y, crime_data[LATITUDE], crime_data[LONGITUDE]):
            if crime_data[CRIME_TYPE] == VIOLENT_CRIME:
                print("위치 (" + str(crime_data[LATITUDE]) + "," + str(crime_data[LONGITUDE]) +
                      ") 반경 200m 이내에서 " + str(int(crime_data[CRIME_TIME])) + "시에 강력범죄가 발생했습니다.")
                del_list.append(int(i))
        else:  # 일반 범죄인 경우
            pass

    crime = crime.iloc[del_list, :]
    vl = QgsVectorLayer("Point?crs=EPSG:4326", "CVS", "memory")
    pr = vl.dataProvider()
    pr.addAttributes([QgsField("시간", QVariant.Int),
                      QgsField("강력범죄", QVariant.String),
                      QgsField("위도", QVariant.Double),
                      QgsField("경도", QVariant.Double)])
    vl.updateFields()
    for i in range(len(crime)):
        f = QgsFeature()
        f.setGeometry(QgsGeometry.fromPointXY(QgsPointXY(
            float(crime.iloc[i, LONGITUDE]), float(crime.iloc[i, LATITUDE]))))
        f.setAttributes([crime.iloc[i, CRIME_TIME], crime.iloc[i, CRIME_TYPE],
                         crime.iloc[i, LONGITUDE], crime.iloc[i, LATITUDE]])
        pr.addFeature(f)
    vl.updateExtents()
    QgsProject.instance().addMapLayer(vl)
