# ws)l中的dock(…r不同安装形式
在 WSL 环 境 下 使 用 Docker 时 , 主 要 有 两 种 方 式 : Docker Desktop ( 集 成 WSL 后 端 ) 和 直 接 在 WSL 发 行 版 中 手 动 安 装 Docker。 以 下 是 它 们 的 区 别 及 安 装 位 置 详 解 :
# 1. Docker Desktop 集 成 WSL 后 端
# 1.1 特 点
s 安 装 方 式 : 通 过 Windows 安 装 程 序 安 装 Docker Desktop, 并 启 用 WSL 2 后 端 支 持 。
。 运 行 机 制 :
o _Docker Desktop 会 在 后 台 启 动 一 个 轻 量 级 的 Linux 虚 拟 机 ( 基 于 WSL 2) , 名 为 docker- desktop 和 docker-desktop-data 。
Docker 守 护 进 程 ( dockerd ) 运 行 在 docker-desktop 虚 拟 机 中 , 而 非 直 接 运 行 在 用 户 安 装 的 WSL 发 行 版 中 。 〇
o 用 户 可 以 在 任 意 WSL 发 行 版 中 直 接 使 用 docker 命 令 ,Docker Desktop 会 自 动 将 命 令 转 发 到 后 台 守 护 进 程 。
。 资 源 管 理 :
o _Docker Desktop 自 动 管 晚 资 源 (CPU、 内 存 、 存 储 ) , 与 WSL 2 共 享 资 源 .
o 镜 像 和 容 器 数 据 存 储 在 专 用 的 WSL 发 行 版 docker-desktop-data 中 。
“ 功 能 支 持 :
o 提 供 图 形 界 面 和 完 整 的 Docker 生 态 工 具 ( 如 Docker Compose、Kubernetes) 。
o 支 持 与 Windows 文 件 系 统 无 缝 集 成 ( 通 过 /mnt/c 访 问 Windows 文 件 ) 。
# 1.2 安 装 位 置
。 主 程 序 :
o Windows 路 径 : C:NProgranl F11es\DoCkKerxDocKker
datavversion-pack-dataxcommunityNdocker ( 通 过 Windows 资 源 管 理 器 访 问 ) 。
o 在 WSL 发 行 版 内 部 , 数 据 位 于 /var/1ib/docker 。
# 2. 直 接 在 WSL 发 行 版 中 安 装 Docker
2.1
特 点
“ 安 装 方 式 : 在 WSL 的 Linux 发 行 版 ( 如 Ubuntu) 中 , 手 动 通 过 apt 安 装 Docker 引 擎 ( docker.io 或 docker-ce ) 。
运 行 机 制 :
o _Docker 守 护 进 程 ( dockerd ) 直 接 运 行 在 WSL 发 行 版 中 。
o 需 要 手 动 启 动 Docker 服 务 ( sudo service docker start ) 。
。 资 源 管 理 :
o 容 器 和 镜 像 存 储 在 WSL 发 行 版 的 文 件 系 统 中 ( 如 /Var/1ib/docker ) 。
o 资 源 (CPU/ 内 存 ) 受 限 于 WSL 发 行 版 的 配 置 ( 通 过 .ws1config 调 整 ) 。
“ 功 能 支 持 :
o 仅 支 持 命 令 行 操 作 , 无 图 形 界 面 。
o 需 要 手 动 配 置 Docker 客 户 端 与 守 护 进 程 的 通 信 ( 通 常 通 过 Unix 套 接 字 unix:///yvar/run/docker.SoCK ) 。
# 2.2 安 装 位 置
。 主 程 序 :
o _WSL 发 行 版 中 的 Linux 路 径 : /usr/ybin/docker ( 客 户 端 ) 和 /usr/bin/dockerd ( 守 护 进 程 ) 。
。 镜 像 与 容 器 数 据
o 存 储 在 WSL 发 行 版 内 : /Nar/1ib/docker 。
# 3. 关 键 区 别 总 结
对 比 项 Docker Desktop (WSL 后 端 ) 颂 林 c Docker 安 装 复 杂 度 一 键 安 装 , 自 动 配 置 手 动 安 装 , 需 配 置 服 务 和 权 限 运 行 环 境 后 台 WSL 虚 拟 机 (docker-desktop ) 当 前 WSL 发 行 版 资 源 隔 离 专 用 虚 拟 机 隔 离 资 源 共 享 WSL 发 行 版 资 源 图 形 界 面 支 持 Docker Dashboard 仅 命 令 行 n Nws1$Ndocker-desktop-data WSL 发 行 版 的 数 据 存 储 位 置 (wWindows 可 见 ) /ar/1ib/docker 誓_菖」bernetes 支 内 置 支 挂 需 手 动 部 署 性 能 优 化 后 的 WSL 2 集 成 依 赖 WSL 发 行 版 配 置
Table 1
# 3.1 如 何 选 择 ?
。 推 荐 Docker Desktop:
适 合 需 要 图 形 界 面 、Kubernetes 支 持 或 希 望 简 化 管 理 的 用 户 , 九 其 是 开 发 跨 平 台 应 用
。
。 推 荐 手 动 安 装 :
适 合 熟 悉 Linux 管 理 、 希 望 减 少 资 源 占 用 ( 关 闭 Docker Desktop 后 台 进 程 ) 或 需 要 完 全 控 制 Docker 环 境 的 用 户 。
# 3.2 附 加 提 示
。 若 同 时 使 用 两 种 方 式 , 注 意 避 兖 端 口 冲 突 ( 如 2375/2376) 。
“ 通 过 docker context 命 令 可 切 换 Docker 客 户 端 连 接 的 目 标 ( 如 本 地 WSL 或 远 程 服 务 器 ) 。
# wslI 与 docker desktop 的 关 系
在 Windows 系 统 上 ,Docker Desktop 依 赖 于 ws| 来 运 行 Linux 内 校 , 从 而 支 持 Docker 引 擎 的 运 行
# 1. 关 系 说 明
1. WSL 提 供 基 础 环 境 : WSL 是 Windows 上 运 行 Linux 二 进 制 可 执 行 文 件 (ELF 格 式 ) 的 兼 容 层 , 它 包 含 了 一 个 轻 量 级 的 Linux 内 核 以 及 相 关 的 系 统 工 具 。 在 Docker Desktop 的 运 行 过 程 中 ,WSL 负 责 提 供 底 层 的 Linux 环 境 , 使 得 Docker 引 擎 能 够 在 Windows 系 统 上 正 常 运 行 。
2. Docker Desktop 集 成 和 管 理 : Docker Desktop 基 于 WSL 构 建 , 它 集 成 了 Docker 引 擎 、Docker CLI 客 户 端 以 及 Docker Compose 等 工 具 , 为 用 户 提 供 了 一 个 图 形 化 和 命 令 行 相 结 合 的 界 面 , 方 便 用 户 管 理 Docker 容 器 、 镜 像 和 网 络 等 资 源 。 用 户 可 以 通 过 Docker Desktop 的 图 形 界 面 轻 松 创 建 、 启 动 、 健 止 和 删 除 容 器 , 也 可 以 使 用 命 令 行 进 行 更 高 级 的 操 作 。
. 数 据 交 互 : Docker Desktop 利 用 WSL 的 文 件 系 统 共 享 功 能 , 实 现 了 Windows 文 件 系 统 和 Docker 容 器 内 文 件 系 统 之 间 的 数 据 交 互 。 用 户 可 以 将 Windows 系 统 上 的 文 件 和 目 录 挂 载 到 Docker 容 器 中 , 方 便 在 容 器 内 访 问 和 处 理 这 些 数 据
# 2. 示′=慧图
windows docker desktop 用 户 安 装 的 wsl| 发 行 版 Docker 引擎 -docker-desktop( 后 台 运 行 docker (】o(>ker4藿…，墓ktop4】at羞】(1定番了著二妄竟{皙l浠【/ 容 器 数 据 ) ws| 的 子 系 统 (hyper-v)
FigtHre 1
# 2.1 关 键 关 系 解 析
# 1. Docker Desktop 的 后 台 WSL 虚 拟 机
o _Docker Desktop 默 认 创 建 两 个 专 用 WSL 发 行 版 :
“ “docker-desktop : 运 行 Docker 守 护 进 程 ( dockerd ) 。
“docker-desktop-data : 存 储 镜 像 、 容 器 等 数 据 ( 位 于 /var/1ib/docker ) 。
o 这 些 虚 拟 机 由 Docker Desktop 自 动 管 理 , 用 户 无 需 直 接 操 作 。
# 2. 用 户 安 装 的 WSL 发 行 版
o 用 户 自 行 安 装 的 WSL 发 行 版 ( 如 Ubuntu) 中 , 可 以 直 接 使 用 docker 命 令 。
0_Docker CLI 默 认 通 过 Unix 套 接 字 ( /Var/run/docker.sock ) 或 TCP 连 接 到 docker- desktop 虚 拟 机 中 的 守 护 进 程 , 无 需 手 动 配 置
# 3. WSL 2 子 系 统
o 所 有 WSL 发 行 版 ( 包 括 Docker Desktop 的 虚 拟 机 和 用 户 安 装 的 发 行 版 ) 均 运 行 在 WSL 2 的 虚 拟 化 层 上 , 依 赖 Hyper-V 提 供 Linux 内 核 和 资 源 隔 禽 。
# 4. 文 件 系 统 互 通
0 WSL 发 行 版 可 直 接 访 问 Windows 文 件 系 统 ( 通 过 /mnt/c 等 路 径 ) 。
o _Docker 容 器 通 过 Volume 挂 载 实 现 与 Windows/WSL 文 件 系 统 的 交 互 。
# 5. 网 络 互 通
0 _Docker 容 器 网 络 与 WSL 发 行 版 共 享 同 一 网 络 栈 , 可 通 过 10calhost 目 接 访 问 容 器 端 口 ( 无 需 配 置 -p 127.0.0.1:8080:80 )
# 2.2 协 作 流 程
1. 用 户 在 WSL 发 行 版 ( 如 Ubuntu) 中 执 行 docKer run 命 令 。
2. Docker CLI 将 命 令 转 发 到 docker-desktop 虚 拟 机 中 的 守 护 进 程 .
3. 守 护 进 程 创 建 容 器 , 容 器 进 程 运 行 在 docker-desktop 虚 拟 机 的 隔 离 环 境 中 。
4. 容 器 数 据 存 储 在 docker-desktop-data 虚 拟 机 中 , 与 用 户 WSL 发 行 版 分 离 。
5. 用 户 可 通 过 Windows 资 源 管 理 器 访 问 AAWws1xdocker-desktop-data 查 看 镜 像 和 容 器 数 据
docker desktop
Figure 2
# 2.3 对 比 手 动 在 WSL 中 安 装 Docker
若 手 动 在 WSL 发 行 版 中 安 装 Docker ( 不 依 赖 Docker Desktop) :
s Docker 守 护 进 程 直 接 运 行 在 用 户 WSL 发 行 版 中 , 与 Docker Desktop 的 虚 拟 机 无 关 。
。 镜 像 和 容 器 数 据 存 储 在 用 户 WSL 发 行 版 的 /var/1ib/docker 目 录 下 。
s 需 手 动 管 理 服 务 ( 如 sudo service docker start ) , 一 无 图 形 界 面 支 持
# 2.4 总 结
Docker Desktop 通 过 WSL 2 虚 拟 机 实 现 Docker 环 境 与 Windows 的 深 度 集 成 , 而 用 户 安 装 的 WSL 发 行 版 仅 作 为 客 户 端 使 用 。 这 种 设 计 既 保 证 了 性 能 , 又 简 化 了 跨 平 台 开 发 流 程