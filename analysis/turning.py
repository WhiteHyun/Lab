from datetime import datetime
from sys import platform
from matplotlib import font_manager, rc
import matplotlib.pyplot as plt
import pandas as pd

if platform == "darwin":  # macOS
    rc("font", family="AppleGothic")
    plt.rcParams["axes.unicode_minus"] = False
else:  # linux, window, etc..
    font_name = font_manager.FontProperties(
        fname="c:/Windows/Fonts/malgun.ttf").get_name()
    rc('font', family=font_name)
    plt.rcParams['axes.unicode_minus'] = False


class ParsingError(Exception):
    def __init__(self, msg: str) -> None:
        super().__init__(msg)


class TossAndTurn():
    """뒤척임 관련 분석 클래스입니다.
    """
    NONE = 0
    LEFT = 1
    CENTER = 2
    RIGHT = 3

    def __init__(self, csv_url: str, header: bool) -> None:
        """
        Parameter
        ---------

        csv_url: str
            csv파일의 경로를 입력받습니다.

        header: bool
            csv파일의 헤더가 있는지 없는지를 입력합니다.
        """
        if header:
            df = pd.read_csv(csv_url)
        else:
            df = pd.read_csv(csv_url, header=None)

        if len(df.columns) != 12:
            raise ParsingError("입력받은 csv의 열의 길이가 12가 아닙니다!")

        elif not df[10].isna().all():
            raise ParsingError("10번째 열은 아무 값도 없어야 합니다!")

        self.__df = self.__pre_processing(df)

    def __pre_processing(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        입력받은 데이터프레임을 전처리합니다.
        """

        # == 필요없는 데이터 삭제 ==
        df.drop(df.columns[2:11], axis=1, inplace=True)
        df.drop(df.columns[0], axis=1, inplace=True)

        # == column명 변경 ==
        df.columns = ["날짜 및 시간", "자세"]

        # == 날짜 데이터를 datetime으로 변경 ==
        df["날짜 및 시간"] = pd.to_datetime(df["날짜 및 시간"])

        # == 학습된 자세 중 오차 제거 ==
        i = 1
        posture = df["자세"]
        while i < len(posture):  # 데이터 개수만큼 반복
            if posture[i] != posture[i-1]:  # 이전 값이랑 비교해서 달라졌을 때 (뒤척였을 때)

                # 값이 바뀐 인덱스가 언제까지 유지되는지 확인하기위한 인덱스
                index = posture[i:][posture != posture[i]].index
                if len(index) == 0:  # series의 끝까지 바뀔 게 없음. 끝.
                    break
                if index[0] - i <= 5:  # 만약 5초간만 값의 오차가 생겼을 때
                    posture[i:index[0]] = posture[i-1]  # 오차가 생긴 것이므로 이전 값으로 대체
                i = index[0]  # 인덱스는 오차 발생된 직후부터 다시 시작
            else:  # 값이 계속 같으면 그냥 1씩 증가
                i += 1
        # == 자세값을 그래프 그릴 수 있도록 정수형으로 변경 ==
        posture[posture == "none"] = TossAndTurn.NONE
        posture[posture == "left"] = TossAndTurn.LEFT
        posture[posture == "center"] = TossAndTurn.CENTER
        posture[posture == "right"] = TossAndTurn.RIGHT
        return df

    def show_tat_posture(self, start: datetime, end: datetime, sep: int, marker: str, size: int) -> None:
        """
        뒤척임 자세를 보여줍니다.

        Parameters
        ----------
        start: datetime
            시작 시간입니다.

        end: datetime
            분석을 끝낼 시간입니다.

        sep: int
            분 단위로 뒤척인 자세를 구분합니다.

        marker: str
            그래프의 마커를 어떻게 보여줄지 설정합니다.

        size: int
            마커의 크기를 설정합니다.

        Example
        -------
        >>> show_tat_posture(datetime(2021, 3, 16, 2, 16, 6), datetime(2021, 3, 16, 5, 59), 60, "-", 5)
        """

        start_index = self.__df[self.__df["날짜 및 시간"] == start].index
        end_index = self.__df[self.__df["날짜 및 시간"] == end].index

        if len(start_index) == 0 or len(end_index) == 0:
            raise ParsingError("없는 데이터를 참조했습니다!")

        start_index = start_index[0]
        end_index = end_index[0]
        plt.plot(self.__df["자세"][start_index:end_index+1],
                 marker, markersize=size)
        plt.xlabel("시간")
        plt.xticks(range(start_index, len(self.__df), sep*60),
                   labels=self.__df.iloc[start_index:end_index+1:sep*60, 0], rotation=45)
        plt.ylabel("자세기준")
        plt.yticks([TossAndTurn.NONE, TossAndTurn.LEFT, TossAndTurn.CENTER, TossAndTurn.RIGHT],
                   labels=("None", "Left", "Center", "Right"))
        plt.grid(True)
        plt.title("뒤척임 자세 (전체 시간대)")
        plt.show()

    def show_tat_count(self, start: datetime, end: datetime, sep: int, marker: str, size: int, verbose: bool = False) -> None:
        """
        뒤척인 횟수를 보여줍니다.

        Parameters
        ----------
        start: datetime
            시작 시간입니다.

        end: datetime
            분석을 끝낼 시간입니다.

        sep: str
            분 단위로 나누어서 분석합니다.

        verbose: bool
            정확한 분석 결과를 터미널로 설명합니다.

        Example
        -------
        >>> show_tat_count(start=datetime(21, 9, 4), end=datetime(21, 9, 4, 6), sep="15", marker="o", size=5)
        # 21년 9월 4일 0시부터 21년 9월 4일 6시까지 15분 단위로 뒤척임 횟수를 보여줌
        """

        # == Parse error part ==
        if type(start) is not datetime or type(end) is not datetime:
            raise ParsingError("start와 end 파라미터는 무조건 datetime 객체여야 합니다!")

        posture = self.__df["자세"]
        # none 이 아닌 첫 데이터 (눕기 시작했을 때의 인덱스)
        sleep_start_index = posture[posture != TossAndTurn.NONE].index[0] + 1
        sleep_start_datetime = self.__df.iloc[sleep_start_index, 0]

        if sleep_start_datetime > start:
            raise ParsingError("취침 전 데이터부터 시작하면 안됩니다.")

        start_index = self.__df[self.__df["날짜 및 시간"] == start].index
        end_index = self.__df[self.__df["날짜 및 시간"] == end].index

        if len(start_index) == 0 or len(end_index) == 0:
            raise ParsingError("없는 데이터를 참조했습니다!")

        # == Parse error part finished ==

        start_index = start_index[0]
        end_index = end_index[0]
        count_list = []
        if verbose:
            count_dict = {
                TossAndTurn.NONE: [],
                TossAndTurn.LEFT: [],
                TossAndTurn.CENTER: [],
                TossAndTurn.RIGHT: []
            }

        count = 0
        index = -1
        for i in range(start_index, end_index+1):
            if count % (sep*60) == 0:
                count_list.append(0)
                index += 1

                if verbose:
                    for key in count_dict:
                        count_dict[key].append(0)

            if verbose:
                count_dict[self.__df["자세"][i]][index] += 1

            if self.__df["자세"][i] != self.__df["자세"][i-1]:
                count_list[index] += 1
            count += 1
        if verbose:
            plt.subplot(211)
            plt.xticks([])
        else:
            plt.xticks(range(0, len(count_list)),
                       labels=self.__df.loc[start_index:end_index+1:sep*60, "날짜 및 시간"], rotation=45)
            plt.xlabel("시간")

        plt.plot(count_list, marker, markersize=size)
        plt.grid(True)
        plt.title(
            f"시간대별 뒤척임 횟수 {start.hour}시{start.minute}분 ~ {end.hour}시{end.minute}분 ({sep}분당)")
        plt.ylabel("횟수")

        if verbose:
            print(count_dict)
            plt.subplot(212)
            for key in count_dict:
                plt.plot(count_dict[key], marker, markersize=size)
            plt.legend(["none", "left", "center", "right"])
            plt.xticks(range(0, len(count_list)),
                       labels=self.__df.loc[start_index:end_index+1:sep*60, "날짜 및 시간"], rotation=45)
            plt.grid(True)
            plt.title("뒤척임 자세 현황 (시간은 위와 동일)")
            plt.xlabel("시간")
            plt.ylabel("횟수")
        plt.show()


if __name__ == "__main__":
    df = TossAndTurn('posture20210316.csv', header=False)

    df.show_tat_count(datetime(2021, 3, 16, 3, 16, 6),
                      datetime(2021, 3, 16, 5, 59), 10, "o-", 5, True)

    # df.show_tat_posture(datetime(2021, 3, 16, 2, 16, 6),
    #                     datetime(2021, 3, 16, 5, 59), 60, "-", 5)
