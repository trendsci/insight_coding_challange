## analysis
from __future__ import print_function
import os, sys
    
def check_files(order_file_path,products_file_path,output_file_path):
    with open(output_file_path, 'w') as f:
        f.write("department_id,number_of_orders,number_of_first_orders,percentage\n")

def get_products_dict(file_path,verbose=0,print_error=1):
    product_id_dict = {}
    try:
        with open(file_path, 'r') as product_file:
            for product in product_file:
                
                product_split_line = product.strip().split(',')
                if verbose: print(product_split_line)
                try:
                    product_id_dict[int(product_split_line[0])] = product_split_line[1:]
                except Exception as e:
                    print(e)
                    #pass
        if verbose: print(product_id_dict)
    except Exception as e:
        if print_error: print(e)
    return product_id_dict


def assign_product_dept(product_dict, order_file_path, output_file_path, verbose=0,print_error=1):
    """
    This file does what? 
    """
    #department_order_dict format:
    #department_id, [number_of_orders,number_of_first_orders,percentage]
    department_order_dict = {}
    try:
        with open(order_file_path, 'r') as order_file:
            for order in order_file:
                if verbose: print (order)
                order_split_line = order.strip().split(',')
                if verbose: print (order_split_line)
                try:
                    dept = product_dict[int(order_split_line[1])]
                    department_id = int(dept[-1])

                    order_split_line.append(department_id)
                    if verbose: print(order_split_line)
                    try: #have we created this department already?
                        val = int(order_split_line[-2])
                        if department_id in department_order_dict:
                            if verbose: print("in {}. {}".format(department_id,val))
                            department_order_dict[department_id][0] += 1
                            department_order_dict[department_id][1] += 1-val
                        else:
                            
                            if verbose: print("not in {}. {}".format(department_id,val))
                            department_order_dict[department_id] = [1,1-val]
                    except Exception as e:
                        # remember to test/try to catch any non int new order flags.
                        if print_error: print(e)
                except Exception as e:
                    if print_error: print(e)
                        #pass
        #print(department_order_dict)
        
        # calculate % new orders:
        for key in department_order_dict:
            percentage_new_orders = round(float(department_order_dict[key][-1])/department_order_dict[key][-2],2)
            department_order_dict[key].append(percentage_new_orders)
        
        if verbose: print("department_id,number_of_orders,number_of_first_orders,percentage")
        for key in sorted(department_order_dict):
            data = department_order_dict[key]
            to_write = "{},{},{},{}\n".format(key, data[0],data[1],data[2])
            try:
                with open(output_file_path, 'a+') as output_file:
                    if verbose: print(to_write)
                    output_file.write(to_write)
            except Exception as e:
                print("No file yet")
                with open(output_file_path, 'w') as output_file:
                    output_file.write(to_write)
                
        return department_order_dict

    except Exception as e:
        print(e)



        
        
def main():

    # Set up file paths from command line or predefined in script.
    try:
        order_file_path = sys.argv[1]
    except:
        print("eeeeeeeeeeeee")
        order_file_path = "order_products.csv"
        #order_file_path = "Big\order_products__train.csv"
        #order_file_path = "Big\order_products__prior.csv"
        
    try:
        products_file_path = sys.argv[2]
    except:
        print("eeeeeeeeeeeee")
        products_file_path = "Big\products.csv" #"products.csv" 

    try:
        output_file_path = sys.argv[3]
        
    except:
        print("eeee")
        output_file_path = "output_file.csv"
    
    #os.chdir(r"C:\Users\Troti\Desktop\Insight\Coding\MainDirectory")
    
    check_files(order_file_path,products_file_path,output_file_path)
    
    product_dict = get_products_dict(products_file_path)
    
    assign_product_dept(product_dict,order_file_path=order_file_path,output_file_path=output_file_path)
    
    #raw_input("Program_Finished (ok?): ")


if __name__ == "__main__":
    main()
   