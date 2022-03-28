# CryptoToolbox

This is a project about cryptography. It is heavily inspired by the german YouTube-Channel Florian Dalwigk.

Because he publishes his videos to educate others,
this repository has the sole purpose of doing the same. Please read the file LICENSE for further details.  

## How to prepare:
You'll need to install the module "requests" for the class QRandom to get Data.

## How to use:
### using the code on its own:
You can just run main.py to get a text UI that helps you to run the different parts of the code. by entering numbers and answering the questions you can generate random numbers in a range of your choice. You can generate a password with a length of your choice from a charset the code generates according to your input. And finally the code is capable of encoding files with existing keyfiles or, if left empty, with a randomly generated keyfile.

### using the code in your own projects:
You can just copy the file qrandom.py into your own file, import it with ```from qrandom import QRandom``` and use it like you want. main.py acts as a tutorial to show you how to declare a QRandom-Object and get random Data from it. Just make sure to have "requests" installed whenever you want to include QRandom in your Project.

You can include file_encryption.py in your code too. Just be aware that it depends on qrandom.py so with this your Code will still need to have requests installed. Dhe code of file_encryption expects two files that are encoded (bitwise XOR) with each other, generating a third file. Each two files will result in the third file so with the original and the encrypted one you can simply recreate the keyfile.

Further explanations will be added as docstrings in later versions to make it easier for you to get the code working.
