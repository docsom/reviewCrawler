import requests

cookies = {
    'NID_AUT': 'hlcCjDBBfth27IPEsMK+7OWdkxWKATa236aORiMrpQi/aQGFSlS2F4kQvtAJx/am',
    'NID_JKL': '7Dh1C3ZrvIbFdsM9f955aS+yDhIM9dadsuhbEFsABms=',
    'NaverSuggestUse': 'use%26unuse',
    'nx_ssl': '2',
    'BMR': 's=1663135968254&r=https%3A%2F%2Fm.blog.naver.com%2Fgassi00%2F222302178273&r2=https%3A%2F%2Fwww.google.com%2F',
    'page_uid': 'hykGLwp0J1ZssgplRTGssssssHN-517530',
    'NID_SES': 'AAABn5rt1BakJNviHH3yBQ/HH4zzYV40HmtZAkkmbgZh2Fi8tPFEkbTgSAx3viGpS42BTX8GM39WD/u8/AlcPQFzKpVGHiSGi8gStC0TrLderyhTVAsPMtE8/4b+addtpy7Rfgf/hHG2rVtMlK8FOPKOLyKOQiRL2/Qlyrbhj0cCgBA+A+EcFAvhBiCPGKEHUmU4Ej8Gat5/PznhERFqvFwOH2Rk+N2tWtNJB/KzI8jDZD7KL/amC+x+hTBVVeNcTgvvZfU4wsnGdxEvO4p4xCshc4VN0S4WY98k/i32GfJFxAqqC/b8CBY3eGZ2ST4r5GM/M2cCXlAYyARwVRNl2S/RlClKgv3U4Lm4QEMV7DZ8I+FTt7coRHHBJTirpju2Ye0f0F/VEzoPREhLiDo+AMGIA8WIvvzmuCUJQoeGWDP5/SGSswQrwqHBzZWx51UFP41y/CyPpVIRxkmg4fGWfjFKKZj4IdUBI3dfb3TXXeGE6rvlp8dE3tYEsY68v5GBNTvmACn/idPqn8O3QWuOif8FVMf54/OajJyGogFX1wPvP/NZ',
    'SBC': '0b2b33af-24a0-4c76-a75f-c9d8a6686a76',
}

headers = {
    'authority': 'smartstore.naver.com',
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'ko,en;q=0.9,en-US;q=0.8',
    'content-type': 'application/json;charset=UTF-8',
    # Requests sorts cookies= alphabetically
    # 'cookie': 'NID_AUT=hlcCjDBBfth27IPEsMK+7OWdkxWKATa236aORiMrpQi/aQGFSlS2F4kQvtAJx/am; NID_JKL=7Dh1C3ZrvIbFdsM9f955aS+yDhIM9dadsuhbEFsABms=; NaverSuggestUse=use%26unuse; nx_ssl=2; BMR=s=1663135968254&r=https%3A%2F%2Fm.blog.naver.com%2Fgassi00%2F222302178273&r2=https%3A%2F%2Fwww.google.com%2F; page_uid=hykGLwp0J1ZssgplRTGssssssHN-517530; NID_SES=AAABn5rt1BakJNviHH3yBQ/HH4zzYV40HmtZAkkmbgZh2Fi8tPFEkbTgSAx3viGpS42BTX8GM39WD/u8/AlcPQFzKpVGHiSGi8gStC0TrLderyhTVAsPMtE8/4b+addtpy7Rfgf/hHG2rVtMlK8FOPKOLyKOQiRL2/Qlyrbhj0cCgBA+A+EcFAvhBiCPGKEHUmU4Ej8Gat5/PznhERFqvFwOH2Rk+N2tWtNJB/KzI8jDZD7KL/amC+x+hTBVVeNcTgvvZfU4wsnGdxEvO4p4xCshc4VN0S4WY98k/i32GfJFxAqqC/b8CBY3eGZ2ST4r5GM/M2cCXlAYyARwVRNl2S/RlClKgv3U4Lm4QEMV7DZ8I+FTt7coRHHBJTirpju2Ye0f0F/VEzoPREhLiDo+AMGIA8WIvvzmuCUJQoeGWDP5/SGSswQrwqHBzZWx51UFP41y/CyPpVIRxkmg4fGWfjFKKZj4IdUBI3dfb3TXXeGE6rvlp8dE3tYEsY68v5GBNTvmACn/idPqn8O3QWuOif8FVMf54/OajJyGogFX1wPvP/NZ; SBC=0b2b33af-24a0-4c76-a75f-c9d8a6686a76',
    'origin': 'https://smartstore.naver.com',
    'referer': 'https://smartstore.naver.com/raintato/products/5089990614',
    'sec-ch-ua': '"Microsoft Edge";v="105", " Not;A Brand";v="99", "Chromium";v="105"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36 Edg/105.0.1343.42',
}

json_data = {
    'page': 1,
    'pageSize': 20,
    'merchantNo': '500158087',
    'originProductNo': '5071615198',
    'sortType': 'REVIEW_RANKING',
}

response = requests.post('https://smartstore.naver.com/i/v1/reviews/paged-reviews', cookies=cookies, headers=headers, json=json_data)
print(response.json())
import pprint

# pprint.pprint(response.text)