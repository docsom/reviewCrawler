mealKit = [
    100002371, # 밀키트 전체
    [
        100002489, # 간식/디저트
        100002490, # 구이
        100002491, # 면/파스타
        100002492, # 밥/죽
        100002493, # 볶음/튀김
        100002495, # 조림/찜
        100002496, # 찌개/국
        100002494, # 세트요리
    ]
]

sideDish = [
    100002367, # 김치/반찬 전체
    [
        100007771, # 김치
        100002366, # 반찬
        100002518, # 젓갈/장류
        100007779, # 김/튀김/부각
    ]
]

HMR = [
    100002364, # 간편조리식품 전체
    [
        100007953, # 도시락/밥류
        100007954, # 샐러드/닭가슴살
        100007955, # 죽/스프
        100007956, # 만두/딤섬
        100002414, # 즉석국/즉석탕
        100007957, # 떡볶이/튀김/어묵
        100007958, # 피자/핫도그/햄버거
        100007959, # 카레/짜장
        100002418, # 맛살/게살
        100007960, # 함박/미트볼
        100002411, # 채식푸드
        100007961, # 기타간편조리식품
    ]
]

snack = [
        100002372, # 과자/떡/베이커리 전체
        [
            100002515, # 떡
            100007947, # 베이커리
            100002513, # 초콜릿
            100007948, # 젤리/캐러멜/푸딩
            100007949, # 사탕/껌/엿
            100002363, # 아이스크림/빙수
            100007950, # 과자/쿠키
            100002498, # 팝콘/강냉이
            100002516, # 시리얼
            100007952, # 전통과자
            100002504, # 가공안주류
            100002506, # 기타과자
        ]
]

cheese = [
    100002378, # 치즈/유가공품 전체
    [
        100002484, # 치즈
        100002485, # 마가린
        100002486, # 버터
        100002487, # 생크림/휘핑크림
        100007946, # 연유
    ]

]

drink = [
    100000832, # 생수/음류 전체
    [
        100002450, # 생수
        100002451, # 탄산수
        100002452, # 청량/탄산음료
        100008883, # 제로음료
        100002456, # 두유
        100007903, # 우유, 요거트
        100002453, # 주스/과즙음료
        100007922, # 건강/기능성음료
        100007923, # 전통/차음료
        100002694, # 파우더/스무디
    ]
]

coffee = [
    100007913, # 커피/차류 전체
    [
        100002454, # 커피
        100002684, # 코코아
        100002455, # 차류
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
    
product_category_splited_section = mealKit[1] + sideDish[1] + HMR[1] + snack[1] + cheese[1] + drink[1] + coffee[1]

product_category_all = [
    mealKit[0],
    sideDish[0],
    HMR[0],
    snack[0],
    cheese[0],
    drink[0],
    coffee[0]
]