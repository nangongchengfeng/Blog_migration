# -*- coding: utf-8 -*-
# @Time    : 2023/1/9 18:00
# @Author  : weidongliang
# @Email   : 1794748404@qq.com
# @File    : CSDN-spider_one.py
# @Software: PyCharm
import requests

url = ['http://pic.netbian.com/uploads/allimg/230109/005404-1673196844ba1d.jpg',
       'http://pic.netbian.com/uploads/allimg/230107/005542-1673024142cc0c.jpg',
       'http://pic.netbian.com/uploads/allimg/230107/005104-1673023864a712.jpg',
       'http://pic.netbian.com/uploads/allimg/190824/212516-1566653116f355.jpg',
       'http://pic.netbian.com/uploads/allimg/200618/005100-1592412660f973.jpg',
       'http://pic.netbian.com/uploads/allimg/210423/224716-16191892361adb.jpg',
       'http://pic.netbian.com/uploads/allimg/210317/001935-16159115757f04.jpg',
       'http://pic.netbian.com/uploads/allimg/221221/113511-16715937115f7b.jpg',
       'http://pic.netbian.com/uploads/allimg/220802/231950-1659453590cc8e.jpg',
       'http://pic.netbian.com/uploads/allimg/220827/223220-166161074052ed.jpg',
       'http://pic.netbian.com/uploads/allimg/220902/224030-16621296304bf2.jpg',
       'http://pic.netbian.com/uploads/allimg/230104/222259-1672842179da4b.jpg',
       'http://pic.netbian.com/uploads/allimg/230101/223603-1672583763e530.jpg',
       'http://pic.netbian.com/uploads/allimg/221024/003442-16665428829bab.jpg',
       'http://pic.netbian.com/uploads/allimg/221227/115356-1672113236843e.jpg',
       'http://pic.netbian.com/uploads/allimg/221225/002446-16718990861a87.jpg',
       'http://pic.netbian.com/uploads/allimg/221222/003558-1671640558d37e.jpg',
       'http://pic.netbian.com/uploads/allimg/221221/004014-16715544141f97.jpg',
       'http://pic.netbian.com/uploads/allimg/221220/001325-16714664053843.jpg',
       'http://pic.netbian.com/uploads/allimg/221220/000909-16714661492e3b.jpg',
       'http://pic.netbian.com/uploads/allimg/221220/000808-1671466088f57a.jpg',
       'http://pic.netbian.com/uploads/allimg/221218/121014-1671336614a41a.jpg',
       'http://pic.netbian.com/uploads/allimg/221208/110844-167046892411bb.jpg',
       'http://pic.netbian.com/uploads/allimg/221213/002248-16708621685849.jpg',
       'http://pic.netbian.com/uploads/allimg/221216/004816-16711228961204.jpg',
       'http://pic.netbian.com/uploads/allimg/221205/155137-16702266973333.jpg',
       'http://pic.netbian.com/uploads/allimg/220909/000311-16626529918d5d.jpg',
       'http://pic.netbian.com/uploads/allimg/220930/004111-1664469671a245.jpg',
       'http://pic.netbian.com/uploads/allimg/221209/113332-1670556812e974.jpg',
       'http://pic.netbian.com/uploads/allimg/221201/005454-16698272941863.jpg',
       'http://pic.netbian.com/uploads/allimg/221214/004624-1670949984ee7a.jpg',
       'http://pic.netbian.com/uploads/allimg/221028/222859-1666967339b9c3.jpg',
       'http://pic.netbian.com/uploads/allimg/220712/233259-1657639979a66c.jpg',
       'http://pic.netbian.com/uploads/allimg/221228/171118-167221867885f0.jpg',
       'http://pic.netbian.com/uploads/allimg/221206/232707-167034042795b0.jpg',
       'http://pic.netbian.com/uploads/allimg/221204/002308-167008458817f1.jpg',
       'http://pic.netbian.com/uploads/allimg/221009/225723-166532744398b2.jpg',
       'http://pic.netbian.com/uploads/allimg/221008/194930-16652297708fbe.jpg',
       'http://pic.netbian.com/uploads/allimg/221222/004543-1671641143532b.jpg',
       'http://pic.netbian.com/uploads/allimg/221222/004442-1671641082909e.jpg',
       'http://pic.netbian.com/uploads/allimg/221214/005137-167095029782cb.jpg',
       'http://pic.netbian.com/uploads/allimg/221214/004930-16709501708e3b.jpg',
       'http://pic.netbian.com/uploads/allimg/221115/153253-1668497573335b.jpg',
       'http://pic.netbian.com/uploads/allimg/221119/000805-1668787685cf0a.jpg',
       'http://pic.netbian.com/uploads/allimg/221204/003137-1670085097232d.jpg',
       'http://pic.netbian.com/uploads/allimg/221121/234549-1669045549ef44.jpg',
       'http://pic.netbian.com/uploads/allimg/221115/154515-1668498315fc46.jpg',
       'http://pic.netbian.com/uploads/allimg/221108/004044-166783924467a7.jpg',
       'http://pic.netbian.com/uploads/allimg/221112/003502-16681845029360.jpg',
       'http://pic.netbian.com/uploads/allimg/221110/004231-166801215177e3.jpg',
       'http://pic.netbian.com/uploads/allimg/221110/004101-16680120612d36.jpg',
       'http://pic.netbian.com/uploads/allimg/221108/203854-166791113442d0.jpg',
       'http://pic.netbian.com/uploads/allimg/221107/004114-166775287499b5.jpg',
       'http://pic.netbian.com/uploads/allimg/221105/003506-1667579706979f.jpg',
       'http://pic.netbian.com/uploads/allimg/221017/004158-16659385186619.jpg',
       'http://pic.netbian.com/uploads/allimg/230106/002914-1672936154790d.jpg',
       'http://pic.netbian.com/uploads/allimg/221105/002355-16675790353984.jpg',
       'http://pic.netbian.com/uploads/allimg/221105/002213-16675789330e59.jpg',
       'http://pic.netbian.com/uploads/allimg/221201/003652-1669826212c799.jpg',
       'http://pic.netbian.com/uploads/allimg/180803/084010-15332568109b5b.jpg',
       'http://pic.netbian.com/uploads/allimg/221027/000526-1666800326b0f9.jpg',
       'http://pic.netbian.com/uploads/allimg/221105/003704-16675798243bf5.jpg',
       'http://pic.netbian.com/uploads/allimg/221025/001813-16666282937fba.jpg',
       'http://pic.netbian.com/uploads/allimg/221021/000251-166628177108fa.jpg',
       'http://pic.netbian.com/uploads/allimg/221011/232259-16655017792354.jpg',
       'http://pic.netbian.com/uploads/allimg/220707/233628-16572081888521.jpg',
       'http://pic.netbian.com/uploads/allimg/220517/005711-165272023100f8.jpg',
       'http://pic.netbian.com/uploads/allimg/221002/231345-16647236259138.jpg',
       'http://pic.netbian.com/uploads/allimg/221105/002838-1667579318f5ba.jpg',
       'http://pic.netbian.com/uploads/allimg/221024/003929-1666543169aee7.jpg',
       'http://pic.netbian.com/uploads/allimg/221020/002105-166619646508b9.jpg',
       'http://pic.netbian.com/uploads/allimg/221019/235303-1666194783e5b6.jpg',
       'http://pic.netbian.com/uploads/allimg/221102/002200-1667319720db25.jpg',
       'http://pic.netbian.com/uploads/allimg/221019/003226-16661107463eff.jpg',
       'http://pic.netbian.com/uploads/allimg/221019/002747-1666110467139c.jpg',
       'http://pic.netbian.com/uploads/allimg/221019/001522-1666109722d14d.jpg',
       'http://pic.netbian.com/uploads/allimg/221016/105016-16658886166227.jpg',
       'http://pic.netbian.com/uploads/allimg/221015/004753-1665766073dbd7.jpg',
       'http://pic.netbian.com/uploads/allimg/221013/000727-1665590847de20.jpg',
       'http://pic.netbian.com/uploads/allimg/221016/102149-16658869094b6a.jpg',
       'http://pic.netbian.com/uploads/allimg/221015/002453-16657646939396.jpg',
       'http://pic.netbian.com/uploads/allimg/221014/001736-166567785639c6.jpg',
       'http://pic.netbian.com/uploads/allimg/221011/004252-166542017285b1.jpg',
       'http://pic.netbian.com/uploads/allimg/221024/002211-16665421310661.jpg',
       'http://pic.netbian.com/uploads/allimg/221022/000039-16663680393290.jpg',
       'http://pic.netbian.com/uploads/allimg/221012/154927-16655609671af6.jpg',
       'http://pic.netbian.com/uploads/allimg/221016/112537-166589073773f5.jpg',
       'http://pic.netbian.com/uploads/allimg/221011/001348-1665418428484f.jpg',
       'http://pic.netbian.com/uploads/allimg/221030/232634-16671435947956.jpg',
       'http://pic.netbian.com/uploads/allimg/221016/112903-16658909438919.jpg',
       'http://pic.netbian.com/uploads/allimg/221009/194117-1665315677bc54.jpg',
       'http://pic.netbian.com/uploads/allimg/221009/225919-1665327559e71b.jpg',
       'http://pic.netbian.com/uploads/allimg/221009/170626-1665306386c600.jpg',
       'http://pic.netbian.com/uploads/allimg/220820/091439-16609580799ee5.jpg',
       'http://pic.netbian.com/uploads/allimg/210920/165135-1632127895c615.jpg',
       'http://pic.netbian.com/uploads/allimg/200216/174956-158184659610a4.jpg',
       'http://pic.netbian.com/uploads/allimg/190824/205524-15666513248366.jpg',
       'http://pic.netbian.com/uploads/allimg/220706/230904-1657120144d7ff.jpg',
       'http://pic.netbian.com/uploads/allimg/221001/234650-1664639210d642.jpg',
       'http://pic.netbian.com/uploads/allimg/221002/183839-1664707119576c.jpg']
count = 1
headers = {
    'Users-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36'
}
for i in url:
    img_data = requests.get(url=i, headers=headers).content
    filePath = './4kdongman/' + str(count) + '.jpg'
    with open(filePath, 'wb')as fp:
        fp.write(img_data)
    print('%s,下载成功' % count)
    count=count + 1
