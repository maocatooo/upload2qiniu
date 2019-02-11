# -*- coding: utf-8 -*-
from qiniu import Auth, put_data
import StringIO
from xlsxwriter import Workbook
import datetime
import time

ak = ""
sk= ''
file_type = "office"
output = StringIO.StringIO()
office = Workbook(output)
worksheet_detail = office.add_worksheet(u"明细")
worksheet_all = office.add_worksheet(u"总表")
worksheet_all.set_column('A:H', 20)
worksheet_all.write_row('A1',
                        [u"被测评人工号",
                         u"被测评人姓名",
                         u"被测评人手机号",
                         u"被测评人职级",
                         u"被测评人部门",
                         u"上对下评分",
                         u"平级平均分",
                         u"下对上评分",
                         u"总平均分"])
office.close()
prefix = 'upload/{0}/'.format(file_type)
q = Auth(ak, sk)
bucket = "demo"
url = "pmr318jrz.bkt.clouddn.com"
file_name = '测评信息'+ datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
full_filename = prefix + file_name + '.xlsx'
token = q.upload_token(bucket,
                       full_filename, 36000)
ret, info = put_data(token, full_filename, output.getvalue())
print '{}{}?t={}'.format(
    url, ret['key'].encode("utf-8"), 111)