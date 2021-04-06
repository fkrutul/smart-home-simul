getwd()
setwd(getwd())
electric = readxl::read_xls("table6.xls")
mean(electric$Price)
weightedmean = mean(rep(electric$Price,electric$Customers))
toDollars = weightedmean/100
print(toDollars)
