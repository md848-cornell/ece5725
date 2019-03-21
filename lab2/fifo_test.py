

def main():
    while True:
        inp = raw_input("mplayer input:")
        if len(inp) == 1 and (inp in 'pq'):
            #write to file
            f = open('video_fifo','w')
            f.write(inp + '\n')
            f.close()
        elif inp == '*':
            f = open('video_fifo','w')
            f.write('volume 10' + '\n')
            f.close()
        elif inp == '/':
            f = open('video_fifo','w')
            f.write('volume -10' + '\n')
            f.close()
        else:
            print 'invalid input:' + inp
        if inp == 'q':
            f.close()
            return


main()
