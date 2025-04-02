import subprocess
import json
import sys

# Ensure UTF-8 encoding
sys.stdout.reconfigure(encoding='utf-8')

def check_tool(command, version_flag="--version", custom_path=None):
    try:
        cmd = [custom_path, version_flag] if custom_path else [command, version_flag]
        print(f"Running: {' '.join(cmd)}")
        output = subprocess.check_output(cmd, stderr=subprocess.STDOUT, text=True, encoding="utf-8")
        return output.strip().split("\n")[0]
    except Exception as e:
        print(f"❌ Error detecting {command}: {str(e)}")
        return None

detected_tools = []

# Detect Node.js
node_version = check_tool("node", "-v")
if node_version:
    detected_tools.append(f"node@{node_version[1:]}")  

# Detect npm
npm_version = check_tool("npm", "-v", "C:/Program Files/nodejs/npm.cmd")
if npm_version:
    detected_tools.append(f"npm@{npm_version}")

# Detect VS Code
vscode_version = check_tool("code", "--version", "C:/Users/manis/AppData/Local/Programs/Microsoft VS Code/bin/code.cmd")
if vscode_version:
    detected_tools.append("vscode")

# Detect Docker
docker_version = check_tool("docker", "--version")
if docker_version:
    docker_version_cleaned = docker_version.split(",")[0].replace("Docker version ", "")
    detected_tools.append(f"docker@{docker_version_cleaned}")

# Print structured output
print("\n📌 **Environment Detection Report** 📌")
print("=" * 40)
for tool in detected_tools:
    print(f"✅ {tool}")
print("=" * 40)

# Print detected tools as JSON for logging
print(json.dumps(detected_tools))
