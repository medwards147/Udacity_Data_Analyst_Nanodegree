#### Load Libraries
library(data.table)
library(ggplot2)
library(lubridate)
library(corrplot)

setwd("C:/Users/MAX/Documents/GitHub/Udacity_Data_Visualization_Project_6/data/")

#### Load data ####
data <- read.csv("prosperLoanData.csv", stringsAsFactors = FALSE)

###
str(data)
summary(data)
dim(data) #113,937  81

# convert to data table
dt <- as.data.table(data)


# Fields removed from data after inspecting descriptions of the variable
remove_cols <- c("ListingKey", "ListingNumber", "ProsperRating..numeric.", 
                 "GroupKey", "LoanKey", "OnTimeProsperPayments", 
                 "ProsperPaymentsLessThanOneMonthLate", 
                 "ProsperPaymentsOneMonthPlusLate", "ScorexChangeAtTimeOfListing",
                 "MemberKey", "Recommendations", "CurrentCreditLines",
                 "TotalCreditLinespast7years", "OpenRevolvingAccounts",
                 "OpenRevolvingMonthlyPayment", "InquiriesLast6Months", "TotalInquiries",
                 "CurrentDelinquencies", "AmountDelinquent", "DelinquenciesLast7Years",
                 "PublicRecordsLast10Years", "PublicRecordsLast12Months", "BankcardUtilization",
                 "AvailableBankcardCredit", "TotalTrades", "TradesNeverDelinquent..percentage.",
                 "TradesOpenedLast6Months", "TotalProsperLoans", "TotalProsperPaymentsBilled", 
                 "LoanCurrentDaysDelinquent", "LoanFirstDefaultedCycleNumber", 
                 "LoanMonthsSinceOrigination", "LoanNumber", "CurrentlyInGroup", 
                 "DateCreditPulled", "FirstRecordedCreditLine", "OpenCreditLines",
                 "LP_CustomerPayments", "LP_CustomerPrincipalPayments", "LP_InterestandFees",
                 "LP_ServiceFees", "LP_CollectionFees", "LP_GrossPrincipalLoss",
                 "LP_NetPrincipalLoss", "LP_NonPrincipalRecoverypayments", 
                 "InvestmentFromFriendsCount", "InvestmentFromFriendsAmount",
                 "Investors")

# Remove unwated columns
dt[, (remove_cols):=NULL]

dt$ListingCreationDate <- gsub(" .*", "", dt$ListingCreationDate)
dt$ListingCreationDate <- as.Date(dt$ListingCreationDate, "%Y-%m-%d")
dt$LoanOriginationDate <- gsub(" .*", "", dt$LoanOriginationDate)
dt$LoanOriginationDate <- as.Date(dt$LoanOriginationDate , "%Y-%m-%d")
range(dt$ListingCreationDate) # "2005-11-09" "2014-03-10"
max(dt$ListingCreationDate) - min(dt$ListingCreationDate) #3043 days



# Convert Listing Category to actual string values. I think this will be useful for a final chart
dt$ListingCategory <- sapply(as.character(dt$ListingCategory..numeric), switch,'0'= "N/A",
       "1" = "Debt Consolidation", "2" = "Home Improvement",
       "3" = "Business", "4" = "Personal Loan", "5" = "Student Use", 
       "6" = "Auto", "7" = "Other", "8" = "Baby&Adoption",
       "9" = "Boat", "10" = "Cosmetic Procedure", "11" = "Engagement Ring",
       "12" = "Green Loans", "13" = "Household Expenses", "14" = "Large Purchases",
       "15" = "Medical/Dental", "16" = "Motorcycle", "17" = "RV", "18" = "Taxes",
       "19" = "Vacation", "20" = "Wedding Loans")

# Convert loan origination quarter
dt$LoanOriginationYear <- sapply(strsplit(dt$LoanOriginationQuarter, " "),'[',2)
dt$LoanOriginationQtr <- sapply(strsplit(dt$LoanOriginationQuarter, " "),'[',1)


# Count by ListingCategory
dt[, .(Count=.N), by = .(ListingCategory)]

# Count by LoanStatus
dt[, .(Count=.N), by = .(LoanStatus)]

# Remove rows with ProsperRating n/a - should be anything before 2009
#dt <- dt[ProsperRating..Alpha. != "" ]

# New date range
range(dt$ListingCreationDate) # "2009-07-13" "2014-03-10"

# Single variate
qplot(dt$ProsperRating..Alpha.)
qplot(dt$ListingCreationDate) # The amount of loans increase from 2009 to 2014
qplot(dt$Term)
qplot(dt$LoanStatus) + scale_y_log10()
qplot(dt$ClosedDate)
qplot(dt$BorrowerAPR) # somewhat normal, big spike at around 3.6% for some reason
ggplot(dt, aes(BorrowerAPR, fill=ProsperRating..Alpha.)) + geom_histogram()
qplot(dt$BorrowerRate) 
ggplot(subset(dt, ProsperRating..Alpha.!= ""), aes(BorrowerRate, fill=ProsperRating..Alpha.)) + 
  geom_density(alpha=.3) + scale_y_sqrt()
qplot(dt$LenderYield)
qplot(dt$Occupation) + coord_flip() + scale_y_log10()
qplot(dt$EmploymentStatus)+ coord_flip() 
qplot(dt$IsBorrowerHomeowner)
qplot(dt$PercentFunded) # mostly all are funded... remove 
qplot(dt$DebtToIncomeRatio)
qplot(dt$BorrowerState) + coord_flip() 
qplot(dt$MonthlyLoanPayment)
qplot(dt$IncomeRange)
qplot(dt$StatedMonthlyIncome, geom = "histogram") + scale_x_log10()
ggplot(data = dt, aes(x = LoanOriginationQtr)) + geom_bar() + facet_grid(~LoanOriginationYear)
ggplot(data = dt, aes(x = LoanOriginationQtr, y = LoanOriginalAmount, fill = LoanStatus)) + 
  geom_bar(stat = "summary", fun.y=sum) +
  facet_grid(~LoanOriginationYear)

ggplot(data = dt, aes(x = LoanOriginationDate, y = log10(LoanOriginalAmount+1), color = LoanStatus)) + 
  geom_line(stat = "summary", fun.y=sum) + scale_y_log10()


# loan_amounts <- dt[, lapply(.SD, sum), 
#                    .SDcols = "LoanOriginalAmount",
#                    by = "LoanOriginationYear"][order(-LoanOriginationYear)]
# ggplot(data = loan_amounts, aes(LoanOriginationYear, LoanOriginalAmount)) + geom_line()

# More cols to remove based on analysis
remove_more_cols <- c("ProsperScore", "ClosedDate", "ListingCategory..numeric.", "PercentFunded", 
                      "EmploymentStatusDuration", "BorrowerAPR", "IsBorrowerHomeowner")
dt[, (remove_more_cols):=NULL]

# Correleations
corrplot(cor(subset(dt, select = c("Term", "BorrowerAPR", "BorrowerRate", "LenderYield",
                   "EstimatedEffectiveYield", "EstimatedLoss", "EstimatedReturn",
                   "CreditScoreRangeLower", "CreditScoreRangeUpper", "DebtToIncomeRatio",
                   "StatedMonthlyIncome","LoanOriginalAmount", "MonthlyLoanPayment")), use = "pairwise"), 
         method="circle")
## Multi
ggplot(data=dt, aes(x=BorrowerRate, y=LenderYield, color=as.factor(Term))) + geom_point()

#plot1 = dt[, lapply(.SD, mean), .SDcols = "BorrowerRate", by = "LoanOriginationYear"]
p1 <- ggplot(data=dt, aes(x=LoanOriginationYear, y=BorrowerRate))
p1 + geom_point()
p1 + geom_point(alpha=.3, size=2, aes(color = as.factor(Term)))
p2 <- ggplot(data=dt, aes(x=LoanOriginationYear, y=BorrowerRate)) + geom_point()
p2 + geom_smooth(aes(group=1), se = FALSE, method ="lm", color = "orange", lwd = 2)


ggplot(dt, aes(x=LoanOriginationYear, y=BorrowerRate)) + 
  geom_line(stat = "summary", fun.y=mean, aes(group=BorrowerRate))

# 
dt1 <- dt[like(LoanStatus, "Past Due"), LoanStatus := "Past Due"]
dt1 <- dt[LoanStatus != "Cancelled"]
ggplot(subset(dt1, StatedMonthlyIncome > 1), aes(x=StatedMonthlyIncome, y=BorrowerRate, color=LoanStatus)) + 
  geom_jitter(alpha = .3) + scale_x_log10()

dt2 <- dt[, CreditScore := as.integer((CreditScoreRangeLower + CreditScoreRangeUpper)/2)]
ggplot(subset(dt2, CreditScore > 10), aes(x=CreditScore, y=BorrowerRate, color=LoanStatus)) + 
  geom_jitter(alpha = .3) + scale_x_log10()


ggplot(subset(dt2, CreditScore > 10), aes(x=LoanOriginalAmount, y=CreditScore, color=LoanStatus)) + 
  geom_jitter(alpha = .3) + scale_x_log10()

# Write out data file
#(player_gamelogs, file = paste0(getwd(), "prosperLoanData_cleaned.csv"), row.names=FALSE)