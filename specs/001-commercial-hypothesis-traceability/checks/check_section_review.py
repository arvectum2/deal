"""Pinned source review; structural only, not product acceptance or task admission."""
import hashlib,json,re,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3]
DIR="specs/001-commercial-hypothesis-traceability"
PIN="a4ec754fe51daef68c2dd9bddb6101ab80108e29"
PRIOR="80c0968218db71f7cb19864cb5faab134283bd3d"
MODE="hypothesis_only"
SOURCES=json.loads("[{\"path\":\"docs/ROADMAP.md\",\"sha256\":\"c88a54b6c2533c8f9020718066e6ebd0a4f089c309729c26737bc153c7ad1232\"}]")
GATES=json.loads("[{\"id\":\"REVIEW-01\",\"source\":\"docs/ROADMAP.md\",\"first_line\":4,\"last_line\":35,\"label\":\"S0–S4\",\"rule\":\"Preserve Kwork rights gate, RFQ, comparability and evidence.\"},{\"id\":\"REVIEW-02\",\"source\":\"docs/ROADMAP.md\",\"first_line\":37,\"last_line\":60,\"label\":\"S5–S8\",\"rule\":\"Commercial pilot, consent, realized savings and scale separate; not client-specific scope.\"}]")
def scan(raw):
    out=[];heading=0;fence=False
    for i,l in enumerate(raw.decode("utf-8").splitlines(),1):
        if not l.strip():continue
        if l.lstrip().startswith(("\x60\x60\x60","~~~")):
            fence=not fence;kind="format"
        elif fence:kind="code"
        elif re.match(r"^#{1,6}\s",l):heading=i;kind="heading"
        elif re.fullmatch(r"\s*\|?\s*[:\-]+(?:\s*\|\s*[:\-]+)+\s*\|?\s*",l) or re.fullmatch(r"\s*[-*_]{3,}\s*",l):kind="format"
        elif re.match(r"^\s*\|",l):kind="table"
        elif re.match(r"^\s*(?:[-*+]|\d+[.)])\s+",l):kind="list"
        else:kind="prose"
        out.append([i,heading,kind])
    return out
def validate(data,original,prior,current):
    errors=[]
    if data.get("schema")!="arvectum.source-section-review/1" or data.get("source_commit")!=PIN or data.get("review_baseline")!=PRIOR or data.get("mode")!=MODE or data.get("actual_acceptance_verified") is not False or data.get("execution_authorized") is not False:errors.append("scope/authority")
    if data.get("gates") is None: return errors+["missing gates"]
    src=data.get("sources",[]);paths=[s["path"] for s in src]
    if paths!=[s["path"] for s in SOURCES]:return errors+["source coverage"]
    for a,s in zip(src,SOURCES):
        p=s["path"];b=original[p]
        if hashlib.sha256(b).hexdigest()!=s["sha256"] or a.get("sha256")!=s["sha256"]:errors.append("source hash "+p)
        if not prior[p].startswith(b) or prior[p]!=current[p]:errors.append("unreviewed source change "+p)
        if a.get("rows")!=scan(b):errors.append("line/heading coverage "+p)
    rows=data["gates"]
    if len(rows)!=len(GATES):errors.append("gate coverage")
    for row,g in zip(rows,GATES):
        if any(row.get(k)!=v for k,v in g.items()):errors.append("gate identity/scope")
        if row.get("review_state") not in {"unverified","verified"}:errors.append("state")
        if row.get("review_state")=="verified":
            ev=row.get("evidence",[])
            if not ev or any(e.get("criterion")!=row["id"] or e.get("outcome")!="pass" or not re.fullmatch(r"[a-f0-9]{64}",e.get("artifact_sha256","")) or not e.get("receipt_ref") or not e.get("review_ref") for e in ev):errors.append("missing criterion-specific evidence "+row["id"])
    return errors
def inputs():
    def read(ref,p):return subprocess.check_output(["git","-C",str(ROOT),"show",ref+":"+p])
    original={s["path"]:read(PIN,s["path"]) for s in SOURCES}
    prior={p:read(PRIOR,p) for p in original}
    current={p:(ROOT/p).read_bytes() for p in original}
    return json.loads((ROOT/DIR/"section-review.json").read_text()),original,prior,current
if __name__=="__main__":
    errors=validate(*inputs())
    if errors:raise SystemExit("\n".join(errors))
    print("Structural source/section coverage PASS; no actual acceptance or authority.")
