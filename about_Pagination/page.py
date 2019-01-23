class Pagination(object):

    def __init__(self,current_page_num,all_count,request,per_page_num=10,pager_count=11):
        """
        封装分页相关数据
        :param current_page_num: 点的是第几页
        :param all_count:   一共多少页
        :param per_page_num: 每页显示几条数据, 默认10条
        :param pager_count:  一个html最多几个页码, 默认11条,点的是第几页,前后各5条
        """
        try:
            current_page_num = int(current_page_num)
        except Exception as e: #如果出现异常,例如,如果输入了非数字,按异常处理显示第一页.
            current_page_num = 1

        if current_page_num <1:
            current_page_num = 1

        self.current_page_num = current_page_num

        self.all_count = all_count
        self.per_page_num = per_page_num

        all_pager, tmp = divmod(all_count, per_page_num)   # 实际总页码
        if tmp:
            all_pager += 1  # 取整
        self.all_pager = all_pager

        self.pager_count = pager_count
        self.pager_count_half = int((pager_count - 1) / 2)


        # 保存搜索条件
        import copy
        self.params=copy.deepcopy(request.GET) # {"a":"1","b":"2"}  request.GET是queryDIct类型不能修改,
                                              # 深拷贝后虽然还是queryDIct类型,但是可以修改,

    @property
    def start(self): #根据用户点击的页码,算出应该取哪些数据,例如点击2页,取第10-20条数据
        return (self.current_page_num - 1) * self.per_page_num

    @property
    def end(self):
        return self.current_page_num * self.per_page_num

    def page_html(self):
        # 如果总页码 < 11个：就全部显示出来就行了
        if self.all_pager <= self.pager_count:
            pager_start = 1
            pager_end = self.all_pager + 1
        # 总页码 > 11页,
        else:
            # 当前页如果<=页面上最多显示11/2个页码
            if self.current_page_num <= self.pager_count_half:
                pager_start = 1
                pager_end = self.pager_count + 1
            # 当前页大于5
            else:
                # 页码翻到最后
                if (self.current_page_num + self.pager_count_half) > self.all_pager:

                    pager_start = self.all_pager - self.pager_count + 1
                    pager_end = self.all_pager + 1

                else:   # 按照点击的页数,左右各显示5页.
                    pager_start = self.current_page_num - self.pager_count_half
                    pager_end = self.current_page_num + self.pager_count_half + 1

        page_html_list = []

        first_page = '<li><a href="?page=%s">首页</a></li>' % (1,)
        page_html_list.append(first_page)

        if self.current_page_num <= 1:
            prev_page = '<li class="disabled"><a href="#">上一页</a></li>'
        else:
            prev_page = '<li><a href="?page=%s">上一页</a></li>' % (self.current_page_num - 1,)

        page_html_list.append(prev_page)

        # 处理保存搜索条件:
        #self.params=copy.deepcopy(request.GET) # {"a":"1","b":"2"}
        #deepcopy后虽然还是querydict,但是可以修改,为什么可以修改看源码.
        for i in range(pager_start, pager_end):

            self.params["page"]=i

            if i == self.current_page_num:
                temp = '<li class="active"><a href="?%s">%s</a></li>' %(self.params.urlencode(),i) #让当前页码呈现active选中,urlencode是将字典变成字符串

            else:
                temp = '<li><a href="?%s">%s</a></li>' % (self.params.urlencode(),i,)
            page_html_list.append(temp)
        if self.current_page_num >= self.all_pager:
            next_page = '<li class="disabled"><a href="#">下一页</a></li>'
        else:
            next_page = '<li><a href="?page=%s">下一页</a></li>' % (self.current_page_num + 1,)
        page_html_list.append(next_page)
        last_page = '<li><a href="?page=%s">尾页</a></li>' % (self.all_pager,)
        page_html_list.append(last_page)

        return ''.join(page_html_list)