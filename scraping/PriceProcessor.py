class PriceProcessor:
    @staticmethod
    def proceed(str_price: str):
        str_price = str_price[:-1]
        res = int(''.join(str_price.split(',')))
        return res
