# ToolGrab
A simple python script to allow me to quickly grab tools I use frequently, and save me the time of always having to go to their repos. It uses the Github api to always grab the latest version of the tool in question.

It currently supports [Linpeas](https://github.com/peass-ng/PEASS-ng), [Pspy](https://github.com/DominicBreuker/pspy), and [Chisel](https://github.com/jpillora/chisel), but it's easily expandable by adding new repos to the library.

## Usage
```
usage: ToolGrab.py [-h] [<Tool Names> ...]

Download latest version of tools from their repos. Valid tools are: linpeas, pspy, chisel

positional arguments:
  <Tool Names>  Specify tool names to download: linpeas, pspy, chisel

options:
  -h, --help     show this help message and exit
```
