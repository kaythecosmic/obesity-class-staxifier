echo "Building the project..."

python3.9 --version
python3.9 -m pip --version
cat requirements.txt
python3.9 -m pip install -r requirements.txt
python3.9 manage.py collectstatic