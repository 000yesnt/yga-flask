# Setting up Lynx and LynxWebP
You'll have to copy images to the ``/var/lynx`` mount. Additionally, a subfolder named ``webp`` must be created and have only .webp files.
### Set up volumes
Copy your source folder to the container:
``docker cp ./path/to/source/. app-container-id:/var/lynx``

### Restart the container
``docker restart app-container-id``