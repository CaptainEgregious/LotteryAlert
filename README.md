# LotteryAlert
Small script to query the national and euromillions lottery and alert if the jackpoit is above a set limit

## Installing

Clone the git repo and install 

`mkvirtualenv lottery -p python3 && pip install -r requirements.txt`

The analyser runs on python 3

## Running
To run the lottery analyser, simply run using
```python lottery.py``` 

## Configuration

Configuration for this script exists in the lottery.yaml file. Included is a template yaml file for base config.

#### Lottery Extraction
This script expects to recieve the current webpage for the national lottery (UK) and euromillions lotteries and is configured to extract from only this source. Other lotteries can be loaded by editing the 
```python
def get_price(self):
```
function that exists within the Webpage Class.

#### Limits
The script assumes that the lottery jackpot will be collected in the order of millions, so a config jackpot value of 10 will alert on jackpots over 10 million.

#### Alerting
The script uses pushed.co to alert users. This requires the user to have created an account on pushed.co and to have created an App and Channel, both of which can be created within the free tier. The config requires the `app_key`, `app_secret`, and `target_alias` values which can be found in the channel page in the pushed.co dashboard
https://account.pushed.co/channels
