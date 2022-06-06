fpath <- ur_data_path
adm <- read.csv(fpath, sep=",", na.strings="")
accept_or_reject <- adm[adm$decision=="Accepted" | adm$decision=="Rejected",]
has_gpa = subset(accept_or_reject, !is.na(accept_or_reject$gpa))
season22 <- has_gpa[has_gpa$season=="Fall 2022" | has_gpa$season=="Spring 2022",]
am_intl <- season22[season22$status=="American" | season22$status=="International",]
has_degree = subset(am_intl, !is.na(am_intl$degree))
all_three_gres <- subset(has_degree, !is.na(has_degree$GRE_AW) & !is.na(has_degree$GRE_V) & !is.na(has_degree$GRE_Quant))
no_gres <- subset(has_degree, is.na(has_degree$GRE_AW) & is.na(has_degree$GRE_V) & is.na(has_degree$GRE_Quant))
all_data <- rbind(all_three_gres, no_gres)

# drop 



#### Modeling
library(MASS)
library("e107")
all_three_gres$accept_01 <- ifelse(all_three_gres$decision=="Accepted", 1, 0)
n = nrow(all_three_gres)
train_id = sample(n, n*0.8)
train_data <- all_three_gres[train_id,]
test_data <- all_three_gres[-train_id,]
glm.fit <- glm(accept_01~school+major+degree+season+gpa+status+GRE_AW+GRE_V+GRE_Quant)
