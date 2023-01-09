+++
author = "南宫乘风"
title = "Linux操作系统账号密码失效检测"
date = "2021-12-23 15:39:37"
tags=['linux', '运维', '服务器']
categories=[' 企业级-Shell脚本案例', 'Linux Shell']
image = "post/4kdongman/62.jpg"
+++
[作者：南宫乘风   原文链接:https://blog.csdn.net/heian_99/article/details/122108856](https://blog.csdn.net/heian_99/article/details/122108856)

根据我开发的邮件接口上调用操作，触发告警

# [GO的WEB编程（GIN实现邮件接口报警）](https://blog.csdn.net/heian_99/article/details/121851358)

# [Gin编写邮件接口（支持多人发送）](https://blog.csdn.net/heian_99/article/details/121912558)

# [Gin编写邮件告警接口（添加优化日志记录）](https://blog.csdn.net/heian_99/article/details/122002534)



首先，我们Linux操作系统可以创建多个用户账号。

但是为了系统安全考虑，我们会给账号密码设置有效期和复杂难度，防止非法操作爆破我们的机器。

但是每次修改完，到规定时间需要修改账号密码，这个每次人工来看，比较麻烦，所以做个账号密码到期的警告。当密码快要过期时，我们可以发邮件告警。

## **账号密码过期设置**

```
function Check_Password_Policy(){
    #查看系统账户策略:密码失效时间90天、密码到期提醒时间14天
    echo "========正在检查账户密码失效时间========"
    Check_Pass_Poli=`grep  -E "^PASS_MAX_DAYS|^PASS_WARN_AGE"  /etc/login.defs | wc -l`
    cp  /etc/login.defs{,_bak$Date_Time}
    if  [ $Check_Pass_Poli -lt 2 ];then
        echo -e "\033[31;40m当前系统未对账户密码进行失效时间设置、密码到期提醒设置\033[0m"
        sed -i  '$iPASS_MAX_DAYS   90'  /etc/login.defs &amp;&amp; echo -e "\033[32;40m 修改成功 \033[0m" || echo -e "\033[31;40m 修改失败 \033[0m"
        sed -i  '$iPASS_WARN_AGE   14'  /etc/login.defs &amp;&amp; echo -e "\033[32;40m 修改成功 \033[0m" || echo -e "\033[31;40m 修改失败 \033[0m"
    else
        PAMAX=`grep  -E "^PASS_MAX_DAYS"  /etc/login.defs | awk -F" " '{ print $2 }'`
        PAWARN=`grep  -E "^PASS_WARN_AGE"  /etc/login.defs | awk -F" " '{ print $2 }'`
        if [ $PAMAX -le 90 ];then     
            echo -e "\033[32;40m密码失效时间为$PAMAX天，符合标准\033[0m"; 
        else     
            echo -e "\033[31;40m密码失效时间为$PAMAX天，不符合标准\033[0m"; 
            sed -i  's/^PASS_MAX_DAYS.*/PASS_MAX_DAYS   90/'  /etc/login.defs &amp;&amp; echo -e "\033[32;40m 修改成功 \033[0m" || echo -e "\033[31;40m 修改失败 \033[0m"
        fi
        if [ $PAWARN -ge 14 ];then    
            echo -e "\033[32;40m密码到期提醒时间为$PAWARN天，符合标准\033[0m"; 
        else     
            echo -e "\033[31;40m密码到期提醒时间为$PAWARN天，不符合标准\033[0m"; 
            sed -i  's/^PASS_WARN_AGE.*/PASS_WARN_AGE   14/'  /etc/login.defs &amp;&amp; echo -e "\033[32;40m 修改成功 \033[0m" || echo -e "\033[31;40m 修改失败 \033[0m"
        fi
    fi
    #chage --warndays  14 root &amp;&amp; echo -e "\033[32;40m 修改成功 \033[0m" || echo -e "\033[31;40m 修改失败 \033[0m"
    #chage --maxdays 90 root &amp;&amp; echo -e "\033[32;40m 修改成功 \033[0m" || echo -e "\033[31;40m 修改失败 \033[0m"
}
```

## **密码复杂度设置**

```
function Check_User_Policy(){
    #查看系统账户策略:密码最小长度12位、密码复杂度为大小写英文字母、数字、特殊字符
    echo "========正在检查账户密码策略========"
    Check_User_Poli=`grep -E "^minlen|^minclass"  /etc/security/pwquality.conf |wc -l`
    cp  /etc/security/pwquality.conf{,_bak$Date_Time}
    if  [ $Check_User_Poli -lt 2 ];then
        echo -e "\033[31;40m当前系统未对账户密码复杂度及密码最小长度设置\033[0m"
        sed -i  '$iminlen = 12'  /etc/security/pwquality.conf &amp;&amp; echo -e "\033[32;40m 修改成功 \033[0m" || echo -e "\033[31;40m 修改失败 \033[0m"
        sed -i  '$iminclass = 4'  /etc/security/pwquality.conf &amp;&amp; echo -e "\033[32;40m 修改成功 \033[0m" || echo -e "\033[31;40m 修改失败 \033[0m"
    else
        PACLS=`grep  -E "^minclass"  /etc/security/pwquality.conf | awk -F"=| " '{ print $NF }'`
        PALEN=`grep  -E "^minlen"   /etc/security/pwquality.conf | awk -F"=| " '{ print $NF }'`
        if [ $PACLS -eq 4 ];then     
            echo -e "\033[32;40m密码负责度为$PACLS种类型，符合标准\033[0m"; 
        else     
            echo -e "\033[31;40m密码负责度为$PACLS种类型，不符合标准\033[0m"; 
            sed -i  's/^minclass.*/minclass = 4/'  /etc/login.defs &amp;&amp; echo -e "\033[32;40m 修改成功 \033[0m" || echo -e "\033[31;40m 修改失败 \033[0m"
        fi
        if [ $PALEN -ge 12 ];then    
            echo -e "\033[32;40m密码长度为$PALEN位，符合标准\033[0m"; 
        else     
            echo -e "\033[31;40m密码长度为$PALEN位，不符合标准\033[0m"; 
            sed -i  's/^minlen.*/minlen = 12/'  /etc/login.defs &amp;&amp; echo -e "\033[32;40m 修改成功 \033[0m" || echo -e "\033[31;40m 修改失败 \033[0m"
        fi
    fi
}
```

## 用户认证失败次数设置

```
function Check_Auth_Failed(){
    echo "========正在检查用户登陆认证失败次数========"
    Check_Auth_Failsystem=`grep pam_faillock.so /etc/pam.d/system-auth | wc -l`
    Check_Auth_Failpasswd=`grep pam_faillock.so /etc/pam.d/password-auth | wc -l`
    cp  /etc/pam.d/system-auth{,_bak$Date_Time}
    cp  /etc/pam.d/password-auth{,_bak$Date_Time}
    if [ $Check_Auth_Failsystem -ge 3 ];then
        if [ $Check_Auth_Failpasswd -ge 3 ];then
            echo -e "\033[32;40m 用户登陆连续认证失败锁定策略设置成功，符合标准 \033[0m"
        else
            echo -e "\033[31;40m 用户登陆连续认证失败锁定策略设置不完全，不符合标准 \033[0m"
        fi
    else
        echo -e "\033[31;40m 用户登陆连续认证失败锁定策略设置不正确，不符合标准 \033[0m" 
        sed -i '/auth        required      pam_env.so/i auth required pam_faillock.so preauth audit silent deny=5 unlock_time=900'  /etc/pam.d/system-auth
        sed -i '/auth        required      pam_deny.so/a auth [default=die] pam_faillock.so authfail audit deny=5 unlock_time=900'  /etc/pam.d/system-auth
        sed -i '/account     required      pam_unix.so/i account required pam_faillock.so' /etc/pam.d/system-auth
        sed -i '/auth        required      pam_env.so/i auth required pam_faillock.so preauth audit silent deny=5 unlock_time=900'  /etc/pam.d/password-auth
        sed -i '/auth        required      pam_deny.so/a auth [default=die] pam_faillock.so authfail audit deny=5 unlock_time=900'  /etc/pam.d/password-auth
        sed -i '/account     required      pam_unix.so/i account required pam_faillock.so' /etc/pam.d/password-auth
    fi    
}
```

## **账号密码过期设置**

**设置定时任务，可以每天自己执行判断，如果快到期会发邮件告警，及时修改，防止过期导致crontab任务不可使用**

```
#!/bin/bash
#定义时间变量，用于告警发送
check_time=`date +"%Y-%m-%d %H:%M:%S"`
#日志位置
log=${HOME}/user-info.log
user_name=`whoami`

end_year=` chage -l ${user_name} | head -2| tail -1 | awk -F: '{print $2}'| awk -F',' '{print $2}'| awk '{print $1}'`
if [ "${end_year}" == "" ];then
    echo "99999"
    exit 0
fi
 
    end_mounth=`chage -l ${user_name} | head -2| tail -1 | awk -F: '{print $2}'| awk -F',' '{print $1}'| awk '{print $1}'`
 
    case ${end_mounth} in
        'Jan') end_mounth=1;;
        'Feb') end_mounth=2;;
        'Mar') end_mounth=3;;
        'Apr') end_mounth=4;;
        'May') end_mounth=5;;
        'Jun') end_mounth=6;;
        'Jul') end_mounth=7;;
        'Aug') end_mounth=8;;
        'Sep') end_mounth=9;;
        'Oct') end_mounth=10;;
        'Nov') end_mounth=11;;
        'Dec') end_mounth=12;;
    esac
 
    end_day=`chage -l ${user_name} | head -2| tail -1 | awk -F: '{print $2}'| awk -F',' '{print $1}'| awk '{print $2}'`
    end_date_s=`/bin/date -d "${end_year}"-"${end_mounth}"-"${end_day}" +%s`
    star_date_s=`/bin/date +%s`
    let diffday=(${end_date_s}-${star_date_s})/86400


    echo ${diffday}
#过期时间判断，如果小于15天，开始发邮件
if [  ${diffday} -gt 15 ]  
then  
	    curl http://mail.ownit.top/send -H "Content-Type:application/json" -X POST -d '{"source" : "game","contacts" : ["1794748404@qq.com"],"subject" : "'" ${user_name} 账号过期警告"'","content" : "'" ${user_name} 账号过期警告 &lt;br&gt;  ${user_name} 即将在 ${diffday} 后过期，请及时修改 &lt;br&gt; 注意: 账号密码过期后,用户的Crontab中的执行任务会失效  &lt;br&gt;&lt;br&gt;&lt;br&gt;&lt;br&gt;&lt;br&gt;&lt;br&gt; "'"}'
    echo " time: $check_time   账号 ${user_name} 即将 在 ${diffday} 天后 密码过期 " &gt;&gt; ${log}
else

    echo " time: $check_time   账号 ${user_name} 还有 ${diffday} 天使用期 " &gt;&gt; ${log}
fi 

```

![d033a1bbe8474b1790781dab2229b3d7.png](https://img-blog.csdnimg.cn/d033a1bbe8474b1790781dab2229b3d7.png)

 ![09b90c8dffa044ac84a038006ff5db29.png](https://img-blog.csdnimg.cn/09b90c8dffa044ac84a038006ff5db29.png)

 

![185bd2a62462402ab3b8cb546d81ae45.png](https://img-blog.csdnimg.cn/185bd2a62462402ab3b8cb546d81ae45.png)

 ![1ce69121181246b79b2c8ae4140b1a5c.png](https://img-blog.csdnimg.cn/1ce69121181246b79b2c8ae4140b1a5c.png)

 
