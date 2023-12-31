
#https://api.kurly.com/v2/categories?ver=1

mainDish = [
    911, # 국반찬메인요리전부
    [
        911001, # 국탕찌개
        911006, # 밀키트메인요리
        911002, # 밑반찬
        911003, # 김치젓갈장류
        911005, # 두부어묵부침개
        911004, # 베이컨햄통조림
    ]
]

saladHMR = [
    912, # 샐러드간편식전부
    [
        912001, # 샐러드닭가슴살
        912003, # 도시락, 밥류
        912004, # 파스타, 면류
        912005, # 떡볶이, 튀김, 순대
        912008, # 피자, 핫도그, 만두
        912007, # 폭립, 떡갈비, 안주
        912006, # 죽, 스프, 카레
        912002, # 선식, 시리얼
    ]
]

snack = [
        249, # 간식, 과자, 떡 전체
        [
            249001, # 과자, 스낵, 쿠키
            249002, # 초콜릿, 젤리, 캔디
            249003, # 떡, 한과
            249004, # 아이스크림
        ]
]

bakeryCheeseDeli = [
    915, # 베이커리, 치즈, 델리 전체
    [
        915001, # 식빵, 빵류
        915002, # 잼, 버터, 스프레드
        915003, # 케이크, 파이, 디저트
        915004, # 치즈
        915005, # 델리
        915006, # 올리브, 피클
    ]

]

drink = [
    914, # 생수, 음류, 우유, 커피 전체
    [
        914001, # 생수, 탄산수
        914002, # 음료, 주스
        914003, # 우유, 두유, 요거트
        914004, # 커피
        914005, # 차
    ]
]

product_category = [
    mainDish, 
    saladHMR,
    snack, 
    bakeryCheeseDeli, 
    drink
]
    
product_category_splited_section = mainDish[1] + saladHMR[1] + snack[1] + bakeryCheeseDeli[1] + drink[1]

product_category_all = [
    mainDish[0],
    saladHMR[0],
    snack[0],
    bakeryCheeseDeli[0],
    drink[0]
]