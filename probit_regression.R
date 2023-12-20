getwd()
setwd("C:/YOUR/WORK/DIRECTORY")

df <- read.csv("diagnostic_performance.csv", stringsAsFactors = T)

library(aod)
library(ggplot2)

str(df)
xtabs(positive ~ antibody_conc, data=df)

myprobit <- glm( positive ~ antibody_conc, family = binomial(link = "probit"), 
                 data = df)

summary(myprobit)


#prediction & plot

newdf <-data.frame(antibody_conc = rep(seq(from = 0, to = 10, by=0.5) ))
head(newdf)

newdf[, c("p", "se")] <- predict(myprobit, newdf, type = "response", se.fit=T)[-3]
ggplot(newdf, aes(x = antibody_conc, y = p)) + geom_line()

#calculate confidence interval using ciTools
library(dplyr) # for pipe
library(ciTools)
df1 <- add_ci(newdf, myprobit, names = c("lwr", "upr"), alpha = 0.05) %>%
  mutate(type = "parametric")
df1

#plot with confidence interval
ggplot(df1, aes(x = antibody_conc, y = p)) + 
  geom_line() +
  geom_ribbon(aes(ymin = lwr, ymax = upr), alpha = 0.4)

