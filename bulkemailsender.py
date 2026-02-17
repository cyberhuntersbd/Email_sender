import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
import time
import sys
import json

# Color codes - Modified for Termux compatibility
a="\033[1;30m";r="\033[1;31m";g="\033[1;32m"
y="\033[1;33m";b="\033[1;34m";p="\033[1;35m"
c="\033[1;36m";w="\033[1;37m"
stp="\033[0m"

# Config file path for saving credentials
CONFIG_FILE = os.path.join(os.path.expanduser("~"), ".email_config.json")

def clear_screen():
    """Clear terminal screen - Termux compatible"""
    os.system('clear' if os.name == 'posix' else 'cls')

def line():
    print(52*f'{g}━{stp}')

def animation(text, delay):
    """Simple animation that works in Termux"""
    for i in text:
        sys.stdout.write(i)
        sys.stdout.flush()
        time.sleep(delay)

def check_termux():
    """Check if running in Termux and setup accordingly"""
    try:
        if 'ANDROID_ROOT' in os.environ:
            print(f"{y}Termux detected! Optimizing for mobile...{stp}")
            time.sleep(1)
            return True
    except:
        pass
    return False

def save_credentials(email, password):
    """Save credentials to config file in home directory"""
    try:
        config = {"email": email, "password": password}
        with open(CONFIG_FILE, 'w') as f:
            json.dump(config, f)
        # Set file permissions to read/write for owner only
        if os.name == 'posix':
            os.chmod(CONFIG_FILE, 0o600)
        return True
    except Exception as e:
        print(f"{r}Failed to save credentials: {str(e)}{stp}")
        return False

def load_credentials():
    """Load credentials from config file if exists"""
    try:
        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, 'r') as f:
                config = json.load(f)
            return config.get("email"), config.get("password")
    except Exception as e:
        print(f"{y}Could not load saved credentials: {str(e)}{stp}")
    return None, None

def delete_saved_credentials():
    """Delete saved credentials file"""
    try:
        if os.path.exists(CONFIG_FILE):
            os.remove(CONFIG_FILE)
            print(f"{g}Saved credentials deleted successfully!{stp}")
    except Exception as e:
        print(f"{r}Failed to delete credentials: {str(e)}{stp}")

#------------LOGO-------------
logo = f"""
{p}╔════════════════════════════════════╗
║     BULK EMAIL SENDER v2.0         ║
╠════════════════════════════════════╣
║                                    ║
║    ██████    ██   ██    ██████     ║
║   ██         ██   ██    ██   ██    ║  
║   ██         ███████    ██████     ║  
║   ██         ██   ██    ██   ██    ║  
║    ██████ ██ ██   ██ ██ ██████     ║  
║                                    ║  
╠════════════════════════════════════╣
║ {c}Author :{g} Cyber Hunters BD           ║
║ {c}GitHub :{g} github.com/cyberhuntersbd ║
║ {c}Termux :{g} Optimized Version        ║
╚════════════════════════════════════╝{stp}
"""

#------------LOADING ANIMATION-------------
def loading_animation(message, duration=1):
    """Simple loading animation for Termux"""
    chars = "⣾⣽⣻⢿⡿⣟⣯⣷"
    for i in range(20):
        sys.stdout.write(f'\r{y}{message} {chars[i % len(chars)]}{stp}')
        sys.stdout.flush()
        time.sleep(duration/20)
    print()

def test_gmail_connection(sender_email, sender_password):
    """Test Gmail login credentials before proceeding"""
    print(f"{c}\n📡 Testing Gmail Connection...{stp}")
    loading_animation("Connecting", 2)
    
    try:
        # Try to connect and login
        test_server = smtplib.SMTP("smtp.gmail.com", 587)
        test_server.starttls()
        test_server.login(sender_email, sender_password)
        test_server.quit()
        print(f"{g}✅ Gmail login successful!{stp}\n")
        return True
    except smtplib.SMTPAuthenticationError:
        print(f"{r}❌ Gmail login failed: Authentication Error{stp}")
        print(f"{y}  Possible reasons:{stp}")
        print("  1. Wrong email or password")
        print("  2. 2-Step Verification is ON - need App Password")
        print("  3. Less Secure App Access is OFF")
        return False
    except Exception as e:
        print(f"{r}❌ Connection failed: {str(e)}{stp}")
        return False

def get_credentials():
    """Get credentials either from saved file or user input"""
    saved_email, saved_password = load_credentials()
    
    if saved_email and saved_password:
        print(f"{g}📁 Found saved credentials for: {saved_email}{stp}")
        print(f"{y}Options:{stp}")
        print("  [1] Use saved credentials")
        print("  [2] Enter new credentials")
        print("  [3] Delete saved credentials")
        
        choice = input(f"{c}Your choice (1/2/3): {stp}").strip()
        
        if choice == '1':
            if test_gmail_connection(saved_email, saved_password):
                return saved_email, saved_password
            else:
                print(f"{r}Saved credentials are invalid.{stp}")
                delete_saved_credentials()
        elif choice == '3':
            delete_saved_credentials()
    
    # Get new credentials
    print(f"{c}📝 Please enter your Gmail credentials:{stp}")
    email = input(f"{p}📧 Your Gmail address: {stp}").strip()
    password = input(f"{p}🔑 Your Gmail password/App password: {stp}").strip()
    
    # Test new credentials
    if test_gmail_connection(email, password):
        save_choice = input(f"{y}💾 Save credentials for next time? (yes/no): {stp}").lower()
        if save_choice in ['yes', 'y']:
            if save_credentials(email, password):
                print(f"{g}✅ Credentials saved successfully!{stp}")
        return email, password
    else:
        return None, None

def validate_email(email):
    """Simple email validation"""
    return '@' in email and '.' in email

def send_bulk_emails():
    """Main function to send bulk emails"""
    clear_screen()
    line()
    animation(logo, 0.001)
    line()
    
    print(f"{y}ℹ️  Note: You need Gmail App Password or Less Secure Access enabled{stp}\n")
    
    # Get credentials with retry
    max_attempts = 3
    for attempt in range(max_attempts):
        sender_email, sender_password = get_credentials()
        
        if sender_email and sender_password:
            break
        else:
            if attempt < max_attempts - 1:
                print(f"{y}⏳ Attempt {attempt + 2} of {max_attempts}{stp}")
            else:
                print(f"{r}❌ Too many failed attempts. Exiting...{stp}")
                return
    
    # Number of recipients input
    while True:
        try:
            num_recipients = int(input(f"{g}👥 How many students to send emails? {stp}"))
            if num_recipients > 0:
                break
            else:
                print(f"{y}Please enter a positive number{stp}")
        except ValueError:
            print(f"{y}Please enter a valid number{stp}")
    
    # Store recipient information
    recipients = []
    print(f"{g}\n📋 Enter information for {num_recipients} students:{stp}")
    for i in range(num_recipients):
        print(f"\n{c}─── Student {i+1} ───{stp}")
        name = input(f"{p}  👤 Name: {stp}").strip()
        email = input(f"{p}  📧 Gmail: {stp}").strip()
        
        # Email validation
        while not validate_email(email):
            print(f"{y}  Invalid email format. Try again:{stp}")
            email = input(f"{p}  📧 Gmail: {stp}").strip()
            
        recipients.append({"name": name, "email": email})
    
    # Message input
    print(f"{a}\n📝 Write confirmation message:{stp}")
    print(f'{y}(Tip: Use "##name##" for student names){stp}')
    print(f'{y}(Type "DONE" on new line to finish){stp}')
    
    message_lines = []
    while True:
        line_input = input()
        if line_input.upper() == "DONE":
            break
        if line_input:
            message_lines.append(line_input)
    
    message_template = "\n".join(message_lines)
    
    # Email subject
    subject = input(f"{g}\n📌 Email subject: {stp}").strip()
    
    # Preview
    print(f"{y}\n🔍 Preview (first recipient):{stp}")
    if recipients:
        preview_msg = message_template.replace("##name##", recipients[0]["name"])
        print(f"{c}To: {recipients[0]['name']} ({recipients[0]['email']}){stp}")
        print(f"{c}Subject: {subject}{stp}")
        print(f"{c}Message:\n{preview_msg}{stp}")
    
    confirm = input(f"{a}\n📤 Send emails to all students? (yes/no): {stp}").lower()
    if confirm not in ['yes', 'y']:
        print(f"{r}❌ Cancelled.{stp}")
        return
    
    # Sending emails
    try:
        print(f"{c}\n📡 Connecting to Gmail SMTP...{stp}")
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender_email, sender_password)
        
        print(f"{g}✅ Connected! Sending emails...{stp}\n")
        successful = 0
        failed = 0
        failed_recipients = []
        
        for i, recipient in enumerate(recipients, 1):
            try:
                msg = MIMEMultipart()
                msg["From"] = sender_email
                msg["To"] = recipient["email"]
                msg["Subject"] = subject
                
                personalized_message = message_template.replace("##name##", recipient["name"])
                msg.attach(MIMEText(personalized_message, "plain"))
                
                server.send_message(msg)
                print(f"{g}✅ [{i}/{num_recipients}] {recipient['name']} - Sent{stp}")
                successful += 1
                
            except Exception as e:
                print(f"{r}❌ [{i}/{num_recipients}] {recipient['name']} - Failed{stp}")
                failed += 1
                failed_recipients.append(f"{recipient['name']} ({recipient['email']}): {str(e)}")
            
            # Small delay to avoid rate limiting
            time.sleep(0.5)
        
        # Summary
        print(f"\n{y}{'═'*40}{stp}")
        print(f"{c}📊 FINAL SUMMARY{stp}")
        print(f"{y}{'═'*40}{stp}")
        print(f"{g}✅ Successful: {successful}{stp}")
        print(f"{r}❌ Failed: {failed}{stp}")
        
        if failed_recipients:
            print(f"\n{r}Failed Details:{stp}")
            for f in failed_recipients:
                print(f"  • {f}")
        
        if successful == num_recipients:
            print(f"\n{g}🎉 ALL EMAILS SENT SUCCESSFULLY!{stp}")
        
    except Exception as e:
        print(f"{r}\n❌ SMTP Connection Failed: {str(e)}{stp}")
        print(f"{y}\nTroubleshooting:{stp}")
        print("1. Check internet connection")
        print("2. Verify Gmail credentials")
        print("3. Use App Password if 2FA is ON")
        print("4. Visit: https://myaccount.google.com/lesssecureapps")
    
    finally:
        try:
            server.quit()
        except:
            pass

def main():
    """Main program loop"""
    is_termux = check_termux()
    
    while True:
        send_bulk_emails()
        
        print(f"\n{c}{'═'*40}{stp}")
        another = input(f"{y}🔄 Send another batch? (yes/no): {stp}").lower()
        
        if another not in ['yes', 'y']:
            print(f"\n{g}✨ Thank you for using Bulk Email Sender!{stp}")
            print(f"{c}📱 Optimized for Termux{stp}")
            print(f"{y}👋 Goodbye!{stp}")
            break

if __name__ == "_main_":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{y}⚠️  Program interrupted by user{stp}")
        print(f"{c}Goodbye!{stp}")
        sys.exit(0)
    except Exception as e:
        print(f"\n{r}❌ Unexpected error: {str(e)}{stp}")
        print(f"{y}Please report this issue{stp}")
