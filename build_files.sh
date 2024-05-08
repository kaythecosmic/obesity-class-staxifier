echo "Building the project..."

curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
python3.9 get-pip.py
chmod +x install_pip.sh
./install_pip.sh
python3.9 -m pip install -r requirements.txt
python3.9 manage.py collectstatic