# Deepdocs

`Deepdocs` is small script that aim to search doc files (.txt, .doc, .docx, .odt, .rtf) recursively in a data drive. This also search in archives content without extracting it.

The motivation of making this software have been the personal need of searching for a specific document in a hundreds of SD cards containing thousands of archives.

## First Use

To get started, run the following command in the root directory:

>```mkdir venv && (cd venv;python3 -m venv env) && (cd venv;source env/bin/activate)```

Then execute the following command to install the requirements:

```sh
./venv/env/bin/pip3.9 install -r requirements.txt
```

## Usage

You are now ready to run `Deepdocs`. The `path` argument is in my case a mounted SD card:

```sh
./venv/env/bin/python3 deepdocs.py --path /Volumes/NO\ NAME
```

The above command will store the files found in a .txt file named `output.txt` at the root directory, but you can change that:

```sh
./venv/env/bin/python3 deepdocs.py --path /Volumes/NO\ NAME --output /tmp/anything.txt
```

And you can also skip the `.txt` files:

>```./venv/env/bin/python3 deepdocs.py --path /Volumes/NO\ NAME --output /tmp/anything.txt --skip-txt```
