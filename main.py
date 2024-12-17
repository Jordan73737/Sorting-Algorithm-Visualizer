import pygame
import random
import math
pygame.init()

# Width adjusted based on number of bars
# Height adjusted based on range of values in the list

class DrawInformation:
    BLACK = 0, 0, 0
    WHITE = 255, 255, 255
    GREEN = 0 , 255 , 0
    RED = 255, 0, 0
    GREY = 128, 128, 128
    BACKGROUND_COLOUR = WHITE

    # shades of grey for the bars
    GRADIENTS = [
        (128, 128, 128),
        (160, 160, 160),
        (192, 192, 192)
    ]

    FONT = pygame.font.SysFont('comicsans', 20)
    LARGE_FONT = pygame.font.SysFont('comicsans', 30)

    # padding on the top/left/right, so bars aren't touching edges
    SIDE_PAD = 100 # 50 pixels on left and right
    TOP_PAD = 150 # pixels above the graph

    def __init__ (self, width, height, lst):
        self.width= width
        self.height = height

        self.window = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Sorting Algorithm Visualizer")
        self.set_list(lst)

    def set_list(self, lst):
        self.lst = lst # to store list internally
        self.min_val = min(lst) # min number in list
        self.max_val = max(lst) # max number in list

        # width of screen - side pad divided by the number of blocks in the list
        self.block_width = round((self.width - self.SIDE_PAD) / len(lst))
        # total drawable area divided by number of values in the range determines height of one block
        self.block_height = math.floor((self.height - self.TOP_PAD) / (self.max_val - self.min_val))
        #start drawing blocks on x coordinate (top left hand corner is 0,0 for pygame)
        self.start_x = self.SIDE_PAD // 2 # start at bottom of the screen

    
def generate_starting_list(n, min_val, max_val):
    # n = number of elements we want in our starting list
    # min = minimum possible value 
    # max = maximum possible value
    lst = []

    for _ in range(n):
        val = random.randint(min_val, max_val) # Make random value between min-max
        lst.append(val) 
    return lst
    
def draw(draw_info, algo_name, ascending):
    draw_info.window.fill(draw_info.BACKGROUND_COLOUR) # makes the draw_info called in main to have white background colour which was defined above
    
    # displays current sorting algorithm and whether its asc or desc
    title = draw_info.LARGE_FONT.render(f"{algo_name} - {'Ascending' if ascending else 'Descending'}", 1, draw_info.BLACK)
    draw_info.window.blit(title, (draw_info.width/2 - title.get_width()/2, 5)) # centres text relative to screen width / 2, using text width / 2
    
    # writes controls onto screen by using .Font.render and windows.blit
    controls = draw_info.FONT.render("R - Reset | A - Ascending | D - Descending", 1, draw_info.GREY)
    draw_info.window.blit(controls, (draw_info.width/2 - controls.get_width()/2, 50)) # centres text relative to screen width / 2, using text width / 2
    
    sorting = draw_info.FONT.render("B - Bubble Sort | H - Heap Sort | I - Insertion | L - Shell Sort | M - Merge Sort | Q - Quick Sort | S - Selection Sort", 1, draw_info.GREY)
    draw_info.window.blit(sorting, (draw_info.width/2 - sorting.get_width()/2, 85)) # 30 pixels below controls
    
    # START SORTING
    start = draw_info.FONT.render("Press Space to start! ", 1, draw_info.RED)
    draw_info.window.blit(start, (draw_info.width/2 - start.get_width()/2, 115)) 

    draw_list(draw_info)
    pygame.display.update()


def draw_list(draw_info, colour_positions={}, clear_bg=False):
    lst = draw_info.lst

    # to only re - render the algorthm section and leave the control strings there constantly, rather than re-rendering the entire page
    if clear_bg:
        clear_rect = (draw_info.SIDE_PAD//2, draw_info.TOP_PAD, 
                        draw_info.width - draw_info.SIDE_PAD, draw_info.height - draw_info.TOP_PAD)
        pygame.draw.rect(draw_info.window, draw_info.BACKGROUND_COLOUR, clear_rect)

    for i, val in enumerate(lst):
        x = draw_info.start_x + i * draw_info.block_width
        y = draw_info.height - (val - draw_info.min_val) * draw_info.block_height
        colour = draw_info.GRADIENTS[i % 3] 

        if i in colour_positions:
            colour = colour_positions[i]

        pygame.draw.rect(draw_info.window, colour, (x, y, draw_info.block_width, draw_info.height))

    if clear_bg:
        pygame.display.update()

def bubble_sort(draw_info, ascending=True): # allows you to do asc/desc since its a parameter
    lst = draw_info.lst # so I don't have to write out draw_info.lst repeatedly

    for i in range(len(lst) - 1): # -1 since we start from 0 in code
        for j in range(len(lst) - 1 - i): 
            num1 = lst[j]
            num2 = lst[j + 1]

            if (num1 > num2 and ascending) or (num1 < num2 and not ascending):
                lst[j], lst[j + 1 ] = lst[j + 1], lst[j] # swaps values in array without using temp variable
                draw_list(draw_info, {j: draw_info.GREEN, j + 1: draw_info.RED}, True)
                yield True # geneator to pause halfway through function 
    return lst


def insertion_sort(draw_info, ascending=True): 
    lst = draw_info.lst 

    for i in range(1, len(lst)): 
        current = lst[i]

        while True:
            ascending_sort = i > 0 and lst[i - 1] > current and ascending
            descending_sort = i > 0 and lst[i - 1] < current and not ascending

            if not ascending_sort and not descending_sort:
                break

            lst[i] = lst[i - 1]
            i = i - 1
            lst[i] = current
            draw_list(draw_info, {i: draw_info.GREEN, i - 1: draw_info.RED}, True)
            yield True
    return lst

def selection_sort(draw_info, ascending=True):
    lst = draw_info.lst

    for i in range(len(lst)):
        min_max_idx = i

        for j in range(i + 1, len(lst)):
            if (lst[j] < lst[min_max_idx] and ascending) or (lst[j] > lst[min_max_idx] and not ascending):
                min_max_idx = j

        lst[i], lst[min_max_idx] = lst[min_max_idx], lst[i]
        draw_list(draw_info, {i: draw_info.GREEN, min_max_idx: draw_info.RED}, True)
        yield True
    return lst
       

def quick_sort(draw_info, ascending=True, low=0, high=None):
    if high is None:
        high = len(draw_info.lst) - 1

    def partition(low, high):
        lst = draw_info.lst
        pivot = lst[high]
        i = low - 1

        for j in range(low, high):
            if (lst[j] < pivot and ascending) or (lst[j] > pivot and not ascending):
                i += 1
                lst[i], lst[j] = lst[j], lst[i]
                draw_list(draw_info, {i: draw_info.GREEN, j: draw_info.RED}, True)
                yield True

        lst[i + 1], lst[high] = lst[high], lst[i + 1]
        draw_list(draw_info, {i + 1: draw_info.GREEN, high: draw_info.RED}, True)
        yield True
        return i + 1

    if low < high:
        partition_index = yield from partition(low, high)
        yield from quick_sort(draw_info, ascending, low, partition_index - 1)
        yield from quick_sort(draw_info, ascending, partition_index + 1, high)
    return draw_info.lst



def heap_sort(draw_info, ascending=True):
    def heapify(n, i):
        lst = draw_info.lst
        largest = smallest = i
        left = 2 * i + 1
        right = 2 * i + 2

        if left < n and ((lst[left] > lst[largest] and ascending) or (lst[left] < lst[largest] and not ascending)):
            largest = left

        if right < n and ((lst[right] > lst[largest] and ascending) or (lst[right] < lst[largest] and not ascending)):
            largest = right

        if largest != i:
            lst[i], lst[largest] = lst[largest], lst[i]
            draw_list(draw_info, {i: draw_info.GREEN, largest: draw_info.RED}, True)
            yield True
            yield from heapify(n, largest)

    lst = draw_info.lst
    n = len(lst)

    for i in range(n // 2 - 1, -1, -1):
        yield from heapify(n, i)

    for i in range(n - 1, 0, -1):
        lst[i], lst[0] = lst[0], lst[i]
        draw_list(draw_info, {i: draw_info.GREEN, 0: draw_info.RED}, True)
        yield True
        yield from heapify(i, 0)
    return lst


def shell_sort(draw_info, ascending=True):
    lst = draw_info.lst
    gap = len(lst) // 2

    while gap > 0:
        for i in range(gap, len(lst)):
            current = lst[i]
            j = i

            while j >= gap and ((lst[j - gap] > current and ascending) or (lst[j - gap] < current and not ascending)):
                lst[j] = lst[j - gap]
                j -= gap

            lst[j] = current
            draw_list(draw_info, {j: draw_info.GREEN, i: draw_info.RED}, True)
            yield True

        gap //= 2
    return lst


# Merge sort is an Out-Of-Place method - as it repeatedly splits the list into two sublists
# Making it more memory intensive 
def merge_sort(draw_info, ascending=True, start=0, end=None):
    if end is None:
        end = len(draw_info.lst)

    if end - start > 1:
        mid = (start + end) // 2

        yield from merge_sort(draw_info, ascending, start, mid)
        yield from merge_sort(draw_info, ascending, mid, end)

        yield from merge(draw_info, ascending, start, mid, end)
    return draw_info.lst

def merge(draw_info, ascending, start, mid, end):
    lst = draw_info.lst
    left = lst[start:mid]
    right = lst[mid:end]

    i = j = 0
    for k in range(start, end):
        if i < len(left) and (j >= len(right) or 
                              (left[i] < right[j] and ascending) or 
                              (left[i] > right[j] and not ascending)):
            lst[k] = left[i]
            i += 1
        else:
            lst[k] = right[j]
            j += 1

        draw_list(draw_info, {k: draw_info.GREEN}, True)
        yield True




#Pygame Event Loop - Allows to click the X button and draw list on the screen
def main():
    run = True
    clock = pygame.time.Clock() # Regulates how quickly loop can run 
    
    n = 50
    min_val = 0
    max_val = 100
    lst = generate_starting_list(n, min_val, max_val)
    draw_info = DrawInformation(1200, 800, lst)
    sorting = False
    ascending = True

    sorting_algorithm = bubble_sort
    sorting_algo_name = "Bubble Sort"
    sorting_algorithm_geneator = None

    # Loop to handle events occuring
    while run:
        clock.tick(60) # max number of times loop can run per second

        if sorting:
            try:
                next(sorting_algorithm_generator)
            except StopIteration:
                sorting = False
        if not sorting:  # Only draw when sorting is not active
            draw(draw_info, sorting_algo_name, ascending)



        for event in pygame.event.get(): #Returns list of events that occured since last loop
            if event.type == pygame.QUIT: # Clicking the red X in the top right corner
                run = False
            if event.type != pygame.KEYDOWN: # when no keys pressed, go to next event
                continue
            if event.key == pygame.K_r: # when pressed, make new random lst with diff min and max values
                lst = generate_starting_list(n, min_val, max_val)
                draw_info.set_list(lst)
                sorting == False # reset causes sorting to be back to 0 
            
            elif event.key == pygame.K_SPACE and sorting == False: # allows you to sort by making sorting = True
                sorting = True 
                sorting_algorithm_generator = sorting_algorithm(draw_info, ascending)
            elif event.key == pygame.K_a and not sorting: 
                ascending = True 
            elif event.key == pygame.K_d and not sorting:
                ascending = False
            elif event.key == pygame.K_i and not sorting:
                sorting_algorithm = insertion_sort
                sorting_algo_name = "Insertion Sort"
            elif event.key == pygame.K_b and not sorting:
                sorting_algorithm = bubble_sort
                sorting_algo_name = "Bubble Sort"
            elif event.key == pygame.K_s and not sorting:
                sorting_algorithm = selection_sort
                sorting_algo_name = "Selection Sort"
            elif event.key == pygame.K_q and not sorting:
                sorting_algorithm = quick_sort
                sorting_algo_name = "Quick Sort"
            elif event.key == pygame.K_h and not sorting:
                sorting_algorithm = heap_sort
                sorting_algo_name = "Heap Sort"
            elif event.key == pygame.K_l and not sorting:
                sorting_algorithm = shell_sort
                sorting_algo_name = "Shell Sort"
            elif event.key == pygame.K_m and not sorting:
                sorting_algorithm = merge_sort
                sorting_algo_name = "Merg Sort"

    pygame.quit() # When while loop breaks it ends the program

# Makes sure we run the module by clicking the run button
if __name__ == "__main__":
    main()















