# Deprecated Tests and Data

此目录包含已废弃的旧测试代码和测试输出数据。

**这些文件将在确认新测试稳定后手动删除。**

## 目录结构

```
_deprecated/
├── test_xvg.py          # 旧 XVG 测试 (引用旧代码结构)
├── test_xpm.py          # 旧 XPM 测试 (引用旧代码结构)
├── test_ndx.py          # 旧 NDX 测试 (引用旧代码结构)
├── test_find_center.py  # 旧 find_center 测试
└── old_outputs/         # 旧的测试输出数据
    ├── xvg_test/        # XVG 测试数据 (包含输出文件 .png, .csv)
    ├── xpm_test/        # XPM 测试数据 (包含输出文件)
    ├── ndx_test/        # NDX 测试数据
    └── find_center_test/ # find_center 测试数据
```

## 新的测试目录结构

请参考 `Tests/fixtures/` 目录获取测试输入数据。

新的测试代码位于:
- `Tests/test_utils.py`
- `Tests/parsers/`
- `Tests/commands/`
