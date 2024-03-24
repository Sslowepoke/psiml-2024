import os
import re
from datetime import datetime


def traverse_dir(path):
    file_count = 0
    error_count = 0
    line_count = 0
    words = dict()

    for root, dirs, files in os.walk(path):
        for name in files:
            if name.endswith('.logtxt'):
                file_count += 1
                has_error, temp_line_count = process_file(os.path.join(root, name), words)
                line_count += temp_line_count
                if has_error:
                    error_count += 1 

    return file_count, line_count, error_count, words


def process_file(path, words):
    has_error = False
    line_count = 0
    
    with open(path, 'r') as file:
        for line in file:
            #if line is just whitespace, ignore it
            if not line.strip():
                continue
            date, level, service, msg = process_line(line)
            line_count += 1

            if 'error' in level.lower() or 'err' in level.lower():
                has_error = True
            
            # with open('log.txt', 'a') as log:
                # log.write(msg + '\n')

            # print(msg)
            new_words = msg.split()
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

    return has_error, line_count

def process_line(line):
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
        # raise Exception('no match in line:'+line)
        return None

    date = datetime(year=int(year), month=int(month), day=int(day), hour=int(hours), minute=int(minutes), second=int(seconds))
    # print(date)
    return date, new_line

def main():
    path = input()

    # with open('log.txt', 'w') as log:
        # log.write('')


    file_count, line_count, error_count, words = traverse_dir(path)
    print(file_count)
    print(line_count)
    print(error_count)
    sorted_words = sorted(words.items(), key=lambda x: (-x[1], x[0])) 
    
    # for x in sorted(words.items(), key=lambda x: (-x[1], x[0])):
        # print (x[0], x[1])
    
    words_for_print = []
    for x in sorted_words:
        words_for_print.append(x[0])

    print(*words_for_print[0:5], sep=', ')

if __name__ == "__main__":
    main()