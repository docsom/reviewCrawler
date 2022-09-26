import requests
import os
import pandas as pd
from bs4 import BeautifulSoup
from csv import DictWriter
import time

nowLoc = os.getcwd()

cookies = {
    'PCID': '20118162313960784610299',
    'X-CP-PT-locale': 'ko_KR',
    '_fbp': 'fb.1.1659588906314.1251726976',
    'MARKETID': '20118162313960784610299',
    'sid': '196c96d64d494f0ca994055f6bfb350f6d55a8e9',
    'x-coupang-origin-region': 'KOREA',
    'x-coupang-target-market': 'KR',
    '_ga': 'GA1.2.644421614.1663552878',
    'gd1': 'Y',
    'trac_src': '1042016',
    'trac_addtag': '900',
    'trac_ctag': 'HOME',
    'searchSoterTooltip': 'OFF',
    'searchKeyword': '%ED%94%84%EB%A0%88%EC%8B%9C%EC%A7%80%20%EB%8D%94%ED%81%B0%20%ED%96%84%EA%B0%80%EB%93%9D%20%EB%B6%80%EB%8C%80%EC%A0%84%EA%B3%A8',
    'searchKeywordType': '%7B%22%ED%94%84%EB%A0%88%EC%8B%9C%EC%A7%80%20%EB%8D%94%ED%81%B0%20%ED%96%84%EA%B0%80%EB%93%9D%20%EB%B6%80%EB%8C%80%EC%A0%84%EA%B3%A8%22%3A0%7D',
    'FUN': '"{\'search\':[{\'reqUrl\':\'/search.pang\',\'isValid\':true}]}"',
    'trac_spec': '10304902',
    'trac_lptag': 'coupang',
    'trac_itime': '20220926164908',
    'overrideAbTestGroup': '%5B%5D',
    'bm_sz': '9C2FF18EC7201D94B4C8AA91A99154FD~YAAQ1pc7F+Ne63GDAQAAxL74eBHPtrl8xhG+SXkt32gMnizPcd2Xc7P7tnzcuO5WRznd9x9PkhtEwIq5uLc0Jw9NxQEP5zJi0Nt5125uGVgEsvUlTDZrMmdRf5qGteSRWPk8NYbAaQmYZB50pIKa3wissGBIe4FfXzVjsl7KcTm1us+aovqUfcUORk4qWHvxL5573OzQHVsHkcxB6vDA9YhLKTVb1lieEHrclHywz5hhZvygf4v6gHGkrD7QZIS+qA0AeZIAUdv6uvkYzrVf23OP1yB/ailztm2phhHeDl2J2X8zXDKVnQLtsfm3limRTKJ1504CszP3f/1C~4277040~4604227',
    'baby-isWide': 'small',
    'bm_sv': '252B6591B7F3B2775E0B8D08BE30332D~YAAQ1pc7F29f63GDAQAAocH4eBHIzjXcMUaZs/LGtjPAmWbJK9WnRFvi8xeQTtNRS9BIzbSN05xedrNlirG2GKp/VKuYIiNWSmM5SWPq+S7VBowt+Ny/WhEDghCDHBPH+hOjhXwHlHKFlZW/MSreP+qG6GIURpFDGfwIsXe1iMx6XrDwAf98YZ7o3VQZ8UqyPDybcb8Xvky8GLVq90ASZY2IeUCZfCEO0jwipnp/ylTrryinceM6/iUwS3cqtfFcAQ==~1',
    'cto_bundle': 'xNyobF8wSTBCNmtVdmVUT0RCc3Vlc09YVld4NHhjQ0tQNEFjUjAzS2NoZ0Q2SmVqQ0F4Qnc2ME45TCUyQkVCTndhTnVoNlZFbjZmVElndWxsZzdDZmlpbFcxbkt2YU41UnMlMkJLQTFvZ1c3QVo0TmJ5NldBejRBMkh0byUyRiUyRiUyQmFvTWt2eiUyQjV4aE5FRnZNVUNrSFdPeU9uQURHYU4lMkJUZyUzRCUzRA',
    '_abck': 'B00E0DF2BD0B5CCE34434E7DA8E8E605~0~YAAQ1pc7F31f63GDAQAAycH4eAhmN0chRARSRwahhjEaorHNyCQwDz6xB+NDAwBieevt6hik8iojSjXtBh1g0NiRWS4MMwk4L256qBPKmDWwTpieeIBW/JlgN82Brkt9A/bbKHdpGl3ilAh9X4HOPdIBm5/iATs9CuONAUFWI2xD/vZ5tfjN9sHIcFqWPd7CjL5uI/f0zC1AteftDqUVj9UtyhYxOwiLISJkad08wSRo0o94VZAgnjgqu3Tper/zxIzjPBeBVlRwaqskDbsIjXGlcp9eJGcqzER3MbvtPriZUQ/d4EHNqAuCG0xf5ggWn/Ss9WN3UwTB4qdPm24Gbr4RSxzhBCBcVpz1jvDUKDTP0BqE2RhPoxQ4QLI=~-1~-1~-1',
    'x-coupang-accept-language': 'ko-KR',
    'ak_bmsc': 'F2CB48D31C310FC26FD24AEFA8BF581E~000000000000000000000000000000~YAAQ1pc7F5Vf63GDAQAALML4eBErwwo+WOX+Evn83hi9PYW7RHBc+ym0wO+bw2S2X6v4JTC0q2PvHSa355oIdKzitpg7qAbyO1nJiqvQ64ki2APibcHDoM5I+bDtS7+EnyvzrBYh+ZQIi44MEYdKBtZyepjVYqt5P6B++40mxYSzQ6wzKsj25TdZTcZkb+s2zFeWXTp7ZnvNeDXOXW1fkdagip0DCEoPTXwL3rDRW/Dp7ClmcUbvweI+OrBF3m7IIof6kJvlMUQmWcWQVba+tnGIxl/9QAnG0RrS//9lXq+/1BlA1jHwqLibZqH/6CEC+5N+MwsQ9iRiFd+QzybaNKYIQ09xJBQey1O9iDCcKiXEfPNJ1/6dZ86imsNHVoGa2uhAuIcqrvk5RFWkR+g8lg1TXlCvQtivIKNcyBCdqu2YrG2X6YlPUZG6n6jFcOTJVZSYTl7+kHZdFnA5yry0kG7VpBGaFKgeG+64Uf2J25txvE6o1UH3f/kqshWr',
    'CLICKED_PAGE': '2',
}

headers = {
    'authority': 'www.coupang.com',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'accept-language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
    # Requests sorts cookies= alphabetically
    # 'cookie': 'PCID=20118162313960784610299; X-CP-PT-locale=ko_KR; _fbp=fb.1.1659588906314.1251726976; MARKETID=20118162313960784610299; sid=196c96d64d494f0ca994055f6bfb350f6d55a8e9; x-coupang-origin-region=KOREA; x-coupang-target-market=KR; _ga=GA1.2.644421614.1663552878; gd1=Y; trac_src=1042016; trac_spec=10304903; trac_addtag=900; trac_ctag=HOME; trac_lptag=%EC%BF%A0%ED%8C%A1; trac_itime=20220926095636; searchSoterTooltip=OFF; bm_sz=7749705569E9172FA9005DE0EC0DE358~YAAQbQI1FymRvHCDAQAAaQQleBHPg1RSd45YJATaJes5KGQafo8noUH5hGBYn40iv+BL9gVM6tKVLkNZRDC29rCkzZ6bqDKMIh1ZhRPo1B5VfjvSkr5PpihPDS/kqfrcX128IyGNEWsYSm/nQwappHSZ0NT4M8t/IqVMGnz0qnnh+6o4rAdnPAct30a3ckW9gZS917pWLVFgUdXMx+5EkIgl4vTUkq34OCIXySnWvnPJ36P5f/UjUE3idGVrWkKnjkynCkobZa/UacLQaX1OWcpQ6pI1hlsuvLE7ZAajuLYndk8r9+x0aXNYsrvkvH7tpSXZq/4J+E+qe15F~3163442~4276545; bm_mi=95634CFF5907175AE08CB9E42082E124~YAAQt5c7Fx4gck+DAQAAdgNteBGbBSCH1h1q/xFvMS1gBtsG4Odw8T7pNy1lHuBVZnXZdQStCyTS+bGkCXqcIR+pzbv1Q9j7fpZE8cLUQT6bqTCH0M51ZNPaxaf45WFRs2tetjWDlJRT0qSI1fvnmkUajj5FhzNSGqqRMC06Z2ban2HHh2+7exkyw3lKN5BTOCFNEwiNp3lZ810VPbrjihgHBwAEpF3+GjynOLVIg2BstF9D1hX/oJJOGVLViHwsy5Uv7jDkoQEciwiqS77lYTim2GI1IX7qUnq5XoZJOy/TBmBxeAPHOitRd22/3B7efP7nKjQSd51tRCpUnuTY2FbaaisgiRVktHTyDvVtRQCqhTuR~1; ak_bmsc=27642A0BAA81998174E481E14B9F41E1~000000000000000000000000000000~YAAQt5c7F0Ynck+DAQAAsCNteBEVGBhn+LoeKzqJ+CSlc4l4Vcy4FTS22wkFuUsITFCHoG51YGFuxtvwvMIYT44Vjdp9A54whRw1jK6P2AxNz2Xa2tjGLEr7rZOdu4lKbWQycoVE+uAKiNjVnG05KW9QogizeFUg+v9WjeWUjlPzwyaWBEQCYNbaZUpJtXA6VjfFteWkKf7i7yPjeUyUiMfbmbFm5OMGH2O+sH9SVIM064KD0z2CCHIdKMs535pIG1TVNg5gk3sA8k2hLe06etwEpXZ4EMXUeyImGnZgv+19f0iJOd3Xe5SrzQ+iQgz207K7j6RJbSVSaHb2RWPVdAeV7zgFalsKLSJqUt+2Z+qDPkUguYQSdUUd1rjgJIjxLyYTZyFrv4SzyzBpSTNb1ovLBgrYS91GYYVkU5jgEX5Nn+/R3BpS6IV7qUA39NdlMXjDIu+oOlIfJzVJ/oT/wmaLzBikR1MXtU0KpG8zIAH9V6E3jRWGY0QWAiXQK4s5jcYqCu84oIILq+xTZOpGs4axQQnzJ0rb1zVHQXgMFbXp/KQcxqATag==; searchKeyword=%ED%94%84%EB%A0%88%EC%8B%9C%EC%A7%80%20%EB%8D%94%ED%81%B0%20%ED%96%84%EA%B0%80%EB%93%9D%20%EB%B6%80%EB%8C%80%EC%A0%84%EA%B3%A8; searchKeywordType=%7B%22%ED%94%84%EB%A0%88%EC%8B%9C%EC%A7%80%20%EB%8D%94%ED%81%B0%20%ED%96%84%EA%B0%80%EB%93%9D%20%EB%B6%80%EB%8C%80%EC%A0%84%EA%B3%A8%22%3A0%7D; FUN="{\'search\':[{\'reqUrl\':\'/search.pang\',\'isValid\':true}]}"; overrideAbTestGroup=%5B%5D; baby-isWide=small; cto_bundle=Ylvgl18wSTBCNmtVdmVUT0RCc3Vlc09YVld6bEFFS0hpUUtISXNRRDYlMkZVaXRpYyUyQmNpbzQlMkIyJTJGendVUnRxYkowYiUyRnhxYyUyRnFkRWhvNlZITVRkM1l5d3hQTnBQYzhqJTJGRDl5b1JnajhmS243OU1jMmNFY29ybVdRWEVHaWNoWHNlV3BpV0hpRDhiUjE3OTZvSDRCNWxFZUFPUE42dyUzRCUzRA; bm_sv=4853930EBB3EC2598A320D85528673F9~YAAQ3Zc7F6s9sW+DAQAAJYu/eBEKmMt+DoEAlRInUH7A00f1Y9PCmG8wu0kX4g50XEum1juWdIA4syvL5npi/Luzz50iP6thdayFFEEOH9ZCUzF15nMIJ9F2eVE4Ve9ilOU2Y8h8OBnooDQKGE07Kk7o01s4wAfQiQxOvvV8dz3tMe1/FWcNKT1lvJz++B9hX/y2Be0IZ2b+3F7PYBRRqk/WX0h4+L//lS+ETLVGwYHf8nnVqEY42SVNN8TN8G7iXR8=~1; x-coupang-accept-language=ko-KR; _abck=B00E0DF2BD0B5CCE34434E7DA8E8E605~0~YAAQ3Zc7F8I9sW+DAQAAR4u/eAjF3ndjC8HX4njLnCQ1eNTBUeqmXX+bDZLx6q+5Zbe4oDBfxm8+1sASl1RBHfsVrwUQQcEt3ME3ZnyyqcX4e8j7TqFgwSczSsPYLUbE7T6mEwNKDEq/T2IidvZ/tH4yqmKhPd6NPjsuswmnjzAs87Xi8y1t8IdW+hlblYroxosQEItRP/DIwrWj518gLZ8wndoiQInjRux9Q/38bHzXKLF0aZj59nCGbN57PhzvBtgqUrzpHUi+uTAdr3fe6QuTzebEQ4Tft+8c1H6mbOwpR7eROCqHPHS6te1qLAOA6B3pK5J7WxZ4VVU4hvNSdWRn3G709Vm0k8DiBksT0DpDwK+F2CAsRyzjHL4=~-1~-1~-1; CLICKED_PAGE=2',
    'referer': 'https://www.coupang.com/np/categories/486687',
    'sec-ch-ua': '"Google Chrome";v="105", "Not)A;Brand";v="8", "Chromium";v="105"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36',
}

params = {
    'page': '2',
}

def extract_product_info(product_html):
    product_id = product_html['data-product-id']
    item_id = product_html.select_one('a.baby-product-link')['data-item-id']
    product_name = product_html.select_one('div.name').get_text().strip()
    rating_count = product_html.select_one('span.rating-total-count').get_text().lstrip('(').rstrip(')')
    
    product_dict = {
        'product_id' : product_id,
        'item_id' : item_id,
        'product_name' : product_name,
        'rating_count' : rating_count,
    }
    
    return product_dict


page = 1
category_id = 486687

cookies['CLICKED_PAGE'] = str(page)
params['page'] = str(page)
headers['referer'] = 'https://www.coupang.com/np/categories/{}'.format(category_id)

response = requests.get('https://www.coupang.com/np/categories/{}'.format(category_id), params=params, cookies=cookies, headers=headers, timeout=3.)

if response.status_code == 200:
    product_list = []
    
    html = response.text
    bsObject = BeautifulSoup(html, 'lxml')
    
    product_htmls = bsObject.select('li.baby-product')
    for product_html in product_htmls:
        product_list.append(extract_product_info(product_html))
        
        
print(product_list)