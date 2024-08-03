
# Scamalytics IP Monitor

## Overview

The **Scamalytics IP Monitor** is a Python-based tool designed to check the fraud score of IP addresses using the Scamalytics API. It processes a list of IP addresses, retrieves their fraud scores, and categorizes them based on risk levels. The tool features real-time progress updates and organizes the results into separate folders based on the fraud score.

## Features

- Fetches fraud scores for IP addresses using the Scamalytics API.
- Categorizes IP addresses into risk levels: Over 50, Over 20, and Below 20.
- Logs errors and processing information.
- Utilizes multithreading for efficient processing.
- Displays a color-coded progress bar for real-time updates.

## Requirements

- Python 3.6+
- [`requests`](https://pypi.org/project/requests/) library
- [`tqdm`](https://tqdm.github.io/) library
- [`colorama`](https://pypi.org/project/colorama/) library

## Installation

1. **Clone the repository:**
    ```sh
    git clone https://github.com/Overdriven187/scamalytics-automated
    cd scamalytics-automated
    ```

2. **Install the required packages:**
    ```sh
    pip install -r requirements.txt
    ```

## Configuration

Update the configuration variables in `scamalytics.py`:

- **`api_user`**: Your Scamalytics API username.
- **`api_key`**: Your Scamalytics API key.
- **`check_interval`**: Time between checks (in seconds).
- **`max_workers`**: Number of threads for concurrent processing.

## Usage

1. **Prepare a file** containing the list of IP addresses to be checked, one per line.

2. **Run the script:**
    ```sh
    python scamalytics.py path_to_ip_list.txt
    ```

3. The script will process the IP addresses, fetch their fraud scores, and categorize them based on the risk level. Results will be saved in the following folders:
    - `fraud_scores/Over_50/`
    - `fraud_scores/Over_20/`
    - `fraud_scores/Below_20/`

   The progress and results are also logged in `ip_monitor.log`.

## Logging

The script logs processing information and errors to `ip_monitor.log`. Ensure that the script has write permissions to create and update this file.

## Example Configuration

```python
# Configuration
api_user = "your_username"
api_key = "your_api_key"
check_interval = 1  # Time between checks (in seconds)
max_workers = 10  # Number of threads
```

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

## Acknowledgements

- [Scamalytics](https://scamalytics.com) for providing the fraud score API.
- [Colorama](https://pypi.org/project/colorama/) for color-coded terminal output.
- [TQDM](https://tqdm.github.io/) for progress bars.
- [Requests](https://docs.python-requests.org/en/master/) for HTTP requests.

---
