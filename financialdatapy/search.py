from financialdatapy import request


class Company:
    def __init__(self, symbol: str) -> dict:
        self.symbol = symbol

    def search_pair_id(self):
        url = 'https://www.investing.com/search/service/searchTopBar'
        form_data = {
            'search_text': self.symbol,
        }
        res = request.Request(url, method='post', data=form_data)
        data = res.get_json()
        pair_id = data['quotes'][0]['pairId']

        return pair_id
