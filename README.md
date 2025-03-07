# CSFloat Trade Summary

CSFloat Trade Summary is an application for fetching and providing a summary of the trades.

## Features

- Fetching trade data from the CSFloat API (only purchases at the moment);
- Display the summary of trades, including the total amount, average price, and the latest trade date for each user;
- Secure replacement of CSFloat session token.

## Installation

> [!IMPORTANT]
> In order to install this app you will need:
> - Python 3.7 or higher
> - pip (Python package installer)

### Step-by-Step Guide

1. **Clone the repository:**

    ```bat
    cd C:\"your desired installation path"
    git clone https://github.com/yourusername/csfloat_trade_summary.git
    cd csfloat_trade_summary
    ```

2. **Create a virtual environment:**

    ```bat
    python -m venv venv
    ```

3. **Activate the virtual environment:**

    - On Windows:

        ```bat
        venv\Scripts\activate
        ```

    - On macOS/Linux:

        ```bash
        source venv/bin/activate
        ```

4. **Install the required packages:**

    ```bat
    pip install -r requirements.txt
    ```

## Usage

1. **Run the application:**

    ```bat
    python main.py
    ```

2. **Follow the on-screen instructions to navigate through the menu:**

    - **Show summary:** Displays a summary of your trade data.
    - **Refresh data:** Fetches your latest trade data from the CSFloat API.
    - **Change session token:** Allows you to change the CSFloat session token.
    - **Exit:**

## License

This project is licensed under the MIT License. See the LICENSE file for details.
