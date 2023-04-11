# -*- coding: utf-8 -*-
# @Time    : 2023/3/31 10:52
# @Author  : 南宫乘风
# @Email   : 1794748404@qq.com
# @File    : day.py
# @Software: PyCharm
import re

html = """
<pre><code class="language-java">package com.springboot.demo.webdemo.controller;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.HashMap;

@RestController
@RequestMapping("/employee")
public class EmployeeController {

    @GetMapping
    public HashMap<String, String> index(){
        HashMap<String, String> hashmap = new HashMap<String, String>();
        hashmap.put("姓名", "王二");
        hashmap.put("年龄", "27");
        hashmap.put("工龄", "6");

        return hashmap;
    }
}</code></pre>
"""

code_pattern = r'language-(\w+)'
code_match = re.search(code_pattern, html)
print(code_match)
if code_match:
    lang = code_match.group(1)
    lang_code = re.search(r'\b(java|python|ruby|yml|shell|bash)\b', lang)
    if lang_code:
        lang = lang_code.group(0)
    else:
        lang = 'bash'
else:
    lang = None

print(lang)