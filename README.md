# MediaTek BPF kernel patcher
![License](https://img.shields.io/github/license/R0rt1z2/mtk-bpf-patcher)
![GitHub Issues](https://img.shields.io/github/issues-raw/R0rt1z2/mtk-bpf-patcher?color=red)

### What is this?
This is a simple Python script that applies a binary patch to the given kernel image. Its purpose is to revert the BPF commit introduced by MTK, which indirectly broke arraymap while attempting to fix ubsan errors. The [specified commit](https://gist.github.com/R0rt1z2/8af7735c6c3802148fa4da61b3cba506), caused connectivity issues on Android 12 based ROMs.

### How does it work?
The patch applied by this script is quite simple. It just NOPs the offending code, in order to allow the `memcpy()` call to be executed.

### Supported kernel(s)
* This tool has only been tested with `4.14.X` and `4.19.X` based kernel(s).
* If your kernel isn't listed, feel free to try the script and report back the results.
* It's possible that each version uses different set of instructions, so beware of that.

### Installation
#### Linux
```bash
sudo apt install python3-pip
pip3 install --upgrade git+https://github.com/R0rt1z2/mtk-bpf-patcher
```
#### Windows
Requires [Windows Terminal](https://github.com/microsoft/terminal) or [PowerShell](https://github.com/PowerShell/PowerShell).
```powershell
# (Requires privileges - start Terminal/PowerShell as administrator)
Invoke-WebRequest https://raw.githubusercontent.com/R0rt1z2/mtk-bpf-patcher/master/Install.ps1 -OutFile .\Install.ps1; .\Install.ps1
```

### Usage
```python
usage: mtk-bpf-patcher [-h] [-l LOG_FILE] [-d] input_file output_file

positional arguments:
  input_file            The input file
  output_file           The output file

options:
  -h, --help            show this help message and exit
  -l LOG_FILE, --log_file LOG_FILE
                        The log file
  -d, --debug           Enable debug mode
```
