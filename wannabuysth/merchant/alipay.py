# -*- coding: utf-8 -*-

import hashlib

www = 'http://192.168.1.120:8000'

consumer_subject = u'帮办管家'
consumer_body = www


class Alipay(object):
    def __init__(self):
        self.params = {}
        # 支付宝gateway
        self.seller_email = 'superpowerlee@hotmail.com'
        self.pay_gate_way = 'https://www.alipay.com/cooperate/gateway.do'
        self.partner = '2088002003071731'
        self.security_code = 'l7o2bbvyk3xvf34eln4w910axald4yep'
        self.return_url = '%s/mc/alipaycallback' % www
        self.notify_url = '%s/mc/alipaynotify' % www
        self.input_charset = 'utf-8'

    # @return
    #---------------------------------------------------------------------------
    def create_order_alipay_url(self,
                                subject,
                                out_trade_no,
                                total_fee,
                                body='',
                                show_url=www,
                                sign_type="MD5"
                                ):

        self.params['service'] = "create_direct_pay_by_user"
        self.params['partner'] = self.partner
        self.params['_input_charset'] = self.input_charset
        self.params['total_fee'] = total_fee

        self.params['show_url'] = show_url
        self.params['return_url'] = self.return_url
        self.params['notify_url'] = self.notify_url
        self.params['subject'] = subject
        self.params['body'] = body
        self.params['out_trade_no'] = out_trade_no
        self.params['payment_type'] = "1"
        self.params['seller_email'] = self.seller_email
        # 返回结果
        return self._create_url(self.params, sign_type)

    def conv_uni(self, param, input_charset):
        data = param
        if type(data) is unicode:
            data = data.encode(input_charset)
        return data

    def sign(self, params, sign_type='MD5', input_charset='utf-8'):
        param_keys = []
        sign = ''

        param_keys = params.keys()
        # 支付宝参数要求按照字母顺序排序
        param_keys.sort()
        # 初始化待签名的数据
        unsigned_data = ''
        # 生成待签名数据
        # 注：要求签名数据为urlencoding之前的数据
        for key in param_keys:
            data = self.conv_uni(params[key], input_charset)
            key = self.conv_uni(key, input_charset)
            unsigned_data += '%s=%s' % (key, data)
            if key != param_keys[-1]:
                unsigned_data += '&'
        # 添加签名密钥
        unsigned_data += self.security_code
        # 计算sign值
        if sign_type == 'MD5':
            m = hashlib.md5()
            m.update(unsigned_data)
            sign = m.hexdigest()
        else:
            sign = ''

        return param_keys, sign

    def _create_url(self, params, sign_type='MD5'):
        ''' Make sure using unicode or utf-8 as params
        '''
        param_keys, sign = self.sign(params, input_charset=params['_input_charset'])

        request_data = self.pay_gate_way + '?'
        for key in param_keys:
            data = params[key]
            if type(data) is unicode:
                data = data.encode(params['_input_charset'])
            request_data += key + '=' + data
            request_data += '&'
        request_data += 'sign=' + sign + '&sign_type=' + sign_type
        # 返回结果
        return request_data

    def create_direct_pay_by_user_url(self,
                                      seller_email,
                                      subject,
                                      body,
                                      out_trade_no,
                                      total_fee,
                                      notify_url,
                                      payment_type
                                ):
        self.params['_input_charset'] = 'utf-8'
        self.params['service'] = 'create_direct_pay_by_user'

        self.params['partner'] = self.partner

        self.params['subject'] = subject
        if body:
            self.params['body'] = body
        self.params['out_trade_no'] = out_trade_no
        self.params['total_fee'] = '%s' % total_fee
        self.params['notify_url'] = notify_url
        self.params['payment_type'] = payment_type
        self.params['seller_email'] = seller_email
        # 返回结果
        return self._create_url(self.params)

    def validate(self, request):
        valid = False
        infos = {}

        if request.method == 'POST':
            data_dict = request.form
        else:
            data_dict = request.args

        sign_type = data_dict.get('sign_type', '').lower()
        if sign_type == 'md5':
            sign = u'%s' % data_dict.get('sign', '')
            params = {}
            for k, v in data_dict.items():
                if k not in ('sign', 'sign_type'):
                    params[k] = v

            # 签名比较防篡改
            keys, our_sign = self.sign(params)
            our_sign = u'%s' % our_sign
            if sign == our_sign:
                # 验证notify_id
                notify_id = params['notify_id']
                notify_verify_url = self.create_notify_verify_url(notify_id)

                from common.http_client import send

                rsp = send(notify_verify_url)

#                req = urllib2.Request(notify_verify_url)
#                fd = urllib2.urlopen(req, {})
#                rsp = fd.read()

#                valid = True
#                infos = params

                if rsp == 'true':
                    valid = True
                    infos = params
                elif rsp == 'false':
                    pass
                else:
                    pass

        return valid, infos

    def create_notify_verify_url(self, notify_id):
        request_data = 'http://notify.alipay.com/trade/notify_query.do?'
#        request_data = self.pay_gate_way + '?service=notify_verify'
        request_data += 'partner=' + self.partner
        request_data += '&notify_id=' + notify_id
        return request_data


    # 支付类型枚举表
    payment_types = {
        '1':'商品购买',
        '2':'服务购买',
        '3':'网络拍卖',
        '4':'捐赠',
        '5':'邮费补偿',
        '6':'奖金',
    }
    # 交易动作枚举表
    actions = {
        # 买家动作
        'PAY':'付款',
        'REFUND':'退款',
        'CONFIRM_GOODS':'确认收货',
        'CANCEL_FAST_PAY':'付款方取消快速支付',
        'WAIT_BUYER_CONFIRM_GOODS':'快速支付付款',
        'FP_PAY':'买家确认收到货，等待支付宝打款给卖家',
        'RM_PAY':'催款中还钱',
        'MODIFY_DELIVER_ADDRESS':'买家修改收货地址',
        # 卖家动作
        'SEND_GOODS':'发货',
        'REFUSE_TRADE':'拒绝交易',
        'MODIFY_TRADE':'修改交易',
        'REFUSE_FAST_PAY':'收款方拒绝付款',
        # 共有动作
        'QUERY_LOGISTICS':'查看物流状态',
        'QUERY_REFUND':'查看退款状态',
        'EXTEND_TIMEOUT':'延长对方超时时间',
        'VIEW_DETAIL':'查看明细',
    }
    # 交易状态枚举表
    trade_statuses = {
        'WAIT_BUYER_PAY':'等待买家付款',
        'WAIT_SELLER_CONFIRM_TRADE':'交易已创建，等待卖家确认',
        'WAIT_SYS_CONFIRM_PAY':'确认买家付款中，暂勿发货',
        'WAIT_SELLER_SEND_GOODS':'支付宝收到买家付款，请卖家发货',
        'WAIT_BUYER_CONFIRM_GOODS':'卖家已发货，买家确认中',
        'WAIT_SYS_PAY_SELLER':'买家确认收到货，等待支付宝打款给卖家',
        'TRADE_FINISHED':'交易成功结束',
        'TRADE_CLOSED':'交易中途关闭（未完成）',
    }
    # 物流状态枚举表
    trade_statuses = {
        'INITIAL_STATUS':'初始状态',
        'WAIT_LOGISTICS_FETCH_GOODS':'等待物流取货',
        'WAIT_LOGISTICS_SEND_GOODS':'等待物流发货',
        'LOGISTICS_SENDING':'物流发货中',
        'WAIT_RECEIVER_CONFIRM_GOODS':'等待收货人确认收货',
        'GOODS_RECEIVED':'货物收到了',
        'LOGISTICS_FAILURE':'物流失败',
    }
    # 退款状态枚举表
    refund_statuses = {
        'WAIT_SELLER_AGREE':'等待卖家同意退款',
        'SELLER_REFUSE_BUYER':'卖家拒绝买家条件，等待买家修改条件',
        'WAIT_BUYER_RETURN_GOODS':'卖家同意退款，等待买家退货',
        'WAIT_SELLER_CONFIRM_GOODS':'等待卖家收货',
        'WAIT_ALIPAY_REFUND':'对方已经一致，等待支付宝退款',
        'ALIPAY_CHECK':'支付宝处理中',
        'OVERED_REFUND':'结束的退款',
        'REFUND_SUCCESS':'退款成功',
        'REFUND_CLOSED':'退款关闭',
    }
    # 物流类型枚举表
    logistics_types = {
        'VIRTUAL':'虚拟物品',
        'POST':'平邮',
        'EMS':'EMS',
        'EXPRESS':'其他快递公司',
    }
    # 物流支付方式枚举表
    logistics_payments = {
        'SELLER_PAY':'卖家支付',  # 由卖家支付物流费用（费用不用计算到总价内）
        'BUYER_PAY':'买家支付',  # 由买家支付物流费用（费用需要计算到总价内）
        'BUYER_PAY_AFTER_RECEIVE':'货到付款',  # 买家收到货物后直接支付给物流公司（费用不用计算到总价内）
    }

