# Confuse

iOS 工程混淆工具集：Objective-C 与 Swift 垃圾代码注入、工程前缀重命名、函数宏混淆。

## 目录结构

```
Confuse/
├── README.md
├── confuse.py                         # 统一入口（自动检测 OC / Swift）
├── project_detect.py                  # 工程源文件类型扫描
├── auto_config.py                     # 加载 profiles/<name>/auto.json
├── profiles/                          # 工程相关配置（按 profile 隔离，便于移植）
│   └── default/                       # 示例 profile，可复制为新工程
│       ├── auto.json                  # 统一入口：忽略目录、enabled_modules 覆盖
│       ├── writecode.json             # OC 垃圾代码写入：白名单、数量、开关类名等
│       ├── swift.json                 # Swift 垃圾代码 / 重命名：白名单、数量、忽略规则等
│       └── rename.env                 # 重命名：白名单、临时目录、宏头文件路径等
├── resource/                          # 共享资源（词库、UIKit API 解析结果等）
│   ├── words.txt                      # 通用英文词库（内置，一行一词，约 3500+）
│   ├── ioswords.txt                   # iOS/OC 风格后缀词库（内置，约 2200+）
│   ├── _generate_wordlists.py         # 从 _word_roots.py 重新生成词库
│   ├── _word_roots.py                 # 词根与组合规则（生成脚本专用）
│   ├── _append_uikit_apis.py          # 去重追加 UIKit API 到 func_orign
│   ├── random_func_create.txt         # OC 运行时生成，Git 忽略
│   ├── random_class_name.txt          # OC 运行时生成，Git 忽略
│   ├── random_swift_func_create.txt   # Swift 运行时生成，Git 忽略
│   ├── random_swift_class_name.txt    # Swift 运行时生成，Git 忽略
│   ├── swift_rename_map.json          # Swift 重命名映射表，Git 忽略
│   ├── func_orign/                    # iOS 原生 API 原文（约 1850 行）
│   └── func_analysised/               # 经 analysis 解析后的 API 字典（JSON 行）
├── writecode/                         # OC 垃圾代码写入模块
│   ├── config.py                      # 加载 profile + 运行时路径
│   ├── profile_loader.py              # profile 解析与 JSON 读取
│   ├── writecontrol.py                # 入口脚本
│   ├── codemodel.py / filemanager.py / randomvalue.py
│   ├── xcodeprojhelp.rb
│   └── analysis/                      # 原生 SDK 解析（analys.py）
├── swift/                             # Swift 混淆模块（与 writecode 并列）
│   ├── config.py                      # 加载 swift.json profile
│   ├── profile_loader.py
│   ├── writecontrol.py                # 入口：注入 / 新建文件 / 重命名
│   ├── codemodel.py / filemanager.py / randomvalue.py
│   ├── rename.py                      # Swift 符号前缀重命名
│   ├── xcodeprojhelp_swift.rb         # 向 .xcodeproj 注册 .swift 文件
│   └── _test_fixtures/                # 本地 dry-run 样例工程
├── rename/                            # OC 重命名模块
│   ├── common.sh                      # 加载 profile 的公共逻辑
│   ├── projectfile.sh                 # 工程前缀重命名
│   └── func.sh                        # 函数宏混淆
└── .work/                             # func.sh 临时 sqlite/列表（Git 忽略）
```

## Profile：创建与切换

工具核心（`writecode/`、`rename/`、`resource/`）与**工程配置**分离。每个 iOS 工程建议复制一份 profile：

```bash
cp -R profiles/default profiles/my_app
# 编辑 profiles/my_app/writecode.json   # OC
# 编辑 profiles/my_app/swift.json      # Swift
# 编辑 profiles/my_app/rename.env      # OC 重命名
```

切换 profile 的两种方式（二选一）：

```bash
# 环境变量
export CONFUSE_PROFILE=my_app

# 或命令行参数
python3 confuse.py --profile my_app --project /Users/you/MyApp
python3 writecode/writecontrol.py --profile my_app
python3 swift/writecontrol.py --profile my_app
sh rename/func.sh --profile my_app
sh rename/projectfile.sh --profile my_app
```

未指定时默认使用 `default`。

### auto.json 字段说明（统一入口）

| 字段 | 说明 |
|------|------|
| `enabled_modules` | `null` 表示按工程自动检测；或 `["oc"]` / `["swift"]` / `["oc","swift"]` 强制指定 |
| `ignore_dirs` | 扫描 `.m/.h/.swift` 时跳过的目录名（默认含 `Pods`、`Carthage`、`Build`、`.git` 等） |

## 推荐：统一入口（自动检测 OC / Swift）

无需手动选择语言，工具会扫描工程并运行对应模块：

```bash
python3 /path/to/Confuse/confuse.py --project /Users/you/MyApp --profile default

# 非交互：白名单注入 + 新建 10 个垃圾文件
python3 confuse.py --project /Users/you/MyApp --inject-white --new-files 10

# 仅预览（Swift 模块 dry-run；OC 模块仍会写入）
python3 confuse.py \
  --project swift/_test_fixtures/MyApp \
  --inject-white --new-files 2 --dry-run --skip-xcode

# 仅查看检测结果
python3 confuse.py --project /Users/you/MyApp --detect-only
```

**自动检测规则：**

| 条件 | 运行模块 |
|------|----------|
| 存在 `.m` 文件（非纯头工程） | OC `writecode/writecontrol.py` |
| 存在 `.swift` 文件 | Swift `swift/writecontrol.py` |
| 混编（同时有 `.m` 与 `.swift`） | **两者都跑**，共用同一 `--profile` |
| 仅有 `.h`、无 `.m` | 不跑 OC 模块（纯头文件/SDK 头） |

扫描时会忽略 `Pods/`、`Carthage/`、`Build/`、`.git/` 等目录（与 `auto.json` 及 Swift profile 白名单一致）。

**交互简化：** 统一入口只问一次工程路径与通用选项（白名单注入、新建文件数、Swift 重命名等），不再询问「选 OC 还是 Swift」。各子模块入口仍可单独使用（向后兼容）。

OC 函数宏 / 工程前缀重命名（`rename/func.sh`、`rename/projectfile.sh`）仍为独立脚本；统一入口的 `--rename` 仅作用于 Swift 符号重命名。

### writecode.json 字段说明

| 字段 | 说明 |
|------|------|
| `file_while_list` | 白名单文件夹名（仅这些目录下的 `.h/.m` 可写入垃圾代码） |
| `m_h_num_min` / `m_h_num_max` | 每个文件生成属性/方法数量的范围 |
| `call_all_class` | 控制开关类名；空字符串则自动创建「工程名+AllCall」 |
| `call_func_name` | 开关类中的入口方法名 |
| `hx_folder` | 使用自定义开关类时，`.h/.m` 所在子目录名（默认 `HX`） |

### swift.json 字段说明

| 字段 | 说明 |
|------|------|
| `file_while_list` | 白名单文件夹名（仅这些目录下的 `.swift` 参与注入/重命名） |
| `member_num_min` / `member_num_max` | 每个类型注入属性/方法数量的范围 |
| `new_file_count_min` / `new_file_count_max` | 交互模式下新建垃圾 Swift 文件的数量参考范围 |
| `call_all_class` | 调用入口类名；空则自动创建「工程名+SwiftAllCall」 |
| `call_func_name` | 入口类中的调用方法名 |
| `hx_folder` | 自定义入口类 `.swift` 所在子目录（默认 `HX`） |
| `output_subdir` | 新建垃圾 `.swift` 的输出子目录；空则写入工程主 target 目录 |
| `inject_properties` / `inject_methods` | 是否向现有 Swift 类型注入属性/方法 |
| `rename_enabled` | profile 默认是否开启重命名（也可用 CLI `--rename`） |
| `rename_prefix` | 符号重命名前缀（如 `Obf` → `ObfMyClass`） |
| `rename_types` / `rename_functions` / `rename_properties` | 重命名范围开关 |
| `skip_line_patterns` | 含这些子串的行跳过注入/重命名（如 `@objc`、`override`、`init(`） |
| `ignore_dirs` / `ignore_files` | 遍历时跳过的目录/文件名 |

### rename.env 字段说明

| 变量 | 说明 |
|------|------|
| `FUNC_IGNORE_FILE` | func.sh 遍历工程时跳过的文件夹 |
| `PROJECT_IGNORE_FILE` | projectfile.sh 复制时跳过的文件/文件夹 |
| `FUNC_WORK_SUBDIR` | 符号表、func.list 等临时文件目录（相对仓库根） |
| `OBFUSCATION_SUBDIR` | 宏头文件相对工程路径的子目录 |
| `OBFUSCATION_HEADER` | 生成的宏头文件名 |
| `OBFUSCATION_HEADER_GUARD` | 头文件 `#ifndef` 宏名 |

## 环境

- macOS
- Python 3
- Ruby（writecontrol 修改 `.xcodeproj` 时需要；Swift 新建文件注册同样需要）
- sqlite3（func.sh）

## resource/ 资源说明

`resource/` 为共享素材目录，与 profile 无关。OC 垃圾代码、符号重命名、Swift 注入均会读取其中词库与 API 解析结果。

### 规模（当前内置）

| 路径 | 条数 | 说明 |
|------|------|------|
| `words.txt` | **3568** 词 | 通用英文词根（动词/名词/形容词），一行一词 |
| `ioswords.txt` | **2219** 词 | UIKit/SwiftUI/Foundation 风格后缀与组件名片段 |
| `func_orign/uikit_class_func.txt` | **210** 行 | UIKit/Foundation 类方法（`+`）原文 |
| `func_orign/uikit_class_instancetype_func.txt` | **89** 行 | 类工厂方法（`+ (instancetype)`）原文 |
| `func_orign/uikit_member_func.txt` | **1352** 行 | 实例方法（`-`）原文 |
| `func_orign/uikit_member_instancetype_func.txt` | **203** 行 | 实例初始化方法（`- (instancetype)`）原文 |
| `func_analysised/*.txt` | 与 `func_orign` 对应 | 经 `analys.py` 解析后的 JSON 行（`params` / `returntype` / `funcname` / `descrip`） |
| `random_func_create.txt` | 运行时生成 | OC 自定义函数模板缓存（Git 忽略） |
| `random_class_name.txt` | 运行时生成 | OC 随机类名列表（Git 忽略） |

### 消费关系

| 消费者 | 读取的资源 |
|--------|------------|
| `writecode/randomvalue.py`、`swift/randomvalue.py` | `words.txt`、`ioswords.txt` |
| `rename/func.sh` | `words.txt`、`ioswords.txt` |
| `writecode/writecontrol.py` → `codemodel.system_func_call_model` | `func_analysised/uikit_class_func.txt`（系统 API 调用模板） |
| `writecode/writecontrol.py` → `randomvalue.func_create` | 写入 `random_func_create.txt`、`random_class_name.txt` |

### 词库格式

| 文件 | 用途 | 格式 |
|------|------|------|
| `words.txt` | 通用英文单词（变量名、参数标签、类名片段等） | **一行一词**的合法 OC 标识符（字母开头，仅字母数字）；空行与 `#` 开头注释行会被忽略 |
| `ioswords.txt` | iOS/OC 风格后缀（如 `View`、`Controller`、`Manager`） | 同上（PascalCase 片段）；与 `words.txt` 随机组合成函数名（如 `fetch` + `Handler`） |

### 扩展与重新生成

**词库（推荐脚本生成）：**

```bash
python3 resource/_generate_wordlists.py
```

脚本从 `resource/_word_roots.py` 中的词根与组合规则生成 `words.txt` / `ioswords.txt`，并过滤 OC/Swift 保留字与常见系统类名冲突。也可手工向上述 `.txt` 追加单词（每行一词）。

**UIKit API：**

1. 向 `func_orign/*.txt` 追加真实 API 声明（每行一条，与头文件一致）
2. 或运行补充脚本：`python3 resource/_append_uikit_apis.py`（去重追加内置补充集）
3. 重新解析：

```bash
python3 writecode/analysis/analys.py
```

`analys.py` 会覆盖 `func_analysised/` 下四个对应文件。`writecode/config.py` 中 `system_func_path` 指向 `func_analysised/uikit_class_func.txt`。

建议避免与 UIKit/Foundation 类名、保留字（`init`、`dealloc` 等）完全相同的单词。

## 使用流程

### 一、垃圾代码写入（writecontrol.py）

**命令：**

```bash
python3 /path/to/Confuse/writecode/writecontrol.py
# 或指定 profile
python3 /path/to/Confuse/writecode/writecontrol.py --profile default
```

**交互说明：**

假设工程 `.xcodeproj` 为 `/Users/you/MyApp/MyApp.xcodeproj`：

1. `HX` 目录（或使用自定义开关类时）为 `/Users/you/MyApp/HX`
2. 白名单文件夹路径示例：`/Users/you/MyApp/MyApp/Services`
3. 输入的路径为 `.xcodeproj` 的**上一级目录**：`/Users/you/MyApp`

**配置（在 profile 中修改，而非改代码）：**

1. `writecode.json` 的 `file_while_list`：仅白名单内文件夹参与写入
2. `call_all_class`：
   - 留空：自动创建「工程名+AllCall」类
   - 设为 `XSDKAllCall` 等：需在工程同级 `HX`（或 `hx_folder`）下已有对应 `.h/.m`

### 二、工程前缀重命名（projectfile.sh）

**命令：**

```bash
sh /path/to/Confuse/rename/projectfile.sh
```

脚本会**拷贝**旧工程到新目录并在副本上重命名，不影响原工程。白名单在 profile 的 `PROJECT_IGNORE_FILE` 中配置。

### 三、函数宏混淆（func.sh）

**命令：**

```bash
sh /path/to/Confuse/rename/func.sh
```

1. 在 profile 的 `FUNC_IGNORE_FILE` 中配置不需处理的目录
2. 三种模式：特征前缀混淆 / 全部 `.h` 声明 / 两者兼有
3. 生成的宏头文件路径由 `OBFUSCATION_*` 配置；临时数据库在 `.work/<profile>/`

跑完后请手动检查宏头文件，删除误混淆的系统方法声明。

### 四、Swift 垃圾代码与重命名（swift/writecontrol.py）

**命令：**

```bash
python3 /path/to/Confuse/swift/writecontrol.py
python3 /path/to/Confuse/swift/writecontrol.py --profile default

# 非交互示例
python3 swift/writecontrol.py \
  --project /Users/you/MyApp \
  --inject-white \
  --new-files 10 \
  --skip-xcode

# 仅预览
python3 swift/writecontrol.py \
  --project swift/_test_fixtures/MyApp \
  --inject-white --new-files 2 --dry-run --skip-xcode

# 符号前缀重命名（生成 resource/swift_rename_map.json）
python3 swift/writecontrol.py --project /Users/you/MyApp --rename
```

**能力：**

1. 向白名单目录内现有 `.swift` 的 `class`/`struct`/`extension` 注入 `private` 属性与方法
2. 在工程目录（或 `output_subdir`）新建完整 Swift 垃圾类文件，并通过 `xcodeprojhelp_swift.rb` 注册到 Xcode（需 Ruby + xcodeproj gem）
3. 可选前缀重命名：类型 / 函数 / 属性，并输出映射表

**Swift 语法与限制：**

| 场景 | 说明 |
|------|------|
| 跳过规则 | 含 `override`、`@objc`、`@IBAction`、`@IBOutlet`、`init(`、`deinit` 等的行不会被注入或作为重命名锚点 |
| 混编 | `@objc` 暴露给 OC 的符号请勿重命名；Swift 侧注入的 `private` 成员不影响 OC 桥接 |
| SPM | 纯 Swift Package 无 `.xcodeproj`，请使用 `--skip-xcode` 并手动维护 Package 源文件列表 |
| 重命名 | 为简单词边界替换，可能误改字符串字面量；重命名后需自行编译验证 |
| rename/ | OC 的 `func.sh` / `projectfile.sh` **不处理** Swift 源文件，Swift 重命名请用本模块 |

### 五、（可选）重新生成词库与 UIKit API 解析文件

```bash
# 词库
python3 /path/to/Confuse/resource/_generate_wordlists.py

# UIKit API 补充（去重追加 func_orign）
python3 /path/to/Confuse/resource/_append_uikit_apis.py

# 解析 func_orign → func_analysised
python3 /path/to/Confuse/writecode/analysis/analys.py
```

路径已相对仓库根目录，无需改本机绝对路径。

## 典型移植步骤

1. 复制 `profiles/default` 为新 profile 名
2. 按目标工程修改 `writecode.json`（OC）、`swift.json`（Swift）、`rename.env`（OC 重命名）
3. （可选）运行 `resource/_generate_wordlists.py` 或手工扩展 `resource/words.txt`、`resource/ioswords.txt`
4. 推荐使用 `python3 confuse.py --project 工程路径 --profile 新名`；或分别运行各子模块
