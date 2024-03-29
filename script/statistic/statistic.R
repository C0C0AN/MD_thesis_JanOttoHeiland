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

d_long %>%
  group_by(run, phase, group) %>%
  shapiro_test(pulse)

# they all differ significantly from a normal distribution, but we talked about that

ggqqplot(d_long[group = 'Musik'], "pulse", ggtheme = theme_bw(),
         title = 'Probanden in Musikbedingung') +
  facet_grid(run ~ phase)

ggqqplot(d_long[group = 'Sound'], "pulse", ggtheme = theme_bw(),
         title = 'Probanden in Musikbedingung') +
  facet_grid(run ~ phase)

# qqplots show that distribution is mostly OK

# 2) homogeneity of variance (only for between-subject factors)


d_long %>%
  group_by(run, phase) %>%
  levene_test(pulse ~ group)

 # not given, we need to correct the results. Keep in mind.


# 3) assumption of sphericity (only for within-subject factors)

# will be checked and corrected for automatically when computing the ANOVA. Look at that then.


#### define model


model1 <- aov_ez("ID", # Variable/column defining your participants
       "pulse", # dv
       d_long, # name of your dataframe
       between = "group", # if sex was also included, this would be c('group', 'sex')
       within = c("phase", "run"), 
       include_aov = TRUE)

model1
summary(model1)

# we see that the assumption of sphericity was corrected for using the Greenhouse-Geisser correction
# we also see that we have an effect for phase: F(8, 176) = 11.3991, p < .001
# as well as for run: F(1, 22) = 10.0513, p = 0.0044
# and for their interaction: F(8, 176) = 24.5168, p < .001


# post-hoc tests:


m1_ph <- emmeans(model1, c("phase","run")) # defining here which variables plus their interaction I would like to include in my posthoc-Tests

pairs(m1_ph) # gives you a massive table with all pair comparisons between the two significant factors, with p-values already corrected for multiple testing

# to combine pairs of factor levels define contrasts:
# e.g. test phases -1 to 3 against phases 4 to 7, but define that for each of the runs

c1 <- list(run1 = c(-1, -1, -1, -1, -1, 0, 0, 0, 0, -1, -1, -1, -1, -1, 0, 0, 0, 0) # this vector gives each line in the object 'm1_ph' a weight
)

# if several contrasts are defined, these go into a list of vectors and each get their own name.
  
contrast(m1_ph, c1, adjust = "holm") # here we define how to adjust the alpha-level, specified here is the Bonferroni-Holm correction, 
                                     # which is less strict than the Bonferroni correction

# and we see: there is a difference, t(22) = -28.069, p < .0001
  
  




