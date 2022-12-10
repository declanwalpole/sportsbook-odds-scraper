library(tidyverse)


#id, subtype, bettype, customer_segment, lower_bound_inclusive, upper_bound_exclusive, boosted_odds


rolls = c(
  seq(1,1.2,0.01),
  seq(1,1.2,0.01),
  seq(1.22,1.4,0.02),
  seq(1.45,2,0.05),
  seq(2.1,3,0.1),
  seq(3.2,5,0.2),
  seq(5.5,10,0.5),
  seq(11,21,1),
  seq(26,101,5)
)

rollsDF <- data.frame(price=rolls) %>%
  mutate(n=row_number()) 

rollsDF2 <- merge(x=rollsDF,y=rollsDF %>% mutate(n=n-1),by="n",all.x=TRUE)

rollsDF2 <- merge(x=rollsDF2,y=rollsDF %>% mutate(n=n-2),by="n",all.x=TRUE)

rollsDF2 <- rollsDF2 %>% select(c(2,3,4)) %>%
  rename(lower_bound_inclusive=price.x,upper_bound_exclusive=price.y,boosted_odds=price) %>%
  mutate(id="",subtype="General",bettype="General",customer_segment="General")

write.csv(rollsDF2,file = "boostRolls.csv")
