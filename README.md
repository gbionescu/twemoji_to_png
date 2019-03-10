# twemoji_to_imgur
Upload twemoji SVG files to imgur and return the link to the uploaded file

## How to use

Prerequisites:
- python3
- imagemagick

Steps:
1. Create a file named `config.json` based on the contents of `config.sample.json`.
2. Add your imgur client ID and client secret in `client.json`.
3. Run `./runme.sh` (note: you'll need to authenticate first)

The uploaded data will be saved in a JSON file called `out.json` where each SVG present in the twemoji repository will be represented as a key, while the imgur link will be represented as a value.

The built in DPI is set to 4000. You can change it in `config.json`.
