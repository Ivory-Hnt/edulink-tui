#!/data/data/com.termux/files/usr/bin/bash

# Edul Termux Installer
# This script installs Edul (Edulink Terminal Interface) on Android using Termux

echo "Starting Edul installation for Termux..."
echo

# Check if we're running in Termux
if [ ! -d "/data/data/com.termux" ]; then
    echo "Error: This installer is designed for Termux on Android."
    echo "Please use the regular install.sh for desktop Linux systems."
    exit 1
fi

# Install required Python packages
echo "Installing required Python packages..."
pip install requests || {
    echo "Error: Failed to install requests. Please check your internet connection and try again."
    exit 1
}
echo "✓ Python dependencies installed successfully"
echo

# Create the installation directory in Termux's bin path
INSTALL_DIR="$PREFIX/bin"
TUI_DIR="$PREFIX/share/edul-tui"

echo "Creating installation directories..."
mkdir -p "$TUI_DIR"
mkdir -p "$HOME/edul/data"

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
#!/data/data/com.termux/files/usr/bin/bash

SCRIPT_PATH="$PREFIX/share/edul-tui"

python "$SCRIPT_PATH/entry.py" "$@"
EOF

# Make the main script executable
chmod +x "$INSTALL_DIR/edul"

# Clean up - remove installer files from installation directory if they were copied
rm -f "$TUI_DIR/install-termux.sh" 2>/dev/null
rm -f "$TUI_DIR/install.sh" 2>/dev/null
rm -f "$TUI_DIR/readme.md" 2>/dev/null

echo "✓ Application files installed successfully"
echo

# Check if installation was successful
if [ -x "$INSTALL_DIR/edul" ] && [ -f "$TUI_DIR/entry.py" ]; then
    echo "🎉 Edul has been successfully installed!"
    echo
    echo "Installation complete! Here's what was installed:"
    echo "• Main executable: $INSTALL_DIR/edul"
    echo "• Application files: $TUI_DIR/"
    echo "• Data directory: $HOME/edul/data/"
    echo
    echo "Next steps:"
    echo "1. Execute 'edul -l' to create your first login profile"
    echo "2. Execute 'edul -a 1' to set your first account as active"
    echo "3. Try 'edul -t' to view your timetable"
    echo
    echo "For help, run: edul --help"
    echo
else
    echo "❌ Installation failed. Please check for errors above."
    exit 1
fi
