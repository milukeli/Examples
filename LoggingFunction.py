#open a new file named "message.log" for writing or if the file already exists, rewrite it
log_file = open("message.log","w+")

#function write_log() which takes string as input argument, writes it to a file and prints it. 
#Function returns default value of NONE (return can be ommited).
def write_log(*args):
    line = ' '.join([str(a) for a in args])
    log_file.write(line+'\n')
    print(line)
    return

write_log("This is line 1 of the output")

write_log("This is line 2 of the output")

write_log("This is line 3 of the output")

sometext = "final line"

write_log("This is " + sometext + " of the output")

#close the file
log_file.close()