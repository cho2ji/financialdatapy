"""This module handles logic of choosing which stock exchange to search."""
from datetime import datetime
import pandas as pd
from typing import Optional
from financialdatapy.financials import UsFinancials
from financialdatapy.price import UsMarket
from financialdatapy.price import KorMarket
from financialdatapy.stocklist import StockList


class NotAvailable(Exception):
    """Raised when a company is not listed in the stock exchange.

    :param msg: Error message, defaults to 'Data is not available.'
    :type msg: str, optional
    """
    def __init__(self, msg: str = 'Data is not available.', *args, **kwargs):
        super().__init__(msg, *args, **kwargs)


class Market:
    """This class represents a stock exchange.

    :param country_code: Country where the stock is listed.
    :type country_code: str
    """

    def __init__(self, country_code: str):
        """Initialize stock exchange."""
        self.country_code = country_code.upper()

    def financial_statement(
                self,
                symbol: str,
                financial: str,
                period: str,
                type_of_financial: Optional[str] = None
    ) -> pd.DataFrame:
        """Get financial statements.

        :param symbol: Symbol of a company/stock.
        :type symbol: str
        :param financial: Which financial statement to retrieve.
        :type financial: str
        :param period: Either 'annual' or 'quarter.
        :type period: str
        :param type_of_financial: Pass 'standard' for the method to return
            standard financials. If empty, finanicials as reported will be
            returned, defaults to None.
        :type type_of_financial: Optional[str], optional
        :raises: :class:`NotAvailable`: If the symbol is not listed in the
            stock exchange.
        :return: Either financials as reported or standard financials.
        :rtype: pandas.DataFrame
        """
        if self.country_code == 'USA':
            comp_cik = StockList.search_cik(symbol)
            market = UsFinancials(symbol, financial, period, comp_cik)

            if type_of_financial == 'standard':
                return market.get_standard_financials()

            return market.get_financials()
        elif self.country_code == 'KOR':
            pass
        else:
            raise NotAvailable()

    def historical_price(self, symbol, start, end) -> pd.DataFrame:
        """Get historical stock price data.

        :param symbol: Symbol of a company/stock.
        :type symbol: str
        :param start: Start date to query.
        :type start: str
        :param end: End date to query.
        :type end: str
        :raises: :class:`NotAvailable`: If the symbol is not listed in the
            stock exchange.
        :return: Historical stock price data.
        :rtype: pandas.DataFrame
        """
        if self.country_code == 'USA':
            return UsMarket(symbol, start, end)
        elif self.country_code == 'KOR':
            return KorMarket(symbol, start, end)
        else:
            raise NotAvailable()