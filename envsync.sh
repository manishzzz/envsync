#!/bin/bash

PROJECT_PATH=$(pwd)  # Get the current project directory
DETECTED_TOOLS=$(python3 detector.py "$PROJECT_PATH")  # Detect tools

echo "🔍 Detected tools: $DETECTED_TOOLS"

# Detect OS and normalize for compatibility
OS=$(uname -s | tr '[:upper:]' '[:lower:]')

# Map MinGW64 to Windows
if [[ "$OS" == "mingw64_nt-"* || "$OS" == "msys" || "$OS" == "cygwin" ]]; then
  OS="windows"
fi

# Install detected tools
for tool in $(echo $DETECTED_TOOLS | jq -r '.[]'); do
  # Normalize Node.js versions (convert node@xx to just "node")
  if [[ "$tool" == node@* ]]; then
    tool="node"
  fi

  # Get the install command from JSON
  COMMAND=$(jq -r ".\"$tool\".\"$OS\"" tool_map.json)

  if [[ "$tool" == "node" && "$(node -v)" =~ "v" ]]; then
    echo "✅ Node.js is already installed. Skipping..."
    continue
  fi

  if [ "$COMMAND" != "null" ]; then
    echo "🚀 Installing $tool..."
    eval "$COMMAND"
  else
    echo "⚠️ No install rule for $tool on $OS."
  fi
done
