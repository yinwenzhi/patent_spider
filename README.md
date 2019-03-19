# patent_spider
使用西瓜代理爬取国家知识产权局专利信息

---

### Step 1: Gain Pagesize
`cd ${spider_root}`

##### 1) publish

1.1) open cfgs/publish.yml,

1.2) let the `pklfile` to the pickle file need to changed

1.3) let the `ip_url` to a vaild ip agent

1.4) If you want to print log onto screen, make the `stdout` `True`

1.5) run

`python gain_pagesize.py publish`

##### 2) authorization

1.1) open cfgs/authorization.yml

1.2) let the `pklfile` to the pickle file need to changed

1.3) let the `ip_url` to a vaild ip agent

1.4) If you want to print log onto screen, make the `stdout` `True`

1.5) run

`python gain_pagesize.py authorization`

### Step 2: Gain Content
`cd ${spider_root}`

##### 1) publish

1.1) open cfgs/publish.yml,

1.2) change the `pklfile` refer to the former step and let the `pklfile` to the pickle file need to changed

1.3) let the `ip_url` to a vaild ip agent

1.4) If you want to print log onto screen, make the `stdout` `True`

1.5) run

`python gain_content.py publish`

##### 2) authorization

1.1) open cfgs/authorization.yml

1.2) change the `pklfile` refer to the former step and let the `pklfile` to the pickle file need to changed

1.3) let the `ip_url` to a vaild ip agent

1.4) If you want to print log onto screen, make the `stdout` `True`

1.5) run

`python gain_content.py authorization`
