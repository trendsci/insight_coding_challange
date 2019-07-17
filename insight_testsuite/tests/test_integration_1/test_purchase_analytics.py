from __future__ import print_function
import unittest
from src import purchase_analytics 
import os


class Test_entire_script(unittest.TestCase):
    """
    Test ./src/purchase_analytics.py
    Input files in ./testing/test_files/
    Compare output from purchase_analytics in testing_output_file_name with reference testing_gold_output_file_name
    """
    # Define testing file paths
    testing_products_file_name = r".\insight_testsuite\tests\test_integration_1\input\test_products.csv"
    #testing_products_file_name = r".\testing\test_files\test_products_wrongformat.csv"
    testing_orders_file_name = r".\insight_testsuite\tests\test_integration_1\input\test_orders.csv"
    testing_gold_output_file_name = r".\insight_testsuite\tests\test_integration_1\input\test_gold_output.csv"
    testing_output_file_name = r".\insight_testsuite\tests\test_integration_1\output\report.csv"
    
    # Clear old data from the generated output file
    open(testing_output_file_name,"w").close()

    def parse_filenames(self):
        """ 
        Override default file paths in purchase_analytics script
        Provide testing input/output files
        """
        return self.testing_orders_file_name, self.testing_products_file_name, self.testing_output_file_name
        
    def test_correct_output(self):  
        """ Test output from purchase_analytics script
        """
        # Change input/output files to testing files specified above
        purchase_analytics.parse_filenames = self.parse_filenames
        purchase_analytics.run_analysis()
        
        # Compare generated output file with gold output file
        with open(self.testing_output_file_name,"r") as f1:
            with open(self.testing_gold_output_file_name,"r") as f2:
                self.assertEqual(f1.read().strip(),f2.read().strip())
                
    def test_correct_output(self):  
        """ Test output from purchase_analytics script
        """
        # Change input/output files to testing files specified above
        purchase_analytics.parse_filenames = self.parse_filenames
        purchase_analytics.run_analysis()
        
        # Compare generated output file with gold output file
        with open(self.testing_output_file_name,"r") as f1:
            with open(self.testing_gold_output_file_name,"r") as f2:
                self.assertEqual(f1.read().strip(),f2.read().strip())


if __name__ == '__main__':
    unittest.main()