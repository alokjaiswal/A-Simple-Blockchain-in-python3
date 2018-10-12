# -*- coding: utf-8 -*-
"""
@author: Alok .S. Jaiswal
"""


import hashlib

coinbase = 'coinbase'
a = []
blockchain = []
userLedger = []
unconfirm_pool = []
confirm_pool = []
public_key = []
hashtab = []
transaction_Ledger = []
index = 0

# input_after_verification function checks wheather the transaction is verified and then inputs the transaction in to blockchain ledger

def input_after_verfication(lis):
    global blockchain
    global index
    if(blockchain.__len__() == 0):  #conditional Statement to create blockchain
        blockchain.append({'prev_hash':'0', 'nonce':0,'merkle_root':0, 'trans':[]})
        blockchain[index]['trans'].append([lis[0], lis[1], lis[2]])
    else:
        blockchain[index]['trans'].append([lis[0], lis[1], lis[2]])
        
lis = ['system', 'coinbase', 100] #inital ISO for our token
confirm_pool.append(lis)
input_after_verfication(lis)


#function returns hash of the previous latest block of the blockchain ledger
def prev_hash():
    return blockchain[index-1]['prev_hash']

#function returns Balance of the user invoking it
def check_Balance(lis):    
    global blockchain
    x=0                      # checks the balance of the particular account
    y=0
    spent=0
    recieved=0
    if check_user(lis):
        while (x < blockchain.__len__()) :
            while y<blockchain[x]['trans'].__len__():
                if lis == blockchain[x]['trans'][y][0]:
                    spent = spent + blockchain[x]['trans'][y][2]
                if lis == blockchain[x]['trans'][y][1]:
                    recieved = recieved + blockchain[x]['trans'][y][2]
                y = y + 1
            y = 0
            x = x + 1
        print('balance of ',end='')
        print(lis,end='')
        print(' :' + str(recieved-spent))
        return (recieved-spent)
    else:
        print("unknown user.....")
   

#function verifies the transaction and if verified pushes the transaction into the confirmed pool to be inserted in  the blockchain ledger
def verify_transaction(unconfirm_pool):
    global confirm_pool
    global index
    for x in range(unconfirm_pool.__len__()):
        if (unconfirm_pool[x][0] == 'coinbase' or unconfirm_pool[x][1] == 'coinbase'):
            print("You are not allowed to use this username ")
        else:
            if((check_user(unconfirm_pool[x][0])) and (check_user(unconfirm_pool[x][1]))):
            
                if unconfirm_pool[x][2] > 0:
                    if ((check_Balance(unconfirm_pool[x][0])>=unconfirm_pool[x][2])):
                        confirm_pool.append(unconfirm_pool[x])
                        transaction_Ledger.append(unconfirm_pool[x])
                        input_after_verfication(confirm_pool[confirm_pool.__len__()-1])           #verifies transaction(sufficient balance)
                    else:
                        print('Insufficient balance....')
                else:
                    print("Please enter a positive amount to be transfered")
    if(confirm_pool.__len__()>0):
        mine_block(confirm_pool)
    confirm_pool = []


#function mines the block once there are 5 transaction ready to be entered into the blockchain 
#Difficulty is currently set to 2 and can be changed as desired
def mine_block(confirm_pool):
    global index
    blockchain.append({'prev_hash':'0', 'nonce':0, 'merkle_root':0, 'trans':[]})
    blockchain[index]['merkle_root'] = merkle_root(confirm_pool)
    if(hashtab.__len__()!=0):
        blockchain[index]['prev_hash']=hashtab[(hashtab.__len__())-1]
    else:
        blockchain[index]['prev_hash']=0
    nonce_str = blockchain[index]['merkle_root'] + str(blockchain[index]['prev_hash'])
    nonce_str = hashlib.sha256(nonce_str.encode()).hexdigest()
    f = 'jhkbfjksdbfjksdbfnkjsdnfsdf'
    nonce = 0
    while f[0:2]!='00':
        f=nonce_str
        hashh = hashlib.sha256()
        hashh.update((f+str(nonce)).encode())
        nonce = nonce + 1
        f = hashh.hexdigest()
    blockchain[index]['nonce'] = nonce
    print('Mining complete nonce value is :'+ str(blockchain[index]['nonce']))
    hashtab.append(f)
    index = index + 1
    

#function returns the root hash of the transaction after computing through the merkle root 
def merkle_root(confirm_array):
    arr = []
    for p in range(confirm_array.__len__()):
        arr.append(hashlib.sha256(str(confirm_array[p][0]+confirm_array[p][1]+str(confirm_array[p][2])).encode()).hexdigest())    
    x = 0
    while(arr.__len__()>1):
        i = 0 
        y = 0
        while(x <arr.__len__()):
            if(((x+1)<arr.__len__())):
                arr[x] = hashlib.sha256((arr[x]+arr[x+1]).encode()).hexdigest()
                x = x + 2

            elif ( arr[x]!=None and (x<arr.__len__())):
                x = x + 1      
        
        while(i<arr.__len__()):
            arr[y] = arr[i]
            i = i + 2
            y = y + 1       
        x = (x+1) / 2
        x = x - (x %1)
        l = arr.__len__()
        while(x<l):
            arr.pop()
            x = x + 1
        x = 0
        
    return(arr[0])
    
                                   
    
#function is used to do the transaction arguments passed is from , to account and amount to be transfered
def transaction(sender,reciever,amount):
    global unconfirm_pool
    global confirm_pool
    lis = [sender,reciever,amount]
    a = 0
    if((unconfirm_pool.__len__() + confirm_pool.__len__() + blockchain[index]['trans'].__len__())<=5):
        a=(unconfirm_pool.__len__() + confirm_pool.__len__() + blockchain[index]['trans'].__len__())
        unconfirm_pool.append(lis)
        print(unconfirm_pool)
        print('          ' + str(unconfirm_pool.__len__()))
        if(a==5):
            verify_transaction(unconfirm_pool)
            unconfirm_pool = []
    
    
#function checks wheather the user is already present in the userLedger or not
def check_user(name) :
    global userLedger
    t = 0
    u = 0
    while t<userLedger.__len__() :
        if(name == userLedger[t]):
            u = u + 1
        t = t + 1
    if u > 0 or name == 'system':
        return 1
    else:
        return 0
        
        
    
#function is used to create new user to the framework
def new_user(name):
    global userLedger
    global confirm_pool
    if not(check_user(name)):
        if name == 'coinbase':
            print('sry,  You cannot use this username')
        userLedger.append(name)
        l = [coinbase,name,5]
        input_after_verfication(l)
    else:
        print('User already exists..')
userLedger = ['coinbase']
    

#function returns the string qwuivalent of the block given as input
def block_str(nos):
    global blockchain
    str_data = ""
    str_data = str_data + str('blockchain') + str('[')
    for i in range(blockchain.__len__()):
        str_data = str_data + '{' + blockchain[i]['prev_hash'] + str(blockchain[i]['nonce'])
        for j in range(blockchain[i]['trans'].__len__()):
            for k in range(3):
                str_data = str_data + str(blockchain[i]['trans'][j][k]) + str(' ')
        str_data = str_data + '}'
    str_data = str_data + ']'
    return str_data
    

#function returns all the transaction sent or recieved from or to that user
def query_transaction(name):
    x = 0
    y = 0
    while (x < blockchain.__len__()) :
            while y<blockchain[x]['trans'].__len__():
                if name == blockchain[x]['trans'][y][0]:
                    print(blockchain[x]['trans'][y])
                if name == blockchain[x]['trans'][y][1]:
                    print(blockchain[x]['trans'][y])
                y = y + 1
            y = 0
            x = x + 1 


#this is to have a runtime interaction which blockchain
def runtime():
    inputt = '0'
    while(inputt!='exit'):
        inputt = input()
        if(inputt == 'transaction'):
            sender = input()
            reciever = input()
            amount = input()
            amount = int(amount)
            transaction(sender,reciever,amount)
            
        elif(inputt == 'check_Balance'):
            person = input()
            check_Balance(person)
            print('check complete')
        elif(inputt == 'new_user'):
            person = input()
            new_user(person)
        elif(inputt == 'userLedger'):
            print(userLedger)
        elif(inputt == 'query_transaction'):
            person = input()
            query_transaction(person)
        elif(inputt== 'blockchain'):
            for x in range(blockchain.__len__()-1):
                print('Block Height :'+str(x+1))
                print('Block hash is : '+ hashtab[x])
                print(blockchain[x])
                print('===================================')
        elif(inputt == 'hashtab'):
            print("Block height   :        hashvalue")
            for x in range(hashtab.__len__()):
                print("     "+ str(x+1)+"         "+hashtab[x])
        






