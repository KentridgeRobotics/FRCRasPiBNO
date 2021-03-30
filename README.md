# Setup

To setup this script, first you will need to setup the virtual environment:

```bash
./setup-venv.sh
```

This will also install all of the necessary dependencies. To activate the virtual environment after it is installed:

```bash
source .bno-tables-env/bin/activate
```

To deactivate the virtual environment once you are done:

```bash
deactivate
```

To configure it to run on boot of a device:

```bash
./install.sh
```

To stop it from running on boot:
```bash
./uninstall.sh
```

**NOTE**: It is highly recommended to test the script by hand **before** installing it to ensure that everything works as intended.
