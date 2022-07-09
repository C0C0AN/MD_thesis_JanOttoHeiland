############################
## Skript Jan Otto
## 26.02.22
############################


# setup -------------------------------------------------------------------
library(readr) # for importing the datafile
library(tidyverse) # for restructuring it
library(afex) # for the anova
library(rstatix) # for testing assumptions
library(ggpubr) # for graphical test of normality
library(emmeans) # for post-hoc tests

# anova -------------------------------------------------------------------
d_long <- read.csv("puls/puls_long.tsv", sep="\t")
names(d_long)[names(d_long) == "puls"] <- "pulse"

#### test assumptions

# 1) normality

norm_test <- d_long %>%
  group_by(run, phase, group) %>%
  shapiro_test(pulse)
