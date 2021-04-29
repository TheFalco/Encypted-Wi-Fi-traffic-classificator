# Encypted Wi-Fi traffic classificator
This project aims to design a software able to classify Wi-Fi encrypted traffic, using _Pyshark_ for analyze online and offline traffic.  
The classification is performed with respect to a trained model.  

# Collaborators
The project was developed by [Matteo Falconi](https://github.com/TheFalco) and [Mattia Iamundo](https://github.com/MattiaIamundo) as part of the Wireless Internet course at [Politecnico di Milano](https://www.polimi.it "Learn more about Politecnico di Milano").

# Requirements
A list of requirements is available [here](requirements.txt).

# Usage
It is possible to train the model, perform offline classification and performe online classification.

## Training
It is possible to configure the training data, specifing in the [input_data.json](input_data.json) file the MAC addresses of the Station and of the Access Point and the training set.
The training set should be already prepared: with only _DATA_ packets filtered, and should be placed in the _/training_captures_ folder.

In order to create your own trained model, delete the _trained_model.sav_ file in the _/learner_ folder
## Offline classification
Perform classification over a _.pcapng_ file: 
```
python main.py -type 0 -f filepath -sta Station_MAC_Address -ap AccessPoint_MAC_Address 
```
MAC addresses should be in the form XX:XX:XX:XX:XX:XX
## Online classification
Perform classification over packets captured live in monitor mode:
```
python main.py -type 1 -i interface -sta Station_MAC_Address -ap AccessPoint_MAC_Address  
```
MAC addresses should be in the form XX:XX:XX:XX:XX:XX  
Interface should be eth0, wlan0 ecc.
