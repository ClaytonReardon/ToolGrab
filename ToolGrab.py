#!/usr/bin/env python3
import sys
import requests
import argparse
import re
import gzip
import shutil

# Define color codes
gray = "\033[1;30m"
green = "\033[1;32m"
red = "\033[1;31m"
reset = "\033[0m"

# List of valid tool names
valid_tools = ['linpeas', 'pspy', 'chisel']

# Parse command line arguments
parser = argparse.ArgumentParser(description='Download latest version of tools from their repos. Valid tools are: ' + ', '.join(valid_tools))
parser.add_argument('files', metavar='<Tool Names>', nargs='*', help='Specify tool names to download: ' + ', '.join(valid_tools))
args = parser.parse_args()

# Check if tool names are provided. If not, print help and exit
if not args.files:
    parser.print_help()
    sys.exit(1)

# Specify repos for tools 
repos = {
    'linpeas': {
        'owner': 'peass-ng',
        'repo': 'PEASS-ng',
        'filename': 'linpeas.sh',
        'output_filename': 'linpeas.sh'
    },
    'pspy': {
        'owner': 'DominicBreuker',
        'repo': 'pspy',
        'filename': 'pspy64',
        'output_filename': 'pspy' 
    },
    'chisel': {
        'owner': 'jpillora',
        'repo': 'chisel',
        'filename': 'chisel_*_linux_amd64.gz',
        'output_filename': 'chisel.gz'
    }
}

# Decompress .gz file is applicable
def decompress_gz(source_path, dest_path):
    with gzip.open(source_path, 'rb') as f_in:
        with open(dest_path, 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)
    print(f"{red}Decompressed{reset} {source_path} to {dest_path}")

# Iterate over each requested tool
for file_name in args.files:
    tool = file_name.lower()
    if tool in repos:
        owner = repos[tool]['owner']
        repo = repos[tool]['repo']
        filename = repos[tool]['filename']
        output_filename = repos[tool]['output_filename']
        
        # Construct the API URL
        url = f"https://api.github.com/repos/{owner}/{repo}/releases/latest"
        
        # Get URL of current latest release
        response = requests.get(url, headers={"Accept": "application/vnd.github.v3+json"})
        if response.status_code == 200:
            data = response.json()
            assets = data.get('assets', [])

            # Download specified file(s)
            for asset in assets:
                if re.match(filename.replace('*', '.*'), asset['name']):
                    download_url = asset['browser_download_url']
                    print(f"\n{gray}Downloading {filename}...{reset}")
                    download_response = requests.get(download_url)
                    
                    if download_response.status_code ==200:
                        with open(output_filename, 'wb') as file:
                            file.write(download_response.content)
                        print(f"{green}{filename}{reset} downloaded successfully")
                        
                        # Decompress if it's a .gz file
                        if output_filename.endswith('.gz'):
                            decomp_filename = output_filename.replace('.gz', '')
                            decompress_gz(output_filename, decomp_filename)
                    else:
                        print(f"Failed to download {filename}")
                    break
            else:
                print(f"{filename} not found in latest release")
        else:
            print(f"Failed to access {url}. Status code: {response.status_code}")
    else:
        print(f"Invalid tool specified: {tool}. Please choose from: " + ', '.join(valid_tools))

