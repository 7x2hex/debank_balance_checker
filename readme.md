# Debank Wallet Balance Checker

This tool checks the balance of multiple wallets using Debank's API and saves the results to a file.

## Installation

### 1. Clone the repository:

```bash
git clone https://github.com/7x2hex/debank_balance_checker.git
cd debank_balance_checker
```

### 2. Install the required dependencies:

 ```bash
pip install -r requirements.txt
playwright install
```

## Usage

### Through Command Line

To run the script from the command line simply put your wallets into wallets.txt, 
run script by command near. Results will appear in balances.txt. 
Also you can define threads number by `max_threads` argument.
```bash
python main.py --max_threads 10
```

Or you can set your own path for input / output files
```bash
python main.py -wallets path/to/wallets.txt -output path/to/balances.txt --max_threads 10
```

## Output example
```
0x0edefa91e99da1eddd1372c1743a63b1595fc413 | TOTAL: 1,350,391.08$ | TOKENS: 34,463.18$ | PROJECTS: 1,315,927.90$
0x7bfee91193d9df2ac0bfe90191d40f23c773c060 | TOTAL: 30,959,806.13$ | TOKENS: 2,707,417.38$ | PROJECTS: 28,252,388.75$
```