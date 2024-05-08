echo "Building the project..."

PYTHON_VERSION="3.9"
# apt update
apt install -y python${PYTHON_VERSION} python${PYTHON_VERSION}-dev python${PYTHON_VERSION}-distutils
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
python${PYTHON_VERSION} get-pip.py
python3.9 -m pip install -r requirements.txt
python3.9 manage.py collectstatic