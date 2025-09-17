#!/usr/bin/bash

# Edul Desktop Linux Installer
# This script installs Edul (Edulink Terminal Interface) on desktop Linux systems

echo "Starting Edul installation for desktop Linux..."
echo

# Check if we're NOT running in Termux (basic check)
if [ -d "/data/data/com.termux" ]; then
    echo "Error: This installer is designed for desktop Linux systems."
    echo "Please use install-termux.sh for Android/Termux systems."
    exit 1
fi

# Check if running as root or with sudo for system-wide installation
if [ "$EUID" -ne 0 ]; then
    echo "Note: This installer requires root privileges for system-wide installation."
    echo "Please run with sudo: sudo ./install.sh"
    exit 1
fi

# Install required Python packages
echo "Installing required Python packages..."
pip3 install requests || pip install requests || {
    echo "Error: Failed to install requests. Please install Python pip and try again."
    echo "On Ubuntu/Debian: sudo apt install python3-pip"
    echo "On Fedora: sudo dnf install python3-pip"
    echo "On Arch: sudo pacman -S python-pip"
    exit 1
}
echo "✓ Python dependencies installed successfully"
echo

# Create the installation directory
INSTALL_DIR="/usr/local/bin"
TUI_DIR="/usr/local/share/edul-tui"

echo "Creating installation directories..."
mkdir -p "$TUI_DIR"

# Copy all Python files to the share directory
echo "Copying application files..."
cp -r edul-tui/* "$TUI_DIR/" 2>/dev/null || {
    # If edul-tui directory doesn't exist, assume files are in current directory
    cp Student.py "$TUI_DIR/" 2>/dev/null
    cp entry.py "$TUI_DIR/" 2>/dev/null
    cp handler.py "$TUI_DIR/" 2>/dev/null
}

# Create the main edul script that calls the Python entry point
cat > "$INSTALL_DIR/edul" << 'EOF'
#!/usr/bin/bash

SCRIPT_PATH="/usr/local/share/edul-tui"

python3 "$SCRIPT_PATH/entry.py" "$@" || python "$SCRIPT_PATH/entry.py" "$@"
EOF

# Make the main script executable
chmod +x "$INSTALL_DIR/edul"

# Clean up - remove installer files from installation directory if they were copied
rm -f "$TUI_DIR/install.sh" 2>/dev/null
rm -f "$TUI_DIR/install-termux.sh" 2>/dev/null
rm -f "$TUI_DIR/readme.md" 2>/dev/null

echo "✓ Application files installed successfully"
echo

# Create user data directory template (will be created per-user when first run)
echo "Setting up user data directory structure..."
# We don't create the actual directory here since it should be per-user in their home directory
echo "✓ User data directory structure configured"
echo

# Check if installation was successful
if [ -x "$INSTALL_DIR/edul" ] && [ -f "$TUI_DIR/entry.py" ]; then
    echo "🎉 Edul has been successfully installed!"
    echo
    echo "Installation complete! Here's what was installed:"
    echo "• Main executable: $INSTALL_DIR/edul"
    echo "• Application files: $TUI_DIR/"
    echo "• User data will be stored in: ~/edul/data/ (created on first run)"
    echo
    echo "Next steps:"
    echo "1. Execute 'edul -l' to create your first login profile"
    echo "2. Execute 'edul -a 1' to set your first account as active"
    echo "3. Try 'edul -t' to view your timetable"
    echo
    echo "For help, run: edul --help"
    echo
    echo "Note: The 'edul' command is now available system-wide for all users."
else
    echo "❌ Installation failed. Please check for errors above."
    exit 1
fi
