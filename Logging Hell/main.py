import os
import re
from datetime import datetime


def traverse_dir(path):
    # jos ukletije
    if not hasattr(traverse_dir, "file_count"):
        traverse_dir.file_count = 0

    if not hasattr(traverse_dir, "error_count"):
        traverse_dir.error_count = 0
    
    if not hasattr(traverse_dir, "words"):
        traverse_dir.words = dict()

    with os.scandir(path) as it:
        for entry in it:
            # ako je .logtxt fajl 
            if entry.is_file() and entry.name.endswith('.logtxt'):
                # poziv neki
                traverse_dir.file_count += 1
                # print(entry.name)
                has_error = process_file(entry, traverse_dir.words)
                if has_error:
                    traverse_dir.error_count += 1

            # ako je dir rekurzivni poziv
            if entry.is_dir():
                traverse_dir(entry)
    
    


def process_file(path, words):
    has_error = False
    
    with open(path, 'r') as file:
        for line in file:
            #if line is just whitespace, ignore it
            if not line.strip():
                continue
            date, level, service, msg = process_line(line)

            if level.lower() == 'error':
                has_error = True
            
            # with open('log.txt', 'a') as log:
                # log.write(msg + '\n')

            # print(msg)
            new_words = msg.split()
            # mask = re.compile(r'((\b\w+\b)+)')
            # match = mask.match(msg)
            # new_words = match.groups()
            # print(new_words)
            unique_words = dict()
            for word in new_words:
                # print(word)
                word = word.strip(';.,')
                if word not in unique_words:
                    unique_words[word] = 1
            for word in unique_words:
                if word in words:
                    words[word] += 1
                else:
                    words[word] = 1

    return has_error

def process_line(line):
    # jos ukletije
    if not hasattr(process_line, "line_count"):
        process_line.line_count = 0
        
    process_line.line_count += 1
    date, new_line = get_datetime(line)

    
    # 25.02.2024.10h:59m:36s information PixelPerfectDesign --- API rate limit exceeded
    exp_1 = re.compile(r"([\w -]+) (\w+) --- (.+)")
    match_1 = exp_1.match(new_line)
    if match_1:
        (level, service, msg) = match_1.groups()
        # print(f"{level=}, {service=}, {msg=}")
        return date, level, service, msg 

    # dt=2024-02-25_11:03:38 level=DEBUG service=DevOpsOrchestrator msg=Exiting from a function with a specific return value
    exp_2 = re.compile(r"level=(\w+) service=(\w+) msg=(.+)")
    match_2 = exp_2.match(new_line)
    if match_2:
        (level, service, msg) = match_2.groups()
        # print(f"{level=}, {service=}, {msg=}")
        return date, level, service, msg 
    
    # 25.02.2024.11:05:18 CEF:0|VistaResourceViewer|loglevel=warning msg=Intrusion detection system triggered # type: ignore
    exp_3 = re.compile(r"CEF:0\|(\w+)\|loglevel=(\w+) msg=(.+)")
    match_3 = exp_3.match(new_line)
    if match_3:
        (service, level, msg) = match_3.groups()
        # print(f"{level=}, {service=}, {msg=}")
        return date, level, service, msg 
    

    # [2024-02-25 11:10:31] [info] [EchoTunnelProxy] - Memory leak detected in application
    exp_4 = re.compile(r"\[(\w+)\] \[(\w+)\] \- (.+)")
    match_4 = exp_4.match(new_line)
    if match_4:
        (level, service, msg) = match_4.groups()
        # print(f"{level=}, {service=}, {msg=}")
        return date, level, service, msg 

    # 2024 02 25 11:11:05 PulseFeedbackEngine: <info> New API key generated
    exp_5 = re.compile(r"(\w+): <(\w+)> (.+)")
    match_5 = exp_5.match(new_line)
    if match_5:
        (service, level, msg) = match_5.groups()
        # print(f"{level=}, {service=}, {msg=}")
        return date, level, service, msg 
    
    
    raise Exception('no matches\n' + line)
    
def get_datetime(line):
    # get date
    date_day_first = re.compile(r'(\[|dt=)?(\d{2}).(\d{2}).(\d{4}).{1,2}(\d{2})h?:(\d{2})m?:(\d{2})s?\]? ')
    match_day_first = date_day_first.match(line)

    date_year_first =  re.compile(r'(\[|dt=)?(\d{4}).(\d{2}).(\d{2}).{1,2}(\d{2})h?:(\d{2})m?:(\d{2})s?\]? ')
    match_year_first = date_year_first.match(line)

    if match_day_first is not None:
        (_, day, month, year, hours, minutes, seconds) = match_day_first.groups()
        new_line = line[match_day_first.end():] 
    elif match_year_first is not None:
        (_, year, month, day, hours, minutes, seconds) = match_year_first.groups()
        new_line = line[match_year_first.end():] 
    else:
        raise Exception('no match in line:'+line)

    date = datetime(year=int(year), month=int(month), day=int(day), hour=int(hours), minute=int(minutes), second=int(seconds))
    # print(date)
    return date, new_line

def main():
    path = input()

    traverse_dir(path)
    print(traverse_dir.file_count)
    print(process_line.line_count)
    print(traverse_dir.error_count)
    
    # if len(traverse_dir.words) <= 5:
    # sorted_words = dict(sorted(traverse_dir.words.items()))
    # word_list =  sorted(sorted_words, key = sorted_words.get, reverse=True)
    # print(sorted_words)
    # print(word_list)
    sorted_words = sorted(traverse_dir.words.items(), key=lambda x: (-x[1], x[0]))  
    # for x in sorted(traverse_dir.words.items(), key=lambda x: (-x[1], x[0])):
        # print (x[0], x[1])
    
    words_for_print = []
    for x in sorted_words:
        words_for_print.append(x[0])

    print(*words_for_print[0:5], sep=', ')

    # if len(sorted_words) < 5:
    #     print(*(sorted_words[:][0]), sep=', ')
    # else:
    #     print(*(sorted_words[0][0:5]), sep=', ')

if __name__ == "__main__":
    main()