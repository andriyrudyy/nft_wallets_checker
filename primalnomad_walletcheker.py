###
### arudyy  2024/11/14
### twitter: https://x.com/_arudyy
### telegram: https://t.me/nftandmore
### git: https://github.com/andriyrudyy/nft_wallets_checker
###

import cloudscraper
import json
import argparse
import os

VER = '1.0'

def checker(wallets):
	for wallet in wallets:
		url = 'https://primalnomad.xyz/api/wallet/info/' + wallet;

		scraper = cloudscraper.create_scraper()		
		data_text = scraper.get(url).text

		if (data_text == 'not-registered'):
			print('[not-registered] - ' + wallet)
		else:
			if (data_text ==  'fcfs-found'):
				print('\033[93m' + data_text + ' - ' + wallet + '\033[0m')
			else:
				print('\033[92m' + data_text + ' - ' + wallet + '\033[0m')	



def main():
	print(f'Primal Nomad Wallet checker {VER}')

	wallets = []

	parser = argparse.ArgumentParser(description='Commands list')
	parser.add_argument('-f', type=str, help='Wallets list. Default are "taproot.txt" for Bitcoin, "evm.txt" for APE')
	args = parser.parse_args()


	wallets_file = ''
	if (args.f == None):
		wallets_file = 'taproot.txt'
	else:
		wallets_file = args.f

	if (not os.path.isfile('./'+wallets_file)):
		print('File not exist')
		exit()

	with open(wallets_file, 'r', encoding='utf-8') as file:
	    wallets = file.readlines()
	wallets = [line.strip() for line in wallets]

	checker(wallets)		
	print('')

if __name__ == '__main__':
    main()