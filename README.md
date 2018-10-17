# DBLP-conference

Small helper script to convert an HTML table with conference proceedings
to data format DBLP can read and easily add to the database.

Currently, this tool is tightly tied to ISMIR's electronic conference proceedings but could be adapted easily.

## Setup

You need to satisfy some Python dependencies.

```
conda env create -f environment.yml
```

## Usage

Get the overview table from the electronic proceedings and save it.
We provide an example file called `ismir_2017.html`.

Then call the parser:

```
python parse.py --input input.html
```

The DBLP-ready output can then be found in `output.txt`.
