"""ceh: Creative Engineering Hub command line."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from . import evaluate as ev
from . import integrate as vf
from . import intake, search, skills, upstream
from .store import CehError, Registry, data, policy, root, set_status


def out(obj, as_json: bool) -> None:
    if as_json or not isinstance(obj, (list, str)):
        print(json.dumps(obj, indent=2, default=str))
    elif isinstance(obj, str):
        print(obj)
    else:
        for row in obj:
            print("  ".join(f"{v}" if not isinstance(v, list) else ",".join(map(str, v)) for v in row.values()))


def summary(rec: dict) -> dict:
    return {"id": rec["id"], "name": rec["name"], "status": rec["status"], "type": rec["type"],
            "capabilities": rec.get("capabilities"), "licence": (rec.get("licence") or {}).get("spdx"),
            "licence_gate": (rec.get("licence") or {}).get("gate"), "security_gate": (rec.get("security") or {}).get("gate"),
            "local_copies": rec.get("local", {}).get("paths"), "recommendation": rec.get("recommendation")}


def validate_all(reg: Registry) -> list[str]:
    problems = []
    states = set(policy()["lifecycle"]["states"])
    caps = set(data("registry/capabilities.yaml")["capabilities"])
    types = set(data("registry/capabilities.yaml")["resource_types"])
    seen = {}
    for r in reg.all():
        if r["status"] not in states:
            problems.append(f"{r['id']}: unknown status {r['status']}")
        if r.get("type") and r["type"] not in types:
            problems.append(f"{r['id']}: unknown type {r['type']}")
        problems += [f"{r['id']}: unknown capability {c}" for c in r.get("capabilities", []) if c not in caps]
        key = r["url"].lower()
        if key in seen:
            problems.append(f"{r['id']}: duplicate of {seen[key]}")
        seen[key] = r["id"]
        if r["status"] in ("APPROVED", "PRODUCTION") and (r.get("licence") or {}).get("gate") == "block":
            problems.append(f"{r['id']}: {r['status']} with a blocking licence")
    cat_ids = {e["id"] for e in vf.catalog()["entries"]}
    for i in cat_ids:
        try:
            if reg.get(i)["status"] != "PRODUCTION":
                problems.append(f"catalog lists {i} but it is not PRODUCTION")
        except CehError:
            problems.append(f"catalog lists unknown {i}")
    for s in skills.all_skills():
        problems += skills.validate(s, reg)
    return problems


def build() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="ceh", description="Creative Engineering Hub")
    p.add_argument("--json", action="store_true", help="machine-readable output")
    sub = p.add_subparsers(dest="cmd", required=True)

    a = sub.add_parser("add", help="register a URL, then inspect it statically in the lab")
    a.add_argument("url")
    a.add_argument("--type", dest="type_hint")
    a.add_argument("--note", default="")
    a.add_argument("--no-inspect", action="store_true")

    i = sub.add_parser("inspect", help="(re)read a resource: licence, deps, security, compatibility")
    i.add_argument("id")
    i.add_argument("--no-vulns", action="store_true", help="skip the osv.dev lookup")

    e = sub.add_parser("evaluate", help="score, gate and write reports/<id>/")
    e.add_argument("id")
    e.add_argument("--score", action="append", default=[], metavar="CRITERION=N", help="record benchmark evidence (0-5)")
    e.add_argument("--evidence", default="")

    s = sub.add_parser("search", help="find resources by capability or text")
    s.add_argument("query")
    s.add_argument("--all", action="store_true", help="include rejected and restricted")

    c = sub.add_parser("compare", help="side-by-side comparison")
    c.add_argument("ids", nargs="*")
    c.add_argument("--capability")

    r = sub.add_parser("recommend", help="plan a workflow for a creative brief")
    r.add_argument("--brief", required=True)
    r.add_argument("--renderer")
    r.add_argument("--agent")
    r.add_argument("--non-commercial", action="store_true")

    ap = sub.add_parser("approve", help="licence + security gates, then APPROVED")
    ap.add_argument("id")
    ap.add_argument("--licence-reviewed", default="")
    ap.add_argument("--security-reviewed", default="")

    ig = sub.add_parser("integrate", help="APPROVED -> PRODUCTION: publish to the Video Factory catalog")
    ig.add_argument("id")
    ig.add_argument("--test", action="store_true", help="run Video Factory tests first")

    w = sub.add_parser("withdraw", help="remove from the Video Factory catalog")
    w.add_argument("id")
    w.add_argument("--to", default="DEPRECATED")
    w.add_argument("--note", default="")

    st = sub.add_parser("set-status", help="move a resource to a non-gated state (PARKED, REJECTED, ...)")
    st.add_argument("id")
    st.add_argument("status")
    st.add_argument("--note", required=True)

    t = sub.add_parser("tag", help="add curated capabilities that survive re-inspection")
    t.add_argument("id")
    t.add_argument("capabilities", nargs="+")

    ins = sub.add_parser("install", help="install a library skill into agents")
    ins.add_argument("skill")
    ins.add_argument("--agent", action="append")

    sk = sub.add_parser("skills", help="list, validate, enable, disable, uninstall library skills")
    sk.add_argument("action", choices=["list", "validate", "enable", "disable", "uninstall"])
    sk.add_argument("skill", nargs="?")

    cat = sub.add_parser("catalog", help="export approved versioned consumer metadata")
    cat.add_argument("action", choices=["export"])
    cat.add_argument("--output", type=Path, default=root() / "integrations/video-factory/catalog-v2.json")

    sub.add_parser("validate", help="check registry, catalog and skills integrity")
    sub.add_parser("status", help="counts by lifecycle state and attention items")

    m = sub.add_parser("migrate", help="import intake/historical/leads.yaml and write the migration report")
    m.add_argument("--no-inspect", action="store_true")

    art = sub.add_parser("artifact", help="validate a renderer output folder against the production contract")
    art.add_argument("path")

    u = sub.add_parser("upstream", help="upstream intelligence")
    usub = u.add_subparsers(dest="ucmd", required=True)
    uc = usub.add_parser("check")
    uc.add_argument("id", nargs="?")
    uc.add_argument("--all", action="store_true")
    uc.add_argument("--report", action="store_true", help="write reports/upstream/<date>.md")
    for name in ("diff", "report", "history"):
        x = usub.add_parser(name)
        x.add_argument("id")
        if name == "report":
            x.add_argument("--run-tests", action="store_true")
    us = usub.add_parser("sync")
    us.add_argument("id")
    us.add_argument("--approve", action="store_true")
    us.add_argument("--to")
    us.add_argument("--note", default="")
    usub.add_parser("status")
    return p


def run(args) -> int:
    reg = Registry()
    j = args.json
    match args.cmd:
        case "add":
            rec, created = intake.add(args.url, type_hint=args.type_hint, note=args.note, inspect_now=not args.no_inspect, reg=reg)
            if created and not args.no_inspect:
                rec = ev.evaluate(rec["id"], reg=reg, promote=False)
            out({"created": created, **summary(rec), "reports": f"reports/{rec['id']}/" if created else None}, j)
        case "inspect":
            out(summary(intake.inspect(args.id, reg=reg, vulns=not args.no_vulns)), j)
        case "evaluate":
            scores = dict(s.split("=", 1) for s in args.score)
            rec = ev.evaluate(args.id, scores={k: float(v) for k, v in scores.items()}, evidence=args.evidence, reg=reg)
            out({**summary(rec), "score": rec["evaluation"]["weighted_score"], "coverage": rec["evaluation"]["evidence_coverage"],
                 "reports": f"reports/{rec['id']}/"}, j)
        case "search":
            out(search.search(args.query, reg, include_unusable=args.all), j)
        case "compare":
            ids = args.ids
            if args.capability:
                ids = ids + [r["id"] for r in search.search(args.capability, reg)]
            if len(ids) < 2:
                raise CehError("compare needs two ids, or --capability matching at least two resources")
            out(search.compare(list(dict.fromkeys(ids)), reg), j)
        case "recommend":
            out(search.recommend(args.brief, reg, renderer=args.renderer, agent=args.agent, commercial=not args.non_commercial), j)
        case "approve":
            out(summary(vf.approve(args.id, reg=reg, licence_note=args.licence_reviewed, security_note=args.security_reviewed)), j)
        case "integrate":
            out(vf.integrate(args.id, reg=reg, run_tests=args.test), j)
        case "withdraw":
            out(summary(vf.withdraw(args.id, reg=reg, to=args.to, note=args.note)), j)
        case "set-status":
            rec = reg.get(args.id)
            set_status(rec, args.status.upper(), by="ceh set-status", note=args.note)
            reg.save(rec)
            out(summary(rec), j)
        case "tag":
            rec = reg.get(args.id)
            known = data("registry/capabilities.yaml")["capabilities"]
            bad = [c for c in args.capabilities if c not in known]
            if bad:
                raise CehError(f"unknown capabilities {bad}; add them to registry/capabilities.yaml first")
            rec["capabilities_manual"] = sorted(set(rec.get("capabilities_manual", [])) | set(args.capabilities))
            rec["capabilities"] = list(dict.fromkeys(rec["capabilities"] + args.capabilities))
            reg.save(rec)
            out(summary(rec), j)
        case "install":
            out(skills.install(args.skill, args.agent), j)
        case "skills":
            if args.action == "list":
                out(skills.listing(), j)
            elif args.action == "validate":
                names = [args.skill] if args.skill else skills.all_skills()
                probs = [p for n in names for p in skills.validate(n, reg)]
                out(probs or "all skills valid", j)
                return 1 if probs else 0
            elif not args.skill:
                raise CehError(f"skills {args.action} needs a skill name")
            elif args.action == "uninstall":
                out(skills.uninstall(args.skill), j)
            else:
                out(skills.set_enabled(args.skill, args.action == "enable"), j)
        case "catalog":
            from .catalog_publish import export_catalog
            out(export_catalog(reg, args.output), j)
        case "validate":
            probs = validate_all(reg)
            out(probs or f"ok: {len(reg.all())} resources, {len(skills.all_skills())} skills, catalog consistent", j)
            return 1 if probs else 0
        case "status":
            recs = reg.all()
            counts = {s: sum(r["status"] == s for r in recs) for s in policy()["lifecycle"]["states"]}
            attention = [f"{r['id']} {r['name']}: {', '.join(r['upstream']['flags'])}" for r in recs
                         if set((r.get("upstream") or {}).get("flags", [])) - {"up-to-date"}]
            out({"resources": len(recs), "by_status": {k: v for k, v in counts.items() if v},
                 "video_factory_catalog": [e["id"] for e in vf.catalog()["entries"]], "upstream_attention": attention}, j)
        case "migrate":
            from .migrate import migrate
            path = migrate(inspect_now=not args.no_inspect, reg=reg, log=lambda s: print(s, file=sys.stderr))
            out(f"report: {path.relative_to(root())}", j)
        case "artifact":
            res = vf.check_artifact(Path(args.path))
            out(res, j)
            return 0 if res["ok"] else 1
        case "upstream":
            return run_upstream(args, reg, j)
    return 0


def run_upstream(args, reg: Registry, j: bool) -> int:
    match args.ucmd:
        case "check":
            targets = [r for r in reg.all() if (r.get("upstream") or {}).get("remote")] if args.all or not args.id else [reg.get(args.id)]
            results = []
            for rec in targets:
                results.append(upstream.check(rec))
                reg.save(rec)
            if args.report:
                print(f"report: {upstream.weekly_report(results).relative_to(root())}", file=sys.stderr)
            out(results if j else [{"id": r["id"], "name": r["name"], "flags": r["flags"]} for r in results], j)
        case "diff":
            d = upstream.diff(reg.get(args.id))
            out(d if j else {k: d[k] for k in ("id", "pinned", "latest", "commit_count", "files_changed", "breaking",
                                                  "licence_files_changed", "manifests", "impacted_skills", "impacted_video_factory",
                                                  "local_modifications")}, j)
        case "report":
            rec = reg.get(args.id)
            d = upstream.report(rec, reg, run_tests=args.run_tests)
            out(f"reports/{rec['id']}/upstream-analysis.md: {d['commit_count']} commits, {len(d['breaking'])} breaking signals, "
                f"impacts VF: {d['impacted_video_factory'] or 'no'}", j)
        case "sync":
            out(upstream.sync(reg.get(args.id), reg, approve=args.approve, to=args.to, note=args.note), j)
        case "history":
            up = reg.get(args.id).get("upstream") or {}
            out({"pins": up.get("pins", []), "checks": up.get("checks", [])[-10:], "last_report": up.get("last_report")}, j)
        case "status":
            out(upstream.status(reg), j)
    return 0


def main(argv=None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    if "--json" in argv:  # accept --json anywhere, not only before the subcommand
        argv = ["--json"] + [a for a in argv if a != "--json"]
    args = build().parse_args(argv)
    try:
        return run(args)
    except CehError as e:
        print(f"ceh: {e}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
