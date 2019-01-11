# Monkeyrider

Monkeyrider is a Python tool for dealing with monkeyrunner android test framework.
It relies on apktool to decompile apk and then analyzes the decoded manifest to guide the monkey through the app.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install monkeyrider.

```bash
pip install git+https://github.com/bnznamco/monkeyrider.git

```

## Usage

```bash
monkeyrider <path_of_your_apk>

```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](LICENSE)