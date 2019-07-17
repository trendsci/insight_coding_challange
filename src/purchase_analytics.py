from __future__ import print_function
import sys

def write_output(file_object,data):
        file_object.write(data)

def parse_filenames():
    """Get file names for input files containing orders and product_listings,
       and output file with analysis results.
       
       return order_file_path, products_file_path, output_file_path
    """
    try:
        order_file_path = sys.argv[1]
        products_file_path = sys.argv[2]
        output_file_path = sys.argv[3]     
    except Exception as e:
        print(e)
    
    return order_file_path, products_file_path, output_file_path

def create_output_file(output_file_path):
    """ Create output file with correct headers """
    with open(output_file_path, 'w') as f:
        write_output(f,"department_id,number_of_orders,number_of_first_orders,percentage\n")
        
        
def sort_and_write_output_file(department_counts_dict, output_file_path):
    """ sort department_counts_dict based on department_id and write the data to file """
    for department_id in sorted(department_counts_dict):
        data = department_counts_dict[department_id]
        to_write = "{},{},{},{}\n".format(department_id, data[0],data[1],data[2])
        try:
            with open(output_file_path, 'a+') as output_file:
                #output_file.write(to_write)
                write_output(output_file,to_write)
        except Exception as e:
            print(e)
        
def get_products_dict(file_path):
    """
    Parses the products file into a dictionary:
    
    Source products*.csv file format:
     product_id,product_name,aisle_id,department_id
     type:
     int, string, int, int
     example:
     1,Chocolate Sandwich Cookies,61,19
    
    Products entries formatted incorrectly are skipped.
    
    return product_id_dict {product_id : [product_name, aisle_id, department_id]}
    """
    product_id_dict = {}
    try:
        with open(file_path, 'r') as product_file:
            next(product_file) # skip header
            
            for product in product_file:
                # Try to get product info.
                # If invalid entry, print error and move to next product.
                try:
                    # Split product into: [product_id, product_name, aisle_id, department_id]
                    product_split_line = product.strip().split(',')
                    # Add product to product dictionary. 
                    # {key = int(product_id): value = [product_name, aisle_id, department_id]}
                    product_id_dict[int(product_split_line[0])] = product_split_line[1:]
                except Exception as e:
                    print(e)
                    
    except Exception as e:
        print(e)
    return product_id_dict


def count_orders_per_deparment_id(product_id_dict, order_file_path, output_file_path):
    """
    Takes product_id_dict, orders file path, and output file path.
    
    product_id_dict format:
    {product_id : [product_name, aisle_id, department_id]}
    
    order_file_path points to a csv file with format:
    order_id,product_id,add_to_cart_order,reordered
    """
    # department_counts_dict to contain order information for each department_id, format:
    # {department_id: [number_of_orders,number_of_first_orders,percentage_of_new_orders]}
    department_counts_dict = {}
    try:
        # Begin processing orders
        with open(order_file_path, 'r') as order_file:
            next(order_file) # skip header
            for order in order_file:
                # Get information about current order
                order_id, product_id, add_to_cart_order, reordered_flag = order.strip().split(',')
                product_id = int(product_id)
                reordered_flag = int(reordered_flag)
                # Check if this is a re-order of product
                # Data source has reordered_flag: 1 = reordered, 0 = new order
                # We are counting how many new orders there are so:
                # Make new_order_flag: 1 = new order, 0 = reordered;
                # If confident that reorder_flag is always 1 or 0 can use a shorter code:
                # new_order_flag = 1-int(reordered_flag)
                if reordered_flag == 1:
                    new_order_flag = 0
                elif reordered_flag == 0:
                    new_order_flag = 1
                else:
                    raise ValueError("Reorder flag can only be 1 or 0, but found flag = {}".format(reordered_flag))
                
                try:
                    # Get product listing of product_id in currently processed order
                    product_listing = product_id_dict[product_id]
                    # Get department_id from product listing, department_id is the last value
                    department_id = int(product_listing[-1])
                    try:                        
                        # Check if we have seen this department already
                        if department_id in department_counts_dict:
                            # increment number of orders in department by 1
                            department_counts_dict[department_id][0] += 1
                            # increment number of NEW orders in department by 1
                            department_counts_dict[department_id][1] += new_order_flag
                            
                        # Create new department if we haven't encountered it yet
                        else:      
                            # set number of orders in deparment to 1 
                            # and reorders to new_order_flag of current product
                            department_counts_dict[department_id] = [1,new_order_flag]
                            
                    except Exception as e:
                        print(e)
                except Exception as e:
                    print(e)
        
        # Calculate percent new orders:
        for department_id in department_counts_dict:
            percentage_new_orders = "{:.2f}".format(
            round(float(department_counts_dict[department_id][-1])/department_counts_dict[department_id][-2],2))
            department_counts_dict[department_id].append(percentage_new_orders)
        
        return department_counts_dict
                   
    except Exception as e:
        print(e)
 
def run_analysis():
    """
    This script analyzes the 2017 Instacard data and 
    returns a csv file that lists how many times a product was ordered from each deparment,
    how many of these orders were a first-time order, and percentage of reorders.
    
    Instracart 2017 data available here:
    https://www.instacart.com/datasets/grocery-shopping-2017
    
    Data format is specified here:
    https://gist.github.com/jeremystan/c3b39d947d9b88b3ccff3147dbcf6c6b
    
    Original Insight instructions:
    https://github.com/InsightDataScience/Purchase-Analytics  
    """
    # Get file paths from command line or can predefine in script.
    order_file_path, products_file_path, output_file_path = parse_filenames()
    
    # Create output file with headers
    create_output_file(output_file_path)
    
    # Get dictionary with product_id key and value of [product_name, aisle_id, department_id]
    product_dict = get_products_dict(products_file_path)
    
    # Run analysis script
    department_counts_dict = count_orders_per_deparment_id(
        product_dict, order_file_path=order_file_path, output_file_path=output_file_path)
    
    # Sort analysis results and write output file
    sort_and_write_output_file(department_counts_dict,output_file_path)
    
if __name__ == "__main__":
    run_analysis()
   