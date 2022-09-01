import math
import os
import pandas as pd
import base64

from Base64Coder import Base64

fileNames = ['txt1.txt', 'txt2.txt', 'txt3.txt']
Base64Chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/'


def base64_coding(file_name):
    if '.bz2' in file_name:
        with open(file_name, 'rb') as file:
            text = file.read()
            text_bytes = bytearray(text)
    else:
        with open(file_name, 'r', encoding="utf-8") as file:
            text = file.read()
            text_bytes = bytearray(text.encode('utf-8'))

    bs64 = Base64()
    base64_str = bs64.encode(text_bytes)

    if '.bz2' in file_name:
        with open(file_name[:-4] + '_Base64' + file_name[-4:], 'wb') as file:
            file.write(str.encode(base64_str))
    else:
        with open(file_name[:-4] + '_Base64' + file_name[-4:], 'w', encoding="utf-8") as file:
            file.write(base64_str)


def calculations(file_name):

    if '.bz2' in file_name:
        with open(file_name, 'rb') as file:
            text = file.read().decode()
    else:
        with open(file_name, 'r', encoding="utf-8") as file:
            text = file.read()

    alphabet = ''.join(sorted(set(text)))
    # Створюємо словник з статистикою знаходження символів в файлі
    letters = dict.fromkeys(alphabet, 0)
    # Підраховуємо скілки разів кожен символ зустрічається у тексті, пілся чого рахуємо відсоток
    for l in letters.keys():
        letters[l] = text.count(l) / len(text)
    # Створюємо словник, який буде містити розрахунки
    entropy = entropy_calc(list(letters.values()))
    result = {'letters': list(letters),
              'FileName': file_name,
              'TotalCount': len(text),
              'FileSize': os.path.getsize(file_name),
              'Percents': list(letters.values()),
              'Entropy': entropy,
              'InformationAmount': int(entropy * len(text) / 8)}
    return result


def entropy_calc(percents):
    res = 0
    for num in percents:
        if num != 0:
            res = res - (num * math.log2(num))
    return res


def ready_coding(filename):
    with open(filename, 'r', encoding="utf-8") as file:
        text = file.read()

    encoded_text = text.encode('utf-8')
    ready64_str = base64.b64encode(encoded_text)

    with open(filename[:-4] + '_Ready64.txt', 'w', encoding="utf-8") as file:
        file.write(ready64_str.decode("UTF-8"))


def main():
    for item in fileNames:
        ready_coding(item)

    base64_coding(fileNames[0])
    print('File ' + fileNames[0][:-4] + '_Base64.txt' + ' is ready!')
    base64_coding(fileNames[1])
    print('File ' + fileNames[1][:-4] + '_Base64.txt' + ' is ready!')
    base64_coding(fileNames[2])
    print('File ' + fileNames[2][:-4] + '_Base64.txt' + ' is ready!')

    Text1 = calculations(fileNames[0][:-4] + '_Base64.txt')
    Text2 = calculations(fileNames[1][:-4] + '_Base64.txt')
    Text3 = calculations(fileNames[2][:-4] + '_Base64.txt')

    page1 = pd.DataFrame({'indexes': ['Text1', 'Text2', 'Text3'],
                          'File name': [Text1['FileName'], Text2['FileName'], Text3['FileName']],
                          'Total characters': [Text1['TotalCount'], Text2['TotalCount'], Text3['TotalCount']],
                          'File Size(bytes)': [Text1['FileSize'], Text2['FileSize'], Text3['FileSize']]})
    page2 = pd.DataFrame({'Letters': Text1['letters'],
                          'Percents': Text1['Percents']})
    page3 = pd.DataFrame({'Letters': Text2['letters'],
                          'Percents': Text2['Percents']})
    page4 = pd.DataFrame({'Letters': Text3['letters'],
                          'Percents': Text3['Percents']})
    page5 = pd.DataFrame({'indexes': ['Text1', 'Text2', 'Text3'],
                          'Entropy': [Text1['Entropy'], Text2['Entropy'], Text3['Entropy']],
                          'Information amount(bytes)': [Text1['InformationAmount'],
                                                        Text2['InformationAmount'],
                                                        Text3['InformationAmount']]})

    pages_sheets = {'General': page1, 'Text1Percents': page2, 'Text2Percents': page3, 'Text3Percents': page4,
                    'Entropy': page5}
    writer = pd.ExcelWriter('./statistic2.xlsx', engine='xlsxwriter')
    for page_name in pages_sheets.keys():
        pages_sheets[page_name].to_excel(writer, sheet_name=page_name, index=False)
    writer.save()

    print('some')
    # ---------------------- 2.4

    base64_coding(fileNames[0][:-4] + '_Base64.txt.bz2')
    print('File ' + fileNames[0][:-4] + '_Base64.txt_Base64.bz2' + ' is ready!')
    base64_coding(fileNames[1][:-4] + '_Base64.txt.bz2')
    print('File ' + fileNames[1][:-4] + '_Base64.txt_Base64.bz2' + ' is ready!')
    base64_coding(fileNames[2][:-4] + '_Base64.txt.bz2')
    print('File ' + fileNames[2][:-4] + '_Base64.txt_Base64.bz2' + ' is ready!')

    Text1 = calculations(fileNames[0][:-4] + '_Base64.txt_Base64.bz2')
    Text2 = calculations(fileNames[1][:-4] + '_Base64.txt_Base64.bz2')
    Text3 = calculations(fileNames[2][:-4] + '_Base64.txt_Base64.bz2')

    page1 = pd.DataFrame({'indexes': ['Text1', 'Text2', 'Text3'],
                          'File name': [Text1['FileName'], Text2['FileName'], Text3['FileName']],
                          'Total characters': [Text1['TotalCount'], Text2['TotalCount'], Text3['TotalCount']],
                          'File Size(bytes)': [Text1['FileSize'], Text2['FileSize'], Text3['FileSize']]})
    page2 = pd.DataFrame({'Letters': Text1['letters'],
                          'Percents': Text1['Percents']})
    page3 = pd.DataFrame({'Letters': Text2['letters'],
                          'Percents': Text2['Percents']})
    page4 = pd.DataFrame({'Letters': Text3['letters'],
                          'Percents': Text3['Percents']})
    page5 = pd.DataFrame({'indexes': ['Text1', 'Text2', 'Text3'],
                          'Entropy': [Text1['Entropy'], Text2['Entropy'], Text3['Entropy']],
                          'Information amount(bytes)': [Text1['InformationAmount'],
                                                        Text2['InformationAmount'],
                                                        Text3['InformationAmount']]})

    pages_sheets = {'General': page1, 'Text1Percents': page2, 'Text2Percents': page3, 'Text3Percents': page4,
                    'Entropy': page5}
    writer = pd.ExcelWriter('./statistic3.xlsx', engine='xlsxwriter')
    for page_name in pages_sheets.keys():
        pages_sheets[page_name].to_excel(writer, sheet_name=page_name, index=False)
    writer.save()


if __name__ == "__main__":
    main()
