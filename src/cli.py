'''
cli.py
Author: Cole J. Krudwig
'''

import argparse
import warnings
from finbot_media import FinBotMedia

def main():
    # Suppress specific warnings
    warnings.filterwarnings("ignore", message="The behavior of DataFrame concatenation with empty or all-NA entries is deprecated.", category=FutureWarning)
    warnings.filterwarnings("ignore", message="Your max_length is set to .*", category=UserWarning)

    parser = argparse.ArgumentParser(description='Financial report generation tool')
    parser.add_argument('command', help='Command to execute (analyze)')
    parser.add_argument('ticker', help='Stock ticker symbol')

    args = parser.parse_args()

    if args.command == 'analyze':
        bot = FinBotMedia(args.ticker)
        bot.fetch_news()
        bot.summarize_and_analyze()
        bot.display()
    else:
        print('Invalid command')

if __name__ == "__main__":
    main()