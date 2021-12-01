

# library(leaps)
library("writexl")
# training_data <- head(liwc_filtered, 536)
# liwc_model <- lm(Q5Mean ~ ppron + ipron + article + prep + shehe + focusfuture + focuspresent + relativ + informal + WPS + auxverb + adverb + verb + adj +
#                    compare + posemo + negemo + affect + quant + affiliation + achieve + reward + insight + cause + discrep + certain + tentat
#                   + percept + bio + work + money + relig + death + family, data=liwc_filtered)
# 
# adjusted_model <- lm(Q5Mean ~ ipron + adverb + money + verb + cogproc + article + focusfuture + affiliation, data=training_data)
#
#summary(liwc_model)
#summary(adjusted_model)
#
# models <- regsubsets(Q5Mean ~ ppron + ipron + article + prep + shehe + focusfuture + focuspresent + relativ + informal + WPS + auxverb + adverb + verb + adj +
#                                          compare + posemo + negemo + affect + quant + affiliation + achieve + reward + insight + cause + discrep + certain + tentat
#                                        + percept + bio + work + money + relig + death + family, nvmax = 10,data=liwc_filtered)
# adjusted_subsets <- regsubsets(Q5Mean ~ adverb + verb + adj + affiliation + insight + cause + money + focusfuture + ipron + article, nvmax = 10, data=liwc_filtered)
# 
# summary(adjusted_subsets)
# 

hist(as.numeric(LIWC2015_Results_scraped_links_$`Source (D)`))
LIWC2015_Results_scraped_links_$transformed.D = log(as.numeric(LIWC2015_Results_scraped_links_$`Source (D)`))
hist(LIWC2015_Results_scraped_links_$transformed.D)

plot(transformed.D ~ focusfuture,
     data = LIWC2015_Results_scraped_links_)

futureplot <- lm(focusfuture ~ transformed.D,
                 data = LIWC2015_Results_scraped_links_)

summary(futureplot)

totalmodel <- lm(transformed.D ~ ., data = LIWC2015_Results_scraped_links_)
summary(totalmodel)

gfm_model <- lm(transformed.D ~ posemo + WC + leisure + Analytic,
                data = LIWC2015_Results_scraped_links_)
summary(gfm_model)


## TITLES

hist(as.numeric(titles$`Source (D)`))
titles$transformed.D = log(as.numeric(titles$`Source (D)`))
hist(titles$transformed.D)

plot(transformed.D ~ focusfuture,
     data = titles)

titles.futureplot <- lm(transformed.D ~ focusfuture,
                 data = titles)

summary(titles.futureplot)
titles$`Source (D)` <- NULL

titles.totalmodel <- lm(transformed.D ~ ., data = titles)
summary(titles.totalmodel)

titles_model <- lm(transformed.D ~ work + leisure + hear + focusfuture,
                data = titles)
summary(titles_model)


# WC, Analytic, Dic, affect, posemo, negemo, anx, sad, family, health, leisure, money
## training_data$log_mean <- log(as.numeric(training_data$Q5Mean))
## training_data <- training_data[-c(375),]

# hist(log(training_data$auxverb))

# experiment_model <- lm(log_mean ~ ., data = training_data)
# summary(experiment_model)
# plot(experiment_model, which=1)

# experiment_subsets <- regsubsets(log_mean ~ 
# pronoun + ppron + ipron + auxverb + `function` + number + sad + social + male + percept + see + hear + feel + affiliation + focusfuture + time + work + money + relig + informal + swear,
#                                  data = training_data, nvmax = 15)
# summary(experiment_subsets)
# 
# plot(log_mean ~ auxverb, data=training_data)
final_model <- lm(log_mean ~ 
                    male + focusfuture + time + work + money + relig,
                  data=training_data)
# total_model <- lm(log_mean ~ ., data=training_data)
summary(final_model)
# summary(experiment_model)
# summary(total_model)
# plot(training_data$female, training_data$log_mean)
plot(final_model)

# log.data <- training_data
# log.data$mean <- as.numeric(head(liwc_filtered, 536)['Q5Mean'][-c(375),])
# log.data <- log(log.data)
# is.na(log.data)<-sapply(log.data, is.infinite)
# log.data[is.na(log.data)]<-0
# log.experiment_model = lm(mean ~
#                           ., 
#                           data=log.data)
# summary(log.experiment_model)
# plot(log.data$bio, log.data$mean)
# (testing_data <-> testing_data2) (final_model <-> total_model)

testing_data <- tail(liwc_filtered, 536)
testing_data$log_mean <- log(as.numeric(testing_data$Q5Mean))

testing_data$prediction <- predict(final_model, testing_data, interval="prediction")
testing_data$difference <- testing_data$prediction - testing_data$log_mean
summary(testing_data$difference)
testing_data$adjusted_difference <- exp(testing_data$difference)
summary(testing_data$adjusted_difference)
testing_data$actual_prediction <- exp(testing_data$prediction)
summary(testing_data$actual_prediction)
testing_data$actual_difference <- testing_data$actual_prediction - as.numeric(testing_data$Q5Mean)
summary(abs(testing_data$actual_difference))

testing_data$Q5Mean <- as.numeric(testing_data$Q5Mean)
summary(as.numeric(testing_data$Q5Mean))
summary(as.numeric(testing_data$actual_prediction))
summary(as.numeric(abs(testing_data$actual_difference)))
plot(testing_data$male, log(as.numeric(testing_data$Q5Mean)))

##

cor.test(training_data[["log_mean"]], training_data[["WC"]])

write_xlsx(training_data,"DATA\\trainingdata.xlsx")

