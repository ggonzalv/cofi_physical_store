#Import necessary libraries
import sys
import pandas as pd
from optparse import OptionParser

sys.path.append('lib')
from utils import Discounts

# Read configuration file. Extract discounts parameters
def readConfig(configFile):
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

# Perform several tests and exit
def perform_tests(n_tests,products,prices,discounts):
    from numpy.random import seed,randint
    seed(1)
    for _ in range(n_tests):
        values = randint(0,20,3)
        template_cart = {prod: values[i] for i,prod in enumerate(products)}
        print (f'Your shopping cart contains {template_cart}.\n Proceeding to checkout...')
        template_price = total(template_cart,prices,discounts,True)
        print (f'Total amount to pay: {template_price:.2f}€. Have a nice day!')


#Print information about products and discounts
def WelcomeMessage(products,discounts):
    print (f"\nWelcome to Cofi Physical store!! This is our list of products:\n\n {products}\n")
    discounts.print_offers()

#Scan different input items
def scan(item,shopping_cart,nunits=1):
    shopping_cart[item] += nunits


#Calculate total price, after applying the discounts
def total(purchase,prices,discounts,tests=False):
    
    total = 0

    #Apply discounts. Elements which have a discount applied are removed from the shopping cart
    for disc in discounts.order:
        money,purchase = getattr(discounts, f'apply_{disc}')(purchase, prices)
        total += money
        if tests:
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
    parser.add_option("-t","--tests",        dest="tests", action='store_true', help="Use a set of default values to test the script (default: %default)")
    parser.set_defaults(config='config/config.ini', products='products.json', tests=False)
    (options,args) = parser.parse_args()

    #Read configuration file
    parameters = readConfig(options.config)

    print (parameters)
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

    #Run tests and exit
    if options.tests:
        n_tests = 100
        perform_tests(n_tests,products,prices,discounts)
        sys.exit()

    #Fill shopping cart
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