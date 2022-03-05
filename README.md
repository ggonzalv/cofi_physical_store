# Project: Cofi Physical store

## How to run the code

The code can be run executing the simple command:

```
python main.py
```

It accepts the following parameters:

```--config```: path to the configuration file. Default is *config/config.ini*

```--products```: path to the products database file. Default is *products.json*

```--tests```: Execute several tests to check the performance of the scripts and exit.


This code includes five main functions:

```readConfig``` reads the configuration file, which includes the information on possible discounts.

```perform_tests``` performs several tests using different random template samples for the user to check if the software works properly. 

 ```WelcomeMessage``` initializes the interaction with the interface, displaying the products in the catalogue and possible discount offers.

```scan``` allows the user to add different products to its shopping cart. It takes two mandatory arguments, the code of the product (specified by the user, not case sensitive) and the shopping cart, which is updated with each new product. It accepts one optional argument, the number of units of the considered product (specified by the user, if not specified the default value is 1)

```total``` calculates the final price, taking into account the shopping cart, the price of each product and the possible discounts.

## How to include products in the catalogue

The file ```products.json``` includes all products in the catalogue. Each product contains an identification *Code*, the *Name* of the product and its *Price*

## How to manage discounts

Discounts are handled by the ```Discounts``` class, defined inside the ```lib/utils.py``` script. The configuration file ```config/config.ini``` contains the configuration of the possible discounts so that you do not need to touch the script if you are not familiarised. There are three possible discounts:

*two_for_one* (list): Each element within this list is considered for a two for one discount.

*bulk* (list of tuples): Each element within this list contains a tuple. The first item in the tuple is the name of the product, and the second item is the price of the item. This is applicable if the user buys 3 or more units of the considered product.

*swag* (list of tuples): Each element within this list contains a tuple. The first item in the tuple is a list which contains the names of the products affected by this discount. If the user selects one item of each element within the list, then a special price is applied for the three items together. The price is specified in the second element of the tuple. 

Finally, the parameter *order* allows the user to specify the order in which each discount is applied. Default is swag, bulk and then two_for_one.