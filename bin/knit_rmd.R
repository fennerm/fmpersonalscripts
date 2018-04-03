#!/usr/bin/env Rscript
# Render an rmarkdown file.
# Output formats must be specified in the input file

library(rmarkdown)
args <- commandArgs(trailingOnly = TRUE)
render(args[1], "all")
