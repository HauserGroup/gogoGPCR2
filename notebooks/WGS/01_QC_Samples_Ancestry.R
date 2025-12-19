# Install bigreadr package in R
# Possibly deprecated, in favor of Genomic Ancestry from Pan-UKN (field 30079)
install.packages("bigreadr")

# Import the pcs file, obtained by running "pcs.ipynb"
# TODO: pcs.ipynb is depcreated in favor of 02_covariates.ipynb
PC_UKBB <- bigreadr::fread2(
    "pcs.csv",
    select = c("eid", paste0("p22009_a", 1:16))
)

# Import population centers
# TODO: Cite
all_centers <- read.csv(
    "https://raw.githubusercontent.com/privefl/UKBB-PGS/main/pop_centers.csv",
    stringsAsFactors = FALSE
)

# Compute distance to each group
all_sq_dist <- apply(all_centers[-1], 1, function(one_center) {
    rowSums(sweep(PC_UKBB[-1], 2, one_center, "-")^2)
})
thr_sq_dist <- max(dist(all_centers[-1])^2) * 0.002 / 0.16

# Get closest population of each sample
group <- apply(all_sq_dist, 1, function(x) {
    grp <- NA
    ind <- which.min(x)
    if (isTRUE(x[ind] < thr_sq_dist)) {
        grp <- all_centers$Ancestry[ind]
# We used a more stringent cutoff for the Ashkenazi group
        if (grp == "Ashkenazi" && x[ind] > 12.5^2) grp <- NA
    }
    grp
})

# Format data frame and export
df <- data.frame(PC_UKBB$eid, group)
write.csv(df, "ancestry.csv")
