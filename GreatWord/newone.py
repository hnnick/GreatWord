class Box:
    def myInit(mySelf, boxname, size, color):
        mySelf.boxname = boxname
        mySelf.size = size
        mySelf.color = color  # 自己写一个初始化函数，一样奏效,甚至不用self命名。其它函数当中用标准self
        return mySelf  # 返回给实例化过程一个对象！神奇！并且含有对象属性/字典

    # def __init__(self, boxname, size, color):
    #     self.boxname = boxname
    #     self.size = size
    #     self.color = color  #注释掉原来标准的初始化

    def open(self, myself):
        print(self)
        print(myself)
        print('-->用自己的myself，打开那个%s,%s的%s' % (myself.color, myself.size, myself.boxname))
        print('-->用类自己的self，打开那个%s,%s的%s' % (myself.color, myself.size, myself.boxname))

    def close(self):
        print('-->关闭%s，谢谢' % self.boxname)


# 经过改造，运行结果和标准初始化没区别

b = Box().myInit('魔盒', '14m', '红色')
# b = Box('魔盒', '14m', '红色')#注释掉原来标准的初始化方法
b.close()
b.open(b)  # 本来就会自动传一个self，现在传入b，就会让open多得到一个实例对象本身，print看看是什么。
print(b.__dict__)  # 这里返回的就是self本身，self存储属性，没有动作。