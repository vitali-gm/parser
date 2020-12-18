import csv

def read_avtors():
    with open('files/avtors.csv', newline='') as csvfile:
        lists = []
        spamreader = csv.reader(csvfile, delimiter=';')
        for row in spamreader:
            lists.append(row)
        return lists

def get_unique_lists(lists):
    unique_lists = []

    count = 0
    for item in lists:
        if count > 0:
            if item in unique_lists:
                continue
            else:
                unique_lists.append(item)
        count += 1
    return unique_lists



lists = read_avtors()
unique_lists = get_unique_lists(lists)


with open('files/avtors_unique.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file, delimiter=';')
    headers_file = [
        'fullname',
        'birthday',
        'text'
    ]
    for i in range(10):
        headers_file.append('thumbnail' + str(i + 1))
    writer.writerow(headers_file)

    for item in unique_lists:
        writer.writerow(item)


