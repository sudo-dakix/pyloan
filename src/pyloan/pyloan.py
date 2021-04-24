# -*- coding: utf-8 -*-

#import datetime as dt
#from dateutil.relativedelta import relativedelta

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
        
    #@property
    def set_parameters(self):
        self._parameters = {
            'no_of_payments':self.duration*self.annual_payments,
            'delta_dt':12/self.annual_payments,
            'compounding_factor':1/self.annual_payments,
            }