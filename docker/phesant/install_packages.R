# library(devtools)

install.packages("remotes",
    repos = "http://cran.rstudio.com/",
    dependencies = TRUE
)

remotes::install_version("optparse", version = "1.3.2")
remotes::install_version("MASS", version = "7.3-45")
remotes::install_version("data.table")
remotes::install_version("lmtest", version = "0.9-34")
remotes::install_version("nnet", version = "7.3-12")
remotes::install_version("forestplot")
