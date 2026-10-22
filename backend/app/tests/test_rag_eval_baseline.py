"""RAGAS 评测基准的契约测试。

README 中承诺的正式基准位于 docs/datas/evals/rag_cases.json，评测提交接口
会按该文件构建评测集。本测试用于保证文档承诺与仓库内容一致，避免出现
「文档写着有、实际不存在」导致评测提交后返回 no_cases 的情况。
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).resolve().parents[3]
BASELINE_PATH = PROJECT_ROOT / "docs" / "datas" / "evals" / "rag_cases.json"

REQUIRED_CASE_FIELDS = {"question", "reference"}


def test_rag_eval_baseline_file_exists() -> None:
    relative = BASELINE_PATH.relative_to(PROJECT_ROOT)
    assert BASELINE_PATH.is_file(), (
        f"README 承诺的评测基准不存在：{relative}。"
        "评测提交后无法构建评测集，接口会返回 no_cases。"
    )


def test_rag_eval_baseline_has_cases() -> None:
    if not BASELINE_PATH.is_file():
        pytest.skip("评测基准文件缺失，跳过结构校验")

    payload = json.loads(BASELINE_PATH.read_text(encoding="utf-8"))

    assert isinstance(payload, dict), "评测集必须是 JSON 对象"
    assert str(payload.get("name") or "").strip(), "评测集缺少 name 字段"
    cases = payload.get("cases")
    assert isinstance(cases, list) and cases, "评测集必须至少包含一个用例"

    for case in cases:
        missing = REQUIRED_CASE_FIELDS - set(case)
        assert not missing, f"用例 {case.get('id') or '<无 id>'} 缺少字段：{sorted(missing)}"
