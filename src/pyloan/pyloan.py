# -*- coding: utf-8 -*-

#import datetime as dt
#from dateutil.relativedelta import relativedelta

from collections import namedtuple
from decimal import Decimal

Payment=namedtuple('Payment',['pmt_no','pmt','int','pmt_regular','pmt_special','pmt_total','balance'])

class Loan(object):

    def __init__(self,principal,interest,duration,payment_amount,interest_only_period=0,annual_payments=12):
        #inputs
        self.principal=principal
        self.interest=interest
        self.duration=duration
        self.interest_only_period=interest_only_period
        self.annual_payments=annual_payments
        self.payment_amount=payment_amount
        #parameters
        self.no_of_payments=self.duration*self.annual_payments
        self.delta_dt=12/self.annual_payments
        self.compounding_factor=1/self.annual_payments
        
        #initial data
        #initial_data=
        
        # to delete
        self._parameters={}
        
    def amortize(self):
        pmt_init=Payment(pmt_no=0,pmt=0,int=0,pmt_regular=0,pmt_special=0,pmt_total=0,balance=self.principal)
        pmt_schedule=[pmt_init]
        
        for i in range(1,self.no_of_payments+1):
            
            balance_bop=pmt_schedule[i-1].balance
            amt_interest = 0. if balance_bop == 0. else balance_bop*self.interest*self.compounding_factor
            amt_principal_regular = self.payment_amount-amt_interest
            amt_principal_special = 0.
            amt_principal_total = min(amt_principal_regular+amt_principal_special,balance_bop)
            amt_total_payment=amt_principal_total + amt_interest
            
            balance_eop=balance_bop-amt_principal_total
            
            installment=Payment(pmt_no=i,pmt=self.payment_amount,int=amt_interest,pmt_regular=amt_principal_regular,pmt_special=amt_principal_special,pmt_total=amt_total_payment,balance=balance_eop)
            pmt_schedule.append(installment)
        
        return pmt_schedule
        
    #@property
    def set_parameters(self):
        self._parameters = {
            'no_of_payments':self.duration*self.annual_payments,
            'delta_dt':12/self.annual_payments,
            'compounding_factor':1/self.annual_payments,
            }