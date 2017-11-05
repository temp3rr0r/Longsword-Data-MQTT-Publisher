# LongswordStances

## Installation

Packages:
```
sudo apt-get update -y && apt-get upgrade -y && apt-get dist-upgrade -y
sudo apt-get install python python-pip glib-2.0-dev libbluetooth-dev libreadline-dev libboost-python-dev pkg-config libboost-python-dev libboost-thread-dev libglib2.0-dev python-dev libblas-dev liblapack-dev -y
```

Pip:
```
sudo pip install AWSIoTPythonSDK gattlib scikit-learn scipy numpy sklearn h5py Pillow Theano TensorFlow
```

Source code samples
```
sudo git clone https://github.com/aws/aws-iot-device-sdk-python.git
cd aws-iot-device-sdk-python/samples
python basicPubSub.py -e <endpoint> -r <rootCAFilePath> -c <certFilePath> -k <privateKeyFilePath>
```
