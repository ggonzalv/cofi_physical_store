class Discounts:
    def __init__(self,parameters):
        self.two_for_one = parameters['two_for_one']
        self.bulk = parameters['bulk']
        self.swag = parameters['swag']
        self.order = parameters['order']
    
    def apply_swag(self,products,prices):
        total_swag = 0
        for n_tuple in self.swag:
            try:
                while all(products[swag_item] > 0 for swag_item in n_tuple[0]):
                    total_swag += n_tuple[1]
                    for item in products.keys():
                        products[item] -= 1
            except (KeyError, TypeError):
                continue
        return total_swag, products
    
    def apply_bulk(self,products,prices):
        total_bulk = 0
        for item in products.keys():
            for n_tuple in self.bulk:
                if item == n_tuple[0]:
                    if products[item] >= 3:
                        total_bulk += products[item]*n_tuple[1]
                        products[item] = 0
        return total_bulk, products

    def apply_2for1(self,products,prices):
        total_2for1 = 0
        for item in products.keys():
            if item in self.two_for_one:
                if products[item] > 1:
                    total_2for1 += prices[item]*(products[item] // 2)
                    products[item] = products[item] - 2*(products[item] // 2)
                if products[item] == 1:
                    total_2for1 += prices[item]
                products[item] = 0
        return total_2for1, products

    def print_offers(self):
        print ('Check out our special offers!!\n')
        print (f'-->Two for one in all these products:\n {self.two_for_one}\n')
        print ('-->Special price if you buy 3 or more units in these products:')
        for n_tuple in self.bulk:
            print (f'{n_tuple[0]}: {n_tuple[1]:.2f}€')
        print ('\n-->Swag discount if you buy one unit of these sets of products:')
        for n_tuple in self.swag:
            print (f'{n_tuple[0]}: {n_tuple[1]:.2f}€')



