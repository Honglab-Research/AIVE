import subprocess

print('작업 시작!')

proc = subprocess.Popen(['test.bat',], stdout=subprocess.PIPE)

aaa = locals()['proc']
  


print(aaa.poll())

#print(proc.poll())

#print(proc.returncode)

#print('지금은 작업중')