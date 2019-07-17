# Insight coding challange - Submission by Sergey Shnitkind
Insight coding challenge - Instacart dataset

# Purcase analytics

Purchase analytics is a script that takes order and product information from the Instacard 2017 database 
and outputs a csv file with the number of orders per department, how many orders are new (not a re-order), 
and percentage of new orders from total orders.

    Instracart 2017 data available here:
    https://www.instacart.com/datasets/grocery-shopping-2017
    
    Data format is specified here:
    https://gist.github.com/jeremystan/c3b39d947d9b88b3ccff3147dbcf6c6b
    
    Original Insight instructions:
    https://github.com/InsightDataScience/Purchase-Analytics  

## Usage
Navigate to root directory (./insight_shnitkind/) and run run.sh or excecute the following:
```bash
python ./src/purchase_analytics.py ./input/order_products.csv ./input/products.csv ./output/report.csv
```

Program takes 3 arguments:
1. order information file location
2. product listing file location
3. desired output file location

## Testing
A simple test is provided that test the entire script for correct output. To excecute, navigate to root directory (./insight_shnitkind/) and run:
```bash
python -m unittest discover -s ./insight_testsuite/tests/test_integration_1/
```