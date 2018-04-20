import re

from db import DataBase

phone_reg = re.compile(
    "(?P<full_number>[78]?[\.) -]*(?P<first>\d{3})[\.)( -]*(?P<second>\d{3})[\.)( -]*(?P<third>\d{4}))|(?P<part_number>\d{7})")

city_code = '495'

db = DataBase()


def parse_phone_numbers(input):
    found = phone_reg.finditer(input)
    numbers = []
    for number_match in found:
        if number_match.group('full_number'):
            kkk = number_match.group('first')
            nnnnnnn = number_match.group('second') + number_match.group('third')
            if kkk and nnnnnnn:
                numbers.append(int(kkk + nnnnnnn))
        elif number_match.group('part_number'):
            numbers.append(int(city_code + number_match.group('part_number')))
    return numbers


def test():
    ph1 = "89059322433;+79811064022,9231950908 9138973664+7-383-3321635 3321635"
    ph1_1 = "89059322434;+79811064023,9231950909 9138973665+7-383-3321636 3321635"
    ph2 = "89059322432;+79811064021,9231950907 9138973663+7-383-3321634 3321634"

    det2 = "2 test 2"
    det1 = "test"

    n1 = parse_phone_numbers(ph1)
    db.save_order(n1, det1)

    n1_1 = parse_phone_numbers(ph1_1)
    db.save_order(n1_1, det2)

    numbers = parse_phone_numbers(ph2)
    db.save_order(numbers, det2)

    assert len(db.get_orders_by_phone(4953321635)) == 2
    assert db.get_orders_by_phone(9059322432) == det2


def test_interactive():
    pn_r = input("Phone numbers:")
    pn = parse_phone_numbers(pn_r)
    if not pn:
        print("Not found any phone numbers:(")

    print("Parse this numbers: %s" % pn)
    det = input("Type your order details:")

    db.save_order(pn, det)

    orders = db.get_orders_by_phone(pn[0])
    print('You have this orders: \n%s' % '\n'.join(orders))


if __name__ == '__main__':
    # test()
    test_interactive()
