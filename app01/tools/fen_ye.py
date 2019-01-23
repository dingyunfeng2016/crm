class Pagination(object):
    def __init__(self, current_page_num, all_count, request, per_page_num=5, pager_count=11):
        """
        封装分页相关数据
        :param current_page_num: 当前访问页的数字
        :param all_count:    分页数据中的数据总条数
        :param per_page_num: 每页显示的数据条数 默认显示10条
        :param pager_count:  最多显示的页码个数  页面上只显示11个页码,左5右5
        """
        try:
            current_page_num = int(current_page_num)
        except Exception as e:
            current_page_num = 1  #有异常默认取第一页

        if current_page_num < 1:
            current_page_num = 1

        self.current_page_num = current_page_num

        self.all_count = all_count
        self.per_page_num = per_page_num

        # 实际总页码
        all_pager, tmp = divmod(all_count, per_page_num)
        if tmp:
            all_pager += 1
        self.all_pager = all_pager

        self.pager_count = pager_count
        self.pager_count_half = int((pager_count - 1) / 2)  # 5

        # 保存搜索条件
        import copy
        self.params = copy.deepcopy(request.GET)#self.params={"a":"1","b":"2"}

    @property    #变成属性,静态方法,调用的时候 不用加()
    def start(self):
        return (self.current_page_num - 1) * self.per_page_num

    @property
    def end(self):
        return self.current_page_num * self.per_page_num

    def page_html(self):  #渲染出页面
        # 如果总页码 < 11个：显示出所有页面
        if self.all_pager <= self.pager_count:
            pager_start = 1
            pager_end = self.all_pager + 1
        # 总页码  > 11   显示左5右5
        else:
            # 当前页如果<=页面上最多显示11/2个页码    e.g点第四页 就把所有页都显示出来
            if self.current_page_num <= self.pager_count_half:
                pager_start = 1
                pager_end = self.pager_count + 1  #range顾头不顾尾 所以+1
            # 当前页大于5
            else:
                # 页码翻到最后
                if (self.current_page_num + self.pager_count_half) > self.all_pager:

                    pager_start = self.all_pager - self.pager_count + 1
                    pager_end = self.all_pager + 1

                else: #排除了所有情况,显示左5右5
                    pager_start = self.current_page_num - self.pager_count_half
                    pager_end = self.current_page_num + self.pager_count_half + 1

        page_html_list = []

        first_page = '<li><a href="?page=%s">首页</a></li>' % (1,)
        page_html_list.append(first_page)

        if self.current_page_num <= 1:  # 如果是第1页  没有上一页
            prev_page = '<li class="disabled"><a href="#">上一页</a></li>'
        else:
            prev_page = '<li><a href="?page=%s">上一页</a></li>' % (self.current_page_num - 1,)

        page_html_list.append(prev_page)

        # self.params=copy.deepcopy(request.GET) # {"a":"1","b":"2"}
        for i in range(pager_start, pager_end):

            self.params["page"] = i  #把page加到self.params字典中,再点页码,新的page覆盖上一次的page

            if i == self.current_page_num: # 如果循环到当前页 当前页加上active
                # 用urlencode()方法,将self.parms字典拼成urlencoded字符串,如a=1&b=2&page=3
                temp = '<li class="active"><a href="?%s">%s</a></li>' % (self.params.urlencode(), i)
            else:
                temp = '<li><a href="?%s">%s</a></li>' % (self.params.urlencode(), i,)
            page_html_list.append(temp)

        if self.current_page_num >= self.all_pager:  #如果当前页是最后一页 没有下一页  下一页置灰
            next_page = '<li class="disabled"><a href="#">下一页</a></li>'
        else:
            next_page = '<li><a href="?page=%s">下一页</a></li>' % (self.current_page_num + 1,)
        page_html_list.append(next_page)
        last_page = '<li><a href="?page=%s">尾页</a></li>' % (self.all_pager,)
        page_html_list.append(last_page)

        return ''.join(page_html_list)
