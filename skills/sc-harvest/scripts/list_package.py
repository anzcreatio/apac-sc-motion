"""List what a Creatio package export (.zip from clio pull-pkg) carries, offline."""
import collections, glob, gzip, json, os, struct, sys, zipfile


def entries(zip_path):
    zf = zipfile.ZipFile(zip_path)
    gz = [n for n in zf.namelist() if n.endswith(".gz")][0]
    data = gzip.decompress(zf.read(gz))
    i = 0
    while i < len(data):
        n = struct.unpack_from("<i", data, i)[0]; i += 4
        path = data[i:i + n * 2].decode("utf-16-le"); i += n * 2
        ln = struct.unpack_from("<i", data, i)[0]; i += 4
        yield path.replace(os.sep, "/").replace(chr(92), "/"), data[i:i + ln]
        i += ln


out = {}
for z in sorted(glob.glob(os.path.join(sys.argv[1], "*.zip"))):
    kinds = collections.defaultdict(set)
    deps = []
    for path, blob in entries(z):
        parts = path.split("/")
        if parts[0] in ("Schemas", "Data", "Files", "Resources", "SqlScripts", "Assemblies") and len(parts) > 1:
            kinds[parts[0]].add(parts[1])
        if path == "descriptor.json":
            try:
                d = json.loads(blob.decode("utf-8-sig"))["Descriptor"]
                deps = [x["Name"] for x in d.get("DependsOn", [])]
            except Exception:
                pass
    name = os.path.basename(z)
    out[name] = {k: sorted(v) for k, v in kinds.items()}
    out[name]["DependsOn"] = deps
    print("##", name)
    for k, v in out[name].items():
        print("  %s (%d): %s" % (k, len(v), ", ".join(v)[:700]))
json.dump(out, open(os.path.join(sys.argv[1], "contents.json"), "w", encoding="utf-8"), indent=1)
