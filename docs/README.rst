####################
PyLoan documentation
####################
Everything you need to know about PyLoan - a simple mortgage/loan calculation tool.

========
Features
========
PyLoan can perform simple mortgage/loan calculations:

* Amortize a loan based on the specified payment schedule.
* Consider ad-hoc or periodic special principal repayments during loan amortization schedule (under development).
* Calculate interest payments using either 30/360 methods or actual methods.

============
Installation
============
Being a Python package, PyLoan requires Python (version 3.6 or higher).

-----------------
Install from PyPI
-----------------
To install the package from PyPI run this simple command in your terminal of choice::

  python -m pip install pyloan

-------------------
Get the Source Code
-------------------
PyLoan is maintained on `GitHub <https://github.com/sudo-dakix/pyloan>`__, where the code is always available.

Your can either clone the public repository::

  git clone https://github.com/sudo-dakix/pyloan.git

Once you have a copy of the source, you can embed it in your own Python package, or install it into your site-packages easily by running this command from the PyLoan source code directory::

  python -m pip install

==========
Quickstart
==========
This section gives an introduction in how to get started with PyLoan.

-------------
Define a loan
-------------
Defining a loan with PyLoan is very simple. Begin by importing the PyLoan module::

 from pyloan import pyloan

Next define a loan::

  loan = pyloan.Loan(loan_amount=160000,interest_rate=1.1,loan_term=10,start_date='2020-06-15',payment_amount=888.33)

The above defined 10-year mortgage/loan of 160,000 EUR with annual interest of 1.1% and monthly payment of 888.33 EUR starting on the 15th of June 2020.

--------------------
Get payment schedule
--------------------
To view the payment schedule and loan amortization use the ``get_payment_schedule`` method::

  payment_schedule = loan.get_payment_schedule()

The above outputs a list of named tuples with the following fields per row:

* `payment_id`: sequence of payment.
* `date`: date of payment.
* `payment_amount`: periodic payment amount of principal and interest.
* `interest_amount`: part of periodic payment amount that is interest.
* `principal_amount`: part of periodic payment amount that is principal.
* `special_principal_amount`: part of periodic payment amount that is ad-hoc/special principal.
* `total_principal_amount`: sum of `principal_amount` and `special_principal_amount` (if applicable).
* `loan_balance_amount`: amount of loan balance as at end of payment `date`.

The first row represents the loan start with the 'loan_balance_column' equal to the loan amount. Each subsequent row represents loan repayment.

.. tip::
   To define payment schedule as `pandas` DataFrame, use the method `from_records`::

    df=pd.DataFrame.from_records(loan.get_payment_schedule(),columns=pyloan.Payment._fields)

   This will generate a familiar DataFrame with named tuple fields as columns.

   .. image:: _static/pandas_df_output.png
      :alt: Pandas DataFrame output of the payment schedule

The main assumption of the above is that repayments are on monthly basis. It is possible to change this to quarterly, semi-annual or annual payments by setting value of the ``Loan`` argument ``annual_payments`` to 4, 2 or 1, respectively. Default argument value is 12 (monthly payments).

In addition, the payment schedule above assumes that payments are made at month end, with the first payment starting on the 30th of June 2020. In case repayments are not made at month end, this can be adjusted by setting the ``Loan`` argument ``payment_end_of_month`` to ``False`` and setting the argument ``first_payment_date`` to the date of the first payment date.

Below is an example of the same loan that is paid on quarterly basis, on the 15th of every month::

 loan = pyloan.Loan(loan_amount=160000,interest_rate=1.1,loan_term=10,start_date='2020-06-15',payment_amount=888.33,first_payment_date='2020-09-15',annual_payments=4)

.. image:: _static/loan_quarterly_payments_on_specific_dates.png
   :alt: Pandas DataFrame output of the payment schedule on specific days on quarterly basis.

--------------------
Add special payments
--------------------
To add special payments to the loand, use the `add_special_payment` method. For instance, following the example above, add special payment of 5000 EUR first paid on 2021-03-15 for next 8 years paid annually::

  loan.add_special_payment(payment_amount=5000,first_payment_date='2021-03-15',special_payment_term=8,annual_payments=1)

Next, recalculate payment schedule considering special payments as defined above::

  payment_schedule = loan.get_payment_schedule()

This updates payment schedule by considering special payments

.. image:: _static/special_payments.png
   :alt: Considering special payments in payment schedule.

-------------------------
Interest rate compounding
-------------------------
By default PyLoan is compounding interest rates based on the 30/360 day count method, specifically the so-called 30E/360 method. To change the method use the `compounding_method` attribute when defining a loan, which accepts the following day count conventions:

* 30A/360.
* 30U/360.
* 30E/360.
* 30E/360 ISDA.

As of current version, actual day count method is under development.
