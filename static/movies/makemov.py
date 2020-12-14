import os 

os.system('rm *.webm')

for m in '_VHI _spi_03 _spi_06'.split():
    cmd = "ffmpeg -framerate 1 -pattern_type glob -i '../plotdata/*"+m+".png'  -r 30 -c:v vp9 -pix_fmt yuva420p m"+m+".webm"
    os.system(cmd)
    
    print(cmd)