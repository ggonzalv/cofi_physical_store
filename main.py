#Import necessary libraries
import pandas as pd
from optparse import OptionParser
from utils import Discounts

#Print information about products and discounts
def WelcomeMessage(products,discounts):
    print (f"\nWelcome to Cofi Physical store!! This is our list of products:\n {products}\n")
    discounts.print_offers()

#Scan different input items
def scan(item,shopping_cart,nunits=1):
    shopping_cart[item] += nunits


#Calculate total price, after applying the discounts
def total(purchase,prices,discounts):
    
    total = 0

    #Apply discounts. Elements which have a discount applied are removed from the shopping cart
    for disc in discounts.order:
        money,purchase = getattr(discounts, disc)(purchase,prices)
        total += money

    #Add remaining items, with regular prices
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
    shopping_cart = {prod: 0 for prod in df['Code'].values} #Initialise shopping cart
    continue_purchase = True
    while continue_purchase:
        item = input('\nSpecify your product. Type nothing to proceed to checkout\n').upper()
        if item == '': continue_purchase = False
        elif item not in df['Code'].values:
            print ("This product is not present in the catalogue. Try again")
        else:
            nunits = input('Specify number of units. If no positive integer value is selected will add one.\n')
            if nunits.isdigit(): 
                nunits =  int(nunits)
                scan(item,shopping_cart,nunits)
            else:
                scan(item,shopping_cart)

    print (f'Your shopping cart contains {shopping_cart}. Proceeding to checkout')

    #Calculate total price
    total_price = total(shopping_cart,prices,discounts)
    print (f'Total amount to pay: {total_price:.2f}€. Have a nice day!')






if __name__ == '__main__':
    main()