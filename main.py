#Import necessary libraries
import pandas as pd
from optparse import OptionParser
from utils import Discounts

def WelcomeMessage(products,discounts):
    print (f"\nWelcome to Cofi Physical store!! This is our list of products:\n {products}\n")
    discounts.print_offers()

def scan(products):
    purchase = {}
    continue_purchase = True
    while continue_purchase:
        item = input('\nSpecify your product. Type nothing to proceed to checkout\n').upper()
        if item in purchase:
            item = input('This product is already in your shopping cart. Type again to replace units or select another product\n').upper()
        if item == '': continue_purchase = False
        elif item not in products:
            print ("This product is not present in the catalogue. Try again")
        else:
            validunits = False
            while not validunits:
                nunits = input('Specify number of units. Type nothing to go back.\n')
                if nunits == '': break
                elif nunits.isdigit(): 
                    validunits = True
                    purchase[item] =  int(nunits)
                else:
                    print ("This is not a valid number of items. Try again")

    return purchase

    
def checkout(purchase,prices,discounts):
    
    total = 0

    for disc in discounts.order:
        money,purchase = getattr(discounts, disc)(purchase,prices)
        total += money

    for item in purchase.keys():
        total += purchase[item]*prices[item]

    return total






def main():
    parser = OptionParser(usage = "usage: %prog arguments", version="%prog")
    parser.add_option("-r","--read",        dest="read", action='store_true', help="read products file (default: %default)")
    parser.set_defaults(read=False)
    (options,args) = parser.parse_args()

    #Import product information and discount offers. 
    discounts = Discounts()
    df = pd.read_json("products.json")
    #Print welcome message
    WelcomeMessage(df,discounts)

    #Perform numerical conversion and store in dictionary
    df['Price'] = df['Price'].replace('[€]','',regex=True).astype(float)
    prices = df.set_index('Code').to_dict()['Price']

    #Fill shopping cart
    
    shopping_cart = scan(df['Code'].tolist())

    print (shopping_cart)

    total_price = checkout(shopping_cart,prices,discounts)

    print (f'Total amount to pay: {total_price:.2f}€. Have a nice day!')






if __name__ == '__main__':
    main()