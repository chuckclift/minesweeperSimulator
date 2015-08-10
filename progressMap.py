#!/usr/bin/python3

import time

def status_bar(function, iterable, status_label="status"):
    return_list = []
    previous = 0
    for i,val in enumerate(iterable):
        return_list.append(function(val))
        percent = round(i / len(iterable), 1)
        out_of_ten = int(10 * percent)
        if out_of_ten != previous:
            bar =  "=" * (out_of_ten - 1) + ">" 
            space = " " * (10-out_of_ten)
            print("\r" + status_label +  " [" +bar + space  + "]" , end=" ")
        previous = out_of_ten
    print("")
    return return_list

if __name__ == "__main__":
    values = status_bar(lambda x: x**2, range(1000000),
                        status_label="calculating squares")
    values = status_bar(lambda x: x**3, range(1000000),
                         status_label="calculating cubes")

