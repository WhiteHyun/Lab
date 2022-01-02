from analysis import turning
from datetime import datetime

if __name__ == "__main__":
    df = turning.TossAndTurn('posture20210316.csv', header=False)
    df.show_tat_count(datetime(2021, 3, 16, 3, 16, 6),
                      datetime(2021, 3, 16, 5, 59), 30, "o-", 5)
    # df.show_tat_posture(30, "-", 5)
    # df.show_tat_posture(30, "o", 5)
