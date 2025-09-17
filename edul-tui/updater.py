# ┌────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
# │███████╗██████╗ ██╗   ██╗██╗     ██╗███╗   ██╗██╗  ██╗    ████████╗███████╗██████╗ ███╗   ███╗██╗███╗   ██╗ █████╗ ██╗         ████████╗██╗   ██╗██╗│
# │██╔════╝██╔══██╗██║   ██║██║     ██║████╗  ██║██║ ██╔╝    ╚══██╔══╝██╔════╝██╔══██╗████╗ ████║██║████╗  ██║██╔══██╗██║         ╚══██╔══╝██║   ██║██║│
# │█████╗  ██║  ██║██║   ██║██║     ██║██╔██╗ ██║█████╔╝        ██║   █████╗  ██████╔╝██╔████╔██║██║██╔██╗ ██║███████║██║            ██║   ██║   ██║██║│
# │██╔══╝  ██║  ██║██║   ██║██║     ██║██║╚██╗██║██╔═██╗        ██║   ██╔══╝  ██╔══██╗██║╚██╔╝██║██║██║╚██╗██║██╔══██║██║            ██║   ██║   ██║██║│
# │███████╗██████╔╝╚██████╔╝███████╗██║██║ ╚████║██║  ██╗       ██║   ███████╗██║  ██║██║ ╚═╝ ██║██║██║ ╚████║██║  ██║███████╗       ██║   ╚██████╔╝██║│
# │╚══════╝╚═════╝  ╚═════╝ ╚══════╝╚═╝╚═╝  ╚═══╝╚═╝  ╚═╝       ╚═╝   ╚══════╝╚═╝  ╚═╝╚═╝     ╚═╝╚═╝╚═╝  ╚═══╝╚═╝  ╚═╝╚══════╝       ╚═╝    ╚═════╝ ╚═╝│
# └────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘

# +=================+
# |Created by Sodium|
# +=================+
#
# Edul is not and has never been created, affiliated or endorsed by Overnet Data
# This software is provided as is without warranty of any kind
#

import os
import sys
import json
import requests
import tempfile
import zipfile
import shutil
import subprocess
import hashlib
from datetime import datetime

class EdulUpdater:
    def __init__(self):
        # GitHub repository information
        self.github_user = "ivory-hnt"  
        self.github_repo = "edulink-tui"           
        self.api_url = f"https://api.github.com/repos/{self.github_user}/{self.github_repo}/releases/latest"
        self.current_version_file = self.get_version_file_path()
        
        # Detect platform
        self.is_termux = os.path.exists("/data/data/com.termux")
        
        if self.is_termux:
            self.install_dir = os.environ.get('PREFIX', '/data/data/com.termux/files/usr') + "/bin"
            self.tui_dir = os.environ.get('PREFIX', '/data/data/com.termux/files/usr') + "/share/edul-tui"
        else:
            self.install_dir = "/usr/local/bin"
            self.tui_dir = "/usr/local/share/edul-tui"

    def get_version_file_path(self):
        """Get the path where version info is stored"""
        if self.is_termux:
            return os.path.join(os.environ.get('PREFIX', '/data/data/com.termux/files/usr'), "share/edul-tui/version.json")
        else:
            return "/usr/local/share/edul-tui/version.json"

    def get_current_version(self):
        """Get the currently installed version"""
        try:
            if os.path.exists(self.current_version_file):
                with open(self.current_version_file, 'r') as f:
                    version_data = json.load(f)
                return version_data.get('version', 'unknown')
            else:
                return 'unknown'
        except Exception:
            return 'unknown'

    def save_version_info(self, version, release_info):
        """Save version information after successful update"""
        try:
            os.makedirs(os.path.dirname(self.current_version_file), exist_ok=True)
            version_data = {
                'version': version,
                'updated_at': datetime.now().isoformat(),
                'release_name': release_info.get('name', ''),
                'release_notes': release_info.get('body', '')
            }
            with open(self.current_version_file, 'w') as f:
                json.dump(version_data, f, indent=2)
        except Exception as e:
            print(f"Warning: Could not save version info: {e}")

    def check_for_updates(self):
        """Check if updates are available"""
        try:
            print("🔍 Checking for updates...")
            response = requests.get(self.api_url, timeout=10)
            response.raise_for_status()
            
            release_info = response.json()
            latest_version = release_info['tag_name'].lstrip('v')
            current_version = self.get_current_version()
            
            print(f"Current version: {current_version}")
            print(f"Latest version: {latest_version}")
            
            if current_version == 'unknown':
                print("⚠️  Current version unknown - update recommended")
                return True, release_info
            elif latest_version != current_version:
                print("🆕 Update available!")
                return True, release_info
            else:
                print("✅ You're already running the latest version!")
                return False, None
                
        except requests.exceptions.RequestException as e:
            print(f"❌ Error checking for updates: {e}")
            print("Please check your internet connection and try again.")
            return False, None
        except Exception as e:
            print(f"❌ Unexpected error: {e}")
            return False, None

    def download_and_extract_update(self, release_info):
        """Download and extract the latest release"""
        try:
            # Find the appropriate download URL
            download_url = None
            for asset in release_info.get('assets', []):
                if asset['name'].endswith('.zip'):
                    download_url = asset['browser_download_url']
                    break
            
            if not download_url:
                # Fallback to source code zip
                download_url = release_info['zipball_url']
            
            print(f"📥 Downloading update from: {download_url}")
            
            # Download to temporary file
            with tempfile.NamedTemporaryFile(delete=False, suffix='.zip') as tmp_file:
                response = requests.get(download_url, stream=True, timeout=30)
                response.raise_for_status()
                
                total_size = int(response.headers.get('content-length', 0))
                downloaded_size = 0
                
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        tmp_file.write(chunk)
                        downloaded_size += len(chunk)
                        if total_size > 0:
                            progress = (downloaded_size / total_size) * 100
                            print(f"\rProgress: {progress:.1f}%", end='', flush=True)
                
                print()  # New line after progress
                tmp_zip_path = tmp_file.name
            
            # Extract to temporary directory
            with tempfile.TemporaryDirectory() as tmp_dir:
                print("📦 Extracting update...")
                with zipfile.ZipFile(tmp_zip_path, 'r') as zip_ref:
                    zip_ref.extractall(tmp_dir)
                
                # Find the extracted directory (might be nested)
                extracted_dirs = [d for d in os.listdir(tmp_dir) if os.path.isdir(os.path.join(tmp_dir, d))]
                if extracted_dirs:
                    source_dir = os.path.join(tmp_dir, extracted_dirs[0])
                    # Look for edul-tui subdirectory
                    if os.path.exists(os.path.join(source_dir, 'edul-tui')):
                        source_dir = os.path.join(source_dir, 'edul-tui')
                else:
                    source_dir = tmp_dir
                
                return source_dir
                
        except Exception as e:
            print(f"❌ Error downloading update: {e}")
            return None
        finally:
            # Clean up temporary zip file
            if 'tmp_zip_path' in locals():
                try:
                    os.unlink(tmp_zip_path)
                except:
                    pass

    def backup_current_installation(self):
        """Create a backup of the current installation"""
        try:
            backup_dir = os.path.join(tempfile.gettempdir(), f"edul_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}")
            print(f"💾 Creating backup at: {backup_dir}")
            
            if os.path.exists(self.tui_dir):
                shutil.copytree(self.tui_dir, backup_dir)
                return backup_dir
            else:
                print("⚠️  No existing installation found to backup")
                return None
                
        except Exception as e:
            print(f"⚠️  Warning: Could not create backup: {e}")
            return None

    def install_update(self, source_dir, backup_dir=None):
        """Install the downloaded update"""
        try:
            print("🔧 Installing update...")
            
            # Check if we need elevated privileges
            needs_sudo = not self.is_termux and os.geteuid() != 0
            
            if needs_sudo:
                print("🔐 This update requires administrator privileges...")
                
                # Create a temporary script for sudo execution
                update_script = f"""#!/bin/bash
                set -e
                echo "Stopping any running edul processes..."
                
                echo "Installing updated files..."
                rm -rf "{self.tui_dir}"
                mkdir -p "{self.tui_dir}"
                cp -r "{source_dir}"/* "{self.tui_dir}/"
                
                echo "Setting permissions..."
                chmod +x "{self.install_dir}/edul" 2>/dev/null || true
                
                echo "Update installed successfully!"
                """
                
                with tempfile.NamedTemporaryFile(mode='w', suffix='.sh', delete=False) as script_file:
                    script_file.write(update_script)
                    script_path = script_file.name
                
                os.chmod(script_path, 0o755)
                result = subprocess.run(['sudo', 'bash', script_path], capture_output=True, text=True)
                os.unlink(script_path)
                
                if result.returncode != 0:
                    raise Exception(f"Installation failed: {result.stderr}")
                    
            else:
                # Direct installation (Termux or already running as root)
                if os.path.exists(self.tui_dir):
                    shutil.rmtree(self.tui_dir)
                
                shutil.copytree(source_dir, self.tui_dir)
                
                # Make main script executable
                main_script = os.path.join(self.install_dir, "edul")
                if os.path.exists(main_script):
                    os.chmod(main_script, 0o755)
            
            return True
            
        except Exception as e:
            print(f"❌ Installation failed: {e}")
            if backup_dir:
                print(f"🔄 Attempting to restore backup from: {backup_dir}")
                try:
                    if os.path.exists(self.tui_dir):
                        shutil.rmtree(self.tui_dir)
                    shutil.copytree(backup_dir, self.tui_dir)
                    print("✅ Backup restored successfully")
                except Exception as restore_error:
                    print(f"❌ Failed to restore backup: {restore_error}")
            return False

    def update(self, force=False):
        """Main update function"""
        print("\n🚀 Edul Update Manager")
        print("=" * 50)
        
        # Check for updates
        has_update, release_info = self.check_for_updates()
        
        if not has_update and not force:
            return True
        
        if not force:
            # Show release notes if available
            if release_info and release_info.get('body'):
                print("\n📋 Release Notes:")
                print("-" * 30)
                print(release_info['body'][:500] + ("..." if len(release_info['body']) > 500 else ""))
                print()
            
            # Ask for confirmation
            try:
                response = input("Do you want to update now? [Y/n]: ").strip().lower()
                if response and response != 'y' and response != 'yes':
                    print("Update cancelled.")
                    return True
            except KeyboardInterrupt:
                print("\nUpdate cancelled.")
                return True
        
        # Create backup
        backup_dir = self.backup_current_installation()
        
        # Download update
        source_dir = self.download_and_extract_update(release_info)
        if not source_dir:
            return False
        
        # Install update
        success = self.install_update(source_dir, backup_dir)
        
        if success:
            # Save version info
            version = release_info['tag_name'].lstrip('v')
            self.save_version_info(version, release_info)
            
            print("🎉 Update completed successfully!")
            print(f"Edul has been updated to version {version}")
            
            # Clean up backup after successful update
            if backup_dir and os.path.exists(backup_dir):
                try:
                    shutil.rmtree(backup_dir)
                except:
                    pass
        else:
            print("❌ Update failed!")
        
        return success

def main():
    """Main function for standalone execution"""
    updater = EdulUpdater()
    
    force_update = '--force' in sys.argv or '-f' in sys.argv
    
    try:
        success = updater.update(force=force_update)
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\nUpdate cancelled by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\nUnexpected error during update: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
