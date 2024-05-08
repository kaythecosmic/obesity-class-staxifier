echo "Building the project..."

PYTHON_VERSION="3.12"
# apt update
apt install -y python${PYTHON_VERSION} python${PYTHON_VERSION}-dev python${PYTHON_VERSION}-distutils
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
python${PYTHON_VERSION} get-pip.py
echo "finished getting pip"
python${PYTHON_VERSION} -m pip install -r requirements.txt
echo "finished installing dependencies..."
python${PYTHON_VERSION} manage.py collectstatic