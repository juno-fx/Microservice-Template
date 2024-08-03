coverage run -m pytest -x -vvv --durations=5 --color=yes tests/ -W ignore::DeprecationWarning
cov_exit_code=$?

coverage report -m
coverage html > /dev/null
zip -r htmlcov.zip htmlcov > /dev/null
curl -XPOST -F 'data=@htmlcov.zip' repo:3000/upload?key=CI > /dev/null
coverage report -m > /dev/null

test_exit_code=$?
exit_code=$((cov_exit_code + test_exit_code))

echo "Coverage exit code: $cov_exit_code"
echo "Test exit code: $test_exit_code"
echo "Exit code: $exit_code"

exit "$exit_code"