from main import *
import sys
import pytest

sys.path.append('lib')
from utils import Discounts

class TestClass:

    ###########################################
    ### Test read config function
    ###########################################

    def test_readConfig(self):
        parameters = readConfig('config/config.ini')
        assert (type(parameters) == dict)

    def test_readConfig2(self):
        with pytest.raises(SystemExit):
            readConfig('')

    ###########################################
    ### Test scan function
    ###########################################
    def test_scan(self):
        products = ["VOUCHER","TSHIRT","MUG"]
        from numpy.random import seed,randint
        seed(0)
        shopping_cart = {prod: randint(0,20) for prod in products} #Initialise random shopping cart
        initial_cart = shopping_cart.copy()
        scan("VOUCHER", shopping_cart)
        scan("TSHIRT", shopping_cart)
        scan("MUG", shopping_cart)
        scan("VOUCHER", shopping_cart,3)
        assert (shopping_cart['VOUCHER'] == (initial_cart['VOUCHER'] + 4) and
                shopping_cart['TSHIRT'] == (initial_cart['TSHIRT'] + 1) and
                shopping_cart['MUG'] == (initial_cart['MUG'] + 1)
        )

    ###########################################
    ### Test total function
    ###########################################
    def test_total1(self):
        '''
        Test swag discount
        '''
        parameters = readConfig('config/config.ini')
        discounts = Discounts(parameters)
        prices = {'VOUCHER': 5.0, 'TSHIRT': 20.0, 'MUG': 7.50}
        random_cart = {'VOUCHER': 1, 'TSHIRT': 2, 'MUG': 1}
        assert (total(random_cart,prices,discounts)==45)

    def test_total2(self):
        '''
        Test bulk discount
        '''
        parameters = readConfig('config/config.ini')
        discounts = Discounts(parameters)
        prices = {'VOUCHER': 5.0, 'TSHIRT': 20.0, 'MUG': 7.50}
        random_cart = {'VOUCHER': 1, 'TSHIRT': 25, 'MUG': 0}
        assert (total(random_cart,prices,discounts)==480)

    def test_total3(self):
        '''
        Test 2for1 discount
        '''
        parameters = readConfig('config/config.ini')
        discounts = Discounts(parameters)
        prices = {'VOUCHER': 5.0, 'TSHIRT': 20.0, 'MUG': 7.50}
        random_cart = {'VOUCHER': 3, 'TSHIRT': 0, 'MUG': 2}
        assert (total(random_cart,prices,discounts)==25)

    def test_total4(self):
        '''
        Test no discount
        '''
        parameters = readConfig('config/config.ini')
        discounts = Discounts(parameters)
        prices = {'VOUCHER': 5.0, 'TSHIRT': 20.0, 'MUG': 7.50}
        random_cart = {'VOUCHER': 1, 'TSHIRT': 0, 'MUG': 2}
        assert (total(random_cart,prices,discounts)==20)

    def test_total5(self):
        '''
        Test all discounts simultaneously
        '''
        parameters = readConfig('config/config.ini')
        discounts = Discounts(parameters)
        prices = {'VOUCHER': 5.0, 'TSHIRT': 20.0, 'MUG': 7.50}
        random_cart = {'VOUCHER': 15, 'TSHIRT': 16, 'MUG': 6}
        assert (total(random_cart,prices,discounts)==365)
