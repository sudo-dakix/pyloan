# PyLoan Package

This is a simple (mortgage) loan calculation tool.

## Installation

To install the package from PyPI run `python -m pip install pyloan`.

## Usage

First, import the package `from pyloan import pyloan`.

Define a loan using the following parameters:
* `loan_amount`: nominal principal amount of the loan.
* `interest_rate`: annual nominal interest rate (in %).
* `loan_term`: duration of the loan in years.
* `payment_amount`: nominal repayment amount in currency units.
* `start_date`: date as at which the loan was issued, must be entered in ISO format; that is YYYY-MM-DD.
* `first_payment_date` (optional): date of the first payment, must be entered in ISO format; that is YYYY-MM-DD. By default, value is set to None. Hence, the first payment date will be set to the start_date plus 1 payment period. If specified, first payment will be set to the first_payment_date.
* `payment_end_of_month` (optional): payments are made as at end of month. By default, value is set to True. Hence, all payment will be as at month end date. If set to False, then payment dates will be set to first_payment_date plus 1 payment period.
* `end_date` (optional): date as at which the loan terminates. Currently not used in the package.
* `interest_only_period` (optional): number of interest only payment periods; that is principal is not repaid, only interest is repaid. By default, value is set to 0. Hence, principal and interest will be paid as of the first payment. If set to value greater than 0, then repayments of principal will begin only after interest_only_period.
* `annual_payments` (optional): number of payments per year. By default, set to 12, which means that there are 12 monthly payments. Value can be set to 4, 2 and 1 for quarterly, semi-annual and annual payments, respectively.

### Illustrative example

Given a 10-year loan of 260000 EUR with annual interest rate of 1.1% and monthly repayments of 888.33 EUR per month paid monthly starting on 2021-06-15 with the first payment on 2020-06-30 and subsequent payments at end of each month, the loan can be defined as:

`loan = pyloan.Loan(
  loan_amount=260000,
  interest_rate=1.1,
  loan_term=10,
  start_date='2021-06-15',
  payment_amount=888.33
  )`

Now, retrieve repayment schedule using `loan.get_payment_schedule()`. This outputs a named tuple, which contains

* payment_id: sequence of payment.
* date: date of payment.
* payment_amount: total amount of interest and principal paid.
* interest_amount: amount of interest paid.
* principal_amount: amount of principal (regular) paid.
* special_principal_amount: amount of special (ad-hoc) principal paid. Currently not used, hence set to 0.
* total_principal_amount: total amount of regular and ah-hoc principal paid.
* loan_balance_amount: amount of loan balance as at end of payment date.

To define the `loan` within a panda's DataFram, use `from_records` method. For example, `loan_df=pd.DataFrame.from_records(loan.get_payment_schedule(),columns=pyloan.Payment._fields)`. This will generate a familiar panda's DataFrame with named tuple elements as columns.

## To-Do

* Add Actual method for interest rate compounding.
* Add special principal repayments.
* Add loan summary details.
* Integrate end_date.
* Extend documentation.
