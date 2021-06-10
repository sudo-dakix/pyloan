# -*- coding: utf-8 -*-
import datetime as dt
import calendar as cal
import collections
from decimal import Decimal
from dateutil.relativedelta import relativedelta

Payment=collections.namedtuple('Payment',['date','payment_amount','interest_amount','principal_amount','special_principal_amount','total_principal_amount','loan_balance_amount'])

Special_Payment=collections.namedtuple('Special_Payment',['payment_amount','first_payment_date','special_payment_term','annual_payments'])
Loan_Summary=collections.namedtuple('Loan_Summary',['loan_amount','total_payment_amount','total_interest_amount','residual_loan_balance'])

# To-do:
### Actual/Actual

class Loan(object):

    def __init__(self,loan_amount,interest_rate,loan_term,start_date,payment_amount=None,first_payment_date=None,payment_end_of_month=True,end_date=False,interest_only_period=0,annual_payments=12,compounding_method='30E/360'):
        self.loan_amount=Decimal(str(loan_amount))
        self.interest_rate=Decimal(str(interest_rate/100)).quantize(Decimal(str(0.0001)))
        self.laon_term=loan_term
        self.payment_amount=payment_amount
        self.start_date=dt.datetime.strptime(start_date,'%Y-%m-%d')
        self.first_payment_date=dt.datetime.strptime(first_payment_date,'%Y-%m-%d') if first_payment_date is not None else None
        self.payment_end_of_month = payment_end_of_month
        self.end_date=end_date
        self.interest_only_period=interest_only_period
        self.annual_payments=annual_payments
        self.compounding_method=compounding_method
        self.special_payments=[]
        self.special_payments_schedule=[]
        self.no_of_payments=self.laon_term * self.annual_payments
        self.delta_dt=Decimal(str(12/self.annual_payments))

    @staticmethod
    def _quantize(amount):
        return Decimal(str(amount)).quantize(Decimal(str(0.01)))

    @staticmethod
    def _get_day_count(dt1,dt2,method,eom=False):
        y1, m1, d1 = dt1.year, dt1.month, dt1.day
        y2, m2, d2 = dt2.year, dt2.month, dt2.day
        dt1_eom_day=cal.monthrange(y1,m1)[1]
        dt2_eom_day=cal.monthrange(y2,m2)[1]

        if method in {'30A/360','30U/360','30E/360','30E/360 ISDA'}:
            if method=='30A/360':
                d1 = min(d1,30)
                d2 = min(d2,30) if d1 == 30 else d2
            if method=='30U/360':
                if eom and m1 == 2 and d1==dt1_eom_day and m2==2 and d2==dt2_eom_day:
                    d2=30
                if eom and m1 == 2 and d1==dt1_eom_day:
                    d1=30
                if d2 == 31 and d1 >= 30:
                    d2=30
                if d1==31:
                    d1=30
            if method=='30E/360':
                if d1 == 31:
                    d1=30
                if d2 == 31:
                    d2=30
            if method=='30E/360 ISDA':
                if d1==dt1_eom_day:
                    d1=30
                if d2==dt2_eom_day and m2 != 2:
                    d2=30

            day_count = (360*(y2-y1)+30*(m2-m1)+(d2-d1))
            year_days = 360

        if method=='A/365F':
            day_count=(dt2-dt1).days
            year_days=365

        if method=='A/360':
            day_count=(dt2-dt1).days
            year_days=360

        if method=='A/A ISDA':
            djn_dt1=(1461 * (y1 + 4800 + (m1 - 14)/12))/4 +(367 * (m1 - 2 - 12 * ((m1 - 14)/12)))/12 - (3 * ((y1 + 4900 + (m1 - 14)/12)/100))/4 + d1 - 32075
            djn_dt2=(1461 * (y2 + 4800 + (m2 - 14)/12))/4 +(367 * (m2 - 2 - 12 * ((m2 - 14)/12)))/12 - (3 * ((y2 + 4900 + (m2 - 14)/12)/100))/4 + d2 - 32075
            if y1==y2:
                day_count=djn_dt2-djn_dt1
                year_days=366 if cal.isleap(y2) else 365
            if y1 < y2:
                djn_dt1_eoy=(1461 * (y1 + 4800 + (12 - 14)/12))/4 +(367 * (12 - 2 - 12 * ((12 - 14)/12)))/12 - (3 * ((y1 + 4900 + (12 - 14)/12)/100))/4 + 31 - 32075
                day_count_dt1=djn_dt1_eoy-djn_dt1
                year_days_dt1=366 if cal.isleap(y1) else 365

                djn_dt2_boy=(1461 * (y2 + 4800 + (1 - 14)/12))/4 +(367 * (1 - 2 - 12 * ((1 - 14)/12)))/12 - (3 * ((y2 + 4900 + (1 - 14)/12)/100))/4 + 1 - 32075
                day_count_dt2=djn_dt2-djn_dt2_boy
                year_days_dt2=366 if cal.isleap(y2) else 365

                diff=y2-y1-1

                day_count=(day_count_dt1*year_days_dt2)+(day_count_dt2*year_days_dt1)+(diff*year_days_dt1*year_days_dt2)
                year_days=year_days_dt1*year_days_dt2

        factor = day_count / year_days
        return factor

    @staticmethod
    def _get_special_payment_schedule(self,special_payment):
        no_of_payments=special_payment.special_payment_term * special_payment.annual_payments
        annual_payments = special_payment.annual_payments
        dt0=dt.datetime.strptime(special_payment.first_payment_date,'%Y-%m-%d')
        special_payment_amount=self._quantize(special_payment.payment_amount)
        initial_special_payment=Payment(date=dt0,payment_amount=self._quantize(0),interest_amount=self._quantize(0),principal_amount=self._quantize(0),special_principal_amount=special_payment_amount,total_principal_amount=self._quantize(0),loan_balance_amount=self._quantize(0))
        special_payment_schedule=[initial_special_payment]

        for i in range(1,no_of_payments):
            date=dt0+relativedelta(months=i*12/annual_payments)
            special_payment=Payment(date=date,payment_amount=self._quantize(0),interest_amount=self._quantize(0),principal_amount=self._quantize(0),special_principal_amount=special_payment_amount,total_principal_amount=self._quantize(0),loan_balance_amount=self._quantize(0))
            special_payment_schedule.append(special_payment)

        return special_payment_schedule

    def get_payment_schedule(self):
        initial_payment=Payment(date=self.start_date,payment_amount=self._quantize(0),interest_amount=self._quantize(0),principal_amount=self._quantize(0),special_principal_amount=self._quantize(0),total_principal_amount=self._quantize(0),loan_balance_amount=self._quantize(self.loan_amount))
        payment_schedule=[initial_payment]

        if self.payment_amount is None:
            regular_principal_payment_amount= self.loan_amount*((self.interest_rate/self.annual_payments)*(1+(self.interest_rate/self.annual_payments))**((self.no_of_payments-self.interest_only_period)))/((1+(self.interest_rate/self.annual_payments))**((self.no_of_payments-self.interest_only_period))-1)
        else:
            regular_principal_payment_amount=self.payment_amount

        if self.first_payment_date is None:
            if self.payment_end_of_month==True:
                if self.start_date.day == cal.monthrange(self.start_date.year,self.start_date.month)[1]:
                    dt0 = self.start_date
                else:
                    dt0 = dt.datetime(self.start_date.year,self.start_date.month,cal.monthrange(self.start_date.year,self.start_date.month)[1],0,0)+relativedelta(months=-12/self.annual_payments)
            else:
                dt0 = self.start_date
        else:
            dt0=self.first_payment_date+relativedelta(months=-12/self.annual_payments)

        # take care of special payments
        special_payments_schedule_raw=[]
        special_payments_schedule=[]
        special_payments_dates=[]
        if len(self.special_payments_schedule)>0:
            for i in range(len(self.special_payments_schedule)):
                for j in range(len(self.special_payments_schedule[i])):
                    special_payments_schedule_raw.append([self.special_payments_schedule[i][j].date,self.special_payments_schedule[i][j].special_principal_amount])
                    if self.special_payments_schedule[i][j].date not in special_payments_dates:
                        special_payments_dates.append(self.special_payments_schedule[i][j].date)

        for i in range(len(special_payments_dates)):
            amt=self._quantize(str(0))
            for j in range(len(special_payments_schedule_raw)):
                if special_payments_schedule_raw[j][0]==special_payments_dates[i]:
                    amt+=special_payments_schedule_raw[j][1]
            special_payments_schedule.append([special_payments_dates[i],amt])

        # calculate payment schedule
        m=0
        for i in range(1,self.no_of_payments+1):

            date=dt0+relativedelta(months=i*12/self.annual_payments)
            if self.payment_end_of_month==True and self.first_payment_date is None:
                eom_day=cal.monthrange(date.year,date.month)[1]
                date=date.replace(day=eom_day)#dt.datetime(date.year,date.month,eom_day)

            special_principal_amount= self._quantize(0)
            bop_date = payment_schedule[(i+m)-1].date
            compounding_factor=Decimal(str(self._get_day_count(bop_date,date,self.compounding_method,eom=self.payment_end_of_month)))
            balance_bop=self._quantize(payment_schedule[(i+m)-1].loan_balance_amount)

            for j in range(len(special_payments_schedule)):
                if date == special_payments_schedule[j][0]:
                    special_principal_amount = special_payments_schedule[j][1]
                if (bop_date < special_payments_schedule[j][0] and special_payments_schedule[j][0] < date):
                    # handle special payment inserts
                    compounding_factor= Decimal(str(self._get_day_count(bop_date,special_payments_schedule[j][0],self.compounding_method,eom=self.payment_end_of_month)))
                    interest_amount = self._quantize(0) if balance_bop == Decimal(str(0)) else self._quantize(balance_bop*self.interest_rate*compounding_factor)
                    principal_amount= self._quantize(0)
                    special_principal_amount = self._quantize(0) if balance_bop == Decimal(str(0)) else min(special_payments_schedule[j][1]-interest_amount,balance_bop)
                    total_principal_amount=min(principal_amount+special_principal_amount,balance_bop)
                    total_payment_amount=total_principal_amount+interest_amount
                    balance_eop = max(balance_bop-total_principal_amount,self._quantize(0))
                    payment = Payment(date=special_payments_schedule[j][0], payment_amount=total_payment_amount,interest_amount=interest_amount,principal_amount=principal_amount,special_principal_amount=special_principal_amount,total_principal_amount=special_principal_amount,loan_balance_amount=balance_eop)
                    payment_schedule.append(payment)
                    m+=1
                    # handle regular payment inserts : update bop_date and bop_date, and special_principal_amount
                    bop_date=special_payments_schedule[j][0]
                    balance_bop=balance_eop
                    special_principal_amount=self._quantize(0)
                    compounding_factor=Decimal(str(self._get_day_count(bop_date,date,self.compounding_method,eom=self.payment_end_of_month)))

            interest_amount= self._quantize(0) if balance_bop == Decimal(str(0)) else self._quantize(balance_bop*self.interest_rate*compounding_factor)
            principal_amount = self._quantize(0) if balance_bop == Decimal(str(0)) or self.interest_only_period >= i else min(self._quantize(regular_principal_payment_amount)-interest_amount,balance_bop)
            special_principal_amount=min(balance_bop-principal_amount,special_principal_amount) if self.interest_only_period < i else self._quantize(0)
            total_principal_amount= min(principal_amount+special_principal_amount,balance_bop)
            total_payment_amount=total_principal_amount+interest_amount
            balance_eop = max(balance_bop-total_principal_amount,self._quantize(0))

            payment=Payment(date=date,payment_amount=total_payment_amount,interest_amount=interest_amount,principal_amount=principal_amount,special_principal_amount=special_principal_amount,total_principal_amount=total_principal_amount,loan_balance_amount=balance_eop)
            payment_schedule.append(payment)

        return payment_schedule

    def add_special_payment(self,payment_amount,first_payment_date,special_payment_term,annual_payments):
        special_payment=Special_Payment(payment_amount=payment_amount,first_payment_date=first_payment_date,special_payment_term=special_payment_term,annual_payments=annual_payments)
        self.special_payments.append(special_payment)
        self.special_payments_schedule.append(self._get_special_payment_schedule(self,special_payment))

    def get_loan_summary(self):
        payment_schedule=self.get_payment_schedule()
        total_payment_amount=0
        total_interest_amount=0
        total_principal_amount=0
        for payment in payment_schedule:
            total_payment_amount +=payment.payment_amount
            total_interest_amount +=payment.interest_amount
            total_principal_amount +=payment.total_principal_amount

        loan_summary=Loan_Summary(loan_amount=self.loan_amount,total_payment_amount=total_payment_amount,total_interest_amount=total_interest_amount,residual_loan_balance=self._quantize(self.loan_amount-total_principal_amount))

        return loan_summary
