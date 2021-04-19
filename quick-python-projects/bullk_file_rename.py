import os

def main():
    i = 0
    path = 'C:/Users/Martin/Desktop/files/'
    for file in os.listdir(path): # get files in the dir as a list
        dest_filename = 'text ' + str(i+1) + '.txt'
        source_filename = path + file
        dest_filename = path + dest_filename
        os.rename(source_filename, dest_filename)
        i+=1

if __name__ == '__main__':
    main()