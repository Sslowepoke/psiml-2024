
# zahtevi 
- A) calculate the total number of .logtxt files
- B) calculate the total number of log entries inside ".logtxt" files
- C) calculate the number of ".logtxt" files that have at least 1 error entry
- D) calculate the 5 most common words that appear int the message body of each log entry at least once. (You need to deduce what exactly is the message body in different log formats based on the given files).
- E) Find the longest period of time (in seconds) with at most 5 Warning log entries from the earliest warning log entry date to the latest warning log entry date. (You will need to how the dates and Warning log entries are described in different log formats based on the given files). Note: Consider warning entries from all files!




# the plan
## prolazenje kroz file tree i otvaranje svih .logtxt fajlova
- rekurzivno prolazi trenutni dir
- ako ima .logtxt fajlova poziva nad njima odgovarajucu funkciju / stavlja ih u dict?
takodje broji koliko ih je
- ako ima dir poziva sebe na taj dir

## obrada .logtxt fajla
- broji linije
- da li je komanda error? ako jeste dodaj na error count
  - skontati sta je tacno message body i koji od njih su error
- 


## obrada komande
da li je razumno pretpostaviti da nece biti novih formata
da li format datuma govori i o formatu ostatka komande i da li to treba da mi znaci nes?

### svi moguci formati datuma 
25.02.2024.10h:59m:36s
dt=2024-02-25_11:03:38
25.02.2024.11h:05m:07s
25.02.2024.11:05:18
[2024-02-25 11:10:31] 
2024 02 25 11:11:05 

### message formats
1.
/datetime /level /service --- /msg
25.02.2024.10h:59m:36s information PixelPerfectDesign --- API rate limit exceeded

2.
dt=/datetime level=/level service=/service msg=/msg
dt=2024-02-25_11:03:38 level=DEBUG service=DevOpsOrchestrator msg=Exiting from a function with a specific return value

3.
/datetime CEF:0|/service|loglevel=/level msg=/msg
25.02.2024.11:05:18 CEF:0|VistaResourceViewer|loglevel=warning msg=Intrusion detection system triggered

4.
[/datetime] [/level] [/service] - /msg
[2024-02-25 11:10:31] [info] [EchoTunnelProxy] - Memory leak detected in application

5.
/datetime /service: </level> /msg
2024 02 25 11:11:05 PulseFeedbackEngine: <info> New API key generated


error je markovan kao level