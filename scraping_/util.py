def convert_to_csv(data: list) -> str:
    """data로 받아온 값을 csv로 바꿔주는 함수


    Return
    -------
    csv로 바뀌어진 str 값

    Example
    --------

        >>> convert_to_csv([{'name': 'sung-kyu', 'age': 24}, {'name': 'seung-hyeon', 'age': 23}])
        "name","age"
        "sung-kyu",24
        "seung-hyeon",23
    """
    try:
        import csv
        import io
        output = io.StringIO()
        w = csv.DictWriter(
            output, fieldnames=data[0].keys(), quoting=csv.QUOTE_NONNUMERIC)
        w.writeheader()
        w.writerows(data)
        csv_str = output.getvalue()
    except Exception as e:
        raise e
    else:
        return csv_str
