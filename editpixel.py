
def edit_pixel(x,y, r,g,b, canvas:list, width=100):
    canvas[((y * (width * 4)) + (x * 4)) + 0] = r
    canvas[((y * (width * 4)) + (x * 4)) + 1] = g
    canvas[((y * (width * 4)) + (x * 4)) + 2] = b

