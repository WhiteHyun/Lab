import pymysql


def connect_sql():
    """
    Connect Attributes:
        user: user name
        passwd: 설정한 패스워드
        host: DB가 존재하는 host
        db: 연결할 데이터베이스 이름
        charset: 인코딩 설정

    Return:
        cursor (Cursor): 연결한 DB와 상호작용하기 위해 사용되는 객체
        test_db (Connection): Connection 객체

        None이 리턴된 경우 연결간 오류가 발생한 것으로 간주하기 때문에
        if문을 통해 None값인지를 확인해주어야합니다.
    """
    try:
        test_db = pymysql.connect(
            user="root",
            passwd="26147660",
            host="127.0.0.1",
            db="testDB",
            charset='utf8'
        )
        cursor = test_db.cursor(pymysql.cursors.DictCursor)
    except:
        return None, None
    return cursor, test_db
