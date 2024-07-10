import random

from ninja.router import Router

from core.standard_response import standard_response

router = Router()


@router.get("/leave/count")
def get_notice_count(request):
    # 返回0-10的随机数
    return standard_response(data=random.randint(0, 10))
    # return standard_response(data=0)


def generate_random_nine_digit_numbers(count):
    """
    生成指定数量的9位随机数字字符串。

    参数:
    count (int): 需要生成的9位数字字符串的数量。

    返回:
    list: 包含生成的9位数字字符串的列表。
    """
    numbers = []
    for _ in range(count):
        # 生成一个范围在100000000到999999999之间的随机整数，确保9位数
        number = random.randint(10000000000, 99999999999)
        numbers.append(str(number))
    return numbers


@router.get("/create_order/{count}")
def create_order(request, count: int):
    return standard_response(data=generate_random_nine_digit_numbers(count))
