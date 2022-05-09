install.packages("fdrtool")
library(fdrtool)

input_path <- "step4-out.csv"
output_path <- "step5-out.csv"

data <- read.csv(input_path)

fdrs = fdrtool::fdrtool(x=data$z)
data$fdr <- fdrs$lfdr


data <- data[order(data$fdr),]
write.csv(data, file=output_path, row.names = FALSE)
