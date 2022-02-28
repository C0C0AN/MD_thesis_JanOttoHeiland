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

d_raw <- read_delim("C:/Users/rahel/OneDrive/Desktop/puls_alles[4094].tsv", 
                    delim = "\t", escape_double = FALSE, 
                    col_names = TRUE, trim_ws = TRUE, skip = 2)


# restructure data --------------------------------------------------------



names(d_raw) <- c("run", "ID", names(d_raw[3:ncol(d_raw)]))

d_raw %>%
  mutate_at(vars(matches("\\.")), as.character) %>%
  pivot_longer(cols = contains(".")) -> d_long




d_long$name <- str_replace_all(d_long$name, c("-1.00\\B\\S*" = "-1.00", "1.00\\B\\S*" = "1.00", "0.00\\B\\S*" = "0.00",
                                                "2.00\\B\\S*" = "2.00", "3.00\\B\\S*" = "3.00", "4.00\\B\\S*" = "4.00", 
                                                "7.00\\B\\S*" = "7.00", "6.00\\B\\S*" = "6.00", "5.00\\B\\S*" = "5.00", 
                                                "8.00\\B\\S*" = "8.00", "9.00\\B\\S*" = "9.00", "10.00\\B\\S*" = "10.00"
                                                ))

d_long$phase <- as.factor(d_long$name)
d_long$pulse <- as.numeric(d_long$value)
d_long$group <- as.factor(d_long$X505)
d_long$sex <- as.factor(d_long$X504)
d_long$age <- as.factor(d_long$X503)


#d_long %>% select('run', 'ID', 'phase', 'pulse', 'group', 'sex', 'age') -> d_smaller

# write.csv(d_smaller, 'pulse_reformatted.csv', row.names = FALSE)

# str(d_long)


# anova -------------------------------------------------------------------

#in order read restructured data again, in case you're only working with that dataset, uncomment the following: 

# d_long <- read_csv("pulse_reformatted.csv",  # exchange for your own path to the datafile 
#                              col_types = cols(run = col_factor(levels = c("1", 
#                                                                           "2")), phase = col_factor(levels = c("-1.00", 
#                                                                                                                "0.00", "1.00", "2.00", "3.00", "4.00", 
#                                                                                                                "5.00", "6.00", "7.00")), group = col_factor(levels = c("Musik", 
#                                                                                                                                                                        "Sound")), sex = col_factor(levels = c("F", 
#                                                                                                                                                                                                               "M"))))
#

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
  
  




