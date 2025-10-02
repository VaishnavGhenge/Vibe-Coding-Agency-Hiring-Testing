# Enterprise RAG Knowledge Management System - Architecture Design

## 1. RAG ARCHITECTURE DIAGRAM (REVISED)

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         DOCUMENT INGESTION LAYER                             │
└─────────────────────────────────────────────────────────────────────────────┘
                                      │
        ┌─────────────────────────────┼─────────────────────────────┐
        │                             │                             │
        ▼                             ▼                             ▼
┌──────────────┐            ┌──────────────┐            ┌──────────────┐
│   S3 Bucket  │            │  API Upload  │            │   NOTE:      │
│  (Existing   │            │   Endpoint   │            │ Email sync   │
│  Documents)  │            │              │            │ Phase 3 only │
└──────────────┘            └──────────────┘            └──────────────┘
        │                             │
        └─────────────────────────────┼─────────────────────────────┘
                                      │
                                      ▼
                        ┌──────────────────────────┐
                        │   S3 Event → SNS Topic   │
                        └──────────────────────────┘
                                      │
                                      ▼
                        ┌──────────────────────────┐
                        │   SQS Queue (FIFO)       │
                        │   + DLQ for failures     │
                        └──────────────────────────┘
                                      │
                                      ▼
                        ┌──────────────────────────┐
                        │   Lambda Processor       │
                        │   (with retry logic)     │
                        └──────────────────────────┘
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                      PROCESSING & EMBEDDING LAYER                            │
└─────────────────────────────────────────────────────────────────────────────┘
                                      │
                        ┌─────────────┴─────────────┐
                        ▼                           ▼
            ┌────────────────────┐      ┌────────────────────┐
            │  Document Parser   │      │  Metadata Extract  │
            │  - Textract (scan) │      │  - Custom Lambda   │
            │  - PyPDF2 (text)   │      │  - Date/Author/ACL │
            │  - Unstructured.io │      │  - Permissions     │
            │    (Word/PPT/etc)  │      │  - Version         │
            └────────────────────┘      └────────────────────┘
                        │                           │
                        └─────────────┬─────────────┘
                                      ▼
                        ┌──────────────────────────┐
                        │   Step Functions         │
                        │   (orchestration)        │
                        └──────────────────────────┘
                                      │
                                      ▼
                        ┌──────────────────────────┐
                        │   Intelligent Chunking   │
                        │   - LangChain splitter   │
                        │   - Semantic boundaries  │
                        │   - 256-1024 tokens      │
                        │   - Doc context metadata │
                        └──────────────────────────┘
                                      │
                                      ▼
                        ┌──────────────────────────┐
                        │  Embedding Generation    │
                        │  - Amazon Titan (primary)│
                        │  - Batch: 100 docs       │
                        │  - 1024 dimensions       │
                        │  - Cost: $0.0001/1K tok  │
                        └──────────────────────────┘
                                      │
                ┌─────────────────────┼─────────────────────┐
                ▼                     ▼                     ▼
┌──────────────────────┐  ┌──────────────────┐  ┌──────────────────┐
│  Vector Database     │  │  PostgreSQL RDS  │  │   S3 Storage     │
│  (Pinecone Standard) │  │  db.r6g.large    │  │  - Raw Docs      │
│  - Embeddings        │  │  - Metadata      │  │  - Processed     │
│  - Metadata filter   │  │  - Permissions   │  │  - Backups       │
│  - Sub-100ms query   │  │  - Audit logs    │  │  - Versions      │
│  - 50M vec capacity  │  │  - Multi-AZ      │  │  - Intelligent   │
│                      │  │  - Read replicas │  │    Tiering       │
└──────────────────────┘  └──────────────────┘  └──────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│                            QUERY & RETRIEVAL LAYER                           │
└─────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
                        ┌──────────────────────────┐
                        │   User Query (REST API)  │
                        │   + Auth Token           │
                        └──────────────────────────┘
                                      │
                                      ▼
                        ┌──────────────────────────┐
                        │  Query Embedding         │
                        │  - Same embedding model  │
                        │  - Real-time processing  │
                        └──────────────────────────┘
                                      │
                                      ▼
                        ┌──────────────────────────┐
                        │  Get User Permissions    │
                        │  - From Redis cache      │
                        │  - Or PostgreSQL         │
                        │  - departments, groups   │
                        └──────────────────────────┘
                                      │
                                      ▼
                        ┌──────────────────────────┐
                        │  Vector Search + Filter  │
                        │  - Pinecone metadata     │
                        │    filtering (IN-QUERY)  │
                        │  - Only authorized docs  │
                        │  - Top 10 chunks         │
                        │  - Cosine similarity     │
                        └──────────────────────────┘
                                      │
                                      ▼
                        ┌──────────────────────────┐
                        │  Context Assembly        │
                        │  - Top 5 chunks          │
                        │  - Source metadata       │
                        │  - Build prompt          │
                        └──────────────────────────┘
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                         GENERATION & RESPONSE LAYER                          │
└─────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
                        ┌──────────────────────────┐
                        │   LLM API Call           │
                        │   - GPT-4o-mini          │
                        │   - System prompt        │
                        │   - Context + Query      │
                        └──────────────────────────┘
                                      │
                                      ▼
                        ┌──────────────────────────┐
                        │  Response Assembly       │
                        │  - Generated answer      │
                        │  - Source citations      │
                        │  - Confidence scores     │
                        └──────────────────────────┘
                                      │
                                      ▼
                        ┌──────────────────────────┐
                        │  Audit Logging           │
                        │  - CloudWatch Logs       │
                        │  - User + Query + Docs   │
                        │  - Timestamp + Response  │
                        └──────────────────────────┘
                                      │
                                      ▼
                        ┌──────────────────────────┐
                        │  Return to User          │
                        │  - JSON Response         │
                        │  - WebSocket (streaming) │
                        └──────────────────────────┘
```

---

## 2. TECHNOLOGY STACK

### **Cloud Provider: AWS** (Cost-effective, mature services, US region compliance)

### **Core Services:**

#### **Document Processing**
- **AWS Textract**: Scanned PDF/image text extraction only
- **PyPDF2**: Text-based PDF parsing (faster, cheaper)
- **Unstructured.io Library**: Word, PowerPoint, Excel parsing (handles complex formatting)
- **Amazon SNS**: Event notifications
- **Amazon SQS**: Queuing with DLQ for failed documents
- **AWS Step Functions**: Processing orchestration and error handling

#### **Vector Database**
- **Pinecone Standard** (Pod-based, p1.x1)
  - Why: Consistent sub-100ms latency required for 500 users
  - $70/month for 1M vectors (5M with compression)
  - Metadata filtering for permission-aware search
  - Namespaces for department/team isolation
  - Note: pgvector on db.r6g.large would work but requires db.r6g.xlarge ($500/mo) for acceptable performance

#### **LLM Provider**
- **OpenAI GPT-4o-mini**: $0.15/1M input tokens, $0.60/1M output tokens
  - Cost-effective for RAG workloads
  - Streaming responses for better UX
- **Embeddings**: Amazon Titan Text Embeddings V2 ($0.0001/1K tokens)
  - 1024 dimensions
  - 95% cost savings vs OpenAI ($400 vs $8,000 for initial load)
  - AWS-native, lower latency
  - Fallback: OpenAI text-embedding-3-small if quality issues

#### **Backend Services**
- **AWS Lambda**: Document processing (15min timeout)
- **Amazon ECS Fargate**: API layer (always-warm, no cold starts)
  - 2 tasks × 0.5 vCPU × 1GB RAM
  - Application Load Balancer
- **Amazon API Gateway**: WebSocket support for streaming responses
- **AWS Step Functions**: Document processing orchestration ($25/month)

#### **Storage**
- **Amazon S3**: Document storage (Intelligent-Tiering from Day 1, versioning enabled)
- **Amazon RDS PostgreSQL**: Metadata, permissions, audit logs
  - db.r6g.large Multi-AZ (production)
  - 2 read replicas for query offloading
  - RDS Proxy for connection pooling
- **Amazon ElastiCache (Redis)**:
  - cache.r6g.large cluster mode (3 shards)
  - Query result caching (1hr TTL)
  - Permission caching (15min TTL)
  - Session management

#### **Frontend**
- **Web App**: React + TypeScript
  - Hosted on S3 + CloudFront CDN
  - Material-UI or Ant Design for components
- **Mobile**: React Native (shared codebase)
  - iOS + Android deployment

#### **Authentication & Security**
- **AWS Cognito**: User authentication and management
- **SAML 2.0 Integration**: SSO with existing corporate identity provider
- **AWS IAM**: Service-level permissions
- **AWS KMS**: Encryption key management

#### **Monitoring & Logging**
- **AWS CloudWatch**: Logs, metrics, alarms
  - Cost Anomaly Detection
  - Billing alarms at $5K, $6.5K, $8K
- **AWS X-Ray**: Distributed tracing for Lambda and Fargate
- **AWS CloudTrail**: AWS API audit logging
- **Custom Dashboards**:
  - Query latency (p50, p95, p99)
  - Cache hit rate
  - Cost per query
  - Document processing status
  - Error rates by component

---

## 3. SECURITY ARCHITECTURE DIAGRAM

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              USER LAYER                                      │
└─────────────────────────────────────────────────────────────────────────────┘
                                      │
                        ┌─────────────┴─────────────┐
                        ▼                           ▼
              ┌──────────────────┐        ┌──────────────────┐
              │   Web Browser    │        │  Mobile App      │
              │   (HTTPS Only)   │        │  (TLS 1.3)       │
              └──────────────────┘        └──────────────────┘
                        │                           │
                        └─────────────┬─────────────┘
                                      ▼
                        ┌──────────────────────────┐
                        │   CloudFront CDN         │
                        │   - WAF enabled          │
                        │   - DDoS protection      │
                        │   - TLS 1.2+ only        │
                        └──────────────────────────┘
                                      │
┌─────────────────────────────────────────────────────────────────────────────┐
│                      AUTHENTICATION LAYER                                    │
└─────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
                        ┌──────────────────────────┐
                        │   AWS Cognito            │
                        │   - SAML 2.0 federation  │
                        │   - MFA support          │
                        │   - JWT token issuance   │
                        └──────────────────────────┘
                                      │
                        ┌─────────────┴─────────────┐
                        ▼                           ▼
              ┌──────────────────┐        ┌──────────────────┐
              │  Corporate SSO   │        │  Backup: Email/  │
              │  (SAML IdP)      │        │  Password + MFA  │
              └──────────────────┘        └──────────────────┘
                                      │
┌─────────────────────────────────────────────────────────────────────────────┐
│                      AUTHORIZATION LAYER                                     │
└─────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
                        ┌──────────────────────────┐
                        │   API Gateway            │
                        │   - JWT verification     │
                        │   - Rate limiting        │
                        │   - Request validation   │
                        └──────────────────────────┘
                                      │
                                      ▼
                        ┌──────────────────────────┐
                        │   Lambda Authorizer      │
                        │   - User role check      │
                        │   - Permission cache     │
                        │   - Token refresh        │
                        └──────────────────────────┘
                                      │
┌─────────────────────────────────────────────────────────────────────────────┐
│                      DATA ACCESS CONTROL                                     │
└─────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
                        ┌──────────────────────────┐
                        │  Document ACL Check      │
                        │  - User groups           │
                        │  - Department mapping    │
                        │  - Role-based access     │
                        │  - Document-level ACL    │
                        └──────────────────────────┘
                                      │
                ┌─────────────────────┼─────────────────────┐
                ▼                     ▼                     ▼
    ┌─────────────────┐   ┌─────────────────┐   ┌─────────────────┐
    │ RDS PostgreSQL  │   │ Vector Search   │   │  S3 Bucket      │
    │ - ACL table     │   │ - Filtered      │   │  - Bucket       │
    │ - User mapping  │   │   results       │   │    policies     │
    │ - Audit logs    │   │ - Metadata join │   │  - Encryption   │
    └─────────────────┘   └─────────────────┘   └─────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│                      ENCRYPTION & DATA PROTECTION                            │
└─────────────────────────────────────────────────────────────────────────────┘

    ┌───────────────────────────────────────────────────────────────┐
    │  Data in Transit                                              │
    │  - TLS 1.3 for all connections                                │
    │  - Certificate pinning (mobile)                               │
    │  - VPC endpoints for AWS services                             │
    └───────────────────────────────────────────────────────────────┘

    ┌───────────────────────────────────────────────────────────────┐
    │  Data at Rest                                                 │
    │  - S3: AES-256 encryption (SSE-KMS)                           │
    │  - RDS: Encryption enabled with KMS                           │
    │  - Pinecone: Encrypted at rest                                │
    │  - EBS volumes: Encrypted                                     │
    └───────────────────────────────────────────────────────────────┘

    ┌───────────────────────────────────────────────────────────────┐
    │  Key Management (AWS KMS)                                     │
    │  - Customer-managed keys                                      │
    │  - Automatic rotation (yearly)                                │
    │  - Separate keys per environment                              │
    └───────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│                      AUDIT & COMPLIANCE                                      │
└─────────────────────────────────────────────────────────────────────────────┘

    ┌───────────────────────────────────────────────────────────────┐
    │  Audit Logging (Immutable)                                    │
    │  - Every query logged with user ID, timestamp                 │
    │  - Documents accessed in each response                        │
    │  - Failed access attempts                                     │
    │  - Stored in CloudWatch Logs → S3 (WORM)                      │
    │  - Retention: 7 years                                         │
    └───────────────────────────────────────────────────────────────┘

    ┌───────────────────────────────────────────────────────────────┐
    │  Compliance                                                   │
    │  - Data residency: us-east-1 or us-west-2 only                │
    │  - No data leaves US regions                                  │
    │  - VPC isolation for sensitive services                       │
    │  - Regular security scans (AWS Inspector)                     │
    └───────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│                      NETWORK SECURITY                                        │
└─────────────────────────────────────────────────────────────────────────────┘

    ┌───────────────────────────────────────────────────────────────┐
    │  VPC Configuration                                            │
    │  - Private subnets for compute/database                       │
    │  - Public subnets for load balancers only                     │
    │  - NAT Gateway for outbound traffic                           │
    │  - VPC Flow Logs enabled                                      │
    └───────────────────────────────────────────────────────────────┘

    ┌───────────────────────────────────────────────────────────────┐
    │  Security Groups                                              │
    │  - Least privilege principle                                  │
    │  - Port 443 only for public access                            │
    │  - Internal services: specific port ranges                    │
    │  - Database: accessible from Lambda SG only                   │
    └───────────────────────────────────────────────────────────────┘

    ┌───────────────────────────────────────────────────────────────┐
    │  WAF Rules                                                    │
    │  - Rate limiting (100 req/min per IP)                         │
    │  - SQL injection protection                                   │
    │  - XSS protection                                             │
    │  - Geo-blocking (US only)                                     │
    └───────────────────────────────────────────────────────────────┘
```

### **Permission Model Implementation**

```
Document ACL Structure (PostgreSQL):
┌──────────────────────────────────────────────────────────────┐
│ documents                                                    │
├──────────────────────────────────────────────────────────────┤
│ id (UUID)                                                    │
│ s3_key (TEXT)                                                │
│ title (TEXT)                                                 │
│ uploaded_at (TIMESTAMP)                                      │
│ uploaded_by (UUID) → users.id                                │
│ department (TEXT)                                            │
│ classification (public/internal/confidential/restricted)     │
└──────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────┐
│ document_permissions                                         │
├──────────────────────────────────────────────────────────────┤
│ document_id (UUID) → documents.id                            │
│ principal_type (user/group/department)                       │
│ principal_id (UUID/TEXT)                                     │
│ permission_level (read/write/admin)                          │
│ granted_at (TIMESTAMP)                                       │
│ granted_by (UUID) → users.id                                 │
└──────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────┐
│ users                                                        │
├──────────────────────────────────────────────────────────────┤
│ id (UUID)                                                    │
│ email (TEXT)                                                 │
│ cognito_sub (TEXT)                                           │
│ department (TEXT)                                            │
│ role (TEXT)                                                  │
│ groups (TEXT[])                                              │
└──────────────────────────────────────────────────────────────┘
```

---

## 4. SCALING STRATEGY

### **Horizontal Scaling**

#### **Compute Layer**
```
API Gateway → Lambda (Auto-scales)
├─ Concurrent executions: 1000 (reserved)
├─ Provisioned concurrency: 50 (warm instances)
├─ Memory: 1024MB per function
└─ Timeout: 30s for API, 15min for processing
```

**Peak Load Calculation:**
- 500 concurrent users
- Average 10 queries/user/hour = 5,000 queries/hour
- Peak: 3x average = 15,000 queries/hour (~4-5/second)
- Lambda can handle this easily with auto-scaling

#### **Database Layer**
```
RDS PostgreSQL
├─ Instance: db.t3.large (2 vCPU, 8GB RAM)
├─ Multi-AZ for HA (99.95% uptime)
├─ Read Replicas: 2 (for query offloading)
├─ Connection pooling via RDS Proxy
└─ Auto-scaling storage: 100GB → 1TB

ElastiCache Redis
├─ Node type: cache.r6g.large (2 vCPU, 13.07GB)
├─ Cluster mode: Enabled (3 shards)
├─ Replicas: 1 per shard
└─ Cache TTL: 1 hour for query results
```

#### **Vector Database**
```
Pinecone Serverless
├─ Auto-scales based on query load
├─ No provisioning needed
├─ Pay per request
└─ Handles millions of queries/second
```

### **Vertical Scaling**

#### **Document Growth Strategy**
```
Year 1: 100K documents → ~2M vector chunks
Year 2: 120K documents → ~2.4M chunks
Year 5: 180K documents → ~3.6M chunks

Pinecone scaling:
├─ Serverless tier handles up to 10M vectors
├─ If exceeding: Upgrade to Pod-based ($70 → $150/month)
└─ Namespace partitioning for logical separation
```

#### **Storage Scaling**
```
S3 Intelligent-Tiering
├─ Frequent access (< 30 days): Standard
├─ Infrequent (30-90 days): IA
├─ Archive (> 90 days): Glacier Instant
└─ Estimated: 1TB total, $15-20/month
```

### **Performance Optimization**

#### **Caching Strategy**
```
3-Tier Cache:
1. CloudFront (Edge): Static assets, 24hr TTL
2. Redis (Application): Query results, 1hr TTL
3. Lambda (Function): Embedding model, connection pools

Cache Hit Rate Target: 60%
├─ Reduces LLM API calls by 60%
├─ Saves ~$2,000/month
└─ Sub-second response for cached queries
```

#### **Query Optimization**
```
1. Semantic Caching:
   - Hash query embeddings
   - If similar query (cosine > 0.95) → return cached

2. Result Re-ranking:
   - Initial: Retrieve top 20 from Pinecone
   - Filter: Apply permissions → ~10 results
   - Re-rank: Cross-encoder model → Top 5
   - Feed to LLM

3. Batch Processing:
   - Document ingestion: Batch embed (100 docs/request)
   - Saves 50% on embedding costs
```

### **High Availability**

```
Component               |  SLA    |  Strategy
─────────────────────────────────────────────────────────────
API Gateway            |  99.95% |  Multi-AZ by default
Lambda                 |  99.95% |  Multi-AZ by default
RDS PostgreSQL         |  99.95% |  Multi-AZ deployment
ElastiCache            |  99.99% |  Cluster mode + replicas
S3                     |  99.99% |  Built-in redundancy
Pinecone               |  99.9%  |  Managed service
CloudFront             |  99.99% |  Global edge network
─────────────────────────────────────────────────────────────
Overall System SLA     |  99.5%  |  ✓ Meets requirement
```

### **Disaster Recovery**

```
RTO (Recovery Time Objective): 4 hours
RPO (Recovery Point Objective): 1 hour

Backup Strategy:
├─ RDS: Automated snapshots (daily) + PITR (5min intervals)
├─ S3: Versioning enabled + Cross-region replication (optional)
├─ Pinecone: Backup to S3 (weekly full + daily incremental)
└─ Infrastructure: Terraform state in S3 with versioning

Failover:
├─ DNS: Route53 health checks + failover routing
├─ Database: Automatic failover to standby (< 2min)
└─ Compute: Lambda auto-deploys to healthy AZs
```

---

## 5. COST OPTIMIZATION STRATEGY

### **Monthly Cost Breakdown (Target: $8,000)**

```
SERVICE                          | MONTHLY COST  | NOTES & OPTIMIZATION
─────────────────────────────────────────────────────────────────────────────
COMPUTE
─────────────────────────────────────────────────────────────────────────────
Lambda (Processing Only)         | $200          | - Document processing only (not API)
  - 5M invocations/month         |               | - ARM64 (Graviton2) for 20% savings
  - 2GB-sec per invocation       |               | - 15min timeout for large docs
                                 |               |
ECS Fargate (API Layer)          | $65           | - Eliminates cold starts
  - 2 tasks × 0.5 vCPU × 1GB     |               | - Always warm, sub-100ms response
  - 24/7 uptime                  |               | - Behind Application Load Balancer
  - us-east-1 pricing            |               |
                                 |               |
Application Load Balancer        | $23           | - For Fargate tasks
  - 1 ALB                        |               | - Health checks, SSL termination
─────────────────────────────────────────────────────────────────────────────
DATABASE & CACHING
─────────────────────────────────────────────────────────────────────────────
RDS PostgreSQL                   | $450          | - db.r6g.large Multi-AZ (not t3!)
  - db.r6g.large Multi-AZ        |               | - Needed for vector performance
  - 2 vCPU, 16GB RAM             |               | - Reserved Instance: $315/month (30% off)
  - 100GB gp3 storage            |               | - 2 read replicas: +$450/month (prod only)
  - RDS Proxy: $15/month         |               |
                                 |               |
ElastiCache Redis                | $270          | - cache.r6g.large cluster (3 shards)
  - 3 shards × $90/month         |               | - Reserved Nodes: $175/month (35% off)
  - 1 replica per shard          |               |
─────────────────────────────────────────────────────────────────────────────
STORAGE
─────────────────────────────────────────────────────────────────────────────
S3 (Documents + Backups)         | $35           | - Intelligent-Tiering from Day 1
  - 1TB stored                   |               | - Versioning enabled
  - 2M PUT/GET requests          |               | - CloudFront reduces GET by 60%
─────────────────────────────────────────────────────────────────────────────
VECTOR DATABASE
─────────────────────────────────────────────────────────────────────────────
Pinecone Standard (p1.x1)        | $70           | - Pod-based for consistent latency
  - 1M vectors (100K docs)       |               | - Metadata filtering support
  - Unlimited queries            |               | - Sub-100ms query time
  - 1 pod in us-east-1           |               |
─────────────────────────────────────────────────────────────────────────────
AI/ML SERVICES
─────────────────────────────────────────────────────────────────────────────
OpenAI GPT-4o-mini               | $270          | CORRECTED CALCULATION:
  - 15K queries/month            |               | - Input: 15K × 2K tokens × $0.15/1M = $4.50
  - Avg 2K input tokens/query    |               | - Output: 15K × 500 tokens × $0.60/1M = $4.50
  - Avg 500 output tokens        |               | - Total: $9/day × 30 = $270/month
  - 60% cache hit rate           |               | - With cache: $108/month (saves $162)
                                 |               |
Amazon Titan Embeddings          | $400          | INITIAL LOAD (Month 1-3 ONLY):
  - INITIAL: 100K docs           |               | - 100K docs × 4K tokens = 400M tokens
  - 4K tokens/doc avg            |               | - Cost: 400M × $0.0001/1K = $40 ONE-TIME
  - Total: 400M tokens           |               | - Spread over 3 months: ~$14/month
                                 |               |
  - ONGOING: 500 docs/month      |               | ONGOING (Month 4+):
  - 2M tokens/month              |               | - 500 new docs × 4K tokens = 2M tokens
                                 |               | - Cost: 2M × $0.0001/1K = $0.20/month
                                 |               |
                                 |               | NOTE: Amazon Titan is 200x cheaper than
                                 |               | OpenAI ($40 vs $8,000 for initial load!)
─────────────────────────────────────────────────────────────────────────────
DOCUMENT PROCESSING
─────────────────────────────────────────────────────────────────────────────
AWS Textract                     | $50           | - OCR scanned PDFs only (~10% of docs)
  - 1,000 pages/month (ongoing)  |               | - Check for text layer first (saves 90%)
  - $1.50 per 1K pages           |               | - Initial bulk: $150 one-time
                                 |               |
Step Functions                   | $25           | - Orchestrate doc processing pipeline
  - 100K state transitions       |               | - Error handling & retries
                                 |               |
SNS + SQS                        | $5            | - Event notifications + queuing
  - 1M SNS publishes             |               | - DLQ for failed documents
  - 1M SQS messages              |               |
─────────────────────────────────────────────────────────────────────────────
NETWORKING & CDN
─────────────────────────────────────────────────────────────────────────────
CloudFront                       | $50           | - Free tier covers first 1TB
  - 5TB data transfer            |               | - gzip compression enabled
  - 10M requests                 |               | - 24hr cache for static assets
                                 |               |
API Gateway (WebSocket)          | $30           | - Streaming responses only
  - 1M messages/month            |               | - REST API via ALB (cheaper)
  - WebSocket connections        |               |
─────────────────────────────────────────────────────────────────────────────
SECURITY & MONITORING
─────────────────────────────────────────────────────────────────────────────
AWS Cognito                      | $0            | - Free tier: 50K MAU (500 users fits)
  - 500 active users             |               | - MFA via TOTP (free)
                                 |               |
CloudWatch Logs & Metrics        | $120          | - 50GB logs/month ($0.50/GB)
  - Logs, custom metrics         |               | - 30-day retention in CloudWatch
  - Custom dashboards            |               | - Archive to S3 for 7-year retention
                                 |               |
AWS WAF                          | $80           | - $5 base + $1/rule + $0.60/1M requests
  - 5 rules                      |               | - Rate limiting, SQL injection, XSS
  - 10M requests                 |               |
                                 |               |
AWS X-Ray                        | $15           | - Distributed tracing
  - 1M traces/month              |               | - Debug performance issues
─────────────────────────────────────────────────────────────────────────────
OTHER
─────────────────────────────────────────────────────────────────────────────
NAT Gateway                      | $35           | - $0.045/hour + $0.045/GB
  - 1 NAT in each AZ (2 total)   |               | - Use VPC endpoints where possible
Data Transfer                    | $30           | - Inter-AZ + outbound traffic
VPC Endpoints                    | $15           | - S3, DynamoDB (reduce NAT costs)
KMS                              | $5            | - 1 customer-managed key
Route53                          | $10           | - Hosted zone + health checks
AWS Inspector                    | $10           | - Monthly security scans
─────────────────────────────────────────────────────────────────────────────
PRODUCTION TOTAL                 | $2,266/month  | Without reserved instances
WITH RESERVED INSTANCES          | $1,891/month  | RDS + Redis 1-year RI (save $375/mo)
─────────────────────────────────────────────────────────────────────────────
INITIAL LOAD SPIKE (Months 1-3) | +$180/month   | Embedding 100K docs over 3 months
                                 |               | ($40 one-time ÷ 3 months = $13/mo)
                                 |               | Textract bulk: $150 one-time
                                 |               | Total spike: ~$50/month extra for 3 months
─────────────────────────────────────────────────────────────────────────────
MONTH 1-3 TOTAL                  | $1,941/month  | Includes initial doc processing
MONTH 4+ TOTAL (OPTIMIZED)       | $1,891/month  | Steady state with reserved instances
─────────────────────────────────────────────────────────────────────────────
BUDGET REMAINING                 | $6,109/month  | 76% under budget - room for growth!
─────────────────────────────────────────────────────────────────────────────

**KEY COST OPTIMIZATIONS:**
1. Amazon Titan Embeddings selected over OpenAI (200x cost reduction for initial indexing)
2. ECS Fargate for API layer provides predictable costs vs Lambda with provisioned concurrency
3. Intelligent caching strategy reduces LLM API costs by 60%
4. Reserved instances for RDS and ElastiCache provide 30-35% savings
5. Total monthly operational cost: $1,891 (well within budget constraints)
─────────────────────────────────────────────────────────────────────────────
```

### **Development Environment Cost Strategy**

```
DEVELOPMENT/STAGING COSTS:
─────────────────────────────────────────────────────────────────────────────
Strategy: Share infrastructure, use smaller instances

Dev Environment:
├─ Lambda: Same code, separate namespace         | Free (within limits)
├─ RDS: db.t3.small (not Multi-AZ)               | $50/month
├─ Redis: cache.t3.micro                         | $15/month
├─ Pinecone: Separate index (starter tier)       | Free tier
├─ S3: Separate bucket                           | $5/month
├─ Cognito: Test user pool                       | Free
├─ OpenAI: Development API key (limited usage)   | $50/month
└─ Total Dev Cost                                | $120/month

CI/CD:
├─ GitHub Actions (2000 min/month free)          | Free
├─ CodePipeline + CodeBuild (minimal usage)      | $20/month
└─ Docker image storage (ECR)                    | $10/month

TOTAL DEVELOPMENT COST: $150/month
─────────────────────────────────────────────────────────────────────────────
```

### **Cost Reduction Tactics**

#### **1. Serverless-First Architecture**
- No idle compute costs
- Pay only for actual usage
- Auto-scales to zero during low traffic

#### **2. Intelligent Caching**
```
Without Cache: 15K queries × $0.50/query = $7,500/month
With 60% Cache Hit: 6K queries × $0.50/query = $3,000/month
Savings: $4,500/month (pays for entire cache infrastructure)
```

#### **3. Reserved Instances** (1-year commitment)
```
RDS: $350 → $245/month (-30%)
ElastiCache: $200 → $130/month (-35%)
Total Savings: $175/month = $2,100/year
```

#### **4. Smart LLM Usage**
```
- Use GPT-4o-mini instead of GPT-4 (90% cheaper)
- Optimize prompts (reduce input tokens by 40%)
- Streaming responses (better UX, same cost)
- Fallback to cached responses when appropriate
```

#### **5. Document Processing Optimization**
```
- Check if PDF has text layer before OCR (90% do)
- Batch embed documents (100 at a time)
- Process during off-peak hours (no SLA for ingestion)
- One-time cost spike, then $50/month ongoing
```

#### **6. Alternative: Self-Hosted Vector DB**
```
Option A: Pinecone Serverless ($150/month)
Option B: pgvector on existing RDS ($0/month)

Trade-off:
├─ pgvector: Slower queries (200ms vs 50ms), but free
├─ Decision: Start with pgvector, migrate to Pinecone if needed
└─ Potential Savings: $150/month = $1,800/year
```

### **Cost Monitoring & Alerts**

```
CloudWatch Billing Alarms:
├─ Alert at $5,000/month (62% of budget)
├─ Alert at $6,500/month (81% of budget)
├─ Alert at $8,000/month (100% of budget)
└─ Daily cost tracking dashboard

AWS Cost Explorer:
├─ Tag resources by component
├─ Track cost per user (should be < $16/user/month)
└─ Forecast next month spend
```

---

## 6. IMPLEMENTATION PHASES

### **Phase 1: MVP (Months 1-3)**

**Objective:** Deliver functional RAG system for internal beta testing

**Scope:** 50 beta users, 5,000 documents indexed

**Timeline:** 12-14 weeks

#### **Weeks 1-3: Infrastructure & Core Setup**
- [ ] AWS account, VPC, security groups, IAM roles
- [ ] RDS PostgreSQL db.t3.medium (not r6g yet) + pgvector extension
- [ ] S3 buckets with versioning and lifecycle policies
- [ ] Cognito user pool + SAML integration testing with corporate IdP
- [ ] Basic Lambda functions for doc processing (boilerplate)
- [ ] SNS topics, SQS queues, DLQ setup
- [ ] CloudWatch logging and basic alarms

#### **Weeks 4-6: Document Ingestion Pipeline**
- [ ] S3 event → SNS → SQS → Lambda architecture
- [ ] PDF parsing: PyPDF2 for text PDFs, fallback to Textract
- [ ] Word/PPT parsing with Unstructured.io library
- [ ] Step Functions workflow for orchestration
- [ ] Error handling, retry logic, DLQ monitoring
- [ ] Intelligent chunking with LangChain (semantic boundaries)
- [ ] Amazon Titan embedding generation (batch: 25 docs at a time)
- [ ] Metadata extraction (author, date, department, permissions)
- [ ] Store vectors in pgvector, metadata in PostgreSQL

#### **Weeks 7-9: Query & Retrieval System**
- [ ] ECS Fargate setup for API layer (2 tasks behind ALB)
- [ ] Query embedding with Amazon Titan
- [ ] pgvector similarity search with permission filtering
- [ ] Context assembly (top 5-8 chunks with source metadata)
- [ ] GPT-4o-mini integration with retry logic
- [ ] Response formatting with citations
- [ ] Basic Redis caching (query results, 1hr TTL)
- [ ] API rate limiting and authentication middleware

#### **Weeks 10-12: Frontend & Security**
- [ ] React + TypeScript web app (Vite for faster builds)
- [ ] Chat interface with streaming responses (Server-Sent Events)
- [ ] Cognito authentication integration
- [ ] Source citation display with clickable document links
- [ ] Basic error handling and loading states
- [ ] Deploy to S3 + CloudFront with HTTPS
- [ ] WAF basic rules (rate limiting, geo-blocking)
- [ ] Audit logging to CloudWatch

#### **Weeks 13-14: Testing & Beta Launch**
- [ ] Load testing with 50 concurrent users (JMeter/Locust)
- [ ] Security testing (OWASP Top 10 checks)
- [ ] User acceptance testing with 10 internal users
- [ ] Documentation (user guide, admin guide)
- [ ] Bug fixes and performance tuning
- [ ] Beta launch to 50 employees

**Phase 1 Success Criteria:**
- Functional web application with authentication and chat interface
- 5,000 documents successfully indexed and searchable
- Department-level access controls implemented
- Real-time document indexing via S3 event triggers
- Audit logging infrastructure operational
- Performance: p95 query latency < 3 seconds

**Infrastructure:** pgvector on RDS PostgreSQL, Fargate for API layer
**Estimated Monthly Cost:** $800

---

### **Phase 2: Production Scale (Months 4-6)**

**Objective:** Production-ready system with enhanced security and scalability

**Scope:** 200 users, 50,000 documents, document-level permissions

**Timeline:** 12 weeks

#### **Weeks 15-17: Security Hardening**
- [ ] Implement document-level ACLs in PostgreSQL
- [ ] Row-level security (RLS) policies
- [ ] Permission caching in Redis (15min TTL)
- [ ] Enhanced WAF rules (SQL injection, XSS protection)
- [ ] Enable MFA requirement for all users
- [ ] Comprehensive audit logging (CloudWatch → S3 archive)
- [ ] KMS customer-managed keys for encryption
- [ ] VPC endpoints (S3, DynamoDB) to reduce NAT costs
- [ ] Security assessment with AWS Inspector

#### **Weeks 18-20: Scaling Infrastructure**
- [ ] Upgrade RDS to db.r6g.large Multi-AZ
- [ ] Deploy RDS read replicas (2x) for query offloading
- [ ] Expand ElastiCache to 3-shard cluster
- [ ] RDS Proxy for connection pooling
- [ ] Evaluate pgvector performance (if slow, migrate to Pinecone)
- [ ] Increase Fargate task count to 4 for redundancy
- [ ] Implement auto-scaling policies for Fargate
- [ ] CloudFront optimization (cache headers, compression)

#### **Weeks 21-23: Advanced Features**
- [ ] Bulk document upload UI (drag & drop, batch processing)
- [ ] Advanced search filters (date, author, department, type)
- [ ] Conversation history tracking (last 10 queries per user)
- [ ] "Similar documents" feature using vector similarity
- [ ] Export query results to PDF/CSV
- [ ] Document versioning support (track updates)
- [ ] Admin dashboard for system monitoring
- [ ] Usage analytics (queries/day, popular topics)

#### **Weeks 24-26: Load Testing & Production Launch**
- [ ] Load test with 200 concurrent users (target p95 < 2s)
- [ ] Stress test at 2x expected load (400 users)
- [ ] Chaos engineering (simulate service failures)
- [ ] Disaster recovery drill (restore from backup)
- [ ] Performance tuning based on test results
- [ ] User training (3 sessions, 50 users each)
- [ ] Create runbooks for common incidents
- [ ] Phased rollout to 200 employees
- [ ] Index remaining documents (5K → 50K over 4 weeks)

**Phase 2 Success Criteria:**
- System supports 200 concurrent users
- 50,000 documents indexed with full-text search
- Document-level permissions with row-level security
- 99.5% uptime SLA achieved
- Mobile-responsive Progressive Web App
- Comprehensive monitoring with custom dashboards
- Performance: p95 query latency < 2 seconds

**Infrastructure:** db.r6g.large Multi-AZ, ElastiCache cluster, optional Pinecone migration
**Estimated Monthly Cost:** $1,400

---

### **Phase 3: Full Deployment & Mobile (Months 7-10)**

**Objective:** Complete system rollout with native mobile applications

**Scope:** 500 users, 100,000 documents, iOS/Android apps

**Timeline:** 16 weeks

#### **Weeks 27-30: Scale to Full Capacity**
- [ ] Index remaining 50K documents (staggered over 4 weeks)
- [ ] Onboard remaining 300 employees (phased rollout)
- [ ] Monitor performance degradation, tune as needed
- [ ] Potentially add RDS read replica #3 if needed
- [ ] Optimize vector search (experiment with index parameters)
- [ ] Implement query result pagination for large result sets
- [ ] Add rate limiting per user (prevent abuse)

#### **Weeks 31-38: Mobile App Development**
- [ ] React Native app setup (shared codebase)
- [ ] iOS app development (authentication, chat UI, citations)
- [ ] Android app development (same features)
- [ ] Offline mode (cache last 20 queries + responses)
- [ ] Push notifications via SNS (new doc alerts, query responses)
- [ ] Biometric authentication (Face ID, fingerprint)
- [ ] App testing on multiple devices
- [ ] App Store submission (iOS) - 2 week review
- [ ] Play Store submission (Android) - 1 week review

**Note:** Mobile app development timeline includes iOS/Android implementation, testing, and app store submission/approval process.

#### **Weeks 39-42: Analytics & AI Improvements**
- [ ] Admin analytics dashboard (QuickSight or custom)
- [ ] Usage metrics (queries/day, active users, popular docs)
- [ ] Document usage heatmap (which docs are most referenced)
- [ ] Query quality metrics (user ratings, click-through rate)
- [ ] Cost tracking dashboard (cost per query, monthly trends)
- [ ] Experiment with hybrid search (BM25 + vector)
- [ ] Query spell-check and autocomplete
- [ ] Multi-turn conversation support (remember context)
- [ ] Confidence scoring for answers

**Phase 3 Success Criteria:**
- Full user base of 500 employees onboarded
- Complete document corpus (100,000 documents) indexed
- Native iOS and Android applications published to app stores
- Administrative analytics dashboard operational
- Hybrid search (BM25 + vector) implemented
- Performance: p95 query latency < 1.5 seconds at full scale
- System stability metrics: 99.5%+ uptime maintained

**Infrastructure:** Full production environment with auto-scaling
**Estimated Monthly Cost:** $1,900

---

### **Phase 4: Future Enhancements (Month 11+) - Ongoing**

#### **Advanced Features (Prioritized by user feedback)**
- [ ] Multi-language support (Spanish, etc.)
- [ ] Document summarization
- [ ] Automatic document tagging/classification
- [ ] Integration with email (query via email)
- [ ] Slack/Teams bot integration
- [ ] Voice queries (speech-to-text)
- [ ] Collaborative features (share queries, annotate)
- [ ] Custom collections (save document sets)
- [ ] Scheduled reports (weekly insights)

#### **AI/ML Improvements**
- [ ] Fine-tuned LLM (company-specific language)
- [ ] Active learning (improve from user feedback)
- [ ] Confidence scoring (flag uncertain answers)
- [ ] Multi-hop reasoning (complex queries)
- [ ] Graph RAG (entity relationships)

#### **Enterprise Features**
- [ ] SSO with multiple IdPs
- [ ] Advanced compliance (HIPAA, SOC 2)
- [ ] Custom retention policies
- [ ] White-labeling options
- [ ] API for third-party integrations

---

## SUMMARY

### **Key Technical Decisions**

1. **Cloud Provider:** AWS (comprehensive service offerings, US data residency compliance)
2. **Vector Database:** pgvector for MVP, evaluate Pinecone migration based on performance requirements
3. **LLM:** OpenAI GPT-4o-mini (optimal cost-to-performance ratio for RAG applications)
4. **Embeddings:** Amazon Titan Text Embeddings V2 (cost-effective, AWS-native)
5. **Architecture Pattern:** Event-driven serverless with managed containers for API layer
6. **Security Model:** Defense-in-depth with WAF, Cognito SSO, document-level ACLs, encryption at rest and in transit

### **Cost Summary**
- **Phase 1 (MVP):** $800/month
- **Phase 2 (Production Scale):** $1,400/month
- **Phase 3 (Full Deployment):** $1,900/month
- **Steady State (with 1-year Reserved Instances):** $1,891/month
- **Budget Headroom:** $6,109/month available for additional features and scaling

### **Project Timeline**
- **Month 3:** Beta release (50 users, 5,000 documents)
- **Month 6:** Production release (200 users, 50,000 documents)
- **Month 10:** Full deployment (500 users, 100,000 documents) with mobile apps
- **Month 12+:** Enhanced features and continuous improvement

**Total Implementation Duration:** 10 months to complete deployment

### **Risk Mitigation**
- **Performance:** Load testing before each phase
- **Cost:** Weekly cost monitoring, automatic alerts
- **Security:** Quarterly penetration testing
- **Availability:** Multi-AZ deployments, automated backups

## ARCHITECTURE REVIEW NOTES

### **Design Principles**
- **Scalability:** Event-driven architecture supports horizontal scaling as document corpus and user base grow
- **Reliability:** Multi-AZ deployments and managed services ensure high availability (99.5% SLA)
- **Security:** Multi-layer security controls with audit logging for compliance requirements
- **Cost Efficiency:** Serverless and managed services minimize operational overhead while staying well within budget
- **Performance:** Sub-2 second p95 response times through intelligent caching and optimized query paths

### **Technical Risk Mitigation**
- **Vector Database Performance:** Start with pgvector, migration path to Pinecone documented if needed
- **Cold Start Latency:** ECS Fargate for API layer eliminates Lambda cold start issues
- **Document Processing Failures:** SQS + DLQ architecture ensures reliable processing with retry mechanisms
- **Cost Overruns:** Reserved instances and caching strategies provide predictable monthly costs
- **Data Privacy:** US-only regions, encryption at rest/transit, document-level ACLs enforced

### **Monitoring & Observability**
- CloudWatch dashboards for query latency (p50, p95, p99)
- Custom metrics for cache hit rates and cost per query
- X-Ray distributed tracing for performance debugging
- Cost anomaly detection with automated alerts
- Audit logging for compliance and security analysis

This architecture provides a production-ready RAG system with phased implementation, staying within budget constraints while meeting all technical and security requirements.