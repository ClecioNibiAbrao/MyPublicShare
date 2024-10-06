# PYTHON + PANDAS

# year to date
MaskYTD = (
    (dfTESTE['date'].dt.year == max(dfTESTE['date'].dt.date).year) &
    (dfTESTE['date'].dt.date <= max(dfTESTE['date'].dt.date))
    )    
dfTESTE['pd_YTD'] = MaskYTD.astype(int)


# year to date YESTERDAY
MaskYTDyest = (
    (dfTESTE['date'].dt.year == max(dfTESTE['date'].dt.date).year) &
    (dfTESTE['date'].dt.date < max(dfTESTE['date'].dt.date))
    )    

dfTESTE['pd_YTDyesterday'] = MaskYTDyest.astype(int)


# year to date LAST YEAR
MaskLastYearYTD = (
    (dfTESTE['date'].dt.year 
         == max(dfTESTE['date'].dt.date + rd.relativedelta(years=-1) ).year)  &
    (dfTESTE['date'].dt.date
     <= max(dfTESTE['date'].dt.date + rd.relativedelta(years=-1) ))
    )    

dfTESTE['pd_LastYearYTD'] = MaskLastYearYTD.astype(int)


# year to date LAST YEAR YESTERDAY
MaskLastYearYTDyest = (
    (dfTESTE['date'].dt.year 
         == max(dfTESTE['date'].dt.date + rd.relativedelta(years=-1) ).year)  &
    (dfTESTE['date'].dt.date
     < max(dfTESTE['date'].dt.date + rd.relativedelta(years=-1) ))
    )    

dfTESTE['pd_LastYearYTDyesterday'] = MaskLastYearYTDyest.astype(int)


# month to date
MaskMTD = (
    (dfTESTE['date'].dt.year == max(dfTESTE['date'].dt.date).year) &
    (dfTESTE['date'].dt.month == max(dfTESTE['date'].dt.date).month) &
    (dfTESTE['date'].dt.date <= max(dfTESTE['date'].dt.date))
    )    

dfTESTE['pd_MTD'] = MaskMTD.astype(int)



# month to date YESTERDAY
MaskMTyest = (
    (dfTESTE['date'].dt.year == max(dfTESTE['date'].dt.date).year) &
    (dfTESTE['date'].dt.month == max(dfTESTE['date'].dt.date).month) &
    (dfTESTE['date'].dt.date < max(dfTESTE['date'].dt.date))
    )    
dfTESTE['pd_MTDyesterday'] = MaskMTyest.astype(int)



# month to date LY
MaskMTDlastyear = (
    (dfTESTE['date'].dt.year 
         == max(dfTESTE['date'].dt.date + rd.relativedelta(years=-1) ).year)  &
    (dfTESTE['date'].dt.month 
        == max(dfTESTE['date'].dt.date + rd.relativedelta(years=-1) ).month) &
    (dfTESTE['date'].dt.date 
         <= max(dfTESTE['date'].dt.date + rd.relativedelta(years=-1) ))
    )    

dfTESTE['pd_MTD_LY'] = MaskMTDlastyear.astype(int)



# month to date LY yesterday
MaskMTyestlastyear = (
    (dfTESTE['date'].dt.year
     == max(dfTESTE['date'].dt.date + rd.relativedelta(years=-1) ).year)  &
    (dfTESTE['date'].dt.month 
     == max(dfTESTE['date'].dt.date + rd.relativedelta(years=-1) ).month) &
    (dfTESTE['date'].dt.date 
     < max(dfTESTE['date'].dt.date + rd.relativedelta(years=-1) ))
)    
dfTESTE['pd_MTDyesterday_LY'] = MaskMTyestlastyear.astype(int)


# MTD LAST MONTH
MaskLastMonth = (
    (dfTESTE['date'].dt.month 
        == max(dfTESTE['date'].dt.date + rd.relativedelta(months=-1) ).month) &
    (dfTESTE['date'].dt.date 
         <= max(dfTESTE['date'].dt.date + rd.relativedelta(months=-1) ))
    )    

dfTESTE['pd_MTD_LM'] = MaskLastMonth.astype(int)



# MTD LAST MONTH yesterday
MaskLastMonthYes = (
    (dfTESTE['date'].dt.month 
     == max(dfTESTE['date'].dt.date + rd.relativedelta(months=-1) ).month) &
    (dfTESTE['date'].dt.date 
     < max(dfTESTE['date'].dt.date + rd.relativedelta(months=-1) ))
    )    
dfTESTE['pd_MTDyesterday_LM'] = MaskLastMonthYes.astype(int)
