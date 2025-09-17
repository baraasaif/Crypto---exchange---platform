# Crypto---exchange---platform
blockchain - based cryptocurrency exchange built with Python and Flask
# Cryptocurrency Exchange Platform (Blockchain-Based)

A secure and user-friendly cryptocurrency exchange platform built using Python and Flask, leveraging blockchain technology to ensure transaction integrity, wallet management, and decentralized data handling.

## Overview

This project simulates a basic cryptocurrency exchange system where users can register, create wallets, perform transactions, and view blockchain records. It demonstrates core blockchain principles such as hashing, block creation, and proof-of-work, all integrated into a web-based interface.

# Key Features

- Secure Authentication: User login with encrypted passwords.
- Wallet Management: Each user gets a unique wallet with public/private keys and initial balance.
- Transaction System: Send and receive cryptocurrency between wallets.
- Blockchain Engine: Transactions are grouped into blocks with hash links and proof-of-work.
- Chain Validation: Ensures blockchain integrity by verifying hashes and block structure.

# Project Structure

project/
│
├── init.py          -> App initialization and routing
├── models.py            -> Database models (User, Wallet, Transaction, Block)
├── wallet.py            -> Wallet generation and hashing logic
├── blockchain.py        -> Blockchain logic (block creation, validation)
├── auth.py              -> User registration and login
├── views.py             -> Web views and user interface logic
├── templates/           -> HTML templates (index, wallet, transaction, user info)
└── static/              -> CSS and Bootstrap assets

# Technologies Used

- Python 3.10+
- Flask (Web framework)
- SQLite (Lightweight database)
- Bootstrap (Frontend styling)
- Werkzeug (Password hashing)

# Installation

1. Clone the repository:
   git clone https://github.com/your-username/crypto-exchange-platform.git
   cd crypto-exchange-platform

2. Install dependencies:
   pip install -r requirements.txt

3. Run the application:
   flask run

4. Open your browser at:
   http://localhost:5000

# Future Enhancements

- Integration with real blockchain networks (e.g., Ethereum via Web3.py)
- Smart contract support
- Mobile app version (Flutter or React Native)
- Two-factor authentication (2FA)
- Fiat currency support and KYC/AML compliance

# Developers

- Baraa Saif
- Abd Al-Ilah Khalifa
Supervised by Dr. Eng. Talal Hammoud – Syrian Private University (SPU)

# License

This project is for educational and demonstration purposes. Feel free to fork, modify, and build upon it.
