import sys
sys.path.append('..')

from src.util.Rextester import Rextester


r = Rextester()
try:
    response = r.execute('python3', 'print("test")')
    if response["Errors"] or response["Warnings"] or response["Result"] != "test\n":
        print('test failed', response, sep='\t')
        exit(-1)
except Exception as e:
    print('test failed', e, sep='\t')
    exit(-1)

print('test completed')
exit(0)
