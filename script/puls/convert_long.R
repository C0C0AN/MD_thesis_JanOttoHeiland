d_raw <- read_delim("puls_alles.tsv",
                    delim = "\t",
		    escape_double = FALSE, 
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
