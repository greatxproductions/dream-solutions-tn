#!/usr/bin/env python3
"""Clean + dedupe the Dream Solutions Tennessee radon client export.

Usage:
    python3 clean_clients.py <path-to-zip-or-csv> [output_dir]

Input: the "RADON CLIENT INFORMATION ... .zip" export (or an already-extracted
"ALL CLIENTS.csv"). Output: clients_clean.csv, review_flags.csv, merge_log.csv.

Pipeline:
  1. Parse ALL CLIENTS.csv (utf-8-sig, CRLF-tolerant).
  2. Split " | "-joined multi-value fields (emails, phones, categories, addresses).
  3. Normalize: names (whitespace), phones (E.164), emails (lowercase), addresses.
  4. Merge true duplicates ONLY where the same person (same normalized name) shares
     a service address. Different people at the same property are NOT merged.
  5. Verify email domains via `dig` MX/A lookup (parallel).
  6. Emit clean master + review flags + merge log.
"""
import csv, os, re, sys, json, subprocess, tempfile, zipfile
from collections import Counter, defaultdict
from concurrent.futures import ThreadPoolExecutor

DISPOSABLE_DOMAINS = {
    "mailinator.com", "10minutemail.com", "guerrillamail.com", "tempmail.com",
    "temp-mail.org", "yopmail.com", "throwawaymail.com", "sharklasers.com",
    "trashmail.com", "getnada.com", "fakeinbox.com", "maildrop.cc", "mohmal.com",
    "tempmail.ninja", "dispostable.com", "none.com", "example.com", "test.com",
    "noemail.com",
}

def split_vals(s):
    return [x.strip() for x in re.split(r"\s*\|\s*|\n", s or "") if x.strip()]

def norm_phone(p):
    d = re.sub(r"\D", "", p)
    if len(d) == 10:
        d = "1" + d
    return "+" + d if len(d) == 11 else p

def norm_email(e):
    return re.sub(r"\s+", "", (e or "").strip().lower())

def norm_name(n):
    return re.sub(r"\s+", " ", (n or "").strip(" .-")).strip()

def norm_addr(a):
    return re.sub(r"\s+", " ", (a or "").strip())

def is_real_name(n):
    return bool(n) and n.lower() != "unidentified contact"

def union_merge(canon, other):
    canon["categories"] = sorted(set(canon["categories"] + other["categories"]))
    canon["source_roles"] = sorted(set(canon["source_roles"] + other["source_roles"]))
    canon["phones"] = sorted(set(canon["phones"] + other["phones"]))
    canon["emails"] = sorted(set(canon["emails"] + other["emails"]))
    canon["service_addrs"] = sorted(set(canon["service_addrs"] + other["service_addrs"]))
    canon["billing_addrs"] = sorted(set(canon["billing_addrs"] + other["billing_addrs"]))
    canon["_ids"] += other["_ids"]
    canon["first_work"] = (canon["first_work"] if canon["first_work"]
                           and (not other["first_work"] or canon["first_work"] <= other["first_work"])
                           else other["first_work"])
    canon["last_work"] = (canon["last_work"] if canon["last_work"]
                          and (not other["last_work"] or canon["last_work"] >= other["last_work"])
                          else other["last_work"])
    canon["invoices"] = " | ".join(sorted(set(split_vals(canon["invoices"] + " | " + other["invoices"]))))
    try:
        canon["distinct_invoices"] = str(max(int(canon["distinct_invoices"] or 0),
                                            int(other["distinct_invoices"] or 0)))
    except (ValueError, TypeError):
        pass

def check_domain(d):
    try:
        mx = subprocess.run(["dig", "+short", "MX", d], capture_output=True,
                            text=True, timeout=8).stdout.strip()
        if mx:
            return "valid"
        a = subprocess.run(["dig", "+short", "A", d], capture_output=True,
                           text=True, timeout=8).stdout.strip()
        return "risky_no_mx" if a else "invalid"
    except Exception:
        return "error"

def load_csv(path):
    with open(path, newline="", encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))

def find_clients_csv(src):
    if os.path.isdir(src):
        p = os.path.join(src, "ALL CLIENTS.csv")
        if os.path.exists(p):
            return p
    elif zipfile.is_zipfile(src):
        tmp = tempfile.mkdtemp(prefix="dstn_clients_")
        with zipfile.ZipFile(src) as z:
            z.extractall(tmp)
        for root, _, files in os.walk(tmp):
            for fn in files:
                if fn.upper() == "ALL CLIENTS.CSV":
                    return os.path.join(root, fn)
    return src  # assume it IS the csv

def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    src = find_clients_csv(sys.argv[1])
    outdir = sys.argv[2] if len(sys.argv) > 2 else os.path.dirname(os.path.abspath(__file__))
    os.makedirs(outdir, exist_ok=True)

    raw = load_csv(src)
    records = []
    for r in raw:
        records.append({
            "id": r["Contact ID"],
            "name": norm_name(r.get("Primary name", "")),
            "other_names": r.get("Other names", "").strip(),
            "categories": sorted(set(split_vals(r.get("Categories", "")))),
            "source_roles": sorted(set(split_vals(r.get("Source roles", "")))),
            "phones": sorted(set(norm_phone(p) for p in split_vals(r.get("Phones", "")))),
            "emails": sorted(set(norm_email(e) for e in split_vals(r.get("Emails", "")))),
            "first_work": (r.get("First work date", "") or "").strip(),
            "last_work": (r.get("Last work date", "") or "").strip(),
            "work_order_dates": r.get("Work order dates", "").strip(),
            "distinct_invoices": (r.get("Distinct invoices", "") or "").strip(),
            "invoices": r.get("Invoices", "").strip(),
            "service_addrs": sorted(set(norm_addr(a) for a in split_vals(r.get("Service addresses", "")))),
            "billing_addrs": sorted(set(norm_addr(a) for a in split_vals(r.get("Billing addresses", "")))),
            "positions": r.get("Contact positions", "").strip(),
            "contexts": r.get("Additional contexts", "").strip(),
            "_ids": [r["Contact ID"]],
        })

    # merge same-name + same-address
    name_idx = defaultdict(list)
    for rec in records:
        name_idx[rec["name"].lower()].append(rec)

    merge_log, merged, used = [], [], set()
    for rec in records:
        if rec["id"] in used:
            continue
        group = name_idx.get(rec["name"].lower(), [rec])
        if not is_real_name(rec["name"]) or len(group) < 2:
            merged.append(rec); used.add(rec["id"]); continue
        addrs = set(rec["service_addrs"])
        same = [g for g in group if g["id"] != rec["id"] and set(g["service_addrs"]) & addrs]
        for other in same:
            union_merge(rec, other)
            merge_log.append({"kept": rec["id"], "merged": other["id"], "name": rec["name"]})
            used.add(other["id"])
        used.add(rec["id"]); merged.append(rec)

    # email verification
    doms = sorted({e.split("@")[1] for r in merged for e in r["emails"] if "@" in e})
    domain_status = {}
    with ThreadPoolExecutor(max_workers=24) as ex:
        for d, s in zip(doms, ex.map(check_domain, doms)):
            domain_status[d] = s

    def email_status(e):
        if not e:
            return "missing"
        if not re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", e):
            return "invalid_syntax"
        d = e.split("@")[1]
        if d in DISPOSABLE_DOMAINS:
            return "disposable"
        return domain_status.get(d, "unknown")

    for r in merged:
        r["email_statuses"] = [email_status(e) for e in r["emails"]]

    # flags
    flags = defaultdict(list)
    for r in merged:
        cid = r["id"]
        if r["name"].lower() == "unidentified contact":
            flags[cid].append("unnamed: no name captured")
        elif len(r["name"].split()) < 2:
            flags[cid].append(f"name_incomplete: {r['name']!r}")
        for e, s in zip(r["emails"], r["email_statuses"]):
            if s in ("invalid", "invalid_syntax", "disposable", "risky_no_mx", "error"):
                flags[cid].append(f"email_{s}: {e}")

    name_count = defaultdict(list)
    for r in merged:
        if is_real_name(r["name"]):
            name_count[r["name"].lower()].append(r["id"])
    for n, ids in name_count.items():
        if len(ids) > 1:
            for cid in ids:
                flags[cid].append(f"possible_duplicate: {len(ids)} records named {n!r}")

    # write outputs
    cols = ["Contact ID", "Primary name", "Other names", "Categories", "Source roles",
            "Phone primary", "Phone secondary", "Phone extra", "Email primary",
            "Email secondary", "Email extra", "Email status", "First work date",
            "Last work date", "Distinct invoices", "Invoices", "Service address primary",
            "Service address count", "Billing address", "State", "Contact positions",
            "Additional contexts", "Merged IDs", "Flags"]

    def state_of(a):
        m = re.search(r",\s*([A-Z]{2})\s+\d{5}", a)
        return m.group(1) if m else ""

    rows = []
    for r in merged:
        em, ph = r["emails"], r["phones"]
        worst = "valid"
        for s in r["email_statuses"]:
            if s not in ("valid", "missing"):
                worst = s
        rows.append({
            "Contact ID": r["id"], "Primary name": r["name"], "Other names": r["other_names"],
            "Categories": " | ".join(r["categories"]), "Source roles": " | ".join(r["source_roles"]),
            "Phone primary": ph[0] if ph else "", "Phone secondary": ph[1] if len(ph) > 1 else "",
            "Phone extra": " | ".join(ph[2:]) if len(ph) > 2 else "",
            "Email primary": em[0] if em else "", "Email secondary": em[1] if len(em) > 1 else "",
            "Email extra": " | ".join(em[2:]) if len(em) > 2 else "",
            "Email status": worst, "First work date": r["first_work"], "Last work date": r["last_work"],
            "Distinct invoices": r["distinct_invoices"], "Invoices": r["invoices"],
            "Service address primary": r["service_addrs"][0] if r["service_addrs"] else "",
            "Service address count": str(len(r["service_addrs"])),
            "Billing address": r["billing_addrs"][0] if r["billing_addrs"] else "",
            "State": state_of(r["service_addrs"][0]) if r["service_addrs"] else "",
            "Contact positions": r["positions"], "Additional contexts": r["contexts"],
            "Merged IDs": " | ".join(r["_ids"][1:]) if len(r["_ids"]) > 1 else "",
            "Flags": " | ".join(flags.get(r["id"], [])),
        })

    with open(os.path.join(outdir, "clients_clean.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader(); w.writerows(rows)

    flag_rows = [{"Contact ID": r["id"], "Name": r["name"], "Email": " | ".join(r["emails"]),
                  "Flags": " | ".join(flags[r["id"]])} for r in merged if flags.get(r["id"])]
    with open(os.path.join(outdir, "review_flags.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["Contact ID", "Name", "Email", "Flags"])
        w.writeheader(); w.writerows(flag_rows)

    with open(os.path.join(outdir, "merge_log.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["kept", "merged", "name"])
        w.writeheader()
        for m in merge_log:
            w.writerow({"kept": m["kept"], "merged": m["merged"], "name": m["name"]})

    fc = Counter()
    for r in merged:
        for fl in flags.get(r["id"], []):
            fc[fl.split(":")[0]] += 1

    print(f"records: {len(raw)} -> {len(merged)} (merged {len(merge_log)} true duplicates)")
    print(f"flag counts: {dict(fc)}")
    print(f"wrote {len(rows)} rows to {os.path.join(outdir, 'clients_clean.csv')}")

if __name__ == "__main__":
    main()
