import bcrypt
import csv
import requests
import re

#! File to store user credentials
USER_DATA_FILE = '12325170.csv'

#! Stock API configuration
API_URL = 'https://www.alphavantage.co/query'
API_KEY = 'O0EYQTAJSX2XIIB8'  # Your Alpha Vantage API Key
MAX_ATTEMPTS = 5

#! Validate email format
def validate_email(email):
    regex = r'^\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    return re.fullmatch(regex, email)

#! Validate password format
def validate_password(password):
    if len(password) < 8:
        return False
    return True

#! Check if user already exists in the CSV file
def user_exists(email):
    try:
        with open(USER_DATA_FILE, mode='r') as file:
            reader = csv.reader(file)
            for row in reader:
                if row[0] == email:
                    return True
        return False
    except FileNotFoundError:
        return False

#! Update the CSV file with login attempts
def update_attempts(email, attempts):
    try:
        with open(USER_DATA_FILE, mode='r') as file:
            users = list(csv.reader(file))

        for row in users:
            if row[0] == email:
                row[3] = str(attempts)
                break

        with open(USER_DATA_FILE, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(users)
    except Exception as e:
        print(f"Error updating attempts: {e}")

#! Signup process
def signup():
    email = input("Enter your email: ")

    if not validate_email(email):
        print("Invalid email format.")
        return

    if user_exists(email):
        print("Email already exists. Please try logging in.")
        return

    password = input("Create a password: ")

    if not validate_password(password):
        print("Password must be at least 8 characters long and contain one uppercase letter, one lowercase letter, one number, and one special character.")
        return

    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    security_question = input("Enter your school name: ")

    # Write new user data to the CSV file
    try:
        with open(USER_DATA_FILE, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([email, hashed_password.decode('utf-8'), security_question, str(MAX_ATTEMPTS)])
        print("Signup successful! You can now log in.")
    except Exception as e:
        print(f"An error occurred while saving user data: {e}")

#! Login process
def login():
    email = input("Enter email: ")

    if not validate_email(email):
        print("Invalid email format.")
        return False

    password = input("Enter password: ")
    if(email==""or password==""):
      print("Fields should not be empty")
    else:

      try:
          with open(USER_DATA_FILE, mode='r') as file:
              users = list(csv.reader(file))

          for row in users:
              # Check if the row has the correct number of elements
              if len(row) < 4:
                  print(f"Error: Malformed row in user data file: {row}")
                  continue  # Skip this row and go to the next one

              if row[0] == email:
                  attempts = int(row[3])
                  if attempts <= 0:
                      print("Account locked due to too many failed login attempts.")
                      return False

                  if bcrypt.checkpw(password.encode('utf-8'), row[1].encode('utf-8')):
                      print("Login successful!")
                      return True
                  else:
                      print(f"Incorrect password. {attempts - 1} attempts remaining.")
                      update_attempts(email, attempts - 1)
                      return False

          print("Email not found.")
      except FileNotFoundError:
          print("Error: User data file not found.")
          return False
      except Exception as e:
          print(f"An error occurred: {e}")
          return False
        
        
#! Password reset using security question
def reset_password():
    email = input("Enter registered email: ")

    if not validate_email(email):
        print("Invalid email format.")
        return

    try:
        with open(USER_DATA_FILE, mode='r') as file:
            users = list(csv.reader(file))

        for row in users:
            if row[0] == email:
                security_answer = input("What is your school name?: ")
                if security_answer == row[2]:
                    new_password = input("Enter new password: ")
                    if validate_password(new_password):
                        hashed_password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())
                        row[1] = hashed_password.decode('utf-8')
                        row[3] = str(MAX_ATTEMPTS)  # Reset login attempts after password reset
                        with open(USER_DATA_FILE, mode='w', newline='') as file:
                            writer = csv.writer(file)
                            writer.writerows(users)
                        print("Password reset successful!")
                        return
                    else:
                        print("New password does not meet the criteria.")
                        return
                else:
                    print("Incorrect answer to security question.")
                    return
        print("Email not found.")
    except FileNotFoundError:
        print("Error: User data file not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

#! Fetch and display stock data for two days using Alpha Vantage API
def fetch_stock_data(ticker_symbol):
    params = {
        'function': 'TIME_SERIES_DAILY',
        'symbol': ticker_symbol,
        'apikey': API_KEY
    }

    try:
        response = requests.get(API_URL, params=params)
        response.raise_for_status()  # Check for HTTP errors

        data = response.json()

        if 'Error Message' in data:
            print("Invalid ticker symbol.")
            return

        time_series = data.get('Time Series (Daily)')
        if time_series:
            # Fetch stock data for the last two days
            dates = list(time_series.keys())[:2]
            for date in dates:
                stock_info = time_series[date]
                print(f"\nStock Data for {ticker_symbol} on {date}:")
                print(f"Open: {stock_info['1. open']}")
                print(f"High: {stock_info['2. high']}")
                print(f"Low: {stock_info['3. low']}")
                print(f"Close: {stock_info['4. close']}")
                print(f"Volume: {stock_info['5. volume']}")
        else:
            print("No data available for the given ticker symbol.")
    except requests.exceptions.ConnectionError:
        print("Network error: Please check your internet connection.")
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except Exception as e:
        print(f"An error occurred: {e}")

#! Main Application
def main():
    print("Welcome to Stock Market Data Application")

    while True:
        print("\n1. Signup\n2. Login\n3. Forgot Password\n4. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            signup()
        elif choice == '2':
            if login():
                while True:
                    ticker_symbol = input("Enter stock ticker symbol (e.g., IBM): ").upper()
                    fetch_stock_data(ticker_symbol)

                    more_search = input("Do you want to search for more tickers? (yes/no): ").lower()
                    if more_search != 'yes':
                        print("Logging out...")
                        break
        elif choice == '3':
            reset_password()
        elif choice == '4':
            print("Exiting application.")
            break
        else:
            print("Invalid choice. Try again.")

if __name__ == '__main__':
    main()
