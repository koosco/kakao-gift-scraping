class PriceProcessor:
    @staticmethod
    def proceed(str_price: str):
        print('before process', str_price)
        str_price = str_price[:-1]
        res = int(''.join(str_price.split(',')))
        print('res', res)
        return res
