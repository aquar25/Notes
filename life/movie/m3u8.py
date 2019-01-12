# -*- coding:utf-8 -*- 
import os
import sys

'''
rename all the files in the folder under windows
`>ren * *.ts`
'''

def get_index(user_path):
    '''list all the file of m3u8 file and sort the file with 0 1 2..
    make sure all the files in the path are video file 
    '''
    dirlist = os.listdir(user_path)
    numNames = []
    extStr = ''
    if len(dirlist) > 0 and dirlist[0].endswith('.ts'):
        extStr = '.ts'
        for one in dirlist:
            fileName,_ = os.path.splitext(os.path.basename(one))
            numNames.append(fileName)
    else:
        numNames = dirlist
    index = [ int(num) for num in numNames]    
    index = sorted(index)

    sortedNames = [ str(idx)+extStr for idx in index]
    return sortedNames

def convert_m3u8(index, output):
    '''use the copy /b file1+file2+...+fileN outputfile to merge the video file'''
    tmp = [item for item in index]
    cmd_str = '+'.join(tmp)
    exec_str = "copy /b " + cmd_str + " " + output
    print(exec_str)
    os.system(exec_str)
        
def work(user_path, output):
    index = get_index(user_path)
    os.chdir(user_path)
    # the cmd cant be too long, so merge part of the file and then merge the parts
    total = len(index)
    max_file_num = 1000
    part = int(total/max_file_num) + 1
    tmpOutput = []
    for x in range(0, part):
        tmp = str('part'+str(x))
        tmpOutput.append(tmp)
        convert_m3u8(index[x*max_file_num : (x+1)*max_file_num], tmp)

    print(tmpOutput)
    convert_m3u8(tmpOutput, output)
    # delete the tmp part files
    [ os.remove(tmpfile) for tmpfile in tmpOutput]

if __name__ == '__main__':
    argn = len(sys.argv)
    if argn == 3:
        path, outputfile = sys.argv[1:]
        work(path, outputfile)