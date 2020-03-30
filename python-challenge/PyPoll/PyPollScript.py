# In this challenge, you are tasked with helping a small, rural town modernize its vote-counting process.
# You will be give a set of poll data called election_data.csv. The dataset is composed of three columns: Voter ID, County, and Candidate. 
# Your task is to create a Python script that analyzes the votes and calculates each of the following:
# The total number of votes cast
# A complete list of candidates who received votes
# The percentage of votes each candidate won
# The total number of votes each candidate won
# The winner of the election based on popular vote.

#Necessary variables: VoteCount, CandidateList, VoteCountList

# Import necessary libraries
import os
import csv

# Define the new variables
candidateList = []
voteCount = 0
mostVotes = 0
mostVotesCandidate = ''

# Create the file path variable
vote_path = os.path.join("Resources", "election_data.csv")

# Import an iterator for the file to read the data
with open(vote_path) as csvfile:
    csv_reader = csv.reader(csvfile, delimiter=",")

    # Skip the headers
    header = next(csv_reader)

    # Read through each row of data after the header
    for row in csv_reader:
        voteCount += 1
        if row[2] in candidateList:
            candIndex = candidateList.index(row[2])
            candidateList[candIndex+1] += 1
        else:
            candidateList.append(row[2])
            candidateList.append(1)

# Print the summary
print("Election Results")
print("-------------------------")
print("Total Votes: " + str(voteCount))
print("-------------------------")
for i in range(0,len(candidateList),2):
  print(f"{candidateList[i]}: {(candidateList[i+1]/voteCount)*100}% ({candidateList[i+1]})")
  if candidateList[i+1]>mostVotes:
      mostVotes = candidateList[i+1]
      mostVotesCandidate = candidateList[i]
print("-------------------------")
print("Winner: " + mostVotesCandidate)
print("-------------------------")

# Write the summary to .csv file
output_path = os.path.join("voteSummary.csv")

# Open the file using "write" mode. Specify the variable to hold the contents
with open(output_path, 'w', newline='') as csvfile:

    # Initialize csv.writer
    csvwriter = csv.writer(csvfile, delimiter=',')
    rows = []
    rows.append(["Election Results"])
    rows.append(["-------------------------"])
    rows.append(["Total Votes: " + str(voteCount)])
    rows.append(["-------------------------"])
    for i in range(0,len(candidateList),2):
        rows.append([candidateList[i] + ": " + str((candidateList[i+1]/voteCount)*100) + "% (" + str(candidateList[i+1]) + ")"])
    rows.append(["-------------------------"])
    rows.append(["Winner: " + mostVotesCandidate])
    rows.append(["-------------------------"])
    
    
    for row in rows:
        csvwriter.writerow(row)