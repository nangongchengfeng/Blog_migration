---
author: 南宫乘风
categories:
- Gitlab
date: 2024-03-22 16:32:28
description: 背景在现代软件开发实践中，持续集成是确保代码质量和快速响应软件缺陷的关键策略。提供了强大的功能，允许开发者自动化测试和部署流程。本文将介绍如何设置流水线计划任务，以实现对分支每小时的自动测试。需求：流。。。。。。。
image: ../../title_pic/64.jpg
slug: '202403221632'
tags:
- gitlab
- 自动化
title: Gitlab的流水线任务【实现每小时自动测试 dev分支的更新】
---

<!--more-->

## 背景

在现代软件开发实践中，持续集成（Continuous Integration, CI）是确保代码质量和快速响应软件缺陷的关键策略。GitLab 提供了强大的 CI/CD 功能，允许开发者自动化测试和部署流程。本文将介绍如何设置 GitLab 流水线计划任务，以实现对 `dev` 分支每小时的自动测试。

**需求：** GitLab 流水线计划任务（pipeline-schedules）：实现每小时自动测试 `dev` 分支的更新

## 环境

Gitlab企业版本：v16.9.2-ee
![在这里插入图片描述](../../image/a222a8305c1c42c9a38a132a16c854ff.png)
GitLab 流水线是一系列作业（jobs）的集合，这些作业可以并行或顺序执行，以完成构建、测试、部署等任务。流水线可以由代码提交、定时计划或其他事件触发。

计划任务是 GitLab 流水线的一个特性，它允许你按计划执行流水线，而不需要代码提交或其他触发条件。这对于定期运行测试、备份或其他维护任务特别有用。

## 每小时自动测试 `dev` 分支的步骤

### 创建 `.gitlab-ci.yml` 配置文件

在项目的根目录下，创建或编辑 `.gitlab-ci.yml` 文件，这是 GitLab 流水线的配置文件。我们将定义两个作业：一个是常规的测试作业，另一个是计划任务作业。

```yml
stages:
  - test
  - alert
  - jar


before_script:
  - export PATH=/usr/lib/jvm/java-21/bin:${PATH}        # 将java路径添加到PATH路径中。如果是java 11，使用/usr/lib/jvm/java-11/bin。

ci_test:
  stage: test
  script:
    - |
      if [ "$(git log origin/dev --since='1 hour ago' --pretty=format:'%h')" != "" ]; then
        mvn clean test
      else
        echo "No changes in the last hour"
      fi
    - export
  rules:
    - if: '$CI_PIPELINE_SOURCE == "schedule" && $CI_COMMIT_BRANCH == "dev"'

dingTalk_fail_alert:
  stage: alert
  script:
    - /bin/bash /opt/k8s/dingtalk/ding_ci_alert.sh fail
  when: on_failure
  allow_failure: true
  rules:
    - if: '$CI_PIPELINE_SOURCE == "schedule" && $CI_COMMIT_BRANCH == "dev"'

dingTalk_succes_alert:
  stage: alert
  script:
    - /bin/bash /opt/k8s/dingtalk/ding_ci_alert.sh success
  when: on_success
  allow_failure: true
  rules:
    - if: '$CI_PIPELINE_SOURCE == "schedule" && $CI_COMMIT_BRANCH == "dev"'
  
jar:
  stage: jar
  tags:
    - pdd
  cache:
    paths:
      - manage-analysis/target/*.jar
      - manage-listener/target/*.jar
      - manage-backend/target/*.jar
    policy: push
    key: ${CI_BUILD_REF_NAME}
  script:
    - mvn clean install -Dmaven.test.skip=true
  rules:
    - if: '$CI_PIPELINE_SOURCE != "schedule" && $CI_COMMIT_BRANCH == "dev"'

```

### 配置钉钉告警机器人

配置钉钉告警机器人：关键字认证 “告警”
![在这里插入图片描述](../../image/598875b5aa294cc78e83fecdaf334237.png)
### 配置告警脚本脚本模板


在GitLab CI/CD 管道中，我们设计了一个名为 `ding_ci_alert.sh` 的Shell脚本，用于对接钉钉机器人发送构建状态的通知。针对不同的构建结果，我们有如下需求：

1. 当Maven测试任务失败时，我们会向脚本传递一个参数 `"fail"`，表示构建失败。此时，脚本不仅会调用钉钉机器人发送一条包含失败详情的告警消息，还会将此次失败的构建ID写入一个专门记录失败构建的文件中。
2. 当后续的Maven测试任务成功时，我们将向脚本传递一个参数 `"success"`，以标识构建成功。这时，脚本首先会检查记录失败构建的文件中是否存在当前构建ID。如果存在，则调用钉钉机器人发送一条成功恢复的消息，并从记录文件中移除此构建ID；反之，若当前构建ID未在文件中找到，则不发送成功告警信息。

这样，我们通过灵活调用和智能判断，确保了在构建失败时及时通知相关人员，并在问题得到解决后发送成功通知，既避免了不必要的通知干扰，又保证了团队能够及时了解到构建状态的变化。在实际的博客文章中，您可以插入示例代码和详细说明，让读者更直观地理解这一过程。


`vim` `/opt/k8s/dingtalk/ding_ci_alert.sh`

```yml
#!/bin/bash

WEBHOOK_URL="https://oapi.dingtalk.com/robot/send?access_token=xxxxx"
# 检查是否提供了参数
if [ "$#" -ne 1 ]; then
  echo "Usage: $0 <success|fail>"
  exit 1
fi

# 定义记录文件路径
RECORD_FILE="/tmp/build_records.txt"

# 根据传入的参数执行相应操作
case $1 in
  fail)
    # 构建失败，发送告警并记录
    echo "构建失败，发送告警..."

    # 准备告警消息
    JSON_DATA=$(printf '{
      "msgtype": "markdown",
      "markdown": {
        "title": "告警:构建失败通知",
        "text": "#### **[%s 的 Maven 测试未通过构建失败](%s/pipelines/%s)**\n\n> - **提交信息**: %s\n> - **提交者名称**: %s\n> - **提交时间**: %s\n\n请及时处理，更多详情可点击项目名称。"
      },
      "at": {
        "isAtAll": false
      }
    }' "$CI_PROJECT_NAME" "$CI_PROJECT_URL" "$CI_PIPELINE_ID" "$CI_COMMIT_MESSAGE" "$CI_COMMIT_AUTHOR" "$CI_COMMIT_TIMESTAMP")

    # 发送告警
    curl "$WEBHOOK_URL" -X POST -H 'Content-Type: application/json;charset=utf-8' -d "$JSON_DATA"

    # 记录失败的构建
    echo "$CI_PROJECT_NAME failed" >> "$RECORD_FILE"
    ;;
  success)
    # 构建成功，检查记录文件
    if grep -q "$CI_PROJECT_NAME failed" "$RECORD_FILE"; then
      echo "构建成功，发送告警..."

      # 准备成功告警消息
      SUCCESS_JSON_DATA=$(printf '{
        "msgtype": "markdown",
        "markdown": {
          "title": "告警:构建成功通知",
          "text": "#### **[%s 的 Maven 测试已通过构建成功]**\n\n> - **提交信息**: %s\n> - **提交者名称**: %s\n> - **提交时间**: %s\n\n构建成功，可以进行下一步操作。"
        },
        "at": {
          "isAtAll": false
        }
      }' "$CI_PROJECT_NAME" "$CI_COMMIT_MESSAGE" "$CI_COMMIT_AUTHOR" "$CI_COMMIT_TIMESTAMP")

      # 发送成功告警
      curl "$WEBHOOK_URL" -X POST -H 'Content-Type: application/json;charset=utf-8' -d "$SUCCESS_JSON_DATA"

      # 清除记录
      sed -i "/$CI_PROJECT_NAME failed/d" "$RECORD_FILE"
    else
      echo "没有找到构建失败的记录，不发送成功告警。"
    fi
    ;;
  *)
    echo "Invalid argument: $1. Expected 'success' or 'fail'."
    exit 1
    ;;
esac

exit 0

```

### 设置流水线计划

步骤1：登录GitLab并进入项目

1. 登录到您的GitLab账号。
2. 导航到您想要设置流水线计划的项目。

步骤2：进入CI/CD设置

1. 在项目主页，点击左侧面板中的“CI/CD”选项卡。
2. 在CI/CD设置区域，点击“Schedules”（调度）。

步骤3：创建新的流水线计划

1. 在“Schedules”页面，点击“New schedule”按钮以创建一个新的流水线计划。

步骤4：配置流水线计划详细信息

1. **描述**：为您的流水线计划提供一个易于理解的描述，以便日后识别。
2. **CRON 表达式**：输入一个cron表达式来定义计划执行的时间规律。例如，每天凌晨1点执行，可以输入`0 1 * * *`。请参考cron表达式文档以获取更多信息。
3. **分支/标签**：可以选择流水线将在哪个分支或标签上执行，默认通常是当前项目的默认分支（如master/main）。
4. **额外变量**（可选）：如果需要，您可以为流水线提供额外的环境变量，这将在计划执行时注入到环境中。
5. **保护**（可选）：如有必要，您可以勾选“Protect this pipeline”，这样只有具有适当权限的用户才能执行或修改该流水线计划。

步骤5：保存流水线计划

1. 配置完所有选项后，滚动到底部并点击“Save changes”。

步骤6：验证流水线计划

1. 在指定的时间，GitLab将根据您设置的cron表达式自动触发流水线。您可以在项目的历史流水线记录中查看流水线计划的执行情况。

**注意事项**

* 确保您的项目中有`.gitlab-ci.yml`文件，并且文件中定义了适当的CI/CD流水线配置，这样才能在计划时间到来时执行预定的任务。
* 如果流水线涉及到敏感信息，您可能需要预先配置好变量并通过密钥管理或GitLab的受保护变量功能来安全地传递这些信息。
* 某些高级设置，如运行特定job，需要在`.gitlab-ci.yml`文件中通过`rules`或`only/except`关键字进行定义。

**注意：第二张图片 `CI_PIPELINE_SOURCE` 是自己定义的变量**

额 外 变 量 （ 可 选 ） ： 如 果 需 要 ， 您 可 以 为 流 水 线 提 供 额 外 的 环 境 变 量 ， 这 将 在 计 划 执 行 时 注 入 到 环 境 中 ， 一 般 我 们 会 配 置 一 个 变 量 名 字 叫 $CI PIPELINE_SOURCE ， 它 的 值 为 s c h ed u le 通 过 这 个 方 式 ， 我 们 就 能 够 确 保 .gitlab-ci.yml 文 件 里 面 只 有 定 义 了 以 下 规 则 的 stage 才 会 执 行 这 个 定 时 任 务 ：
```bash
  rules:
    - if: '$CI_PIPELINE_SOURCE == "schedule" && $CI_COMMIT_BRANCH == "dev"'
```
保 护 （ 可 选 ） ： 如 有 必 要 ， 您 可 以 勾 选 "Protect this pipeline", 这 样 只 有 具 有 适 当 权 限 的 用 户 才 能 执 行 或 修 改 该 流 水 线 计 划 。
![在这里插入图片描述](../../image/0997cea0bf3e403b8e896d46a8e44eac.png)
![在这里插入图片描述](../../image/dd91755e83e44a39843efaeb2ce340ce.png)

## 验证流水线自动化
![在这里插入图片描述](../../image/e1d9aec68b204ba9a65083658bde1970.png)
![在这里插入图片描述](../../image/41fcdcb60138410cb92293ad0f21d285.png)

![在这里插入图片描述](../../image/896f6b93e79840f5954dc6ab3b9df608.png)


![在这里插入图片描述](../../image/d3c02b02d3c7461ba38c6645ab5fefde.png)






