from iota import *
from random import SystemRandom
from requests.exceptions import ConnectionError

url = "http://210.240.162.109:14265"

depth = 3
min_weight_magniude = 16

def GenerateSeed():
    alphabet = u'9ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    generator = SystemRandom()
    seed = str(u''.join(generator.choice(alphabet) for _ in range(81)))
    return seed

api = Iota(url,GenerateSeed())

def NodeInfo():
    node_info = api.get_node_info()
    print("node_info:")
    print node_info

def GenerationAddress():
    address =  api.get_new_addresses(index=937)[u'addresses'][0]
    print ("Address:")
    print address
    return address



def SendTransfer(TheMessage,address):
    input_message = TheMessage
    api.send_transfer(
        depth=depth,
        transfers=[
                    ProposedTransaction(
                        address=Address(address),
                        value=0,
                        message=TryteString.from_string(str(input_message))
                    )
                ],
        min_weight_magnitude=min_weight_magniude,
        inputs=[Address(address, key_index=0, security_level=0)]
    )

def GetTransactiuonsHash(address):
    transactions_hash = api.find_transactions(addresses = [address])[u'hashes'][-1]
    return transactions_hash

def GetBundleInfo(TranHash):
    bundle_deatil = api.get_bundles(TranHash)
    return bundle_deatil

def GetTrytes(address):
    transaction_trytes_raw = api.get_trytes(api.find_transactions(addresses=[address])[u'hashes'])['trytes'][0]    #format is TryteString
    transaction_trytes_split = TryteString(str(transaction_trytes_raw).split('99')[0])
    print transaction_trytes_split
    return transaction_trytes_split

def MessageDecode(TrytesSplit):
    transaction_string = TrytesSplit.decode()
    return transaction_string


try:

    #NodeInfo()
    address = GenerationAddress()
    n = raw_input("Input your message:")
    SendTransfer(n,address)
    TransactiuonsHash = GetTransactiuonsHash(address)
    bundle_deatil = GetBundleInfo(TransactiuonsHash)
    Message = MessageDecode(GetTrytes(address))


    
except ConnectionError as e:
    print("Connection Error: {e}".format(e=e))
except BadApiResponse as e:
    print("Bad Api: {e}".format(e=e))
else:
    print("Transfer Success")
    print("TransactiuonsHash:")
    print(TransactiuonsHash)
    print("Decode Message:")
    print(Message)

