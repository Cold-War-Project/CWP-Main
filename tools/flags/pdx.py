"""Minimal Paradox script reader and writer for the flag tools (stdlib only).

parse(text) returns a list of Node. A Node is (key, op, value, comment):
  value is a str for a scalar, a list of Node for a block, or a Block for an
  anonymous-item block such as `{ 0.5 0.5 }` (Block.items holds the bare tokens).
Multi-token values such as `coa = list "communist"` are kept as one str ("list \"communist\"").
The comment is the `#` text on the same line as the key, if any (blocks: the line of the `{`).
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path

OPS = ("?=", ">=", "<=", "!=", "==", "=", ">", "<")


@dataclass
class Node:
    key: str
    op: str
    value: "str | list[Node] | Block"
    comment: str = ""

    def is_block(self) -> bool:
        return isinstance(self.value, list)


@dataclass
class Block:
    """A `{ ... }` holding bare values (e.g. `{ 0.5 0.5 }`), possibly mixed with nodes."""
    items: list = field(default_factory=list)


@dataclass
class Tok:
    kind: str  # 'str', 'op', '{', '}', 'comment', 'nl'
    text: str


_TOKEN_RE = re.compile(
    r"""
    (?P<nl>\n)
  | (?P<ws>[ \t\r﻿]+)
  | (?P<comment>\#[^\n]*)
  | (?P<lbrace>\{)
  | (?P<rbrace>\})
  | (?P<op>\?=|>=|<=|!=|==|=|>|<)
  | (?P<quoted>"(?:[^"\\]|\\.)*")
  | (?P<math>@\[[^\]]*\])
  | (?P<word>[^\s=<>!?{}\#"]+)
    """,
    re.VERBOSE,
)


def tokenize(text: str) -> list[Tok]:
    toks = []
    pos = 0
    n = len(text)
    while pos < n:
        m = _TOKEN_RE.match(text, pos)
        if not m:
            raise ValueError(f"cannot tokenize at {pos}: {text[pos:pos+40]!r}")
        pos = m.end()
        k = m.lastgroup
        if k == "ws":
            continue
        if k == "nl":
            toks.append(Tok("nl", "\n"))
        elif k == "comment":
            toks.append(Tok("comment", m.group().strip()))
        elif k == "lbrace":
            toks.append(Tok("{", "{"))
        elif k == "rbrace":
            toks.append(Tok("}", "}"))
        elif k == "op":
            toks.append(Tok("op", m.group()))
        else:
            toks.append(Tok("str", m.group()))
    return toks


class _Parser:
    def __init__(self, toks: list[Tok]):
        self.t = toks
        self.i = 0

    def peek(self, skip_nl=True, skip_comment=True):
        j = self.i
        while j < len(self.t):
            k = self.t[j].kind
            if (k == "nl" and skip_nl) or (k == "comment" and skip_comment):
                j += 1
                continue
            return self.t[j], j
        return None, j

    def same_line_comment(self) -> str:
        """Consume a comment if it is the next token before a newline."""
        j = self.i
        if j < len(self.t) and self.t[j].kind == "comment":
            self.i = j + 1
            return self.t[j].text
        return ""

    def parse_block(self, top=False):
        nodes = []
        bare = []
        while True:
            tok, j = self.peek()
            if tok is None:
                if not top:
                    raise ValueError("unexpected end of file inside a block")
                break
            self.i = j
            if tok.kind == "}":
                if top:
                    raise ValueError("unbalanced } at top level")
                self.i += 1
                break
            if tok.kind == "{":
                # anonymous block inside a list
                self.i += 1
                bare.append(self.parse_block())
                continue
            if tok.kind != "str":
                raise ValueError(f"unexpected token {tok.text!r}")
            key = tok.text
            self.i += 1
            nxt, j2 = self.peek(skip_nl=True, skip_comment=True)
            if nxt is not None and nxt.kind == "op":
                self.i = j2 + 1
                op = nxt.text
                val_tok, j3 = self.peek()
                self.i = j3
                if val_tok.kind == "{":
                    self.i += 1
                    comment = self.same_line_comment()
                    val = self.parse_block()
                    nodes.append(Node(key, op, val, comment))
                else:
                    self.i += 1
                    val = val_tok.text
                    # multi-token value: `list "name"`
                    if val == "list":
                        t2, j4 = self.peek(skip_nl=False)
                        if t2 is not None and t2.kind == "str":
                            val = f"{val} {t2.text}"
                            self.i = j4 + 1
                    comment = self.same_line_comment()
                    nodes.append(Node(key, op, val, comment))
            else:
                bare.append(key)
        if bare and not top:
            if nodes:
                return Block(bare + nodes)
            return Block(bare)
        return nodes


def parse(text: str) -> list[Node]:
    return _Parser(tokenize(text)).parse_block(top=True)


def read(path: Path) -> list[Node]:
    return parse(Path(path).read_text(encoding="utf-8-sig"))


def scripted_vars(text: str) -> dict[str, str]:
    """Top-level `@name = value` definitions, in file order."""
    out = {}
    for n in parse(text):
        if n.key.startswith("@") and not n.is_block():
            out[n.key] = n.value
    return out


def get(nodes: list[Node], key: str, default=None):
    for n in nodes:
        if n.key == key:
            return n.value
    return default


def walk(nodes, fn):
    """Call fn(node) for every node, depth first."""
    for n in nodes:
        fn(n)
        if isinstance(n.value, list):
            walk(n.value, fn)
        elif isinstance(n.value, Block):
            walk([x for x in n.value.items if isinstance(x, Node)], fn)


def fmt_value(v, indent: int) -> str:
    if isinstance(v, str):
        return v
    if isinstance(v, Block):
        parts = []
        for it in v.items:
            if isinstance(it, Node):
                parts.append(f"{it.key} {it.op} {fmt_value(it.value, indent + 1)}")
            elif isinstance(it, Block):
                parts.append(fmt_value(it, indent + 1))
            else:
                parts.append(str(it))
        return "{ " + " ".join(parts) + " }"
    return fmt_block(v, indent)


def fmt_block(nodes: list[Node], indent: int, head_comment: str = "") -> str:
    """Format `{ ... }` with tabs; short leaf-only blocks stay on one line."""
    if not nodes:
        return "{ }"
    if (len(nodes) == 1 and not nodes[0].is_block() and not nodes[0].comment
            and not isinstance(nodes[0].value, Block) and not head_comment):
        n = nodes[0]
        return f"{{ {n.key} {n.op} {n.value} }}"
    tab = "\t" * (indent + 1)
    lines = ["{" + (f"\t{head_comment}" if head_comment else "")]
    for n in nodes:
        lines.append(tab + fmt_node(n, indent + 1))
    lines.append("\t" * indent + "}")
    return "\n".join(lines)


def fmt_node(n: Node, indent: int) -> str:
    if n.is_block():
        return f"{n.key} {n.op} {fmt_block(n.value, indent, n.comment)}"
    s = f"{n.key} {n.op} {fmt_value(n.value, indent)}"
    if n.comment:
        s += f"\t{n.comment}"
    return s
