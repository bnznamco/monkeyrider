# Monkeyrider
<img src="logo.png" width="300">


Monkeyrider is a Python tool for dealing with monkeyrunner android test framework.
It relies on apktool to decompile apk and then analyzes the decoded manifest to guide the monkey through the app.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install monkeyrider.

```bash
pip install git+https://github.com/bnznamco/monkeyrider.git

```

## Requirements

The tool needs Android Sdk to be installed.
It will search for an env variable called ANDROID_HOME.

You can set it as follows:

```bash
export ANDROID_HOME=<path_to_your_sdk>

```
to make permanent this env variable, add it to your bashrc.

If the variable is not available, the tool will search it in the standard location

```bash
~/Android/Sdk

```

## Usage

```bash
monkeyrider <path_of_your_apk>

```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.


## License
[MIT](LICENSE)