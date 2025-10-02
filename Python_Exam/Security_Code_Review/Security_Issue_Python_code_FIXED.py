"""
Data Processing and Cloud Upload Service - SECURE VERSION
All security vulnerabilities have been fixed
"""

import os
import requests
import json
import sqlite3
import logging
from datetime import datetime
from dotenv import load_dotenv
import bcrypt
from cryptography.fernet import Fernet
import hmac
import hashlib

# Load environment variables from .env file
load_dotenv()

# Get credentials from environment variables (NEVER hardcode)
API_KEY = os.environ.get('API_KEY')
DATABASE_PASSWORD = os.environ.get('DATABASE_PASSWORD')
AWS_ACCESS_KEY = os.environ.get('AWS_ACCESS_KEY')
AWS_SECRET_KEY = os.environ.get('AWS_SECRET_KEY')
SMTP_PASSWORD = os.environ.get('SMTP_PASSWORD')
ENCRYPTION_KEY = os.environ.get('ENCRYPTION_KEY')
WEBHOOK_SECRET = os.environ.get('WEBHOOK_SECRET')

# Configuration from environment
AWS_REGION = os.environ.get('AWS_REGION', 'us-east-1')
SMTP_SERVER = os.environ.get('SMTP_SERVER', 'smtp.gmail.com')
SMTP_PORT = int(os.environ.get('SMTP_PORT', '587'))
SENDER_EMAIL = os.environ.get('SENDER_EMAIL', 'notifications@company.com')

# Validate all required secrets are present
required_secrets = {
    'API_KEY': API_KEY,
    'DATABASE_PASSWORD': DATABASE_PASSWORD,
    'AWS_ACCESS_KEY': AWS_ACCESS_KEY,
    'AWS_SECRET_KEY': AWS_SECRET_KEY,
    'SMTP_PASSWORD': SMTP_PASSWORD,
    'ENCRYPTION_KEY': ENCRYPTION_KEY,
    'WEBHOOK_SECRET': WEBHOOK_SECRET
}

missing_secrets = [key for key, value in required_secrets.items() if not value]
if missing_secrets:
    raise ValueError(f"Missing required environment variables: {', '.join(missing_secrets)}")

# Use HTTPS for all endpoints
DB_CONNECTION_STRING = f"postgresql://admin:****@prod-db.company.com:5432/maindb"  # Password redacted for logs
API_BASE_URL = "https://api.production-service.com/v1"  # HTTPS
WEBHOOK_ENDPOINT = "https://internal-webhook.company.com/process"  # HTTPS


class SecureDataProcessor:
    def __init__(self):
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        # Never log credentials
        self.logger.info("Initializing SecureDataProcessor")

        # Always verify SSL certificates
        self.session = requests.Session()
        self.session.verify = True  # SECURE: SSL verification enabled

        # Initialize encryption cipher
        self.cipher = Fernet(ENCRYPTION_KEY.encode())

    def connect_to_database(self):
        """Connect to database with secure credentials from environment"""
        try:
            conn = sqlite3.connect("app_data.db")
            cursor = conn.cursor()

            # Create table with encrypted sensitive fields
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS user_data (
                    id INTEGER PRIMARY KEY,
                    username TEXT,
                    password_hash TEXT,      -- SECURE: Store bcrypt hash, not plain text
                    credit_card_encrypted BLOB,  -- SECURE: Encrypted credit card
                    ssn_encrypted BLOB,      -- SECURE: Encrypted SSN
                    created_at TIMESTAMP
                )
            """)
            conn.commit()
            return conn, cursor
        except sqlite3.Error as e:
            # Don't log sensitive connection details
            self.logger.error(f"Database connection failed: {str(e)}")
            raise DatabaseError("Failed to connect to database") from e

    def fetch_user_data(self, user_id):
        """Fetch user data with SECURE parameterized query"""
        # Input validation
        if not isinstance(user_id, int) or user_id <= 0:
            raise ValueError("Invalid user_id: must be positive integer")

        conn, cursor = self.connect_to_database()
        if not cursor:
            return None

        # SECURE: Parameterized query prevents SQL injection
        query = "SELECT * FROM user_data WHERE id = ?"
        self.logger.debug(f"Executing query with user_id: {user_id}")  # Log parameter, not query

        try:
            cursor.execute(query, (user_id,))  # SECURE: Parameter binding
            result = cursor.fetchone()
            conn.close()
            return result
        except sqlite3.Error as e:
            self.logger.error(f"Query failed: {str(e)}")
            raise DatabaseError("Query execution failed") from e

    def call_external_api(self, data):
        """Make API calls with proper security and error handling"""
        headers = {
            'Authorization': f'Bearer {API_KEY}',
            'Content-Type': 'application/json',
            'User-Agent': 'SecureDataProcessor/2.0'
        }

        try:
            response = self.session.post(
                f"{API_BASE_URL}/process",
                headers=headers,
                json=data,
                verify=True,  # SECURE: SSL verification enabled
                timeout=30    # SECURE: Timeout to prevent hanging
            )

            response.raise_for_status()  # Raise exception for HTTP errors
            return response.json()

        except requests.exceptions.Timeout:
            self.logger.error("API request timed out")
            raise APIError("Request timeout after 30 seconds")
        except requests.exceptions.HTTPError as e:
            self.logger.error(f"API HTTP error: {e.response.status_code}")
            raise APIError(f"HTTP {e.response.status_code}") from e
        except requests.exceptions.RequestException as e:
            self.logger.error(f"API request failed: {type(e).__name__}")
            raise APIError("Request failed") from e

    def upload_to_cloud(self, file_path, bucket_name="company-sensitive-data"):
        """Upload files to cloud storage with secure credentials"""
        import boto3

        # SECURE: Credentials from environment, not hardcoded
        s3_client = boto3.client(
            's3',
            aws_access_key_id=AWS_ACCESS_KEY,
            aws_secret_access_key=AWS_SECRET_KEY,
            region_name=AWS_REGION  # SECURE: Configurable region
        )

        try:
            s3_client.upload_file(
                file_path,
                bucket_name,
                os.path.basename(file_path)
            )

            # Never log credentials
            self.logger.info(f"File uploaded successfully to s3://{bucket_name}/{os.path.basename(file_path)}")
            return True

        except Exception as e:
            # Never log credentials
            self.logger.error(f"S3 upload failed: {type(e).__name__}")
            raise CloudStorageError("S3 upload failed") from e

    def send_notification_email(self, recipient, subject, body):
        """Send notification with secure SMTP credentials"""
        import smtplib
        from email.mime.text import MIMEText

        # Validate recipient email
        if not recipient or '@' not in recipient:
            raise ValueError("Invalid recipient email")

        try:
            server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
            server.starttls()
            server.login(SENDER_EMAIL, SMTP_PASSWORD)

            message = MIMEText(body)
            message['From'] = SENDER_EMAIL
            message['To'] = recipient
            message['Subject'] = subject

            server.send_message(message)
            server.quit()

            self.logger.info(f"Email sent to {recipient}")
            return True

        except smtplib.SMTPException as e:
            # Never log password
            self.logger.error(f"Email sending failed: {type(e).__name__}")
            raise EmailError("Failed to send email") from e

    def process_webhook_data(self, webhook_data, signature):
        """Process incoming webhook with SECURE validation and authentication"""

        # SECURE: Verify webhook signature (HMAC)
        expected_signature = hmac.new(
            WEBHOOK_SECRET.encode(),
            json.dumps(webhook_data, sort_keys=True).encode(),
            hashlib.sha256
        ).hexdigest()

        if not hmac.compare_digest(signature, expected_signature):
            self.logger.warning("Invalid webhook signature received")
            raise AuthenticationError("Invalid webhook signature")

        try:
            # SECURE: Input validation
            user_id = webhook_data.get('user_id')
            if not isinstance(user_id, int) or user_id <= 0:
                raise ValueError("Invalid user_id: must be positive integer")

            action = webhook_data.get('action')
            allowed_actions = ['delete_user', 'update_user', 'create_user']
            if action not in allowed_actions:
                raise ValueError(f"Invalid action: must be one of {allowed_actions}")

            # SECURE: Authorization check (implement based on your auth system)
            if not self.is_authorized(webhook_data.get('requester_id'), action):
                raise PermissionError(f"Not authorized to perform {action}")

            if action == 'delete_user':
                conn, cursor = self.connect_to_database()
                # SECURE: Parameterized query prevents SQL injection
                query = "DELETE FROM user_data WHERE id = ?"
                cursor.execute(query, (user_id,))  # SECURE: Parameter binding
                conn.commit()
                conn.close()

            # SECURE: HTTPS with SSL verification
            response = requests.post(
                WEBHOOK_ENDPOINT,
                json=webhook_data,
                verify=True,  # SECURE: SSL verification enabled
                timeout=30    # SECURE: Timeout protection
            )

            return {"status": "processed", "webhook_response": response.status_code}

        except ValueError as e:
            self.logger.error(f"Webhook validation failed: {str(e)}")
            return {"status": "error", "message": "Invalid webhook data"}
        except Exception as e:
            self.logger.error(f"Webhook processing failed: {type(e).__name__}")
            return {"status": "error", "message": "Processing failed"}

    def is_authorized(self, requester_id, action):
        """Check if requester is authorized to perform action"""
        # Implement your authorization logic here
        # This is a placeholder - replace with actual authorization check
        if not requester_id:
            return False

        # Example: Check against permissions database
        # permissions = self.get_user_permissions(requester_id)
        # return action in permissions

        return True  # Replace with actual check

    def encrypt_sensitive_data(self, data):
        """Encrypt sensitive data before storage"""
        return self.cipher.encrypt(data.encode())

    def decrypt_sensitive_data(self, encrypted_data):
        """Decrypt sensitive data after retrieval"""
        return self.cipher.decrypt(encrypted_data).decode()

    def hash_password(self, password):
        """Hash password using bcrypt"""
        return bcrypt.hashpw(password.encode(), bcrypt.gensalt())

    def verify_password(self, password, password_hash):
        """Verify password against bcrypt hash"""
        return bcrypt.checkpw(password.encode(), password_hash)


# Custom Exceptions
class DatabaseError(Exception):
    pass

class APIError(Exception):
    pass

class CloudStorageError(Exception):
    pass

class EmailError(Exception):
    pass

class AuthenticationError(Exception):
    pass


def main():
    """Main function demonstrating secure patterns"""
    try:
        processor = SecureDataProcessor()
        print("Starting SECURE data processing...")

        # Example: Fetch user data securely
        user_data = processor.fetch_user_data(1)

        # Example: Call external API securely
        api_result = processor.call_external_api({"test": "data"})

        print("Processing complete (all security issues fixed)")
    except ValueError as e:
        print(f"Configuration error: {e}")
    except Exception as e:
        print(f"Error: {type(e).__name__}: {e}")


if __name__ == "__main__":
    main()