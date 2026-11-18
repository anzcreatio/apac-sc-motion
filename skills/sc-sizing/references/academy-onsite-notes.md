# Creatio Academy: on-site deployment, notes for infrastructure sizing

- **Source tree:** https://academy.creatio.com/guides/setup-and-administration/category/on-site-deployment
- **Date read:** 2026-11-18
- **Version read:** **10** is the default ("latest") on the site; 8.3, 8.2, 8.1 and 8.0 can also be selected. URLs without a version segment serve v10. The 8.3 pages live under `/guides/setup-and-administration/8.3/on-site-deployment/...`.
- **8.3 vs 10:** I diffed 22 pages against their 8.3 copies: server-side requirements, client-side, general procedure, the 4 DB pages, file migration, 2 Identity Service pages, Creatio.ai, web farm, Email Listener, RabbitMQ, global search, Redis Cluster, ML service, bulk duplicate search and the .NET products FAQ. Apart from the "Version" label they are **identical**. So every fact below holds for both 8.3 and 10 unless it says otherwise.
- **Method:** each page was downloaded as server-rendered HTML and the article text extracted. Spot-checked against the rendered page in a browser, and the text matched exactly. Two table images were read as images (noted where used).
- **Tags:** **C** = stated on the page (quoted or close paraphrase). **I** = my inference, marked "(I)".
- **The tree has no sizing table.** No page maps users to servers, CPU, RAM or disk. Every page sends sizing to the separate **System requirements calculator** (https://academy.creatio.com/docs/requirements/calculator, not read here; another agent covers it). The only numeric sizing rules in the tree are bandwidth, IOPS and network latency rules, the marketing-email IOPS tiers, the Email Listener replica table and per-replica specs, RabbitMQ, MongoDB and NginX specs, the Redis Cluster minimums and the PostgreSQL max_connections formula.

---

## 1. Tree structure (what the docs cover)

| Sub-category | Articles |
|---|---|
| System requirements | Client-side, Server-side |
| General deployment procedure | (single article) |
| Database server | MS SQL; PostgreSQL (Linux); PostgreSQL (Windows); PostgreSQL (AWS RDS) |
| Caching server | General setup (Redis); Redis Cluster; Secure connection (TLS) |
| Application server on Linux | Prepare setup files; Installation; Move .NET 6 → .NET 8 |
| Application server on Windows | Required components; ConnectionStrings for MS SQL; ConnectionStrings for PostgreSQL; Web.config; IIS; WebSockets; HTTPS |
| Additional setup | Creatio.ai; Web farm; Google integration; Data enrichment; Chat access; Case notifications; Secure portal access; Version control (SVN); Landing pages; RabbitMQ; **File storage** (External storage, AWS S3, Azure Blob, File migration); **Identity Service** (Deploy, Connect, OAuth health, Update, PFX certificate) |
| Containerized components | Global search; Global search & dedup FAQ; Bulk duplicate search; Email Listener; Machine learning service |
| FAQ | Framework compatibility; Creatio .NET products; Creatio setup FAQ |

The tree has no separate page for bulk email (marketing) or Creatio Messaging Service. The general procedure links to "Bulk emails", which sits outside this tree.

---

## 2. Required vs optional components and general architecture rules

Source: https://academy.creatio.com/guides/setup-and-administration/on-site-deployment/system-requirements/server-side-system-requirements (C)

- **Required for any on-site Creatio:**
  - (1) Web server, which is also the Creatio application server.
  - (2) Database server with the chosen DBMS.
  - (3) Session storage server (Redis), "also known as caching server".
- **Optional:**
  - Version control server (SVN), "recommended for development environments".
  - Load balancers for the application, database and caching servers, for fault-tolerant configurations (Fig. 2 "Creatio fault-tolerant infrastructure", a diagram only, with no numbers in the text).
- **Need containerization ("operating-system-level virtualization"):** machine learning, data enrichment, bulk email service, global search, deduplication, Exchange Listener.
- **Supported virtual and cloud platforms:** "Amazon Web Services; Microsoft Azure / Hyper-V; VMware vCloud Director / vSphere". "Compatibility with other cloud / virtual platforms is not guaranteed."
- "All system components should be functional in a virtual environment."
- "Active system component instances must be placed in a single location (data center / server room / office building, etc.). Placing backup components in remote locations when implementing protection against catastrophic events is acceptable." This is the only DR statement in the tree.
- "All components should function in their dedicated operating systems. Merging components is possible, but not recommended."
- "To organize a DBMS cluster, you can use either a shared file storage or separate disk space of cluster nodes."
- **Load balancer** is optional. It "may be useful" when there is increased network load on the app servers, or when the app servers run as a web farm. It can be hardware or software. For fault tolerance, use an "HTTP/HTTPS traffic balancer that supports the WebSocket protocol".
  - Tested: **HAProxy** and **MS ARR**.
  - "Known cases" of success: Citrix, Cisco, NginX, FortiGate.
- **Deployment options** (https://academy.creatio.com/guides/setup-and-administration/on-site-deployment/general-creatio-deployment-procedure, C):
  - Cloud, Creatio-managed.
  - Cloud, customer-managed (AWS, Azure, GCP, others).
  - On-site, customer-managed (physical servers in the customer's DC).
  - "From a technical perspective, customer-managed cloud and on-site deployments follow the same procedure", apart from the connection strings.
  - Note: GCP is named here as a customer-managed cloud option, but it is **not** in the server-side "officially supported" platform list. (I) This is an inconsistency to flag.

---

## 3. Supported software stack (software requirements table)

Source: server-side page (C). The table is the same in 8.3 and 10.

| Component | Software (exact wording) |
|---|---|
| Web server (.NET Framework application) | Windows Server 2022 and later; IIS; .Net framework 4.7.2 |
| Web server (.NET) | Linux Debian 12 with kernel version 5.10 or later; .NET 8; GDI+ compatible API on non-Windows OS; development libraries and header files for GNU C |
| Database server (Windows) | Windows Server 2022 and later; Microsoft SQL 2022 and later, or PostgreSQL 16 and later |
| Database server (Linux) | Linux Debian 12; PostgreSQL 16 and later |
| Database server (Amazon RDS for PostgreSQL) | PostgreSQL 16 |
| Caching server | Linux Debian 12; Redis Server 7.4 and up |
| Load balancer server | Linux Debian 12; HAproxy |
| Version control system server (SVN) | Linux Debian 12; SVN |
| Containers | Linux Debian 12; Docker; Kubernetes |

**Redis edition note (C, server-side page):** "Creatio supports Redis Open Source and other Redis editions… fully compatible with all supported Redis versions. Redis Open Source provides all the required functionality for performance, reliability, and scalability in standard Creatio environments." Choosing a commercial edition is up to the customer's infrastructure and licensing.

**Oracle:** not mentioned anywhere in the tree. The only DB engines listed are MS SQL and PostgreSQL. (I) Oracle is not a supported option for current versions.

### .NET Framework vs .NET (Core/8): what that means for the stack

- **.NET 8 is mandatory for the .NET line since 8.2.1.** "Since Microsoft ended official support for .NET 6 in November 2024, starting from version 8.2.1 Creatio no longer supports .NET 6 and switches to .NET 8." Sources: general procedure, https://academy.creatio.com/guides/setup-and-administration/on-site-deployment/application-server-on-linux/move-creatio-net-6-to-net-8 (C).
  - Server prerequisites for the move: ".NET 8 SDK version 8.0.404 or later"; "Hosting Bundle for ASP.NET Core Runtime version 8.0.11 or later (for Windows)" (C, same page).
  - They recommend running the move on a test or pre-production environment first (C).
- **Creatio .NET products FAQ** (https://academy.creatio.com/guides/setup-and-administration/on-site-deployment/deployment-faq/creatio-net-products, C):
  - "We recommend using Linux to deploy Creatio .NET products."
  - Features "will be implemented in .NET products in future Creatio releases":
    - **Microsoft SQL DBMS**
    - authentication of incoming integrations via OAuth 2.0 ("available in Creatio 8.3.2 and later")
    - integration with SVN
    - portal in the mobile app
    - webhooks on .NET 8
  - So **.NET (Linux) deployments must use PostgreSQL.** MS SQL is supported only with the .NET Framework (Windows/IIS) line. (I, but strongly implied by the C statement.)
  - "Deploy the messaging service (Creatio Messaging Service) on Windows to integrate Avaya, TAPI telephony systems."
  - "The long-term plan is to move the entire Creatio product lineup to .NET and retire support for .NET Framework."
  - "Support for Creatio migration from .NET Framework to .NET is planned in the upcoming releases." So no migration path exists yet.
  - Marketplace apps need to be checked for .NET support.
- **Framework compatibility** (https://academy.creatio.com/guides/setup-and-administration/on-site-deployment/deployment-faq/framework-compatibility, C):
  - All products are available on .NET Framework.
  - .NET Core 3.1 applied to "Creatio 8.0.8 and earlier" and .NET to "Creatio 8.0.9 and later" for: Marketing, Sales Enterprise, Service Enterprise, Studio, SE+Mkt+SvcE, Sales Team+Mkt+Customer Center, and Bank Sales+BCJ+Lending+Marketing.
  - **Sales Commerce, Sales Team, Customer Center, Lending, Bank Customer Journey and Bank Sales on their own show .NET Framework only** (blank cells for .NET Core and .NET). (I) This table looks old (it stops at 8.0.x). Treat the per-product .NET availability for current versions as needing confirmation.
  - OS × framework: Windows supports .NET Framework (+), .NET Core 3.1 (+, "Linux recommended") and .NET (+). Linux does **not** support .NET Framework (–) but supports .NET Core 3.1 and .NET (+).
- **Production OS rules** (https://academy.creatio.com/guides/setup-and-administration/on-site-deployment/application-server-on-windows/enable-required-windows-components, C):
  - "Production environment for Creatio .NET Framework requires a Windows Server OS. You can deploy application server on Windows 10 only for development and pre-production environments."
  - The same applies to Creatio .NET on Windows (Windows 10/11 for dev and pre-prod only).
  - Windows components needed: Microsoft Visual C++ 2013; .NET 8 SDK and .NET Framework SDK 4.7.2 (for .NET Framework compilation); .NET 8 SDK and .NET 8 Hosting bundle (for .NET on Windows).
- **IIS:**
  - WebSockets need "Windows Server 2022 or Windows 10/11 deployed and Internet Information Services (IIS) version 10 or later" (https://academy.creatio.com/guides/setup-and-administration/on-site-deployment/application-server-on-windows/set-up-websockets, C).
  - App pool: ".NET CLR Version v.4.0.30319" for .NET Framework, "No Managed Code" for .NET (https://academy.creatio.com/guides/setup-and-administration/on-site-deployment/application-server-on-windows/deploy-creatio-application-server-on-iis, C).
  - Required IIS role services (ASP.NET, .NET extensibility, ISAPI, WebSocket Protocol, logging, request filtering, IP and Domain Restriction, WCF activation, TCP port sharing and others) are listed in https://academy.creatio.com/guides/setup-and-administration/on-site-deployment/deployment-faq/creatio-setup-faq (C).
- **Docker for the app server:** "We recommend deploying Creatio using Docker for development and testing environments only. Avoid using Docker for the production environment." (https://academy.creatio.com/guides/setup-and-administration/on-site-deployment/application-server-on-linux/deploy-the-creatio-net-application-on-linux, C). So for production, the **Creatio app server itself runs natively**: IIS on Windows Server, or `dotnet Terrasoft.WebHost.dll` on Linux. Only the microservices go in containers.
  - Linux run command: `COMPlus_ThreadPool_ForceMinWorkerThreads=100 dotnet Terrasoft.WebHost.dll`. HTTP on port 5000, HTTPS on port 5002 (C).
- **Client side** (https://academy.creatio.com/guides/setup-and-administration/on-site-deployment/system-requirements/client-side-system-requirements, C):
  - "The recommended data channel for the client-server connection is 3 Mbps per one active user."
  - Minimum screen 1280x768.
  - Browsers: latest Chrome, Firefox, Edge or Safari as of the release date.
  - (I) The 3 Mbps figure conflicts with the server-side "minimum 256 Kb/sec, recommended 512 Kb/sec per active user". They likely measure different things (client last-mile vs server uplink per user), but the docs don't reconcile them. Flag this.

---

## 4. Sizing numbers in the tree (all of them)

### 4.1 Network and I/O (server-side page, C)

| Link | Rule (exact) |
|---|---|
| IIS ↔ SQL | "the capacity of 10Mb/sec per 100 active users"; "delays no more than 15-20 ms" |
| IIS ↔ user | "minimum 256 Kb/sec per 1 active user"; "recommended 512 Kb/sec per 1 active user"; "formula: 30kByte/sec * (total number of users working at a time) * 10%" |
| I/O, app server | "IIS; 100 IOPS per 1000 active users" |
| I/O, DB | "SQL: 1000 IOPS per 1000 active users." |
| Client channel | "3 Mbps per one active user" (client-side page) |

(I) Read as linear rules: DB IOPS ≈ 1 IOPS per active user, app-server IOPS ≈ 0.1 IOPS per active user, and app-to-DB bandwidth ≈ 0.1 Mb/s per active user. The text never defines "active user" or "users working at a time".

### 4.2 Marketing (bulk) email: DB disk speed (server-side page, C)

"The recommended speed of DB disks depends on the number of recipients."

| Audience | Min DB disk IOPS | Latency |
|---|---|---|
| Up to 1 mln recipients in an email, or above 1 mln recipients per month | 300 IOPS | < 8 ms |
| 1 mln to 2 mln recipients in an email, or above 3 mln per month | 500 IOPS | < 8 ms |
| 2 mln to 5 mln recipients in an email, or above 5 mln per month | 1000 IOPS | < 7 ms |

### 4.3 Email Listener (Exchange Listener) sizing

**Server-side page (C):**
- "Exchange Listener processes requests by separate handlers simultaneously serving 40 active mailboxes each."
- The number of handlers is set at install time, based on the planned mailboxes.
- "One processor requires 30% of the 1GHz processor time and 850 Mb of RAM (disk storage is not used)."

**Email Listener page** (https://academy.creatio.com/guides/setup-and-administration/on-site-deployment/containerized-components/email-listener-synchronization-service, C):
- Sizing is based on the "average flow of emails (both incoming and outgoing) that the company mailboxes handle per second".
- Replica table (read from the page image `scr_exchange_listener_table_system_requirements.png`):

| Mailboxes | Avg email flow / s | EL Worker replicas | EL API replicas | RabbitMQ |
|---|---|---|---|---|
| 1–150 | <1 | 0 | 4 | Required |
| 1–150 | 1–5 | 15 | 4 | Required |
| 1–150 | >5 | 25 | 4 | Required |
| >150 | <1 | 2 | 1 replica per each 30 mailboxes | Required |
| >150 | 1–5 | 15 | 1 per 30 mailboxes | Required |
| >150 | >5 | 25 | 1 per 30 mailboxes | Required |

- Worked example in the text: one support mailbox with a flow of 4 → "15 EL Worker replicas, 4 EL API replicas, and RabbitMQ service".
- You can run fewer replicas than the table, at the cost of slower handling at peak.
- Per-replica requirements (C, "recommended, the actual resource consumption might vary"):

| Component | vCPU | RAM |
|---|---|---|
| EL Worker | 0.1 | 1.1 GB |
| EL API | 0.150 | 850 MB |
| Redis | 0.5 | 3 GB |
| RabbitMQ | 0.5 | 4 GB |

- Note the two pages disagree on mailboxes per instance: the server-side page says 40 mailboxes per handler, the Email Listener page says 1 EL API per 30 mailboxes above 150. (I) The Email Listener page is newer and more specific, so use it. EL API 0.150 vCPU / 850 MB matches the "30% of 1 GHz / 850 Mb" figure.
- Redis needs "a separate database for the Exchange Listener service".
- Deployment: "We recommend using the Kubernetes orchestrator and Helm package manager." Use Docker only for development: "For the product environment, we strongly recommend using the Kubernetes orchestrator and Helm" (Docker gives no fault tolerance or scaling).
- Repository access is required; "Contact Creatio support to verify your license and gain access to the repository."
- Required "to manage emails in Creatio .NET Framework and .NET Core since version 7.17.2 and .NET 6 since version 8.0.8".
- Ports in the examples: RabbitMQ AMQP 5672 and HTTP 15672; Redis 6379; Docker dev UI at http://localhost:10000/; NodePort example 31318. HTTPS needs Ingress with a valid SSL certificate.

### 4.4 RabbitMQ (message broker for background tasks and Email Listener)

Source: https://academy.creatio.com/guides/setup-and-administration/on-site-deployment/deployment-additional-setup/rabbit-mq (C)

- **Purpose:**
  - Out of the box, Creatio queues background tasks in web-node RAM.
  - With RabbitMQ, the background-task queue survives node restarts.
  - "All web-farm nodes will consume messages from a single queue."
  - You can dedicate some nodes to background processing "without routing HTTP traffic to these nodes".
- **Sizing:** per node, "0.5 vCPU, 4 GB RAM, 10 GB disk space".
  - "If you are going to use both the Email Listener and Creatio, a single RabbitMQ instance can be shared."
  - If you don't use Email Listener, "allocate equal resources to each RabbitMQ node".
  - Kubernetes: the pod RAM limit should be "at least twice the configured RabbitMQ memory limit"; use a generous liveness probe, e.g. 5 minutes.
- **High availability:**
  - Single node = "single point of failure".
  - A clustered RabbitMQ gives HA. "Out of the box, Creatio uses quorum queues". These can be disabled for brokers that don't support them, e.g. Amazon MQ.
  - Upgrade quorum clusters one node at a time.
- **Behaviour on failure:** if the broker is unreachable, Creatio falls back to "in-memory mode". Delivery is "at least once", not exactly once.
- **Monitoring:** consumers (must be 1 per Creatio node), creatio_main queue size, creatio_main_error (must be 0), rates, memory, disk.
- **Config:** connection string `messageBroker` = `amqp://user:pass@host:5672/vhost`; `serviceBus operatingMode="Auto"`, `messageProcessingThreadsCount="10"` (default example).
- (I) For sizing: RabbitMQ is optional for core Creatio but **required for Email Listener** and recommended for web farms with heavy background processing.

### 4.5 Global search (ElasticSearch) and bulk duplicate search (MongoDB)

**Global search** (https://academy.creatio.com/guides/setup-and-administration/on-site-deployment/containerized-components/global-search, C):

- Global search version 3.0 is deployed with Kubernetes + Helm, or with Docker.
- "We recommend always using the latest version of the global search service with the latest version of Creatio."
- Repository access via Creatio support ("verify your license").
- **Docker layout: "The global search requires 2 dedicated physical or virtual servers ("server 1" and "server 2") with Linux installed. Use the requirements calculator to check the server requirements."** No CPU, RAM or disk figures are given in the tree.
  - Server 1: elasticsearch.
  - Server 2: postgres (service DB), rabbitmq, redis, gs-web-api, gs-web-indexing-service, gs-search-service, gs-scheduler, gs-worker, gs-worker-replay, gs-worker-single, gs-worker-single-replay, gs-worker-single-task, gs-worker-queried-single-task.
- Kubernetes: the chart can install its own Redis, RabbitMQ, ElasticSearch and PostgreSQL, or point to existing ones.
- "For highly loaded environments, we recommend deploying ElasticSearch in a cluster."
- **Backup:** "We also recommend backing up ElasticSearch daily."
- **Time sync:** container host UTC must match the Creatio DB server UTC within 5 minutes, or indexing may miss records.
- **Ports (firewall):**
  - gs-web-api: in 81
  - gs-web-indexing-service: in 82
  - gs-search-service: in 83, out 9200
  - gs-worker and gs-worker-single: out 9200
  - elasticsearch: in 9200
  - Kubernetes public search-service URL example: http://k8s-node:30332
- **Indexing load knobs:**
  - GS_DB_INCREMENT_DAYS default "500 days".
  - GS_DB_FILL_QUEUE_INTERVAL default "30000" ms. "The lower the variable, the higher the load on Creatio database and the faster the primary indexing."
- **Search templates trade-off** (relative to default.json = 1x):

| Template | Search speed | Index size | Indexing time |
|---|---|---|---|
| ngram_2.json | 13x | 4x | 1.8x |
| ngram_3.json | 7x | 2.5x | 1.4x |
| without_ngram.json | <1x | <1x | <1x |

  (I) This drives ElasticSearch disk sizing: an n-gram template multiplies index size by 2.5–4x.
- Supports MS SQL and PostgreSQL Creatio databases (`databaseType: mssql | postgresql`).

**Global search & dedup FAQ** (https://academy.creatio.com/guides/setup-and-administration/on-site-deployment/containerized-components/global-search-and-deduplication-faq, C):
- Production and dev environments can each have their own independent GS and dedup services.
- "Since you must deploy the global search and deduplication service using Docker, microservices do not support Windows authentication."
- ElasticSearch clustering → see Elastic docs.
- **MongoDB** (dedup):
  - "can run outside the Kubernetes cluster", which "can reduce the risk of storage corruption".
  - "For deduplication search, a standalone MongoDB instance is sufficient. If high availability and redundancy are required, use a 3-node replica set."
  - "As a starting point, allocate: 1 CPU core, 16 GB RAM, Reliable SSD storage with sufficient IOPS. The final resource allocation depends on dataset size and expected workload."
- **Persistent storage:** "Only PostgreSQL and MongoDB must use persistent volumes"; no other GS or dedup Kubernetes component needs persistent storage.
- ElasticSearch password protection: HAProxy basic auth or the x-pack plugin.

**Bulk duplicate search** (https://academy.creatio.com/guides/setup-and-administration/on-site-deployment/containerized-components/bulk-duplicate-search, C):
- Depends on global search; "always uses the same ElasticSearch service as global search".
- "To optimize the load on Redis and RabbitMQ, we recommend using the same service instances for both global search and bulk duplicate search."
- Components: Mongodb, dd-web-api, dd-data-service, dd-duplicates-search-worker, dd-duplicates-deletion-worker, dd-duplicates-confirmation-worker, dd-duplicates-cleaner, dd-deduplication-task-worker, dd-deduplication-preparation-worker, dd-deduplication-task-diagnostic-worker.
- dd-web-api on port **8086**.
- "We recommend performing mongodb backup once a day."
- Sizing: "Use the requirements calculator".

### 4.6 Redis (caching server)

**General setup** (https://academy.creatio.com/guides/setup-and-administration/on-site-deployment/caching-server/general-setup-procedure-for-data-caching-server-redis, C):
- Installed with apt on Debian.
- "Creatio lets you use Amazon ElastiCache for Redis."

**Redis Cluster** (https://academy.creatio.com/guides/setup-and-administration/on-site-deployment/caching-server/redis-cluster, C):
- "Deploy Redis Cluster on Linux with Redis Server 7.4 or later."
- "Since Redis is a single-threaded application and uses a single processor core, use a node… with at least a dual-core processor to deploy a single Redis instance."
- "To ensure the maximum fault tolerance, use a physical machine for each Redis instance so that every master-slave instance is physically separated."
- "To ensure fault tolerance, use at least six Redis instances running on separate computers or virtual machines" (minimal fault-tolerant config = 6 nodes, i.e. 3 masters + 3 replicas per Fig. 1). (I) The 3+3 split is my reading of the figure.
- Scales "up to 1000 instances".
- Failover risk: asynchronous replication can lose writes. "The automatic reconfiguration that assigns a new master instance may take up to 15 seconds."
- RAM: none stated. "Use the requirements calculator."
- Creatio config:
  - `clusterHosts=ip1:port1,...`
  - `Feature-UseRetryRedisOperation=true`
  - Required redis section values: clientConnectTimeoutMs 5000, clientSyncTimeoutMs 5000, clientAsyncTimeoutMs 5000, operationRetryIntervalMs 5000, operationRetryCount 25, timeToCheckConfigurationSeconds 60, among others.

**Redis Sentinel:**
- No dedicated article.
- The only mention is a `redisSentinel` connection string example on https://academy.creatio.com/guides/setup-and-administration/on-site-deployment/application-server-on-windows/modify-connectionstrings-config-for-postgresql (C): `sentinelHosts=localhost:26380,localhost:26381,localhost:26382;masterName=mymaster;...`
- (I) Sentinel is technically supported through the connection string, but the documented HA path is **Redis Cluster**.

**TLS** (https://academy.creatio.com/guides/setup-and-administration/on-site-deployment/caching-server/set-up-secure-connection-to-redis, C):
- TLS 1.2 to standalone or Cluster Redis (Redis 6.0+), via `useTls=true` plus a password and/or certificate.

**Redis DB numbering (C):** "The Redis database number must be unique for each Creatio site" (https://academy.creatio.com/guides/setup-and-administration/on-site-deployment/application-server-on-linux/prepare-creatio-net-setup-files-on-linux). (I) One Redis server can host several environments (prod, test, dev) on different DB numbers. Email Listener needs its own Redis DB.

### 4.7 Database server

**MS SQL** (https://academy.creatio.com/guides/setup-and-administration/on-site-deployment/database-server/deploy-ms-sql-database-for-creatio, C):
- "Using Microsoft SQL Always On availability groups is a recommended method of setting up a high availability configuration."
- Two users: a superuser to restore, and a regular user (db_owner) for runtime.
- Default connection string `Max Pool Size = 100` (ConnectionStrings for MS SQL page).
- Data and log files: TSOnline_Data and TSOnline_Log.

**PostgreSQL (Linux / Windows)**
(https://academy.creatio.com/guides/setup-and-administration/on-site-deployment/database-server/deploy-postgresql-database-linux and https://academy.creatio.com/guides/setup-and-administration/on-site-deployment/database-server/deploy-postgresql-database-windows, C):
- "Creatio requires PostgreSQL 16 or later."
- "Remote DBMS (recommended)."
- Clustering → "High Availability, Load Balancing, and Replication" in the PostgreSQL docs. Creatio gives no HA guidance of its own.
- **Connection tuning, "only if your Creatio deployment is going to serve more than 100 simultaneous users":**
  - `max_connections` = expected simultaneous users × 1.5, capped at **1024**.
  - `shared_buffers` = max_connections × 0.24 MB, rounded up (1024 → 246 MB).
  - Linux only: `kernel.shmmax` = shared_buffers + 16 MB, in bytes (246 MB → 274 726 912).
  - (I) The 1024 cap matches `MaxPoolSize=1024` in the PostgreSQL connection string. So beyond ~683 simultaneous users (683 × 1.5 ≈ 1024) the formula saturates. This is a pointer to web farm and DB tuning beyond the documented guidance.

**PostgreSQL (AWS RDS)** (https://academy.creatio.com/guides/setup-and-administration/on-site-deployment/database-server/deploy-postgresql-database-aws-rds, C):
- "This article covers AWS RDS PostgreSQL v16.12 instances."
- "Disable auto-updating of your PostgreSQL instance in AWS to maintain compatibility."
- Port 5432.

**DB size, storage growth, backup cadence:** the tree gives **no** DB size estimates, growth rates or backup schedules for the Creatio DB.
- The only backup cadence guidance is daily backups for ElasticSearch and MongoDB, a MySQL backup before ML updates, and DB backups before Identity Service updates.

### 4.8 File storage

Source: https://academy.creatio.com/guides/setup-and-administration/on-site-deployment/deployment-additional-setup/file-storage/use-external-file-storages (C)

- "By default, all files uploaded to Creatio are stored in the database."
- External storage "reduce[s] the size of the database and time for maintenance".
- Out of the box: **AWS S3** and **Azure Blob**. Custom storage is possible through the file management API.
- S3 (https://academy.creatio.com/guides/setup-and-administration/on-site-deployment/deployment-additional-setup/file-storage/set-up-s3-file-storage-integration, C): "Creatio officially supports and guarantees compatibility with AWS S3 only." (I) S3-compatible on-prem stores such as MinIO are not guaranteed.
- Soft delete: a recycle bucket or container keeps deleted files "for database backups".
- FileMigrator (from support) moves existing files from DB to storage and deletes them from the DB afterwards. Custom code that reads file content straight from the DB stops working (https://academy.creatio.com/guides/setup-and-administration/on-site-deployment/deployment-additional-setup/file-storage/file-migration, C).
- (I) For sizing: with DB file storage, attachment volume adds directly to DB size and backup size.

### 4.9 Machine learning service

Source: https://academy.creatio.com/guides/setup-and-administration/on-site-deployment/containerized-components/machine-learning-service (C)

- Licence: "Creatio on-site requires the 'creatio predictive service on-site' license."
- A server (physical or VM) with Linux or Windows, running Docker CE or EE.
- "We recommend using a Linux-based server for production environment. You can only use a Windows based server for the development environment."
- Components:
  - ML Service (the only one exposed externally)
  - Python Engine
  - ML Task Scheduler
  - MySQL (port 3306)
  - (The health check also mentions an R Engine on 8081.)
- Ports: ML web service 5005, ML Task Scheduler 5004, R Engine 8081.
- Sizing: "Use the requirements calculator". No figures in the tree.
- Offline install: export and import the images if the server has no Internet.

### 4.10 Creatio.ai on-site (generative AI)

Source: https://academy.creatio.com/guides/setup-and-administration/on-site-deployment/deployment-additional-setup/creatio-ai-on-site (C). The page exists, identical, in 8.3 and 10.

- Deployed with Docker Compose ("simple deployments on a single Linux server") or Kubernetes ("production-grade deployments with scalability and high availability").
- **Prerequisites:**
  - Linux machine or Kubernetes cluster
  - credentials for **registry.creatio.com**
  - "OpenAI or Azure OpenAI API keys"
  - firewall open on **5006** (Docker) or **30082** (Kubernetes NodePort), or a custom Ingress
- Services:
  - **enrichment-service**: the REST endpoint for genAI requests.
  - **litellm**: LLM abstraction layer for OpenAI and Azure OpenAI.
  - **postgres**: stores "operational statistics, for example, request logs". By default it runs without persistent storage, since it holds only "non-critical information such as request counts and token usage statistics".
- Kubernetes: version **1.19 or later**, Helm **3.0 or later**.
- Creatio points the "Account enrichment service url" (AccountEnrichmentServiceUrl) setting at the service.
- **No CPU, RAM or disk requirements are stated.**
- **The LLM is not hosted on-site.** The docs only cover OpenAI or Azure OpenAI through API keys. (I) Outbound Internet to OpenAI or Azure is needed. A fully air-gapped or self-hosted LLM is not documented (litellm could in theory route elsewhere, but that's undocumented).
- "Creatio.ai is pre-configured out of the box in Creatio cloud."

### 4.11 Data enrichment, chat, other Internet-dependent services

- **Data enrichment** (https://academy.creatio.com/guides/setup-and-administration/on-site-deployment/deployment-additional-setup/data-enrichment-service, C):
  - "only available for Classic UI pages".
  - Needs a personal cloud key, the "Creatio cloud services API key" (from support), and the "Account enrichment service URL" pointing at Creatio cloud services.
  - (I) This means outbound calls to Creatio cloud. It contrasts with the server-side page listing "data enrichment" among the containerized services; that is likely legacy wording.
- **Chats** (https://academy.creatio.com/guides/setup-and-administration/on-site-deployment/deployment-additional-setup/chat-access-setup, C):
  - HTTPS is required.
  - The app server needs access to https://sm-account.creatio.com/, plus an incoming HTTPS connection with a valid certificate for that chat service.
  - Whitelist `mcs.us1.twilio.com/*` for WhatsApp.
  - Telegram needs Internet access from the app server.
  - Ada needs the webhook service.
- **Google integration:** Calendar API keys (Client ID and Secret) set as system settings (https://academy.creatio.com/guides/setup-and-administration/on-site-deployment/deployment-additional-setup/google-integration).
- **Landing pages:** set "Landing pages data collection service URL" to the external URL when the firewall or URL rules differ (https://academy.creatio.com/guides/setup-and-administration/on-site-deployment/deployment-additional-setup/landing-page-integration).
- **Case notifications:** set "Website URL" (https://academy.creatio.com/guides/setup-and-administration/on-site-deployment/deployment-additional-setup/case-resolution-notifications).

### 4.12 Identity Service (OAuth 2.0 for incoming integrations)

Source: https://academy.creatio.com/guides/setup-and-administration/on-site-deployment/deployment-additional-setup/identity-service/set-up-the-identity-service-instruction (C)

- Separate service on IIS or Docker. Needs .NET 8 Runtime and Hosting Bundle.
- "Use dedicated application pool for every Creatio instance."
- Unique port (example 8090).
- Its own DB tables on MS SQL or PostgreSQL ("MsSqlServer" or "Postgres").
- One certificate per instance is recommended.
- Availability: "for Creatio deployed on either .NET Framework or .NET 8 in Creatio 8.3.2 and later. In Creatio 8.3.1 and earlier… .NET Framework only."
- Certificates: RSA, or ECDSA P-256/SHA-256, P-384/SHA-384 or P-521/SHA-512 (https://academy.creatio.com/guides/setup-and-administration/on-site-deployment/deployment-additional-setup/identity-service/openssl).
- No hardware figures.

### 4.13 NginX static-content offload (web farm page)

- "To install NginX, deploy it in Kubernetes. We recommend using the Helm chart from Bitnami… with two replicas. Each replica utilizes 100 Mb of CPU and 128 Mb of memory." (C)
- (I) "100 Mb of CPU" is probably 100m (0.1 vCPU).
- Described as "usually unnecessary". It helps static-content load time, e.g. when the static server is closer geographically.

---

## 5. High availability, web farm, DR

**Web farm** (https://academy.creatio.com/guides/setup-and-administration/on-site-deployment/deployment-additional-setup/application-server-web-farm, C):
- "You can enhance the performance of large-scale Creatio projects (up to several thousand users) through horizontal scaling, i. e., by increasing the number of servers with deployed Creatio applications and setting up workload distribution between them."
- Load balancer:
  - Tested on HAProxy. Others in use: Citrix, Cisco, NginX, FortiGate, Microsoft ARR.
  - Must support WebSocket for fault tolerance.
  - HAProxy example: `maxconn 10000`; roundrobin with per-server weights; health checks on `GET /0/ping` or `/Login/NuiLogin.aspx`; stats page on :9000.
- All nodes share the same SQL and Redis databases.
- Node clocks must be synchronized.
- .NET Framework specifics: identical `TenantId` in the internal Web.config, an identical `machineKey`, and Quartz clustering (`quartz.jobStore.clustered=true`, `instanceId=AUTO`).
- .NET specifics: run `dotnet Terrasoft.WebHost.dll configureWebFarmMode`, then copy the config to all nodes.
- "If necessary, set up load balancing for database and session servers." Clustering for MS SQL → Microsoft docs; Redis → Redis Cluster article.
- Marketplace add-ons and customizations install differently behind a balancer.
- Audit-log real client IP: ForwardedHeaders in appsettings.json (.NET).

**Portal security** (https://academy.creatio.com/guides/setup-and-administration/on-site-deployment/deployment-additional-setup/secure-access-to-the-portal, C):
- "To ensure data security, deploy Creatio on-site as a web farm when installing the portal."
- A reverse proxy must be "the only publicly accessible component in your DMZ".
- "Deploy a separate set of application nodes on the web farm for servicing portal users. This set must not overlap with application nodes for servicing internal users."
- Use separate DB accounts for the portal and the user app.
- Portal nodes accept only the SSPUserPassword auth provider.
- "Deploy portal application nodes, DBMS, and user applications in separate segments with restricted access."
- (I) Sizing impact: **portal = at least 2 node groups (internal + portal) + reverse proxy in the DMZ.**

**HA per tier, as the docs give it:**

| Tier | Documented HA mechanism |
|---|---|
| App | Web farm behind an LB |
| DB, MS SQL | Always On availability groups ("recommended") |
| DB, PostgreSQL | Vendor HA docs only |
| Redis | Redis Cluster, ≥6 instances (Sentinel string example only) |
| RabbitMQ | Cluster with quorum queues |
| ElasticSearch | Cluster "for highly loaded environments" |
| MongoDB | 3-node replica set |
| Email Listener | Kubernetes replicas |
| Creatio.ai | Kubernetes |

**DR:** only the "single location for active components; backup components may be remote" rule. There is no RPO/RTO guidance, no Creatio DB backup schedule and no DR runbook in the tree.

---

## 6. Environments (prod / test / dev)

| Rule | Source |
|---|---|
| SVN recommended for development environments only | server-side page; https://academy.creatio.com/guides/setup-and-administration/on-site-deployment/deployment-additional-setup/version-control-system-for-development-environments |
| SVN 1.14+; web-server frontend (HTTP/HTTPS) recommended | VCS page |
| Git usable in file-system development mode | VCS page |
| Each developer needs an isolated app server + DB unless SVN is the only contact point | VCS page |
| Windows 10/11 app servers: dev and pre-prod only | Windows components page |
| Docker for the Creatio app server: dev and test only | Linux install page |
| Docker for Email Listener: dev only (Kubernetes for production) | Email Listener page |
| ML on Windows: dev only (Linux for production) | ML page |
| Redis TLS certificate validation may be disabled in dev | Redis TLS page |
| Test .NET 8 moves on test or pre-prod first | .NET 8 page |
| Production and dev can each have their own global search and dedup services | GS FAQ |
| Redis DB number unique per site (one Redis can serve several sites) | Linux prep page (I for the multi-site reading) |

---

## 7. Licensing-related deployment notes (C)

- ML: "creatio predictive service on-site" licence required.
- Global search, bulk duplicate search and Email Listener: repository access granted by Creatio support after "verify[ing] your license".
- Creatio.ai: registry.creatio.com credentials needed, plus the customer's own OpenAI or Azure OpenAI keys (I: the LLM cost is the customer's).
- Data enrichment: a personal Creatio cloud services API key from support.
- FileMigrator.dll comes from support.

---

## 8. Ports and protocols (consolidated, C unless noted)

| Service | Port(s) |
|---|---|
| Creatio .NET on Linux | 5000 HTTP, 5002 HTTPS |
| IIS site | as bound (80/443) |
| HAProxy | 80, 443 front; 9000 stats |
| Redis | 6379; Sentinel example 26380–26382 |
| PostgreSQL | 5432 (example strings also show 31436) |
| RabbitMQ | 5672 AMQP, 15672 HTTP/management |
| Global search | 81, 82, 83 (Docker); 9200 ElasticSearch; 30332 (Kubernetes example) |
| Dedup dd-web-api | 8086 |
| Email Listener | 10000 (Docker dev); NodePort example 31318 |
| ML | 5005, 5004, 8081, MySQL 3306 |
| Creatio.ai | 5006 (Docker), 30082 (Kubernetes NodePort) |
| Identity Service | example 8090 |

Protocol and certificate notes:
- WebSockets must pass through any proxy or LB.
- HTTPS "recommended". It needs a PFX certificate.
- With a self-signed certificate, "Creatio mobile application will not be able to connect" (https://academy.creatio.com/guides/setup-and-administration/on-site-deployment/application-server-on-windows/switch-creatio-website-from-http-to-https).
- On Linux dev over HTTP, `CookiesSameSiteMode=Lax` breaks the mobile app.

---

## 9. "Recommended" vs "required" wording and large-load guidance

- **Required:** app/web server, DB server, Redis; Windows Server for production on Windows; PostgreSQL 16+; Redis 7.4+ (for Cluster); WebSocket-capable LB for fault tolerance; RabbitMQ for Email Listener (table: "Required"); licences and repository access as above.
- **Recommended:** separate OS per component; Linux for .NET products; remote DBMS; MS SQL Always On for HA; ≥6-node Redis Cluster with a physical machine per instance; Kubernetes for Email Listener, Creatio.ai (production) and GS/dedup; daily ElasticSearch and MongoDB backups; ElasticSearch cluster for high load; latest GS version; HTTPS.
- **Large or non-standard loads:**
  - Web farm for "up to several thousand users".
  - LB for DB and session servers "if necessary".
  - ElasticSearch cluster for highly loaded environments.
  - PostgreSQL connection tuning above 100 simultaneous users (cap 1024).
  - Email Listener replica table by mailbox count and email flow.
  - Marketing IOPS tiers by audience size.
  - Everything else: "Use the requirements calculator". **The tree never says to contact Creatio for sizing beyond the calculator.** (I) Non-standard loads need Creatio or partner sizing outside the docs.
- **Caveats in the docs themselves:**
  - The Email Listener figures "are recommended, the actual resource consumption might vary"; monitor and adjust.
  - MongoDB "final resource allocation depends on dataset size and expected workload".
  - Merging components is "possible, but not recommended".
  - Other virtualization platforms are "not guaranteed".

---

## 10. Gaps and inconsistencies to flag for the tool (I)

1. There is no user-count → CPU/RAM/disk table anywhere in the tree. The calculator is the only source, so the tool's server specs must come from it.
2. Client bandwidth: 3 Mbps per active user (client page) vs 256–512 Kb/s per active user (server page).
3. Email Listener capacity: 40 mailboxes per handler (server page) vs 1 EL API per 30 mailboxes (Email Listener page).
4. GCP is listed as a customer-managed cloud option, but is not in the "officially supported" virtualization list.
5. The "data enrichment" container is listed as required, but the data-enrichment page describes a Creatio-cloud service called with an API key.
6. MS SQL is not available on Creatio .NET (Linux). The framework-compatibility table looks dated (8.0.x) and shows several products, including Bank Sales, BCJ and Lending, as .NET Framework only. Confirm before recommending Linux for those products.
7. No Oracle support; no Redis Sentinel article; no DB size or growth guidance; no Creatio DB backup or RPO/RTO guidance.
8. Creatio.ai on-site gives no hardware figures and relies on external OpenAI or Azure OpenAI.

---

## 11. Every URL read (2026-11-18)

Category pages:
- https://academy.creatio.com/guides/setup-and-administration/category/on-site-deployment
- https://academy.creatio.com/guides/setup-and-administration/category/system-requirements
- https://academy.creatio.com/guides/setup-and-administration/category/database-server
- https://academy.creatio.com/guides/setup-and-administration/category/caching-server
- https://academy.creatio.com/guides/setup-and-administration/category/application-server-on-linux
- https://academy.creatio.com/guides/setup-and-administration/category/application-server-on-windows
- https://academy.creatio.com/guides/setup-and-administration/category/additional-setup
- https://academy.creatio.com/guides/setup-and-administration/category/file-storage
- https://academy.creatio.com/guides/setup-and-administration/category/identity-service
- https://academy.creatio.com/guides/setup-and-administration/category/сontainerized-components (Cyrillic "С" in the slug)
- https://academy.creatio.com/guides/setup-and-administration/category/faq

Articles (v10). All are prefixed `https://academy.creatio.com/guides/setup-and-administration/on-site-deployment/`:
- system-requirements/client-side-system-requirements
- system-requirements/server-side-system-requirements
- general-creatio-deployment-procedure
- database-server/deploy-ms-sql-database-for-creatio
- database-server/deploy-postgresql-database-linux
- database-server/deploy-postgresql-database-windows
- database-server/deploy-postgresql-database-aws-rds
- caching-server/general-setup-procedure-for-data-caching-server-redis
- caching-server/redis-cluster
- caching-server/set-up-secure-connection-to-redis
- application-server-on-linux/prepare-creatio-net-setup-files-on-linux
- application-server-on-linux/deploy-the-creatio-net-application-on-linux
- application-server-on-linux/move-creatio-net-6-to-net-8
- application-server-on-windows/enable-required-windows-components
- application-server-on-windows/modify-connectionstrings-config-for-ms-sql-server
- application-server-on-windows/modify-connectionstrings-config-for-postgresql
- application-server-on-windows/modify-web-config
- application-server-on-windows/deploy-creatio-application-server-on-iis
- application-server-on-windows/set-up-websockets
- application-server-on-windows/switch-creatio-website-from-http-to-https
- deployment-additional-setup/creatio-ai-on-site
- deployment-additional-setup/application-server-web-farm
- deployment-additional-setup/google-integration
- deployment-additional-setup/data-enrichment-service
- deployment-additional-setup/chat-access-setup
- deployment-additional-setup/case-resolution-notifications
- deployment-additional-setup/secure-access-to-the-portal
- deployment-additional-setup/version-control-system-for-development-environments
- deployment-additional-setup/landing-page-integration
- deployment-additional-setup/rabbit-mq
- deployment-additional-setup/file-storage/use-external-file-storages
- deployment-additional-setup/file-storage/set-up-s3-file-storage-integration
- deployment-additional-setup/file-storage/set-up-azure-blob-file-storage-integration
- deployment-additional-setup/file-storage/file-migration
- deployment-additional-setup/identity-service/set-up-the-identity-service-instruction
- deployment-additional-setup/identity-service/connect-the-identity-service
- deployment-additional-setup/identity-service/oauth-health-monitoring
- deployment-additional-setup/identity-service/update-the-identity-service-using-iis-instruction
- deployment-additional-setup/identity-service/openssl
- containerized-components/global-search
- containerized-components/global-search-and-deduplication-faq
- containerized-components/bulk-duplicate-search
- containerized-components/email-listener-synchronization-service
- containerized-components/machine-learning-service
- deployment-faq/framework-compatibility
- deployment-faq/creatio-net-products
- deployment-faq/creatio-setup-faq

8.3 copies read for comparison (identical apart from the version label). Prefix `https://academy.creatio.com/guides/setup-and-administration/8.3/on-site-deployment/`:
- system-requirements/server-side-system-requirements
- system-requirements/client-side-system-requirements
- general-creatio-deployment-procedure
- the 4 database-server pages
- deployment-additional-setup/file-storage/file-migration
- identity-service/set-up-the-identity-service-instruction
- identity-service/connect-the-identity-service
- deployment-additional-setup/creatio-ai-on-site
- deployment-additional-setup/application-server-web-farm
- containerized-components/email-listener-synchronization-service
- deployment-additional-setup/rabbit-mq
- containerized-components/global-search
- caching-server/redis-cluster
- containerized-components/machine-learning-service
- containerized-components/bulk-duplicate-search
- deployment-faq/creatio-net-products

Images read:
- https://academy.creatio.com/docs/sites/academy_en/files/images/Setup_and_Administration/exchange_listener/scr_exchange_listener_table_system_requirements.png (the Email Listener replica table)

Not read:
- The fault-tolerant architecture diagram (server-side Fig. 2) could not be rendered. Its surrounding text has no numbers.
- Out-of-tree links: system requirements calculator (deliberately skipped), "Bulk emails" setup, mobile system requirements, and the legacy `/documents?id=...` links.
