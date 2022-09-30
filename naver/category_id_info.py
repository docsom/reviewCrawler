# [category_id, catId]

mealKit = [
    [100002371, 50014240],  # 밀키트 전체
    [
        [100002489, 50014001],  # 간식/디저트
        [100002490, 50013781],  # 구이
        [100002491, 50014201],  # 면/파스타
        [100002492, 50014260],  # 밥/죽
        [100002493, 50014280],  # 볶음/튀김
        [100002495, 50014101],  # 조림/찜
        [100002496, 50013821],  # 찌개/국
        [100002494, 50014042],  # 세트요리
    ]
]

sideDish = [
    [100002367, 50000147],  # 김치/반찬 전체
    [
        [100007771, 50000147],  # 김치
        [100002366, 50000146],  # 반찬
        [100002518, 50001050],  # 젓갈/장류
        [100007779, 50001176],  # 김/튀김/부각
    ]
]

HMR = [
    [100002364, 50000026],  # 간편조리식품 전체
    [
        [100007953, 50006199],  # 도시락/밥류
        [100007954, 50001873],  # 샐러드/닭가슴살
        [100007955, 50012440],  # 죽/스프
        [100007956, 50001871],  # 만두/딤섬
        [100002414, 50001876],  # 즉석국/즉석탕
        [100007957, 50012340],  # 떡볶이/튀김/어묵
        [100007958, 50001867],  # 피자/핫도그/햄버거
        [100007959, 50012302],  # 카레/짜장
        [100002418, 50012380],  # 맛살/게살
        [100007960, 50012360],  # 함박/미트볼
        [100002411, 50001872],  # 채식푸드
        [100007961, 50000026],  # 기타간편조리식품
    ]
]

snack = [
        [100002372, 50000149],  # 과자/떡/베이커리 전체
        [
            [100002515, 50013161],  # 떡
            [100007947, 50013260],  # 베이커리
            [100002513, 50002000],  # 초콜릿
            [100007948, 50001763],  # 젤리/캐러멜/푸딩
            [100007949, 50002001],  # 사탕/껌/엿
            [100002363, 50013220],  # 아이스크림/빙수
            [100007950, 50001998],  # 과자/쿠키
            [100002498, 50001918],  # 팝콘/강냉이
            [100002516, 50013181],  # 시리얼
            [100007952, 50002003],  # 전통과자
            [100002504, 50001920],  # 가공안주류
            [100002506, 50001921],  # 기타과자
        ]
]

cheese = [
    [100002378, 50001085],  # 치즈/유가공품 전체
    [
        [100002484, 50001085],  # 치즈
        [100002485, 50001758],  # 마가린
        [100002486, 50001759],  # 버터
        [100002487, 50001757],  # 생크림/휘핑크림
        [100007946, 50013180],  # 연유
    ]

]

drink = [
    [100000832, 50000148],  # 생수/음류 전체
    [
        [100002450, 50002032],  # 생수
        [100002451, 50002033],  # 탄산수
        [100002452, 50001079],  # 청량/탄산음료
        [100008883, 50000148],  # 제로음료
        [100002456, 50012800],  # 두유
        [100007903, 50012820],  # 우유/요거트
        [100002453, 50001080],  # 주스/과즙음료
        [100007922, 50012140],  # 건강/기능성음료
        [100007923, 50012200],  # 전통/차음료
        [100002694, 50012701],  # 파우더/스무디
    ]
]

coffee = [
    [100007913, 50001081],  # 커피/차류 전체
    [
        [100002454, 50001081],  # 커피
        [100002684, 50012960],  # 코코아
        [100002455, 50001082],  # 차류
    ]
]

product_category = [
    mealKit,
    sideDish,
    HMR,
    snack,
    cheese,
    drink,
    coffee
]

product_category_splited_section = mealKit[1] + sideDish[1] + \
    HMR[1] + snack[1] + cheese[1] + drink[1] + coffee[1]

product_category_all = [
    mealKit[0],
    sideDish[0],
    HMR[0],
    snack[0],
    cheese[0],
    drink[0],
    coffee[0]
]

# print(product_category_splited_section)
# print(product_category_all)
# print(product_category)