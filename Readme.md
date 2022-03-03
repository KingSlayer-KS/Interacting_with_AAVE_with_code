In this project we will not be deploying any projects as all the projects are 
already deployed, So we will just communicate with then and perform folowing 
opperations:
1. Depositing Some ETH as colletral
2. Borrowing that asset on behalf of the colletral
    1. Sell the borrowed asset, this method is called short selling.
3. Repay the borrowed asset in full. 

Step-1:lets Analyse the deposit function, we see that initally the Kovan ETH is converted to WETH(ERC20_Version_of_ETH).Now in our interface we will copy-paste  the contract converion from ETH -> WETH. 

Step-2: we will make a yaml file and add nesseary configrations.Now we need to figure out how to test the scripts on alocal net, here we need not to deploy any mocks as oracles are not in use but if one deem to tinker with it one can surely can. So for local testing we will be using Mainnet-Fork. After that we will fetch some WETH if the active network is mainnet-fork(local) 

Step-4: Now we will deposit some WETH in the AAVE. For reference we will use the lending pool page on ther aave documentation. Heres the tricky part the address for the lending pool for each market(network) is diffferent so we need to add the contract that fetches the address to our intefaces which is also given in the lending pool page under address provider and from there the function we will use is 'getLendingPool()' to get the add res of the pool.

Step-5:Now we will add the address for the contract that will fetch us the addres for the lending_pool, select your network thn copy the address from the 'LendingPoolAddressesProvider'. Sounds Confusing IK. Now paste the address in the YAML file. Complete the get_lending_pool() function.

Step-6:Now we got the addres for the desired pool we need the interface for that address whic we will copy from the documntation and paste it in the interfaces.We need to make some chande in the impot statmen and add those remapping in YAML file, complete the lenging pool function.

Step-7:Address sorted out, we nees to approve the ERC-20 token(WETH) so that the deposit is performed. For that we will cretea different function, before that we will copy-pate an interface standard from github. Now complete the function till apploving.

Step-8:Now we need to deposit the colletral. we will use the "deposit" function form the 'ILendingPool interface'or the 'get_lending_pool()' function