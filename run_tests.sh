echo "Testing utility module..."
python3.9 -m unittest discover -s ./tests/
echo "Testing pysatmc module..."
python3.9 -m unittest discover -s ./tests/test_pysatmc/
echo "Testing space module..."
python3.9 -m unittest discover -s ./tests/test_space/
echo "Testing function module..."
python3.9 -m unittest discover -s ./tests/test_function/
echo "Testing algorithm module..."
python3.9 -m unittest discover -s ./tests/test_algorithm/
echo "Testing core module..."
python3.9 -m unittest discover -s ./tests/test_core/