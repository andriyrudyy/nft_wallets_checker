###
### arudyy  2024/11/12
### twitter: https://x.com/_arudyy
### telegram: https://t.me/nftandmore
### git: https://github.com/andriyrudyy/nft_wallets_checker
###

import cloudscraper
import json
import argparse
import os

VER = '1.0'

def ordinals(wallets, collection):
	for wallet in wallets:
		url = 'https://api-mainnet.magiceden.io/v2/ord/launchpad/limits?collectionSymbol=' + collection + '&buyerAddress=' + wallet;

		scraper = cloudscraper.create_scraper()		
		data_text = scraper.get(url).text
		data = json.loads(data_text)
		if (len(data) == 0 ):
			print(data_text + ' - ' + wallet)
			continue
		if (len(data) == 1 ):
			print('\033[92m' + data_text + ' - ' + wallet + '\033[0m')
		else:
			found = False
			for element in data[:-1]:
				if (element['limit'] > 0):
					found = True
					break

			if (found):
				print('\033[92m' + data_text + ' - ' + wallet + '\033[0m')
			else:
				if (data[-1]['limit'] > 0):
					print('\033[94m' + data_text + ' - ' + wallet + '\033[0m')
				else:
					print('[Not allowed] - ' + wallet)


def ape(wallets, collection):
	for wallet in wallets:
		url = 'https://api-mainnet.magiceden.io/launchpads/' + collection + '?account=' + wallet;
		scraper = cloudscraper.create_scraper()		
		data_text = scraper.get(url).text
		data = json.loads(data_text)

		if (len(data) == 0 ):
			print('[No info] - ' + wallet)
			continue

		if (len(data) == 1 ):
			print('\033[92m' + '[It\'s just one phase] - ' + wallet + '\033[0m')
		else:
			found = False
			for element in data['evm']['stages'][:-1]:
				phase = element['displayName']
				walletLimit = element['walletLimit']
				eligible = element['eligible']

				if (eligible == True):
					found = True
					break

			if (found):
				print('\033[92m' + f'[{phase}] - {walletLimit} per wallet' + ' - ' + wallet + '\033[0m')
			else:
				phase = data['evm']['stages'][-1]['displayName']
				walletLimit = data['evm']['stages'][-1]['walletLimit']
				eligible = data['evm']['stages'][-1]['eligible']
				if (eligible == True):
					print('\033[94m' + f'[{phase}] - {walletLimit} per wallet' + ' - ' + wallet + '\033[0m')
				else:
					print('[Not allowed] - ' + wallet)

def main():
	print(f'ME Wallet checker {VER}')

	wallets = []

	parser = argparse.ArgumentParser(description='Commands list')
	parser.add_argument('-b', type=str, help='Blockchain [bitcoin/ape]')	
	parser.add_argument('-c', type=str, help='Collection/collections')
	parser.add_argument('-f', type=str, help='Wallets list. Default are "taproot.txt" for Bitcoin, "evm.txt" for APE')
	args = parser.parse_args()

	if (args.b == None and (args.b != 'bitcoin' or args.b != 'ape')):
		print('Incorrect blockhain parameter')
		exit()

	if (args.c == None or args.c == ''):
		print('Incorrect collection name(s)')
		exit()


	wallets_file = ''
	if (args.b == 'bitcoin'):
		if (args.f == None):
			wallets_file = 'taproot.txt'
		else:
			wallets_file = args.f

	if (args.b == 'ape'):
		if (args.f == None):
			wallets_file = 'evm.txt'
		else:
			wallets_file = args.f		

	if (not os.path.isfile('./'+wallets_file)):
		print('File not exist')
		exit()

	with open(wallets_file, 'r', encoding='utf-8') as file:
	    wallets = file.readlines()
	wallets = [line.strip() for line in wallets]

	collections = args.c.split(',')
	for collection in collections:
		print(f'Checking WL for {collection}')
		if (args.b == 'bitcoin'):
			ordinals(wallets, collection)
		if (args.b == 'ape'):
			ape(wallets, collection)			
		print('')

if __name__ == '__main__':
    main()