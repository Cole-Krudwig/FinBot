# FinBot

FinBot is a project to automate equity and market research tasks. The current functionality is finbot_media.py which handles the reading, summarizing, analyzing recent news from Yahoo Finance.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Requirements](#requirements)
- [Features](#features)
- [Author](#author)

## Installation

To install FinBot Media, clone the repository and set up the environment:

```bash
git clone https://github.com/Cole-Krudwig/FinBot.git
cd FinBot
conda create -n finbot python=3.12
conda activate finbot
pip install -r requirements.txt
```

## Usage

After installation, you can use the finbot command-line tool to analyze a stock ticker symbol. For example:

```bash
finbot analyze <ticker>
```

## Requirements

- Python 3.12 or higher
- Dependencies specified in `requirements.txt`

## Features

- **News Fetching:** Retrieves recent news articles related to a specified stock ticker.
- **Summarization:** Summarizes fetched news articles to extract key information.
- **Sentiment Analysis:** Analyzes the sentiment of summarized content to provide insights.
- **CLI Interface:** Simple command-line interface for easy interaction.

## Author

**Cole J. Krudwig**