# scourgify

run python and r formatters (black, styler), and test frameworks (pytest, testthat). 

``` text
   (\.   .      ,/)
    \(   |\     )/
    //\  | \   /\      SCOURGIFY!
   (/ /\_#oo#_/\ \)
    \/\  ####  /\/
         `##'
         
Cast this spell to test assert,
Ensure these errors do avert,
Clean code, this does convert.

ascii source: https://ascii.co.uk/art/wizard
```

## Usage

Install libraries.

``` bash
$ pip install black, pytest  # can i comma seperate these?

$ R.exe
install.packages(c("styler", "testthat"))
```

Add this program as an alias to `.bashrc` or `.bash_proflie` so that it can be run via terminal.

```bash
alias scourgify='python "/path/to/scourgify/scourgify.py"'
```

