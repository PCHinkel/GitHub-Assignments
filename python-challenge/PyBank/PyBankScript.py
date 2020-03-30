#Your task is to create a Python script that analyzes the records to calculate each of the following:
#The total number of months included in the dataset
#The net total amount of "Profit/Losses" over the entire period
#The average of the changes in "Profit/Losses" over the entire period
#The greatest increase in profits (date and amount) over the entire period
#The greatest decrease in losses (date and amount) over the entire period

#Necessary variables: MonthCount, Sum of Profit/Losses, Month Over Month difference (to calculate average, max, min), Max Date, Min Date

# Import necessary libraries
import os
import csv

# Define the new variables
monthCount = 0
totalPNL = 0.0
lastMonth = 0.0
thisMonth = 0.0
monDiff = 0.0
monDiffTotal = 0.0
maxAmount = 0.0
minAmount = 0.0
maxDate = ''
minDate = ''

# Create the file path variable
bank_path = os.path.join("Resources", "budget_data.csv")

# Import an iterator for the file to read the data
with open(bank_path) as csvfile:
    csv_reader = csv.reader(csvfile, delimiter=",")

    # Skip the headers
    header = next(csv_reader)

    # Read through each row of data after the header
    for row in csv_reader:
        monthCount += 1
        totalPNL += float(row[1])
        if monthCount > 1:
            lastMonth = thisMonth
            thisMonth = float(row[1])
            monDiff = thisMonth - lastMonth
            monDiffTotal += monDiff
            if monDiff > maxAmount:
                maxAmount = monDiff
                maxDate = row[0]
            if monDiff < minAmount:
                minAmount = monDiff
                minDate = row[0]
        else:
            thisMonth = float(row[1])

# Calculate the average change
avgChange = monDiffTotal / (monthCount-1)

# Print the summary
print("Financial Analysis")
print("----------------------------")
print(f"Total Months: {monthCount}")
print(f"Total: ${totalPNL}")
print(f"Average  Change: ${avgChange}")
print(f"Greatest Increase in Profits: {maxDate} (${maxAmount})")
print(f"Greatest Decrease in Profits: {minDate} (${minAmount})")

# Write the summary to .txt file
output_path = os.path.join("bankSummary.csv")

# Open the file using "write" mode. Specify the variable to hold the contents
with open(output_path, 'w', newline='') as csvfile:

    # Initialize csv.writer
    csvwriter = csv.writer(csvfile, delimiter=',')
    rows = [["Financial Analysis"],
    ["----------------------------"],
    ["Total Months: " + str(monthCount)],
    ["Total: $" + str(totalPNL)],
    ["Average  Change: $" + str(avgChange)],
    ["Greatest Increase in Profits: " + maxDate + " ($" + str(maxAmount) + ")"],
    ["Greatest Decrease in Profits: " + minDate + " ($" + str(minAmount) + ")"]]
    for row in rows:
        csvwriter.writerow(row)