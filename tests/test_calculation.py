import pytest
from app.calculation import add, subtract, multiply, devide, BankAccount, InsufficientFunds


# pytest fixture will be called before every test function run,
# fixture method needs to be passed to the test function
@pytest.fixture
def zero_bank_account(): return BankAccount()


@pytest.fixture
def bank_account(): return BankAccount(50)


# test you function with multiple set of values.
@pytest.mark.parametrize("n1, n2, result", [(3, 2, 5), (7, 1, 8), (12, 4, 16)])
def test_add(n1, n2, result): assert add(n1, n2) == result


@pytest.mark.parametrize("n1, n2, result", [(3, 2, 1), (7, 1, 6), (12, 4, 8)])
def test_subtract(n1, n2, result): assert subtract(n1, n2) == result


@pytest.mark.parametrize("n1, n2, result", [(3, 2, 6), (7, 1, 7), (12, 4, 48)])
def test_multiply(n1, n2, result): assert multiply(n1, n2) == result


@pytest.mark.parametrize("n1, n2, result", [
    (3, 2, 1.5), (7, 1, 7), (12, 4, 3)
])
def test_devide(n1, n2, result): assert devide(n1, n2) == result


def test_bank_set_initial_amount(bank_account):
    assert bank_account.balance == 50


def test_bank_default_amount(zero_bank_account):
    assert zero_bank_account.balance == 0


def test_withdraw(bank_account):
    bank_account.withdraw(20)
    assert bank_account.balance == 30


def test_deposit(bank_account):
    bank_account.deposit(30)
    assert bank_account.balance == 80


def test_collect_interest(bank_account):
    bank_account.collect_interest()
    assert round(bank_account.balance, 6) == 55


# combo of parametrize and fixture
@pytest.mark.parametrize("deposited, withdrew, balance", [
        (200, 100, 100),
        (50, 10, 40),
        (1200, 200, 1000)
])
def test_bank_transaction(zero_bank_account, deposited, withdrew, balance):
    zero_bank_account.deposit(deposited)
    zero_bank_account.withdraw(withdrew)
    assert zero_bank_account.balance == balance


# for the test where exception will be occured, we need to write separate test case
# and with the `with pytest.raises(<expected_exception>)` we are telling pytest that we expecting an exception
# and thus if we got the exception our test case will be passed.
def test_insufficient_funds(bank_account):
    with pytest.raises(InsufficientFunds):
        bank_account.withdraw(200)
