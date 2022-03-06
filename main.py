#Import necessary libraries
import sys
import pandas as pd
from optparse import OptionParser

sys.path.append('lib')
from utils import Discounts

def readConfig(configFile: str) -> dict:
    '''
    Read configuration file. Extract discounts parameters

    input: 
        configFile: Path to the configuration file (script)
    output:
        parameters: Dictionary with the discount parameters
    '''
    parameters = {}
    try:
        with open(configFile, 'r') as inputFile:
            while 1:
                line = inputFile.readline()
                if not line: break
                if "#" not in line and len(line) > 1:
                    command = line.split('=')
                    parameters[command[0].strip()] = eval(command[1].strip())
        return parameters
    except IOError:
        print (f"File {configFile} does not exist!")
        sys.exit()

def perform_debug(n_tests: int, products: list, prices: dict,discounts: Discounts):
    '''
    For debugging. Print out shopping carts after applying each discount 
    for 100 different random samples to visualise and check the process

    input:
        n_tests: number of tests to perform (int)
        products: list of available products in catalogue (list)
        prices: prices for each product (dictionary)
        discounts: applicable discounts (Discounts class object)
    '''
    from numpy.random import seed,randint
    seed(1)
    for _ in range(n_tests):
        values = randint(0,20,3)
        template_cart = {prod: values[i] for i,prod in enumerate(products)}
        #Print your random shopping cart
        print (f'Your shopping cart contains {template_cart}.\n Proceeding to checkout...')
        template_price = total(template_cart,prices,discounts,True)
        #Print total price
        print (f'Total amount to pay: {template_price:.2f}€. Have a nice day!')

def WelcomeMessage(products: list, discounts: Discounts):
    '''
    Print information about products and discounts.
    The user can check the information and then proceed to fill its shopping cart

    input:
        products: list of available products in catalogue (list)
        discounts: applicable discounts (Discounts class object)

    '''
    print (f"\nWelcome to Cofi Physical store!! This is our list of products:\n\n {products}\n")
    discounts.print_offers()

def scan(item: str, shopping_cart: dict, nunits=1):
    '''
    Scan different input items. It scans one product and updates the shopping cart

    Input:
        item: Name of the scanned item (str)
        shopping_cart: Current shopping cart of the user (dict)
        nunits (optional): Number of units of the associated item to fill the shopping cart (int)
    '''
    shopping_cart[item] += nunits

def total(purchase: dict, prices: dict, discounts: Discounts,debug=False):
    '''
    Apply the discounts and calculate total price
    
    Input: 
        purchase: This is the shopping cart (dict)
        prices: prices for each product (dict)
        discounts: applicable discounts (Discounts class object)
    Output:
        total: total price to be paid (float)
    '''
    
    total = 0

    #Apply discounts. Elements which have a discount applied are removed from the shopping cart
    for disc in discounts.order:
        money,purchase = getattr(discounts, f'apply_{disc}')(purchase, prices)
        total += money
        if debug:
            #Check total money after discount and remaining shopping cart
            print (f'Total money after discount {disc}: {total:.2f}€ and the remaining shopping cart is {purchase}')

    #Add remaining items, with regular prices
    for item in purchase.keys():
        total += purchase[item]*prices[item]

    return total

# #########################################################
#
# main function: useCheckout
#
# #########################################################

def useCheckout():
    parser = OptionParser(usage = "usage: %prog arguments", version="%prog")
    parser.add_option("-c","--config",        dest="config", help="configuration file (default: %default)")
    parser.add_option("-p","--products",        dest="products", help="products file (default: %default)")
    parser.add_option("-d","--debug",        dest="debug", action='store_true', help="Use a set of default values to test the script (default: %default)")
    parser.set_defaults(config='config/config.ini', products='products.json', debug=False)
    (options,args) = parser.parse_args()

    #Read configuration file
    parameters = readConfig(options.config)
    
    #Import product information and discount offers. 
    discounts = Discounts(parameters)
    df = pd.read_json(options.products)
    #Print welcome message
    WelcomeMessage(df,discounts)

    #Perform numerical conversion and store in dictionary
    df['Price'] = df['Price'].replace('[€]','',regex=True).astype(float)
    prices = df.set_index('Code').to_dict()['Price']
    #Get product catalogue
    products = df['Code'].values

    #Run debug and exit
    if options.debug:
        n_tests = 100
        perform_debug(n_tests,products,prices,discounts)
        sys.exit()

    #Fill shopping cart. Interaction with user
    shopping_cart = {prod: 0 for prod in products} #Initialise shopping cart
    continue_purchase = True
    while continue_purchase:
        item = input('\nSpecify your product (introduce product code). Type nothing to proceed to checkout\n').upper()
        if item == '': continue_purchase = False
        elif item not in products:
            print ("This product is not present in the catalogue. Try again")
        else:
            nunits = input('Specify number of units. If no positive integer value is selected will add one.\n')
            if nunits.isdigit(): 
                nunits =  int(nunits)
                scan(item,shopping_cart,nunits)
            else:
                scan(item,shopping_cart)

    print (f'Your shopping cart contains {shopping_cart}.\n Proceeding to checkout...')

    #Calculate total price
    total_price = total(shopping_cart,prices,discounts)
    print (f'Total amount to pay: {total_price:.2f}€. Have a nice day!')


if __name__ == '__main__':
    useCheckout()