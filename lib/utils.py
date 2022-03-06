class Discounts:
    '''
    The class discounts takes as input the parameters read from the configuration file. 
    It then knows which products are selectable for each type of discount.
    It contains several built-in functions to apply each type of discount.
    An additional print function is included so that the user can retrieve the discounts information.

    Input:
        parameters: Discount parameters (dict). More details are given in the configuration file
    '''

    def __init__(self,parameters: dict):
        self.two_for_one = parameters['two_for_one']
        self.bulk = parameters['bulk']
        self.swag = parameters['swag']
        self.order = parameters['order']
    
    def apply_swag(self,products: dict, prices: dict):
        '''
        Apply swag discount. 

        Input:
            products: current items in shopping cart (dict)
            prices: prices for each product (dict)

        Output:
            total_swag: total amount of money after applying swag discount (float)
            products: updated shopping cart after removing items eligible for swag discount (dict)
        '''
        total_swag = 0
        for n_tuple in self.swag:
            try:
                while all(products[swag_item] > 0 for swag_item in n_tuple[0]):
                    total_swag += n_tuple[1]
                    for item in products:
                        products[item] -= 1
            except (KeyError, TypeError):
                continue
        return total_swag, products
    
    def apply_bulk(self,products: dict, prices: dict):
        '''
        Apply bulk discount. 

        Input:
            products: current items in shopping cart (dict)
            prices: prices for each product (dict)

        Output:
            total_bulk: total amount of money after applying bulk discount (float)
            products: updated shopping cart after removing items eligible for bulk discount (dict)
        '''
        total_bulk = 0
        for item in products:
            for n_tuple in self.bulk:
                if item == n_tuple[0]:
                    if products[item] >= 3:
                        total_bulk += products[item]*n_tuple[1]
                        products[item] = 0
        return total_bulk, products

    def apply_2for1(self,products: dict, prices: dict):
        '''
        Apply two for one discount. 

        Input:
            products: current items in shopping cart (dict)
            prices: prices for each product (dict)

        Output:
            total_2for1: total amount of money after applying two for one discount (float)
            products: updated shopping cart after removing items eligible for two for one discount (disc)
        '''

        total_2for1 = 0
        for item in products:
            if item in self.two_for_one and products[item] > 1:
                total_2for1 += prices[item]*(products[item] // 2)
                products[item] = products[item] - 2*(products[item] // 2)
        return total_2for1, products

    def print_offers(self):
        '''
        Display discount information
        '''
        print ('Check out our special offers!!\n')
        print (f'-->Two for one in all these products:\n {self.two_for_one}\n')
        print ('-->Special price if you buy 3 or more units in these products:')
        for n_tuple in self.bulk:
            print (f'{n_tuple[0]}: {n_tuple[1]:.2f}€')
        print ('\n-->Swag discount if you buy one unit of these sets of products:')
        for n_tuple in self.swag:
            print (f'{n_tuple[0]}: {n_tuple[1]:.2f}€')





