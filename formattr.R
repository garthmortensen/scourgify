library(styler)

# style entire directory of .R files
style_dir(style = tidyverse_style, strict = TRUE, filetype = ".R")
# style_dir(transformers = tidyverse_style(strict = TRUE))
# style_dir("G:\\My Drive\\github\\acme_model\\styler\\dir", filetype = ".R")

# use:
# rscript formatter.R target_dir/
# https://style.tidyverse.org/
