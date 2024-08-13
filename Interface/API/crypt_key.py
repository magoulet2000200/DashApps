import pyAesCrypt
import os
import pickle

# data and access for crypted file
BUFFER_SIZE = 124 * 1024
PASSWORD = '$anuv0x2018'


def get_secret_id_key(client, password=PASSWORD):
    """
    decrypt and fetch the client_id and secret_id for the API credential
    :return: pandas dataframe that containt the client_id and secret_id
    """
    cwd = os.getcwd()
    os.chdir(os.path.dirname(__file__))
#    if os.getcwd()
    pyAesCrypt.decryptFile('data/api_key.aes', 'data/api_key.pkl', password,
                           BUFFER_SIZE)
    # df = pd.read_pickle('data/api_key.pkl')
    with open('data/api_key.pkl', 'rb') as handle:
        data = pickle.load(handle)
    os.remove('data/api_key.pkl')
    os.chdir(cwd)
    print()
    return data[client]


def encrypt(data, fn, password=PASSWORD):
    """
    Encrypt any kind of data in an AES file.
    Call one time to create the encrypted file.
    :param data: Data string to encrypt
    :param fn: file name with filepath if necessary
    :param password: password to encrypt the file
    :return: None
    """
    fnpkl = fn + '.pkl'
    fnaes = fn + '.aes'
    
    with open(fnpkl, 'wb') as handle:
        pickle.dump(data, handle, protocol=pickle.HIGHEST_PROTOCOL)
    
    pyAesCrypt.encryptFile(fnpkl, fnaes, password, BUFFER_SIZE)
    os.remove(fnpkl)


def decrypt(fn, password=PASSWORD):
    """
    Decrypt an AES file and read the retreive the information.
    Call to read a encrypted file.
    :param fn: file name with filepath if necessary
    :param password: password to decrypt the file
    :return: decrypted data
    """
    fnpkl = fn + '.pkl'
    fnaes = fn + '.aes'
    pyAesCrypt.decryptFile(fnaes, fnpkl, password, BUFFER_SIZE)
    data = None
    with open(fnpkl, 'rb') as input:
        data = pickle.load(input)
    os.remove(fnpkl)
    return data
