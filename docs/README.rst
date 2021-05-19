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

  loan = pyloan.Loan(loan_amount=160000,interest_rate=1.1,loan_term=10,start_date='2021-06-15',payment_amount=888.33)

The above defined 10-year mortgage/loan of 160,000 EUR with annual interest of 1.1% and monthly payment of 888.33 EUR starting on the 15th of June 2021.

--------------------
Get payment schedule
--------------------
To view the payment schedule and loan amortization use the ``get_payment_schedule`` method::

  payment_schedule = loan.get_payment_schedule()

This defined a named tuple with the following fields:

* `payment_id`: sequence of payment.
* `date`: date of payment.
* `payment_amount`: periodic payment amount of principal and interest.
* `interest_amount`: part of periodic payment amount that is interest.
* `principal_amount`: part of periodic payment amount that is principal.
* `special_principal_amount`: part of periodic payment amount that is ad-hoc/special principal.
* `total_principal_amount`: sum of `principal_amount` and `special_principal_amount` (if applicable).
* `loan_balance_amount`: amount of loan balance as at end of payment `date`.

.. tip::
   To define payment schedule as `pandas` DataFrame, use the method `from_records`::

    df=pd.DataFrame.from_records(loan.get_payment_schedule(),columns=pyloan.Payment._fields)

   This will generate a familiar DataFrame with named tuple fields as columns.

   .. image:: _static/pandas_df_output.png
      :alt: Pandas DataFrame output of the payment schedule
