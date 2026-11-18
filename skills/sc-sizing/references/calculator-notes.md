> Reference only. The live calculator is the source: `sizing.py calc` fetches it per deal. Captured 18 Nov 2026.

# Creatio on-site system requirements calculator: extracted logic

- Retrieved: 2026-11-18. No login used.
- Calculator: https://academy.creatio.com/resources/system-requirements-calculator
- Results URL (the form's real output, a plain GET page; usable directly by a tool):
  `https://academy.creatio.com/resources/system-requirements-calculator/results?users=<N>&portal=<P>&options=<ids joined by ->`
  e.g. `...results?users=500&portal=1000&options=398-391-421-401-404-414-418`. When "Without portal" is picked the UI omits `portal`.
- Creatio version: the calculator page shows no version. The Academy docs it links to are version-selector "10" (current; 8.3/8.2/8.1/8.0 also listed). The 8.x URL of the server-side page now serves the version 10 content. **Inferred:** the calculator reflects Creatio 10 requirements (Windows Server 2022, MSSQL 2022, PostgreSQL 16, Redis 7.4, Debian 12, .NET 8).
- How it was taken: the logic runs on the server (Drupal module `ts_calc`). The only JS, `/modules/custom/ts_calc/js/ts-calc.js`, just handles the UI. So I submitted ~190 input combinations (users 10 to 50,000; every 50 users to 3,000, every 100 to 6,000, every 500 to 20,000; all option toggles) and fitted the rules. **Every formula marked "exact" below reproduces all 152 sampled simple/full-recovery outputs with zero mismatches** (fitting scripts and raw runs were not kept; re-run the live calculator to check).
- Tags: **C** = shown verbatim by the calculator or Academy page; **I** = inferred formula (fitted, exact on all samples unless stated otherwise).

## 1. Inputs (C, calculator form, 2026-11-18)

| Input | Options (form value id) | Default | Effect on sizing |
|---|---|---|---|
| Application type | .NET Framework (398), .NET (399) | .NET Framework | Only OS and software text. **.NET allows PostgreSQL only** (the form rejects 391 MSSQL; the DB list collapses to PostgreSQL) |
| Database | MSSQL (391), Oracle (392), PostgreSQL (393) | MSSQL | Only software text. Sizing is identical |
| Number of active users | integer, min 10, max 1,000,000 | 10 | Main driver |
| Bulk emails | Without (421), With (420) | Without | **No change** to any output (tested 100/500/1000/3000/5000) |
| Deployment scheme | Fault tolerant (402), Simple (401) | Fault tolerant | Server counts plus a load balancer (sec. 4) |
| Recovery mode | Full (405), Simple (404) | Full | DB log disk and DB IOPS step (sec. 3.3) |
| Portal | With (414), Without (415) | With | Adds a portal-users field |
| Portal users | integer, min 10, max 1,000,000 | 10 | **Effective users = users + portal users / 4** (I, exact: 100 + 4000 portal gives the same output as 1100 users; 500 + 1000 portal = 750; 100 + 10 portal = 102.5, so fractions are kept) |
| Containerized components | With (417, "recommended"), Without (418) | With | Adds Kubernetes and component sections (sec. 5) |
| Components (checkboxes, at least 1) | Global search (409), Bulk duplicate search (410, needs Global search), Predictive data analysis (411), MS Exchange integration (412) | all 4 | Which component sections show |

Below, `u` = effective users. `ceil` = round up; `even(x)` = round up to the next even number.

## 2. Connection channels (exact; matches the Academy server-side page)

| Output | Formula | Example at 1,000 users |
|---|---|---|
| Web server to DBMS | 0.1 Mb/sec × u | 100 Mb/sec |
| Web server to user, minimum | 0.256 Mbps × u | 256 Mbps |
| Web server to user, recommended | 0.512 Mbps × u | 512 Mbps |
| Input/output (app) | 100 IOPS × ceil(u/1000) | 100 IOPS |
| Input/output (DBMS) | 1000 IOPS × ceil(u/1000) | 1000 IOPS |

## 3. Per-role sizing, simple scheme (the calculator states every spec "per server")

### 3.1 Application server
| Item | Rule | Tag |
|---|---|---|
| Count | u < 5000: ceil(u/500). u ≥ 5000: ceil(u/1000) | I exact |
| vCPU | u ≤ 300: 2; 301 to 5000: 4; > 5000: 8. Always "Maximum number of cores — 16", 2.6 GHz+ (Haswell or newer) | I exact; text C |
| vRAM | **No closed form found.** Single server (u ≤ 500): ceil(0.0275·u + 2.75), min 8 (I, exact for u ≤ 500). For 2+ servers it depends on users per server and total users, non-linearly: see the lookup table in sec. 8 | I |
| HDD (OS) | 60 GB, 100 IOPS, latency < 10 ms | C |
| HDD (application) | 20 GB, 100 IOPS, latency < 10 ms | C |
| NIC | 1 × 1 GbE | C |
| vCPU:pCPU | no more than 2:1 | C |
| OS / software, .NET Framework | Windows Server 2022+; IIS 10+, 64-bit .NET Framework 4.7.2, .NET 8 | C |
| OS / software, .NET | Linux Debian 12 or Windows 10+; .NET 8, IIS for Windows, GDI+-compatible API on non-Windows, GNU C dev libraries and headers | C |

Quirk (C): at exactly u = 5000 the calculator gives 5 servers × 4 vCPU × 47 GB; 4999 gives 10 × 4 × 26 and 5001 gives 6 × 8 × 41 (an edge case in their thresholds).

### 3.2 Database server
| Item | Rule | Tag |
|---|---|---|
| Count | 1 | C |
| vCPU | max(2, 2·ceil(u/280)), 3 GHz+ (Haswell or newer) | I exact |
| vRAM (GB) | max(16, even(ceil(1.1 × (0.05·u + 5)))) computed in IEEE floats: the float error adds +2 GB at some exact multiples, e.g. u = 1900 gives 112, not 110 | I exact |
| HDD (OS) | 80 GB, 100 IOPS, latency < 8 ms if u < 500, else < 7 ms | I exact |
| NIC | 1 × 0.1 GbE if u < 1000; 0.5 GbE if 1000 ≤ u < 7000; 1 GbE if u ≥ 7000 | I exact |
| vCPU:pCPU | no more than 1:1; "Virtual infrastructure (physical servers preferable)" | C |
| OS | Windows Server 2022+ or Linux Debian 12; with PostgreSQL also "OS (Amazon RDS): PostgreSQL 16" | C |
| Software | MSSQL 2022+ (Database Engine) / PostgreSQL 16+ / Oracle Database 19c+ with ODAC 11 | C |

### 3.3 Database disks (HDD (Database), per server)
Latency for all three: < 8 ms if u < 500; < 7 ms if 500 ≤ u < 3000; < 6 ms if 3000 ≤ u < 7000; < 5 ms if u ≥ 7000 (I exact).

| Disk | Simple recovery | Full recovery | Tag |
|---|---|---|---|
| Data size | 0.3 GB × u (not rounded, e.g. 30.3 GB at 101) | same | I exact |
| Data IOPS | 50·ceil(u/50) | 100·ceil(u/100) | I exact |
| Tempdb size | max(5, 5·ceil(0.03·u/5)) GB | same | I exact |
| Tempdb IOPS | = data IOPS | = data IOPS | I exact |
| Logs size | = tempdb size | max(20, 10·ceil(0.12·u/10)) GB | I exact |
| Logs IOPS | 50·ceil(data IOPS/100) | = data IOPS | I exact |

Caveat shown on the page (C): the disk values "are general recommendations. Actual requirements can vary based on the user dataset size, workload, and system usage patterns."

### 3.4 Caching server (Redis, user sessions)
| Item | Rule | Tag |
|---|---|---|
| Count | simple 1; fault tolerant 6, "Fault tolerance scheme: Redis Cluster" | C |
| vCPU | u ≤ 1000: 1; 1001 to 5000: 2; > 5000: 4; 2.4 GHz+ | I exact |
| vRAM | max(2, even(ceil(1.1 × (0.003·u + 1)))) GB "(on Linux)" | I exact |
| HDD | 20 GB, 20 IOPS, "latency less than ms" (number missing on the page) | C |
| NIC | same tiers as the DB server: 0.1 / 0.5 (≥ 1000) / 1 GbE (≥ 7000) | I exact |
| vCPU:pCPU | no more than 2:1 | C |
| OS / software | Linux Debian 12; Redis Server 7.4+ (Open Source or other editions) | C |

## 4. Fault-tolerant scheme (exact against all 37 paired samples)
Every per-server spec is the same as in the simple scheme. Only the counts change, plus a load balancer:

| Role | Count (FT) |
|---|---|
| Application server | simple count + 1 (N+1) |
| Database server | 2 |
| Redis | 6 (Redis Cluster) |
| Load balancer (web servers) | 2 |

Load balancer, per server (I exact; text C): Linux Debian 12; HDD 20 GB, 20 IOPS, < 10 ms; vCPU:pCPU ≤ 2:1; 2.6 GHz.

| Effective users | vCPU | vRAM | NIC |
|---|---|---|---|
| u < 500 | 1 | 8 GB | 2 × 1 GbE |
| 500 ≤ u ≤ 1000 | 2 | 8 GB | 2 × 10 GbE |
| u > 1000 | 2 | 16 GB | 2 × 10 GbE |

## 5. Containerized components (C; **these do not scale with users**: identical at 100 and 5000)

Kubernetes cluster. It appears when Bulk duplicate search, Predictive data analysis or MS Exchange is ticked. **Global search alone shows no Kubernetes servers**, only its own section.

| Role | Simple count | FT count | vCPU | vRAM | HDD | NIC |
|---|---|---|---|---|---|---|
| Kubernetes master | 1 | 3 | 2, 2.60 GHz | 4 GB | 30 GB, 100 IOPS, < 10 ms | 1 × 1 Gbit/s |
| Kubernetes node | 2 | 3 | 4, 2.60 GHz | 16 GB | 120 GB, 500 IOPS, < 10 ms | 1 × 1 Gbit/s |
| Kubernetes balancer | 1 | 2 | 1, 2.60 GHz | 1 GB | 30 GB, 100 IOPS, < 10 ms | 1 × 1 Gbit/s |
All are Linux Debian 12, virtual, vCPU:pCPU ≤ 2:1.

Component sections (fixed text, C):
- **Global search on Kubernetes (recommended):** 4 cores at 2.4 GHz, 12 GB+, SSD = 50% of the Creatio DB size, minimum 30 GB.
- **Global search in Docker:** ElasticSearch server, minimum 1 core / 4 GB / HDD 50% of DB, min 15 GB; recommended 2 cores / 8 GB / SSD 50% of DB, min 15 GB. Components server, minimum 1 core / 2 GB / 30 GB HDD; recommended 2 cores / 4 GB / 30 GB SSD.
- **Bulk duplicate search:** Pentium 4 / Athlon 64 with SSE2+, 3 GB+, 30 GB+.
- **Machine learning:** Docker-friendly Linux (Ubuntu/Debian) or 64-bit Windows 10 / Server 2022 with Hyper-V; Docker 18.03.1+; 64-bit, 4+ cores; 8 GB+; 20 GB+.
- **Email Listener (MS Exchange):** 1 processor replica per 40 active mailboxes; each needs "30% of the 2Hz processor time" (sic; the Academy page says 1 GHz) and 850 Mb RAM; no disk.

Fixed notes on every result (C): Marketplace solutions may change the requirements. "Listed system requirements are based on common user workloads." Other load drivers named: number of integrations, sections and pages, average requests, response times, file storage mode, average file size.

## 6. Academy page: Server-side system requirements (C)
URL: https://academy.creatio.com/guides/setup-and-administration/on-site-deployment/system-requirements/server-side-system-requirements. Version 10 (selector; no updated date shown). Retrieved 2026-11-18. The page gives **no per-tier vCPU/RAM/disk tables**; it sends you to the calculator.

- Required roles: web/application server, database server, caching (Redis) server. Optional: SVN (development), load balancers for app, DB and cache in fault-tolerant setups.
- Containerization required for: machine learning, data enrichment, bulk email service, global search, deduplication, Exchange Listener.
- Supported virtualisation/cloud: AWS, Microsoft Azure / Hyper-V, VMware vCloud Director / vSphere (others not guaranteed).
- Channels: IIS to SQL 10 Mb/sec per 100 active users, latency up to 15–20 ms. IIS to user min 256 Kb/sec and recommended 512 Kb/sec per active user (formula 30 kByte/sec × concurrent users × 10%). IIS 100 IOPS per 1,000 active users; SQL 1,000 IOPS per 1,000 active users. These match the calculator.
- Marketing email DB disk: up to 1 mln per email or > 1 mln/month, 300 IOPS, < 8 ms; 1–2 mln per email or > 3 mln/month, 500 IOPS, < 8 ms; 2–5 mln per email or > 5 mln/month, 1,000 IOPS, < 7 ms. (The calculator's "Bulk emails" toggle does not apply these; its output doesn't change.)
- Exchange Listener: 40 mailboxes per handler; 30% of 1 GHz CPU and 850 Mb RAM per processor; no disk.
- Software: web (.NET Framework) Windows Server 2022+, IIS, .NET Framework 4.7.2. Web (.NET) Debian 12 with kernel 5.10+, .NET 8, GDI+, GNU C libs. DB on Windows Server 2022+ with MSSQL 2022+ or PostgreSQL 16+; DB on Debian 12 with PostgreSQL 16+; Amazon RDS PostgreSQL 16. Cache: Debian 12, Redis 7.4+. LB: Debian 12, HAProxy. SVN: Debian 12. Containers: Debian 12, Docker, Kubernetes.
- **Oracle is not listed on the v10 docs page, but the calculator still offers it** ("Oracle Database 19c or higher", ODAC 11).

Redis Cluster page (https://academy.creatio.com/guides/setup-and-administration/on-site-deployment/caching-server/redis-cluster, v10, 2026-11-18, C): at least 6 Redis instances on separate machines/VMs, at least a dual-core CPU per node, every master has at least one replica. Note: this "dual-core" conflicts with the calculator's 1 vCPU for Redis at ≤ 1000 users.

## 7. Worked examples (C, calculator output; simple scheme, simple recovery, no portal or containers)

| Users | App n × vCPU × RAM | DB vCPU / RAM | DB data / tempdb / logs (GB) | Redis vCPU / RAM | Web-DB Mb/s |
|---|---|---|---|---|---|
| 50 | 1 × 2 × 8 | 2 / 16 | 15 / 5 / 5 | 1 / 2 | 5 |
| 100 | 1 × 2 × 8 | 2 / 16 | 30 / 5 / 5 | 1 / 2 | 10 |
| 300 | 1 × 2 × 11 | 4 / 22 | 90 / 10 / 10 | 1 / 4 | 30 |
| 500 | 1 × 4 × 17 | 4 / 34 | 150 / 15 / 15 | 1 / 4 | 50 |
| 1000 | 2 × 4 × 21 | 8 / 62 | 300 / 30 / 30 | 1 / 6 | 100 |
| 2000 | 4 × 4 × 24 | 16 / 116 | 600 / 60 / 60 | 2 / 8 | 200 |
| 5000 | 5 × 4 × 47 (edge case) | 36 / 282 | 1500 / 150 / 150 | 2 / 18 | 500 |
| 10000 | 10 × 8 × 51 | 72 / 556 | 3000 / 300 / 300 | 4 / 36 | 1000 |
| 20000 | 20 × 8 × 53 | 144 / 1106 | 6000 / 600 / 600 | 4 / 68 | 2000 |

Fault tolerant: add 1 app server, a 2nd DB, Redis × 6 and 2 LBs. Full recovery at 1000: logs 120 GB at 1000 IOPS.

## 8. Application server lookup table (C, observed; simple-scheme count; FT = count + 1, same vCPU/RAM)
For a tool: the server count and vCPU follow the exact rules in sec. 3.1, so only vRAM needs this table. vRAM is not monotonic (it drops each time a server is added), so for unsampled user counts call the results URL live, or take the higher vRAM of the two neighbouring samples that have the same server count. Not sampled: 3,000 to 6,000 between the 100s; 6,000 to 20,000 between the 500s.

| Users | App servers (simple) | vCPU/server | vRAM GB/server |
|---|---|---|---|
| 10 | 1 | 2 | 8 |
| 25 | 1 | 2 | 8 |
| 50 | 1 | 2 | 8 |
| 75 | 1 | 2 | 8 |
| 100 | 1 | 2 | 8 |
| 101 | 1 | 2 | 8 |
| 150 | 1 | 2 | 8 |
| 200 | 1 | 2 | 9 |
| 250 | 1 | 2 | 10 |
| 300 | 1 | 2 | 11 |
| 301 | 1 | 4 | 12 |
| 350 | 1 | 4 | 13 |
| 400 | 1 | 4 | 14 |
| 450 | 1 | 4 | 16 |
| 499 | 1 | 4 | 17 |
| 500 | 1 | 4 | 17 |
| 501 | 2 | 4 | 12 |
| 550 | 2 | 4 | 12 |
| 600 | 2 | 4 | 14 |
| 650 | 2 | 4 | 14 |
| 700 | 2 | 4 | 15 |
| 750 | 2 | 4 | 16 |
| 800 | 2 | 4 | 17 |
| 850 | 2 | 4 | 18 |
| 900 | 2 | 4 | 19 |
| 950 | 2 | 4 | 20 |
| 999 | 2 | 4 | 21 |
| 1000 | 2 | 4 | 21 |
| 1001 | 3 | 4 | 16 |
| 1050 | 3 | 4 | 16 |
| 1100 | 3 | 4 | 17 |
| 1150 | 3 | 4 | 18 |
| 1200 | 3 | 4 | 18 |
| 1250 | 3 | 4 | 19 |
| 1300 | 3 | 4 | 20 |
| 1350 | 3 | 4 | 20 |
| 1400 | 3 | 4 | 21 |
| 1450 | 3 | 4 | 22 |
| 1500 | 3 | 4 | 22 |
| 1550 | 4 | 4 | 19 |
| 1600 | 4 | 4 | 19 |
| 1650 | 4 | 4 | 20 |
| 1700 | 4 | 4 | 20 |
| 1750 | 4 | 4 | 21 |
| 1800 | 4 | 4 | 22 |
| 1850 | 4 | 4 | 22 |
| 1900 | 4 | 4 | 23 |
| 1950 | 4 | 4 | 23 |
| 2000 | 4 | 4 | 24 |
| 2050 | 5 | 4 | 20 |
| 2100 | 5 | 4 | 21 |
| 2150 | 5 | 4 | 21 |
| 2200 | 5 | 4 | 22 |
| 2250 | 5 | 4 | 22 |
| 2300 | 5 | 4 | 22 |
| 2350 | 5 | 4 | 23 |
| 2400 | 5 | 4 | 23 |
| 2450 | 5 | 4 | 24 |
| 2500 | 5 | 4 | 24 |
| 2550 | 6 | 4 | 21 |
| 2600 | 6 | 4 | 22 |
| 2650 | 6 | 4 | 22 |
| 2700 | 6 | 4 | 22 |
| 2750 | 6 | 4 | 23 |
| 2800 | 6 | 4 | 23 |
| 2850 | 6 | 4 | 24 |
| 2900 | 6 | 4 | 24 |
| 2950 | 6 | 4 | 24 |
| 2999 | 6 | 4 | 25 |
| 3000 | 6 | 4 | 25 |
| 3100 | 7 | 4 | 22 |
| 3200 | 7 | 4 | 23 |
| 3300 | 7 | 4 | 24 |
| 3400 | 7 | 4 | 25 |
| 3500 | 7 | 4 | 25 |
| 3600 | 8 | 4 | 23 |
| 3700 | 8 | 4 | 24 |
| 3800 | 8 | 4 | 24 |
| 3900 | 8 | 4 | 25 |
| 4000 | 8 | 4 | 26 |
| 4100 | 9 | 4 | 24 |
| 4200 | 9 | 4 | 24 |
| 4300 | 9 | 4 | 25 |
| 4400 | 9 | 4 | 25 |
| 4500 | 9 | 4 | 26 |
| 4600 | 10 | 4 | 24 |
| 4700 | 10 | 4 | 24 |
| 4800 | 10 | 4 | 25 |
| 4900 | 10 | 4 | 26 |
| 4999 | 10 | 4 | 26 |
| 5000 | 5 | 4 | 47 |
| 5001 | 6 | 8 | 41 |
| 5100 | 6 | 8 | 41 |
| 5200 | 6 | 8 | 42 |
| 5300 | 6 | 8 | 43 |
| 5400 | 6 | 8 | 44 |
| 5500 | 6 | 8 | 44 |
| 5600 | 6 | 8 | 45 |
| 5700 | 6 | 8 | 46 |
| 5800 | 6 | 8 | 47 |
| 5900 | 6 | 8 | 48 |
| 6000 | 6 | 8 | 48 |
| 6500 | 7 | 8 | 46 |
| 6600 | 7 | 8 | 47 |
| 6800 | 7 | 8 | 48 |
| 6901 | 7 | 8 | 49 |
| 6999 | 7 | 8 | 49 |
| 7000 | 7 | 8 | 49 |
| 7500 | 8 | 8 | 47 |
| 8000 | 8 | 8 | 50 |
| 8500 | 9 | 8 | 48 |
| 9000 | 9 | 8 | 51 |
| 9500 | 10 | 8 | 48 |
| 10000 | 10 | 8 | 51 |
| 10500 | 11 | 8 | 49 |
| 11000 | 11 | 8 | 51 |
| 11500 | 12 | 8 | 50 |
| 12000 | 12 | 8 | 52 |
| 12500 | 13 | 8 | 50 |
| 13000 | 13 | 8 | 52 |
| 13500 | 14 | 8 | 50 |
| 14000 | 14 | 8 | 52 |
| 14500 | 15 | 8 | 51 |
| 15000 | 15 | 8 | 52 |
| 15500 | 16 | 8 | 51 |
| 16000 | 16 | 8 | 53 |
| 16500 | 17 | 8 | 51 |
| 17000 | 17 | 8 | 53 |
| 17500 | 18 | 8 | 52 |
| 18000 | 18 | 8 | 53 |
| 18500 | 19 | 8 | 52 |
| 19000 | 19 | 8 | 53 |
| 19500 | 20 | 8 | 52 |
| 20000 | 20 | 8 | 53 |
| 25000 | 25 | 8 | 54 |
| 30000 | 30 | 8 | 54 |
| 50000 | 50 | 8 | 55 |
