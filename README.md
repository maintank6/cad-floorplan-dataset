# CAD 平面图数据集交接

原 `CAD图纸数据` 目录的完整文件交接，整理日期：2026-10-11。

- 文件数：22,265。
- 原始总大小：6,169,821,441 字节（约 6.17 GB）。
- `cubicasa5k/`：平面图图片、SVG、已有 DXF 转换结果和 train/val/test 划分文本。
- `pathfinder图/`：已有 Pathfinder 工程、轨迹 / 统计输出和其他仿真文件。
- 代码项目：[cad-evacuation-toolkit](https://github.com/maintank6/cad-evacuation-toolkit)。

## 获取完整数据

数据文件放在本仓库的 [Release 下载区](https://github.com/maintank6/cad-floorplan-dataset/releases/tag/handoff-2026-10-11)。网页上的 **Code → Download ZIP** 只包含说明、清单和下载脚本。

```powershell
git clone https://github.com/maintank6/cad-floorplan-dataset.git
cd cad-floorplan-dataset
python fetch_dataset.py
```

脚本只需 Python 3.9+ 标准库，会下载 5 个独立 TAR.XZ 包、逐包核对 SHA-256、解压到 `dataset/`，最后按 `FILES.csv` 逐文件核对大小和 SHA-256。成功下载的包可复用；中断包会重新下载。默认保留下载包，总磁盘空间建议预留至少 15 GB。

指定目录：`python fetch_dataset.py --output D:/CAD图纸数据 --downloads D:/CAD下载包`。

也可以在 Release 中手动下载全部 TAR.XZ，逐个解压到同一个目录（Windows 可用 7-Zip 或 `tar -xf 包名.tar.xz`）。它们是独立 TAR.XZ，**无需拼接**，保留内部的 `cubicasa5k/` 与 `pathfinder图/` 路径即可。

## 文件清单

| 文件 | 内容 |
| --- | --- |
| `FILES.csv` | 全部 22,265 个数据文件的相对路径、大小、SHA-256、所属压缩包 |
| `dataset.json` | 压缩包文件名、大小、SHA-256、文件数与 Release 标签 |
| `SHA256SUMS.txt` | TAR.XZ 包 SHA-256 汇总 |
| `DATA_SOURCES.md` | 数据来源、上游许可和本地转换说明 |

这是本地交接快照，未重新生成图纸或仿真结果，内部数据内容保持原样。解压后查看 `pathfinder图` 工程需要另行安装 Pathfinder。

## 来源与许可

[CubiCasa5K](https://github.com/CubiCasa/CubiCasa5k) 上游许可为 [CC BY-NC 4.0](https://github.com/CubiCasa/CubiCasa5k/blob/master/LICENSE)。使用时保留来源和许可信息、标明修改并遵守非商业条件。更多见 [DATA_SOURCES.md](DATA_SOURCES.md)。
