library(testthat)

# test entire directory of .R files
test_dir("path/to/tests_directory")

style_dir(style = tidyverse_style, strict = TRUE, filetype = ".R")

# a comment

# use:
# rscript formatter.R target_dir/
# https://style.tidyverse.org/
