"""
Dependencies:
https://github.com/dgrtwo/ParsePy

Install:
pip install git+https://github.com/dgrtwo/ParsePy.git


CREATE SAMPLE
-------------

addOrModifyItem("All.Electronics.Watches.Time Master", {'itemImage': u'https://encrypted-tbn2.gstatic.com/images?q=tbn:ANd9GcRy1EpOm6BoOXyBPymTLwogw3yOJnGtseIjQ52yxWLwKqPNXJdz', 'productType': 1})
addOrModifyItem("All.Electronics.t1.t2", {"productType":1, "itemImage": "blahblah"})
addOrModifyItem("All.Electronics.Phones.Amazon Fire", {'itemImage': u'http://drop.ndtv.com/TECH/product_database/images/619201492915AM_635_amazon_fire_phone_new.jpeg', 'productType': 1})
addOrModifyItem("All.Electronics.Phones.Samsung Galaxy", {'itemImage': u'http://www.boostmobile.com/shop/phones/_images/phones/samsung-galaxy-s3/views/full/front.png', 'productType': 1})
addOrModifyItem("All.Toys.Panda", {'itemImage': u'http://images4.fanpop.com/image/photos/16200000/Pandas-pandas-16256344-600-750.jpg', 'productType': 1})
addOrModifyItem("All.Clothing.Shirts.Canadian Lumber Jack", {'itemImage': u'https://encrypted-tbn1.gstatic.com/images?q=tbn:ANd9GcT0ZhXm9a7bfBUs7PTnllm1U6KIfhWbecPE_aT5F5-euEkzfqPRhQ', 'productType': 1})
"""
from parse_rest.connection import register
from parse_rest.datatypes import Object
import fnmatch
import pprint
import re

CMD_PREFIX = "cmd_"


class Product(Object):
    pass

register("T5COsNbanlLkzcafpo6CkyeXlRNNvkL5RqQv8isL", "MgTs0PAaQ2VZM77r1CUEM4R7PttDdq1L1yTCUxvc", master_key=None)

"""
Example:

getAllProducts('All\.[^\.]*')
"""
def cmd_getAllProducts(regex=".*"):
    #regex = fnmatch.translate(fnmtch)
    #print(regex)
    ret = []
    for p in Product.Query.all():
        #template = "{ACL:8}|{Hierarchy:10}|{_created_at:15}|{_updated_at:7}|{itemImage:10}|{productType:1}|{objectId:10}" # same, but named
        #print template.format( ACL="ACL", Hierarchy="Hierarchy", _created_at="_created_at", _updated_at="_updated_at", itemImage="itemImage", productType="productType", objectId="objectId")
        match = re.match(regex, p.Hierarchy)
        if match and match.group(0) == p.Hierarchy:
            ret.append(p)
            pprint.pprint(vars(p), width=1500, indent=4)
        #print template.format(vars(p))
    return ret

def cmd_x():
    exit()

"""
Example:

addOrModifyItem("All.Electronics.t1.t2", {"productType":1, "itemImage": "blahblah"})
"""
def cmd_addOrModifyItem(path, properties):
        if path == None or len(path) == 0:
            return

        path = path.split('.')
        regexsrch = hrchy = path[0]
        for i in range(1, len(path)):
            # getAllProducts("All\.Electronics.[^\.]*$")
            if len(cmd_getAllProducts(regexsrch+'\.[^\.]*$')) == 0:
                row = Product()
                row.productType = 0
                row.Hierarchy = hrchy
                row.itemImage = "http://icons.iconarchive.com/icons/kyo-tux/aeon/256/Folder-Blue-Folder-icon.png"
                row.save()
            hrchy += '.' + path[i]
            regexsrch += '\.' + path[i]

        row = None
        productList = cmd_getAllProducts(regexsrch)

        if len(productList) == 0:
            row = Product()
            row.productType = 1
            row.Hierarchy = hrchy
        else:
            for obj in productList:
                row = obj

        if properties:
            row.__dict__.update(properties)
            #for p in properties:
            #    row.setattr(p, properties[p])

        row.save()

"""
Example:

addOrModifyItem("All.Electronics.t1.t2", {"productType":1, "itemImage": "blahblah"})

deleteItem("All.Electronics.t1.t2")
"""
def cmd_deleteItem(path, deleteNonLeaf=False):

    if path == None or len(path) == 0:
            return

    path = path.split('.')
    regexsrch = "\.".join(path)
    childProducts = cmd_getAllProducts(regexsrch+'\.[^\.]*$')
    if len(childProducts) == 0: #No children, safe to delete
        for c in cmd_getAllProducts(regexsrch):
            print('Deleting %s' % c.Hierarchy)
            c.delete()
        cmd_deleteItem(".".join(path[0:-1]), False)
    else:
        if deleteNonLeaf:
            for c in childProducts:
                print("%% Deleting %s..." % c.Hierarchy)
                cmd_deleteItem(c.Hierarchy, deleteNonLeaf)

"""--------------------------------------------------------------------------------------------"""
for fn in locals().keys():
    if callable(locals()[fn]) and fn.startswith(CMD_PREFIX):
        fn = fn.replace(CMD_PREFIX, "")
        print(fn)

while(True):
    try:
        fn = CMD_PREFIX + raw_input("Enter command: ")
        fn_name = fn.split("(")[0]
        if fn_name in locals().keys() and callable(locals()[fn_name]):
            #locals()[fn_name]()
            exec(fn)
            print('-'*80)
        else:
            print 'Function %s not found. Please check again.' % fn
    except Exception as e:
        print("Unexpected error: " + e.message)