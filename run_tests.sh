echo "Testing utility module..."
python -m unittest discover -s ./tests/
echo "Testing pysatmc module..."
python -m unittest discover -s ./tests/test_pysatmc/
echo "Testing space module..."
python -m unittest discover -s ./tests/test_space/
echo "Testing function module..."
python -m unittest discover -s ./tests/test_function/
echo "Testing algorithm module..."
python -m unittest discover -s ./tests/test_algorithm/
echo "Testing core module..."
python -m unittest discover -s ./tests/test_core/