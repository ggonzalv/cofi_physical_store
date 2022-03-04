# Project: Cofi Physical store

## How to run the code

The code can be run executing the simple command:

```
python main.py
```

This code includes three main functions:

 ```WelcomeMessage``` initializes the interaction with the interface, displaying the products in the catalogue and possible discount offers.

```scan``` allows the user to add different products to its shopping cart. It takes two arguments, the code of the product (mandatory, not case sensitive) and the number of units (options, if not specified the default value is 1)

```total``` calculates the final price, taking into account the shopping cart and the possible discounts.

## How to include products in the catalogue

The file ```products.json``` includes all products in the catalogue. Each product contains an identification *Code*, the *Name* of the product and its *Price*

## How to manage discounts

Discounts are handled by the ```Discounts``` class, defined inside the ```utils.py``` script. There are three possible discounts:

*two_for_one* (list): Each element within this list is considered for a two for one discount.

*bulk* (list of tuples): Each element within this list contains a tuple. The first item is the name of the product, and the second item is the price of the item if the user buys 3 or more units of the considered product.

*swag* (list of tuples): Each element within this list contains a tuple. The first item is a list which contains the names of the products affected by this discount. If the user selects one item of each element within the list, then a special price is applied for the three items together, as specified in the second element of the tuple. 

The self parameter *order* allows the user to specify the order in which each discount is applied

All new discounts can be handled inside the ```__init__``` function within the ```Discounts``` class. Then, specific functions within the ```Discounts``` class apply the associated discounts if applicable.