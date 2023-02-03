from os import listdir as ld
from os import getcwd as getcwd
from os import rename as re_name
from math import sqrt
import matplotlib.pyplot as plt

#Главная функция
def main():
    retyping()
    data = fitting_data(reading())
    medium_voltage, medium_current = medium(data)
    time = data[0][0]
    deviation_voltage,deviation_current = deviation(data, medium_voltage, medium_current)
    plotting(time, deviation_voltage, medium_voltage)
    plotting(time, deviation_current, medium_current)


#Рисование графика
def plotting(y, x1, x2):
    plt.plot(y, x1, y, x2)
    plt.legend(['Deviation', 'Medium'])
    plt.show()

#Переформатирование из .dat в .txt
def retyping():
    old_type = 'dat'
    new_type = '.txt'
    print(f'Retyping from .{old_type} to {new_type}...')
    for filename in ld("."):
        if filename.split('.')[-1] == old_type:
            new_fname = filename.split('.')[0] + new_type
            re_name(filename, new_fname.replace(' ',''))
    print('Done!')

#Для корректного суммирования чисел с двумя знаками после запятой
def summing_floats(result, value):
    return (int(float(result)*100)+int(float(value)*100))/100
    
#Возвращает индекс минимальной длины массива времени
def min_time_len(struct): 
    minlen = len(struct[0][0])
    index = 0
    for i in range(len(struct)):
        if len(struct[i][0]) < minlen:
            index = i
            minlen = len(struct[i][0])
    return index

#Срезаем лишние длины массива, подгоняя под минимальный размер
def fitting_data(data):
    print('fitting data...')
    min_time = data[min_time_len(data)]
    for file in data:
        n = 0
        while len(file[0]) > len(min_time[0]):
            try:
                if file[0][n] != min_time[0][n]:
                    file[0].pop(n)
                    file[1].pop(n)
                    file[2].pop(n)
                else:
                    n += 1
            except IndexError:
                print(f' INDEXERROR! len of current file = {len(file[0])}')
                print('BREAKED the loop')
                break
    print('Fitting finished! ')
    return data



#Сюда считываем вообще все данные обо всех экспериментах в папке
def reading():
    path = ld(".")
    data = []
    postfix = 'txt'
    print(f'Start reading .{postfix.upper()} files from {getcwd()}...')
    filelist = [i for i in path if i.split(".")[-1] == postfix]
    for file in filelist:
        print(file)
        #Каждый раз создаём новые массивы под данные,
        #которые в конце объединим в tuple и засунем в data
        time, current, voltage = [], [], []
        with open(file, 'r') as opening:
            f = [i.replace(",", '.') for i in opening]
            max_time = 0
            for ind, string in enumerate(f):
                cur_str = string.split() #Делим строку на отдельные данные
                if cur_str[0] == 'A:':
                    time.append(round(float(cur_str[1]), 2))
                    if float(f[ind+1].split()[1]) < float(f[ind].split()[1]):
                        max_time = f[ind].split()[1]
                else:
                    time.append(summing_floats(cur_str[1], max_time))
                        
                voltage.append(round(float(cur_str[2]), 2))
                current.append(round(float(cur_str[3]), 2))
            data.append( (time, voltage, current) )
    return data

#Находим среднее значение
def medium(data):
    print('Calculating medium...')
    sum_voltage = data[0][1].copy()
    sum_current = data[0][2].copy()
    len_data = len(data)
    for i in range(1, len_data):
        for j in range(len(data[i][0])):
            sum_voltage[j] += data[i][1][j]
            sum_current[j] += data[i][2][j]
    result_voltage = list(map(lambda x: round(x/len_data, 1), sum_voltage))
    result_current = list(map(lambda x: round(x/len_data, 1), sum_current))
    print('Medium calculated!')
    return result_voltage, result_current


#Считаем отклонение от среднего// В конце к положительному и отрицательному отклонению запихиваем ещё и средние значения
def deviation(data, medium_voltage, medium_current):
    print('Calculating deviation...')
    deviation_voltage = [0 for i in range(len(data[0][0]))]
    deviation_current = [0 for i in range(len(data[0][0]))]
    for i in range(len(data)):
        for j in range(len(data[i][0])):
            deviation_voltage[j] += round((data[i][1][j]-medium_voltage[j])**2, 2)
            deviation_current[j] += round((data[i][2][j]-medium_current[j])**2, 2)
    temp_dev_voltage = list(map(lambda x: sqrt(x/len(data)), deviation_voltage)) #Поделили на количество членов, взяли корень
    temp_dev_current = list(map(lambda x: sqrt(x/len(data)),deviation_current))
    result_dev_voltage = [round(medium_voltage[i]+temp_dev_voltage[i], 1) for i in range(len(medium_voltage))]
    result_dev_current = [round(medium_current[i]+temp_dev_current[i], 1) for i in range(len(medium_current))]
    print('Deviation calculated!')
    #temp_dev_current выводится отклонение вдоль нуля
    #result_dev_current выводится отклонение вдоль графика
    return temp_dev_voltage, temp_dev_current 

if __name__ == '__main__':
    main()
