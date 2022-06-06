library(tidyverse)
fpath <- "Admission_Predict_Ver1.1.csv"
adm <- read.csv(fpath, sep=",", na.strings="") %>% 
  select(-Serial.No.)
head(adm)
summary(adm)
# Checking for missing values 
colSums(is.na(adm))
View(adm)

names(adm) <- c("gre", "toefl","uni_rating",
                 "sop","lor","gpa","research","admit")
attach(adm)
## Visualization 

### Admission Chance Distribution 
ggplot(adm,aes(admit)) + 
  geom_histogram(aes(fill=..count..),bins=40)

### Chance of admission by school rating 
ggplot(adm,aes(factor(uni_rating),
    admit)) + geom_boxplot(aes(fill=uni_rating))

# GRE vs Research 
ggplot(adm, aes(gre, color=factor(research)))+
  geom_density(alpha=0.5)+ggtitle("GRE vs Research Distribution")

# 3D Graph for chance of admission vs CGPA, TOEFL and GRE
#install.packages("plotly")
library(plotly)
plot_ly(adm, x=~gre, y=~toefl, z=~gpa, color = ~admit, 
        type="scatter3d", mode="markers") %>% 
  layout(scene = list(xaxis = list(title = "GRE Score"),
                      yaxis = list(title = "TOEFL Score"),
                      zaxis = list(title = "CGPA")))
# From the 3D graph, we could see that chance of
# admission is higher when the CGPA, TOEFL and GRE score
# is higher.

# Correlation between variables 
library(corrplot)
corrplot(cor(adm), method = "number")

# The more extreme the correlation coefficient 
# (the closer to -1 or 1), the stronger the relationship.
# a positive correlation implies that the two variables 
# under consideration vary in the same direction, i.e., 
# if a variable increases the other one increases and if 
# one decreases the other one decreases as well.


# Data Preparation 
# Predictive Modeling 
#install.packages("caTools")
library(caTools)

# Cross Validation
set.seed(1)
sample=sample.split(adm$admit,SplitRatio = 0.80)
train_data=subset(adm,sample==TRUE)
test_data=subset(adm,sample==FALSE)

# Random Forest 
install.packages("randomForest")
library(randomForest)
rf_model <- randomForest(admit ~., data = train_data, importance=TRUE)
rf_model
importance(rf_model)



# Multiple Linear Regression
# Let's try to do linear regression modeling using admit as the target
# variable 
install.packages("modelr")
library(modelr)
model1 <- lm(admit ~., data=train_data)
summary(model1)
mae(model1, data = train_data)

# Interpretation 
# The p-value of SOP and GPA are more than 0.05, making them 
# insignificant variables. This means they have no influence on the 
# chance of getting admitted. 


# Logistic Regression 
library(MASS)
lr.fit <- glm(adm)
summary(lr.fit)




















