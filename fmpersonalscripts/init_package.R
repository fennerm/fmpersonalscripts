#!/usr/bin/env Rscript
"Initialize an R package

Usage: init_package.R <name>
" -> doc

library(devtools)
library(docopt)
library(fen.R.util)

opts <- docopt::docopt(doc)

print("Creating package root")
dir.create(opts$name, showWarnings=FALSE)
print("Creating package skeleton")
devtools::create(opts$name)

print("Creating a DESCRIPTION template")
d <- script_dir()
description_template <- file.path(d, "resources", "init_package", "DESCRIPTION")
print(description_template)
description_path <- file.path(opts$name, "DESCRIPTION")
print(description_path)
file.remove(description_path)
file.copy(description_template, description_path)

print("Remember to fill in the missing fields in the DESCRIPTION!")
