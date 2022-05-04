import csv

def edit_pixel(x,y, r,g,b, canvaspath:str, width=100):
    with open(canvaspath,'r') as csv_file:
        reader = csv.reader(csv_file, delimiter=',')
        listread = list(reader)[0]
        csvlist = list(map(int,listread))

        csvlist[((y * (width * 4)) + (x * 4)) + 0] = r
        csvlist[((y * (width * 4)) + (x * 4)) + 1] = g
        csvlist[((y * (width * 4)) + (x * 4)) + 2] = b

        csv_file.close()

        save_to_csv(csvlist, canvaspath)

def save_to_csv(canvas, canvaspath):
    with open(canvaspath,'w') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(canvas)
