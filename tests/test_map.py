from sqletic import merge, product

def test_merge_scope():
    scope = {'as': {}}
    
    for entry in ({'a':0, 'b':None, 'qw':(1, 2)}, {'a':1, 'b':True}):
        print('inner scope:', merge(scope, 'realm', entry))
    
    print('outer scope:', scope)

def test_product():
    for scope in product({'realm': ({'a':0, 'b':None, 'qw':(1, 2)}, {'a':1, 'b':True}),
                         'citizen': ({'c':0, 'd':None, 'er':(1, 2)}, {'c':1, 'd':True})}):
        print(scope)
    
def main():
    test_merge_scope()
    test_product()
