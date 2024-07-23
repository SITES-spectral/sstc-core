### Using Keyring in Python

`keyring` is a Python library used to access the system's keyring service to store and retrieve credentials securely. This is useful for managing credentials like usernames, passwords, and API keys in a secure manner. Below are the steps to install and use `keyring`.

### Installation

First, install the `keyring` library using `pip`:

```bash
pip install keyring
```

### Storing Credentials

To store credentials in the keyring, you can use the `keyring.set_password` function. This function takes three arguments: the name of the service, the username, and the password.

```python
import keyring

# Store credentials
service_name = 'sftp'
username = 'your_username'
password = 'your_password'

keyring.set_password(service_name, username, password)
```

### Retrieving Credentials

To retrieve credentials from the keyring, use the `keyring.get_password` function. This function takes two arguments: the name of the service and the username.

```python
import keyring

# Retrieve credentials
service_name = 'sftp'
username = 'your_username'

password = keyring.get_password(service_name, username)
print(f"Password for {username} on {service_name} is {password}")
```

### Example Usage

Below is a complete example demonstrating how to store and retrieve SFTP credentials using `keyring`:

```python
import keyring

# Define service name and credentials
service_name = 'sftp'
username = 'your_username'
password = 'your_password'

# Store credentials in keyring
keyring.set_password(service_name, username, password)

# Retrieve credentials from keyring
retrieved_password = keyring.get_password(service_name, username)

print(f"Retrieved password for {username} on {service_name}: {retrieved_password}")

# Use retrieved credentials to connect to SFTP
import paramiko

hostname = 'sftp.example.com'
port = 22

transport = paramiko.Transport((hostname, port))
transport.connect(username=username, password=retrieved_password)
sftp = paramiko.SFTPClient.from_transport(transport)

# Perform SFTP operations...

# Close the SFTP connection
sftp.close()
transport.close()
```

### Summary

1. **Installation**: Install `keyring` using `pip`.
2. **Storing Credentials**: Use `keyring.set_password(service_name, username, password)` to store credentials.
3. **Retrieving Credentials**: Use `keyring.get_password(service_name, username)` to retrieve credentials.
4. **Example**: Demonstrates storing and retrieving SFTP credentials and using them to connect to an SFTP server.

By using `keyring`, you can securely manage sensitive credentials without hardcoding them into your scripts.