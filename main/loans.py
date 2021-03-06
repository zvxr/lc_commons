"""Includes loan entity class, and methods for validating and casting variables.
"""

import dateutil.parser
import time

from collections import OrderedDict


DAY_EPOCH = 60 * 60 * 24  # One day, in seconds.


def _get_epoch(date_string):
    """Casts value (datestring) to unix timestamp. Nonetype is preserved."""
    if date_string:
        if type(date_string) == int:
            return date_string
        return int(time.mktime(dateutil.parser.parse(date_string).timetuple()))


def _get_float(value):
    """Casts value to float. Nonetype is preserved."""
    return float(value) if value else None


def _get_int(value):
    """Casts value to integer. Nonetype is preserved."""
    return int(value) if value else None


def _get_str(value):
    """Casts value to string. Nonetype is preserved."""
    return unicode(value) if value else None


class Loan(object):
    """Loan instances are meant to reflect an individual loan as presented by
    the LC API. It primarily acts as a sanitation and transportation from API
    response data to database.
    """
    # Class attribute `attributes` is defined as an ordered dict.
    # This is meant to provide the blueprint for operations on Loan instances.
    # Keys are attribute names.
    # Values are the type/method that is applied when instantiating.
    attributes = OrderedDict([
        ('acceptD', _get_epoch),
        ('accNowDelinq', _get_int),
        ('accOpenPast24Mths', _get_int),
        ('addrState', _get_str),
        ('addrZip', _get_str),
        ('annualInc', _get_float),
        ('avgCurBal', _get_int),
        ('asOfDate', _get_epoch),
        ('bcOpenToBuy', _get_int),
        ('bcUtil', _get_float),
        ('chargeoffWithin12Mths', _get_int),
        ('collections12MthsExMed', _get_int),
        ('creditPullD', _get_epoch),
        ('delinq2Yrs', _get_int),
        ('delinqAmnt', _get_float),
        ('desc', _get_str),
        ('dti', _get_float),
        ('earliestCrLine', _get_epoch),
        ('empLength', _get_int),
        ('empTitle', _get_str),
        ('expD', _get_epoch),
        ('expDefaultRate', _get_float),
        ('ficoRangeHigh', _get_int),
        ('ficoRangeLow', _get_int),
        ('fundedAmount', _get_float),
        ('grade', _get_str),
        ('homeOwnership', _get_str),
        ('id', _get_int),
        ('ilsExpD', _get_epoch),
        ('initialListStatus', _get_str),
        ('inqLast6Mths', _get_int),
        ('installment', _get_float),
        ('intRate', _get_float),
        ('investorCount', _get_int),
        ('isIncV', _get_str),
        ('listD', _get_epoch),
        ('loanAmount', _get_float),
        ('memberId', _get_int),
        ('mortAcc', _get_int),
        ('moSinOldIlAcct', _get_int),
        ('moSinOldRevTlOp', _get_int),
        ('moSinRcntRevTlOp', _get_int),
        ('moSinRcntTl', _get_int),
        ('mthsSinceLastDelinq', _get_int),
        ('mthsSinceLastMajorDerog', _get_int),
        ('mthsSinceLastRecord', _get_int),
        ('mthsSinceRecentBc', _get_int),
        ('mthsSinceRecentBcDlq', _get_int),
        ('mthsSinceRecentInq', _get_int),
        ('mthsSinceRecentRevolDelinq', _get_int),
        ('numAcctsEver120Ppd', _get_int),
        ('numActvBcTl', _get_int),
        ('numActvRevTl', _get_int),
        ('numBcSats', _get_int),
        ('numBcTl', _get_int),
        ('numIlTl', _get_int),
        ('numOpRevTl', _get_int),
        ('numRevAccts', _get_int),
        ('numRevTlBalGt0', _get_int),
        ('numSats', _get_int),
        ('numTl120dpd2m', _get_int),
        ('numTl30dpd', _get_int),
        ('numTl90gDpd24m', _get_int),
        ('numTlOpPast12m', _get_int),
        ('openAcc', _get_int),
        ('pctTlNvrDlq', _get_int),
        ('percentBcGt75', _get_float),
        ('pubRec', _get_int),
        ('pubRecBankruptcies', _get_int),
        ('purpose', _get_str),
        ('reviewStatus', _get_str),
        ('reviewStatusD', _get_epoch),
        ('revolBal', _get_float),
        ('revolUtil', _get_float),
        ('serviceFeeRate', _get_float),
        ('subGrade', _get_str),
        ('taxLiens', _get_int),
        ('term', _get_int),
        ('totalAcc', _get_int),
        ('totalBalExMort', _get_int),
        ('totalBcLimit', _get_int),
        ('totalIlHighCreditLimit', _get_int),
        ('totalRevHiLim', _get_int),
        ('totCollAmt', _get_int),
        ('totCurBal', _get_int),
        ('totHiCredLim', _get_int)
    ])

    def __init__(self, asOfDate, loan):
        """Initialized with date string asOfDate, and loan, a JSON dictionary
        containing loan data as part of the API response.
        """
        self.values = {'asOfDate': asOfDate}

        for key, cast in Loan.attributes.iteritems():

            if key == 'asOfDate':
                continue

            self.values[key] = cast(loan[key])

    def iteritems(self):
        for key in Loan.attributes:
            yield key, self.values[key]

    @property
    def asOfDate(self):
        return self.values.get('asOfDate')

    @property
    def fundedAmount(self):
        return self.values.get('fundedAmount')

    @property
    def id(self):
        return self.values.get('id')

    def get_raw_loans_tuple(self):
        return tuple([
            v for k, v in self.iteritems() if k not in (
                'asOfDate', 'fundedAmount'
            )
        ])

    def get_funded_tuple(self):
        return (self.asOfDate, self.fundedAmount, self.id)


class LoanOverTime(Loan):
    """LoanOverTime instances reflect an individual loan over time. It inherits
    from `Loan` but includes a list of tuples which reflects a time and amount.
    """

    def __init__(self, logger=None):
        self.__loanTuples = []
        self.logger = logger
        self.values = {}
        self._reset_properties()

    def _reset_properties(self):
        """Sets all dynamic properties to None. This method is called internally
        when instantiating or when methods are used to alter loans object is
        tracking.
        """
        self._amounts = None
        self._dates = None

    def load(self, *loans):
        """Accepts any number of Loan instances recording their asOfDate and
        fundedAmount. If it is the first loan, will also populate other fields.
        If the asOfDate has already been recorded, will ignore with a warning.
        If any loans beyond the first do not match the id recorded, will throw
        an exception.
        """
        self._reset_properties()  # No longer valid. Lazy-loaded as needed.

        for loan in loans:
            if type(loan) != Loan:
                raise TypeError("method params must only be Loan instances.")

            # If it is the first loan, set values of static fields.
            if not self.id:
                for key in Loan.attributes.iterkeys():

                    if key in ('asOfDate', 'fundedAmount'):
                        continue

                    self.values[key] = loan.values[key]

            # Ignore if the date has already been recorded.
            if loan.asOfDate in self.dates:
                if self.logger:
                    self.logger.warn(
                        "Skipping %s: has already been loaded." % loan.asOfDate
                    )
                print "Skipping %s: has already been loaded." % loan.asOfDate ##
                continue

            self.__loanTuples.append((loan.asOfDate, loan.fundedAmount))

    @property
    def amounts(self):
        if self._amounts == None:
            self._amounts = [lt[1] for lt in self.__loanTuples]
        return self._amounts

    @property
    def amountStart(self):
        if self.amounts:
            return sorted(self.amounts)[0]

    @property
    def amountEnd(self):
        if self.amounts:
            return sorted(self.amounts)[-1]

    @property
    def amountLeft(self):
        """Return integer difference between total and starting amount."""
        if self.amounts:
            return self.loanAmount - self.amountStart

    @property
    def dates(self):
        if self._dates == None:
            self._dates = [lt[0] for lt in self.__loanTuples]
        return self._dates

    @property
    def dateStart(self):
        if self.dates:
            return sorted(self.dates)[0]

    @property
    def dateDifference(self):
        """Returns epoch difference between first and last loan date."""
        if self.dates:
            return _get_epoch(self.dateEnd) - _get_epoch(self.dateStart)

    @property
    def dateEnd(self):
        if self.dates:
            return sorted(self.dates)[-1]

    @property
    def fundedRate(self):
        """Returns rate in which amounts have been funded, as float."""
        if self.amounts:
            if self.amountLeft != 0:
                return self.amountEnd / float(self.loanAmount)
            else:
                return 0

    @property
    def loanAmount(self):
        return self.values.get('loanAmount')

    def get_daily_funding_score(self):
        """Represents the rate in which the a loan was funded. It is then
        mulitplied out by how much the timespan covered using a 24 hour period
        as neutral (1).
        """
        dateDifference = self.dateDifference
        if dateDifference:
            return self.fundedRate * (DAY_EPOCH / dateDifference)
        else:
            return 0
