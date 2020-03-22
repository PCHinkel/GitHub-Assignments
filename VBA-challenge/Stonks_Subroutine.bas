Attribute VB_Name = "Module1"
Sub Stonks()
    ' Code written by Preston Hinkel on March 22 2020
    
    ' Establishing variables
    ' currentTicker is necessary for the summary and to find when I switch tickers
    ' firstPrice and lastPrice are used to calculate yearly and percent change
    ' currentTickerVolume is used to aggregate the volume
    ' currRow is for looping through all of the data and sumOneRow is for keeping track of the summary row
    ' The "greatest" variables are for the challenge summary (including gI, gD, gD)
        
    Dim currentTicker, gITicker, gDTicker, gVTicker As String
    Dim firstPrice, lastPrice As Double
    Dim currTickerVolume, currRow, sumOneRow As LongLong
    Dim i As Integer
    Dim greatestIncrease, greatestDecrease As Double
    Dim greatestVolume As LongLong
    
    ' looping through every sheet in the workbook
    For i = 1 To ActiveWorkbook.Worksheets.Count
        Worksheets(i).Activate
    ' Establishing the ticker summary headers
        Range("I1").Value = "Ticker"
        Range("J1").Value = "Yearly Change"
        Range("K1").Value = "Percent Change"
        Range("L1").Value = "Total Stock Volume"
        Range("O1").Value = "Ticker"
        Range("P1").Value = "Value"
        Range("N2").Value = "Greatest % Increase"
        Range("N3").Value = "Greatest % Decrease"
        Range("N4").Value = "Greatest Total Volume"
        
    ' Establishing the base case for the first iteration on this worksheet
        currRow = 2
        sumOneRow = 2
        currentTicker = Cells(currRow, 1)
        firstPrice = Cells(currRow, 3)
        lastPrice = 0
        currTicketVolume = 0
        greatestIncrease = 0
        greatestDecrease = 0
        greatestVolume = 0
        gITicker = ""
        gDTicker = ""
        gVTicker = ""
        
        While IsEmpty(Cells(currRow, 1)) = False
    ' Adding the volume to the sum
            currTickerVolume = currTickerVolume + Cells(currRow, 7).Value
    ' Checking if the next line is a ticker switch, if it is then we summarize the current ticker
            If Cells(currRow + 1, 1) <> currentTicker Then
                lastPrice = Cells(currRow, 6)
                Cells(sumOneRow, 9).Value = currentTicker
                Cells(sumOneRow, 10).Value = lastPrice - firstPrice
                If (lastPrice - firstPrice) < 0 Then
                    Cells(sumOneRow, 10).Interior.ColorIndex = 3
                Else
                    Cells(sumOneRow, 10).Interior.ColorIndex = 4
                End If
                If firstPrice <> 0 Then
                    Cells(sumOneRow, 11).Value = (lastPrice - firstPrice) / firstPrice
                    If ((lastPrice - firstPrice) / firstPrice) < greatestDecrease Then
                        greatestDecrease = ((lastPrice - firstPrice) / firstPrice)
                        gDTicker = currentTicker
                    End If
                    If ((lastPrice - firstPrice) / firstPrice) > greatestIncrease Then
                        greatestIncrease = ((lastPrice - firstPrice) / firstPrice)
                        gITicker = currentTicker
                    End If
                Else
                    Cells(sumOneRow, 11).Value = 0
                End If
                Cells(sumOneRow, 12).Value = currTickerVolume
                If currTickerVolume > greatestVolume Then
                    greatestVolume = currTickerVolume
                    gVTicker = currentTicker
                End If
    ' Resetting/redefining variables for the next ticker
                sumOneRow = sumOneRow + 1
                currTickerVolume = 0
                currentTicker = Cells(currRow + 1, 1)
                firstPrice = Cells(currRow + 1, 3)
            End If
            currRow = currRow + 1
        Wend
        Range("O2").Value = gITicker
        Range("O3").Value = gDTicker
        Range("O4").Value = gVTicker
        Range("P2").Value = greatestIncrease
        Range("P3").Value = greatestDecrease
        Range("P4").Value = greatestVolume
    Next i
End Sub
