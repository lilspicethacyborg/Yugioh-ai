#!/usr/bin/env bash
set -e
echo "=== Yu-Gi-Oh! AI Deck Builder Setup ==="
echo ""
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is required but not installed."
    exit 1
fi
echo "[1/2] Installing Python dependencies..."
pip3 install -q -r requirements.txt
echo "[2/2] Setup complete!"
echo ""
echo "Run the deck builder:"
echo "  python3 app.py     # Web app (works on phone!)"
echo "  python3 main.py    # Terminal CLI"
echo ""
echo "For phone: open http://<your-computer-ip>:5000 in your phone browser"
echo "(both devices must be on the same WiFi network)"
echo ""
echo "On first run, the full card database (~25MB) will be downloaded"
echo "from YGOPRODeck (free API). 200+ popular cards bundled for offline use."
echo ""
