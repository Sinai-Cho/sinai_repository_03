import json
import time


# ==================================================
# 1. 사용자에게 행렬 입력받기
# ==================================================

def input_matrix(name, size):

    print()
    print(name + "을 입력하세요.")
    print(
        "각 줄에 "
        + str(size)
        + "개의 숫자를 공백으로 구분해서 입력하세요."
    )

    matrix = []

    row_number = 0

    while row_number < size:

        user_input = input(
            str(row_number + 1) + "번째 줄 입력: "
        )

        values = user_input.split()

        # 열 개수가 맞는지 확인
        if len(values) != size:

            print(
                "입력 형식 오류: 각 줄에 "
                + str(size)
                + "개의 숫자를 공백으로 구분해 입력하세요."
            )

            continue

        row = []

        error = False

        for value in values:

            try:
                number = float(value)
                row.append(number)

            except:
                error = True

        # 숫자가 아닌 값이 들어온 경우
        if error == True:

            print("입력 형식 오류: 숫자만 입력하세요.")

            continue

        matrix.append(row)

        row_number = row_number + 1

    return matrix


# ==================================================
# 2. MAC 연산
# ==================================================

def mac(pattern, filter_data):

    score = 0.0

    size = len(pattern)

    row = 0

    while row < size:

        column = 0

        while column < size:

            score = (
                score
                + pattern[row][column]
                * filter_data[row][column]
            )

            column = column + 1

        row = row + 1

    return score


# ==================================================
# 3. 두 점수 비교
# ==================================================

def compare_scores(score_a, score_b, label_a, label_b):

    epsilon = 0.000000001

    difference = score_a - score_b

    # abs()를 쓰지 않고 절댓값 계산
    if difference < 0:

        difference = difference * -1

    # epsilon보다 작으면 동점
    if difference < epsilon:

        return "UNDECIDED"

    elif score_a > score_b:

        return label_a

    else:

        return label_b


# ==================================================
# 4. 라벨 정규화
# ==================================================

def normalize_label(label):

    if label == "+":

        return "Cross"

    elif label == "cross":

        return "Cross"

    elif label == "Cross":

        return "Cross"

    elif label == "x":

        return "X"

    elif label == "X":

        return "X"

    else:

        return "UNKNOWN"


# ==================================================
# 5. 행렬 크기 검사
# ==================================================

def check_matrix_size(matrix, size):

    # 리스트인지 확인
    if type(matrix) != list:

        return False

    # 행 개수 확인
    if len(matrix) != size:

        return False

    row = 0

    while row < size:

        # 각 행도 리스트인지 확인
        if type(matrix[row]) != list:

            return False

        # 열 개수 확인
        if len(matrix[row]) != size:

            return False

        column = 0

        while column < size:

            value = matrix[row][column]

            # 숫자인지 확인
            if type(value) != int and type(value) != float:

                return False

            column = column + 1

        row = row + 1

    return True


# ==================================================
# 6. Cross / X 필터 찾기
# ==================================================

def get_filters(filter_data):

    cross_filter = None

    x_filter = None

    for key in filter_data:

        normal_label = normalize_label(key)

        if normal_label == "Cross":

            cross_filter = filter_data[key]

        elif normal_label == "X":

            x_filter = filter_data[key]

    return cross_filter, x_filter


# ==================================================
# 7. 패턴 이름에서 크기 가져오기
# ==================================================

def get_size_from_pattern_name(pattern_name):

    # 예:
    # size_13_1
    #
    # split 결과:
    # ["size", "13", "1"]

    parts = pattern_name.split("_")

    if len(parts) < 3:

        return 0

    try:

        size = int(parts[1])

        return size

    except:

        return 0


# ==================================================
# 8. JSON 파일 읽기
# ==================================================

def load_json():

    try:

        file = open(
            "data.json",
            "r",
            encoding="utf-8"
        )

        data = json.load(file)

        file.close()

        return data

    except FileNotFoundError:

        print()
        print("오류: data.json 파일을 찾을 수 없습니다.")

        return None

    except:

        print()
        print("오류: data.json 파일을 읽을 수 없습니다.")
        print("JSON 형식을 확인하세요.")

        return None


# ==================================================
# 9. 모드 1
# 3x3 사용자 입력
# ==================================================

def mode1():

    print()

    print("#---------------------------------------")
    print("# 사용자 입력 (3x3)")
    print("#---------------------------------------")

    filter_a = input_matrix(
        "필터 A",
        3
    )

    filter_b = input_matrix(
        "필터 B",
        3
    )

    pattern = input_matrix(
        "입력 패턴",
        3
    )


    # ------------------------------
    # 필터 A MAC 연산
    # ------------------------------

    start_time = time.perf_counter()

    score_a = mac(
        pattern,
        filter_a
    )

    end_time = time.perf_counter()

    time_a = (
        end_time - start_time
    ) * 1000


    # ------------------------------
    # 필터 B MAC 연산
    # ------------------------------

    start_time = time.perf_counter()

    score_b = mac(
        pattern,
        filter_b
    )

    end_time = time.perf_counter()

    time_b = (
        end_time - start_time
    ) * 1000


    # ------------------------------
    # 판정
    # ------------------------------

    result = compare_scores(
        score_a,
        score_b,
        "A",
        "B"
    )


    print()

    print("필터 A MAC 점수 :", score_a)

    print("필터 B MAC 점수 :", score_b)

    print(
        "필터 A 연산 시간 :",
        round(time_a, 6),
        "ms"
    )

    print(
        "필터 B 연산 시간 :",
        round(time_b, 6),
        "ms"
    )

    print(
        "전체 연산 시간 :",
        round(time_a + time_b, 6),
        "ms"
    )


    if result == "UNDECIDED":

        print("판정 결과 : 판정 불가")

    else:

        print("판정 결과 :", result)


# ==================================================
# 10. JSON 패턴 하나 분석
# ==================================================

def analyze_pattern(pattern_name, pattern_data, filters):

    # 반환할 기본값
    result_data = {}

    result_data["name"] = pattern_name

    result_data["pass"] = False

    result_data["reason"] = ""


    # --------------------------------
    # 패턴 이름에서 크기 추출
    # --------------------------------

    size = get_size_from_pattern_name(
        pattern_name
    )

    if size == 0:

        print("--- " + pattern_name + " ---")
        print("FAIL: 패턴 이름 형식 오류")

        result_data["reason"] = "패턴 이름 형식 오류"

        return result_data


    # --------------------------------
    # input 존재 확인
    # --------------------------------

    if "input" not in pattern_data:

        print("--- " + pattern_name + " ---")
        print("FAIL: input 데이터 없음")

        result_data["reason"] = "input 데이터 없음"

        return result_data


    pattern = pattern_data["input"]


    # --------------------------------
    # expected 존재 확인
    # --------------------------------

    if "expected" not in pattern_data:

        print("--- " + pattern_name + " ---")
        print("FAIL: expected 데이터 없음")

        result_data["reason"] = "expected 데이터 없음"

        return result_data


    expected = normalize_label(
        pattern_data["expected"]
    )


    if expected == "UNKNOWN":

        print("--- " + pattern_name + " ---")
        print("FAIL: expected 라벨 오류")

        result_data["reason"] = "expected 라벨 오류"

        return result_data


    # --------------------------------
    # 해당 크기의 필터 선택
    # --------------------------------

    filter_name = "size_" + str(size)


    if filter_name not in filters:

        print("--- " + pattern_name + " ---")
        print(
            "FAIL: "
            + filter_name
            + " 필터 없음"
        )

        result_data["reason"] = (
            filter_name
            + " 필터 없음"
        )

        return result_data


    filter_data = filters[filter_name]


    cross_filter, x_filter = get_filters(
        filter_data
    )


    # --------------------------------
    # 필터 존재 확인
    # --------------------------------

    if cross_filter == None:

        print("--- " + pattern_name + " ---")
        print("FAIL: Cross 필터 없음")

        result_data["reason"] = "Cross 필터 없음"

        return result_data


    if x_filter == None:

        print("--- " + pattern_name + " ---")
        print("FAIL: X 필터 없음")

        result_data["reason"] = "X 필터 없음"

        return result_data


    # --------------------------------
    # 크기 확인
    # --------------------------------

    if check_matrix_size(
        pattern,
        size
    ) == False:

        print("--- " + pattern_name + " ---")
        print("FAIL: 패턴 크기 오류")

        result_data["reason"] = "패턴 크기 오류"

        return result_data


    if check_matrix_size(
        cross_filter,
        size
    ) == False:

        print("--- " + pattern_name + " ---")
        print("FAIL: Cross 필터 크기 오류")

        result_data["reason"] = "Cross 필터 크기 오류"

        return result_data


    if check_matrix_size(
        x_filter,
        size
    ) == False:

        print("--- " + pattern_name + " ---")
        print("FAIL: X 필터 크기 오류")

        result_data["reason"] = "X 필터 크기 오류"

        return result_data


    # --------------------------------
    # MAC 연산
    # --------------------------------

    cross_score = mac(
        pattern,
        cross_filter
    )

    x_score = mac(
        pattern,
        x_filter
    )


    # --------------------------------
    # 판정
    # --------------------------------

    result = compare_scores(
        cross_score,
        x_score,
        "Cross",
        "X"
    )


    # --------------------------------
    # PASS / FAIL 판정
    # --------------------------------

    if result == expected:

        pass_text = "PASS"

        result_data["pass"] = True

    else:

        pass_text = "FAIL"

        result_data["pass"] = False


        if result == "UNDECIDED":

            result_data["reason"] = (
                "동점(UNDECIDED) 처리 규칙에 따라 FAIL"
            )

        else:

            result_data["reason"] = (
                "판정 결과와 expected가 다름"
            )


    # --------------------------------
    # 결과 출력
    # --------------------------------

    print("--- " + pattern_name + " ---")

    print(
        "Cross 점수:",
        cross_score
    )

    print(
        "X 점수:",
        x_score
    )

    print(
        "판정:",
        result,
        "| expected:",
        expected,
        "|",
        pass_text,
        end=""
    )


    # 동점으로 실패한 경우
    if result == "UNDECIDED" and pass_text == "FAIL":

        print(" (동점 규칙)")

    else:

        print()


    return result_data


# ==================================================
# 11. 성능 측정
# ==================================================

def measure_mac(pattern, filter_data):

    repeat_count = 10

    total_time = 0.0

    count = 0


    while count < repeat_count:

        start_time = time.perf_counter()

        mac(
            pattern,
            filter_data
        )

        end_time = time.perf_counter()


        run_time = (
            end_time - start_time
        ) * 1000


        total_time = (
            total_time
            + run_time
        )


        count = count + 1


    average_time = (
        total_time
        / repeat_count
    )


    return average_time


# ==================================================
# 12. 특정 크기의 패턴 찾기
# ==================================================

def find_pattern(patterns, size):

    for pattern_name in patterns:

        pattern_size = get_size_from_pattern_name(
            pattern_name
        )

        if pattern_size == size:

            pattern_data = patterns[
                pattern_name
            ]

            if "input" in pattern_data:

                return pattern_data["input"]

    return None


# ==================================================
# 13. 성능 분석 출력
# ==================================================

def performance_analysis(filters, patterns):

    print()
    print("#---------------------------------------")
    print("# [3] 성능 분석 (평균/10회)")
    print("#---------------------------------------")


    # --------------------------------
    # 3x3은 JSON에 없기 때문에
    # 성능 측정용 데이터를 직접 만든다.
    # --------------------------------

    pattern_3 = [
        [1, 1, 1],
        [1, 0, 1],
        [1, 1, 1]
    ]

    filter_3 = [
        [1, 1, 1],
        [1, 1, 1],
        [1, 1, 1]
    ]


    average_time = measure_mac(
        pattern_3,
        filter_3
    )


    print(
        "3x3",
        "          ",
        format(average_time, ".3f"),
        "          ",
        9
    )


    # --------------------------------
    # JSON에 있는 크기 측정
    # --------------------------------

    sizes = [
        5,
        13,
        25
    ]


    for size in sizes:

        filter_name = (
            "size_"
            + str(size)
        )


        if filter_name not in filters:

            print(
                str(size)
                + "x"
                + str(size),
                "필터 없음"
            )

            continue


        filter_data = filters[
            filter_name
        ]


        cross_filter, x_filter = get_filters(
            filter_data
        )


        if cross_filter == None:

            print(
                str(size)
                + "x"
                + str(size),
                "Cross 필터 없음"
            )

            continue


        pattern = find_pattern(
            patterns,
            size
        )


        if pattern == None:

            print(
                str(size)
                + "x"
                + str(size),
                "패턴 없음"
            )

            continue


        # 크기 검증
        if check_matrix_size(
            pattern,
            size
        ) == False:

            print(
                str(size)
                + "x"
                + str(size),
                "패턴 크기 오류"
            )

            continue


        if check_matrix_size(
            cross_filter,
            size
        ) == False:

            print(
                str(size)
                + "x"
                + str(size),
                "필터 크기 오류"
            )

            continue


        average_time = measure_mac(
            pattern,
            cross_filter
        )


        operation_count = (
            size * size
        )


        size_text = (
            str(size)
            + "x"
            + str(size)
        )


        print(
            size_text,
            "         ",
            format(average_time, ".3f"),
            "          ",
            operation_count
        )


# ==================================================
# 14. 모드 2
# data.json 전체 분석
# ==================================================

def mode2():

    data = load_json()


    if data == None:

        return


    # ==============================================
    # JSON 기본 구조 확인
    # ==============================================

    if "filters" not in data:

        print(
            "오류: filters 데이터가 없습니다."
        )

        return


    if "patterns" not in data:

        print(
            "오류: patterns 데이터가 없습니다."
        )

        return


    filters = data["filters"]

    patterns = data["patterns"]


    # ==============================================
    # [1] 필터 로드
    # ==============================================

    print()
    print("#---------------------------------------")
    print("# [1] 필터 로드")
    print("#---------------------------------------")


    sizes = [
        5,
        13,
        25
    ]


    for size in sizes:

        filter_name = (
            "size_"
            + str(size)
        )


        if filter_name not in filters:

            print(
                "X "
                + filter_name
                + " 필터 없음"
            )

            continue


        filter_data = filters[
            filter_name
        ]


        cross_filter, x_filter = get_filters(
            filter_data
        )


        if cross_filter != None and x_filter != None:

            print(
                "✓ "
                + filter_name
                + " 필터 로드 완료 (Cross, X)"
            )

        else:

            print(
                "X "
                + filter_name
                + " 필터 로드 실패"
            )


    # ==============================================
    # [2] 패턴 분석
    # ==============================================

    print()
    print("#---------------------------------------")
    print("# [2] 패턴 분석 (라벨 정규화 적용)")
    print("#---------------------------------------")
    print()


    results = []


    for pattern_name in patterns:

        pattern_data = patterns[
            pattern_name
        ]


        result = analyze_pattern(
            pattern_name,
            pattern_data,
            filters
        )


        results.append(
            result
        )


    # ==============================================
    # [3] 성능 분석
    # ==============================================

    performance_analysis(
        filters,
        patterns
    )


    # ==============================================
    # [4] 결과 요약
    # ==============================================

    print()
    print("#---------------------------------------")
    print("# [4] 결과 요약")
    print("#---------------------------------------")


    total_count = len(results)

    pass_count = 0

    fail_count = 0


    for result in results:

        if result["pass"] == True:

            pass_count = pass_count + 1

        else:

            fail_count = fail_count + 1


    print(
        "총 테스트:",
        str(total_count) + "개"
    )

    print(
        "통과:",
        str(pass_count) + "개"
    )

    print(
        "실패:",
        str(fail_count) + "개"
    )


    # 실패가 있는 경우
    if fail_count > 0:

        print()
        print("실패 케이스:")
        print()


        for result in results:

            if result["pass"] == False:

                print(
                    "- "
                    + result["name"]
                    + ": "
                    + result["reason"]
                )


# ==================================================
# 15. 메인 메뉴
# ==================================================

def main():

    while True:

        print()
        print("==============================")
        print("       MINI NPU Simulator")
        print("==============================")

        print("[모드 선택]")
        print()

        print("1. 사용자 입력 (3x3)")
        print("2. data.json 분석")
        print("3. 종료")


        menu = input("선택: ")


        if menu == "1":

            mode1()


        elif menu == "2":

            mode2()


        elif menu == "3":

            print()
            print("프로그램을 종료합니다.")

            break


        else:

            print()
            print(
                "잘못된 입력입니다."
            )

            print(
                "1, 2, 3 중 하나를 입력하세요."
            )


# ==================================================
# 프로그램 시작
# ==================================================

main()