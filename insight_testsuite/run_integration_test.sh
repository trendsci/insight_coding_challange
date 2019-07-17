#!/bin/bash
#
# Run test to check entire ./src/purchase_analytics.py code for correct output.

cd ..
python -m unittest discover -s ./insight_testsuite/tests/test_integration_1/