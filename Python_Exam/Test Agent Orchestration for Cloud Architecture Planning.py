# Agent Orchestration for Cloud Architecture Planning
# Format: Problem statement + Written response

"""
AGENT ORCHESTRATION CHALLENGE

You need to design a multi-agent system that can analyze business problems and recommend 
cloud architecture solutions. Focus on the orchestration strategy, not implementation details.

SAMPLE SCENARIOS (choose 2 to address):

1. "Simple E-commerce Site"
   - Online store for small business (1000 daily users)
   - Product catalog, shopping cart, payment processing
   - Basic admin dashboard for inventory management

2. "Customer Support Chatbot"
   - AI chatbot for customer service 
   - Integration with existing CRM system
   - Handle 500+ conversations per day
   - Escalate complex issues to human agents

3. "Employee Expense Tracker"
   - Mobile app for expense reporting
   - Receipt photo upload and processing
   - Approval workflow for managers
   - Integration with payroll system

YOUR TASK:
Design an agent orchestration approach that can take these problems and output 
a cloud architecture recommendation including basic services needed (database, 
API gateway, compute, storage, etc.).
"""

# Your Code Here

# This is a design/architecture challenge focused on orchestration strategy
# The implementation would be a multi-agent system that analyzes business problems
# and recommends cloud architecture solutions

# Example orchestration flow pseudocode:
"""
def orchestrate_architecture_planning(problem_statement):
    # Step 1: Requirements Analyst processes input
    requirements = requirements_agent.analyze(problem_statement)

    # Step 2: Load Estimator calculates traffic and data needs
    load_profile = load_estimator_agent.estimate(requirements)

    # Step 3: Architecture Designer proposes services
    architecture = architecture_agent.design(requirements, load_profile)

    # Step 4: Cost Optimizer reviews and optimizes
    optimized_arch = cost_optimizer_agent.optimize(architecture)

    # Step 5: Validator ensures completeness
    final_recommendation = validator_agent.validate(optimized_arch)

    return final_recommendation
"""

# ADDRESSING TWO SCENARIOS AS REQUIRED
# Scenario 1: Customer Support Chatbot (detailed in Q2 & Q3)
# Scenario 2: E-commerce Site (brief overview below)

ECOMMERCE_SCENARIO_BRIEF = """
E-COMMERCE SITE ARCHITECTURE (Brief Overview):

Requirements Analysis:
- 1000 daily users, product catalog, shopping cart, payment, inventory management
- Peak traffic during sales events, PCI-DSS compliance required

Recommended Architecture:
- Compute: Lambda for APIs, ECS for admin dashboard
- Database: RDS PostgreSQL (product catalog), DynamoDB (shopping cart sessions)
- Storage: S3 for product images, CloudFront CDN
- Payment: Stripe/PayPal integration via API Gateway
- Security: WAF, Cognito for admin auth, SSL/TLS
- Cost: ~$150-200/month

Key Differences from Chatbot:
- More database-intensive (product catalog, inventory)
- Requires PCI-DSS compliance (payment processing)
- Read-heavy workload (browsing) with burst writes (checkouts)
- CDN critical for product images performance
"""

# === WRITTEN RESPONSE QUESTIONS ===

"""
QUESTION 1: AGENT DESIGN (20 points)
What agents would you create for this orchestration? Describe:
- 3-5 specific agents and their roles
- How they would collaborate on the sample problems
- What each agent's input and output would be

Example format:
Agent Name: Requirements Analyst
Role: Break down business requirements into technical needs
Input: Problem description + business context
Output: List of functional requirements, expected load, compliance needs

QUESTION 2: ORCHESTRATION WORKFLOW (25 points)
For ONE of the sample scenarios, walk through your complete workflow:
- Step-by-step process from problem statement to final recommendation
- How agents hand off information to each other
- What happens if an agent fails or produces unclear output
- How you ensure the final solution is complete and feasible

QUESTION 3: CLOUD RESOURCE MAPPING (20 points)
For your chosen scenario, what basic cloud services would your system recommend?
- Compute (serverless functions, containers, VMs)
- Storage (databases, file storage, caching)
- Networking (API gateways, load balancers, CDN)
- Security and monitoring basics
- Justify why each service fits the requirements

QUESTION 4: REUSABILITY & IMPROVEMENT (15 points)
How would you make this system work across different projects?
- What would you standardize vs. customize per project?
- How would the system learn from previous recommendations?
- What feedback mechanisms would improve future solutions?

QUESTION 5: PRACTICAL CONSIDERATIONS (20 points)
What challenges would you expect and how would you handle:
- Conflicting recommendations between agents
- Incomplete or vague problem statements
- Budget constraints not mentioned in requirements
- Integration with existing legacy systems
- Keeping up with new cloud services and pricing
"""

# ============================================================================
# QUESTION 1: AGENT DESIGN (20 points)
# ============================================================================

AGENT_DESIGN_ANSWER = """
I would design 5 specialized agents that work together in a pipeline:

1. Agent Name: Requirements Analyst Agent
   Role: Parse business problems into structured technical requirements
   Input:
   - Raw problem statement (text description)
   - Business context (industry, scale, constraints)
   Output:
   - Functional requirements (features needed)
   - Non-functional requirements (performance, security, compliance)
   - User personas and expected usage patterns
   - Integration points with existing systems

   Example for E-commerce:
   Input: "Online store for small business (1000 daily users), product catalog,
          shopping cart, payment processing, admin dashboard"
   Output: {
       "functional": ["product_catalog", "shopping_cart", "payment_processing",
                     "inventory_management", "admin_dashboard"],
       "non_functional": {"availability": "99.9%", "response_time": "<500ms"},
       "users": {"daily_active": 1000, "concurrent_peak": 150},
       "integrations": ["payment_gateway", "shipping_provider"]
   }

2. Agent Name: Load & Scale Estimator Agent
   Role: Calculate infrastructure capacity needs based on traffic patterns
   Input:
   - Requirements from Requirements Analyst
   - Usage patterns (daily users, peak hours, growth projections)
   Output:
   - Traffic estimates (requests/second, data volume)
   - Storage needs (database size, file storage)
   - Compute requirements (CPU, memory)
   - Scaling triggers and patterns

   Example for E-commerce:
   Input: 1000 daily users, product catalog
   Output: {
       "rps_average": 10,
       "rps_peak": 50,
       "database_size_gb": 5,
       "storage_gb": 100,
       "compute": "2 vCPU, 4GB RAM",
       "scaling_pattern": "predictable_daily_peaks"
   }

3. Agent Name: Cloud Architecture Designer Agent
   Role: Map requirements to specific cloud services and architecture patterns
   Input:
   - Structured requirements from Requirements Analyst
   - Load profile from Load Estimator
   - Cloud provider preference (AWS/Azure/GCP)
   Output:
   - Architecture diagram (JSON/YAML structure)
   - Service selections with justifications
   - Data flow and integration patterns
   - Deployment topology

   Example for E-commerce:
   Input: Requirements + load profile
   Output: {
       "compute": "AWS Lambda for APIs + ECS for admin dashboard",
       "database": "RDS PostgreSQL (t3.small)",
       "storage": "S3 for product images",
       "api_gateway": "AWS API Gateway",
       "pattern": "serverless_microservices"
   }

4. Agent Name: Cost Optimizer Agent
   Role: Analyze proposed architecture for cost efficiency and suggest optimizations
   Input:
   - Architecture design from Designer Agent
   - Budget constraints (if specified)
   - Usage patterns
   Output:
   - Cost estimate (monthly breakdown)
   - Optimization recommendations
   - Cost/performance trade-offs
   - Reserved capacity suggestions

   Example for E-commerce:
   Input: Proposed architecture
   Output: {
       "monthly_cost_usd": 250,
       "breakdown": {"compute": 80, "database": 100, "storage": 20, "networking": 50},
       "optimizations": ["Use S3 Intelligent-Tiering", "Reserved RDS instance saves 30%"],
       "cost_alerts": "Set budget alert at $300/month"
   }

5. Agent Name: Validation & Compliance Agent
   Role: Verify architecture completeness, security, and best practices
   Input:
   - Complete architecture from Cost Optimizer
   - Requirements (especially compliance needs)
   Output:
   - Validation report (completeness checklist)
   - Security recommendations
   - Compliance gaps (PCI-DSS, GDPR, HIPAA)
   - Best practice violations
   - Final approved architecture

   Example for E-commerce:
   Input: Complete architecture design
   Output: {
       "completeness": "PASS - all requirements covered",
       "security_issues": ["Enable RDS encryption", "Add WAF to API Gateway"],
       "compliance": {"PCI_DSS": "REQUIRED - payment processing present"},
       "recommendations": ["Add CloudWatch monitoring", "Implement backup strategy"],
       "status": "APPROVED_WITH_CHANGES"
   }

COLLABORATION PATTERN:
The agents work in a sequential pipeline with feedback loops:
1. Requirements Analyst → Load Estimator → Architecture Designer → Cost Optimizer → Validator
2. If Validator finds issues, feedback goes back to Architecture Designer
3. If Requirements are unclear, Requirements Analyst can request clarification
4. Cost Optimizer can negotiate with Architecture Designer for cheaper alternatives
5. All agents share a common context/memory store for coordination
"""

# ============================================================================
# QUESTION 2: ORCHESTRATION WORKFLOW (25 points)
# ============================================================================

ORCHESTRATION_WORKFLOW_ANSWER = """
SCENARIO CHOSEN: Customer Support Chatbot
(AI chatbot, 500+ conversations/day, CRM integration, human escalation)

STEP-BY-STEP ORCHESTRATION WORKFLOW:

Step 1: Requirements Analysis (Requirements Analyst Agent)
Input: "AI chatbot for customer service, integrate with CRM, handle 500+ conversations
       per day, escalate complex issues to human agents"

Process:
- Parse problem statement using NLP
- Identify key components: chatbot UI, NLP engine, CRM integration, escalation logic
- Extract constraints: 500+ daily conversations, real-time response needed
- Infer unstated needs: conversation history, analytics, multi-channel support

Output: {
    "functional_requirements": [
        "natural_language_processing",
        "conversation_management",
        "crm_integration",
        "escalation_workflow",
        "conversation_history_storage",
        "analytics_dashboard"
    ],
    "non_functional": {
        "response_time": "<2s",
        "availability": "99.95%",
        "concurrent_conversations": 50
    },
    "integrations": {
        "crm_system": "salesforce_or_hubspot",
        "channels": ["web_widget", "mobile_app"]
    },
    "estimated_load": {
        "daily_conversations": 500,
        "avg_messages_per_conversation": 8,
        "peak_concurrent": 50
    }
}

Handoff: Pass structured requirements to Load Estimator Agent

---

Step 2: Load & Scale Estimation (Load Estimator Agent)
Input: Requirements object from Step 1

Process:
- Calculate API calls: 500 conversations × 8 messages = 4000 messages/day
- Estimate storage: 4000 messages × 365 days × 1KB = ~1.5GB/year
- Determine concurrent capacity: 50 simultaneous conversations
- Identify scaling needs: NLP processing is compute-intensive

Output: {
    "traffic_profile": {
        "messages_per_second_avg": 0.05,
        "messages_per_second_peak": 2,
        "api_calls_daily": 4000,
        "data_volume_daily_mb": 4
    },
    "storage_requirements": {
        "conversation_history_gb": 2,
        "analytics_data_gb": 1,
        "growth_rate": "1.5GB/year"
    },
    "compute_requirements": {
        "nlp_processing": "GPU_optional_for_advanced_models",
        "api_backend": "2_vCPU_4GB_RAM",
        "concurrent_connections": 50
    },
    "scaling_pattern": "moderate_predictable_business_hours"
}

Handoff: Pass requirements + load profile to Architecture Designer Agent

---

Step 3: Cloud Architecture Design (Architecture Designer Agent)
Input: Requirements + load profile from previous agents

Process:
- Map chatbot → AWS Lex or Dialogflow or custom NLP with Lambda
- Map conversation storage → DynamoDB (NoSQL for flexibility)
- Map CRM integration → API Gateway + integration layer
- Map escalation → SNS notifications + Queue system
- Map analytics → CloudWatch + QuickSight

Output: {
    "architecture": {
        "compute": {
            "chatbot_nlp": "AWS Lex (managed NLP service)",
            "api_backend": "Lambda functions (serverless)",
            "integration_layer": "ECS Fargate containers (for CRM webhooks)"
        },
        "storage": {
            "conversation_db": "DynamoDB (on-demand pricing)",
            "crm_cache": "ElastiCache Redis (session management)"
        },
        "integration": {
            "api_gateway": "AWS API Gateway (REST + WebSocket)",
            "crm_connector": "AWS AppFlow (Salesforce integration)",
            "event_bus": "EventBridge (for escalations)"
        },
        "ai_ml": {
            "nlp_service": "AWS Lex",
            "sentiment_analysis": "AWS Comprehend",
            "custom_model": "SageMaker (optional for advanced scenarios)"
        },
        "monitoring": {
            "logs": "CloudWatch Logs",
            "metrics": "CloudWatch Metrics",
            "analytics": "QuickSight dashboards"
        }
    },
    "data_flow": [
        "User → Web/Mobile → API Gateway (WebSocket) → Lambda → Lex",
        "Lex → Lambda → DynamoDB (store conversation)",
        "Lambda → AppFlow → Salesforce CRM (sync customer data)",
        "Lambda → EventBridge → SNS → Human Agent (escalation)"
    ],
    "justifications": {
        "lex": "Managed NLP reduces development time, built-in conversation flow",
        "lambda": "Serverless scales automatically, pay per request",
        "dynamodb": "Flexible schema for conversation history, fast reads",
        "appflow": "Native Salesforce integration without custom code"
    }
}

Handoff: Pass complete architecture to Cost Optimizer Agent

---

Step 4: Cost Optimization (Cost Optimizer Agent)
Input: Architecture design from Step 3

Process:
- Calculate Lex pricing: 500 conversations × $0.004 = $2/day = $60/month
- Calculate Lambda: 4000 invocations × 2s × $0.0000166667 = $0.13/day = $4/month
- Calculate DynamoDB: 2GB storage + on-demand requests = $3/month
- Calculate API Gateway: 4000 requests = $0.01/month
- Total monthly cost ≈ $70-100/month
- Identify savings: Use DynamoDB on-demand vs provisioned

Output: {
    "cost_estimate": {
        "monthly_total_usd": 85,
        "breakdown": {
            "lex": 60,
            "lambda": 4,
            "dynamodb": 3,
            "api_gateway": 1,
            "elasticache": 10,
            "monitoring": 5,
            "data_transfer": 2
        }
    },
    "optimizations": [
        "Use DynamoDB on-demand (cheaper for low traffic)",
        "Consider Lex automated chatbot (cheaper than custom Lambda)",
        "Enable CloudWatch log retention limit (7 days) to reduce costs",
        "Use S3 for conversation archive (move old data from DynamoDB)"
    ],
    "cost_projections": {
        "current_load": 85,
        "2x_growth": 150,
        "5x_growth": 350
    },
    "budget_alerts": "Set alert at $120/month (40% buffer)"
}

Handoff: Pass optimized architecture to Validation Agent

---

Step 5: Validation & Compliance (Validation Agent)
Input: Optimized architecture + original requirements

Process:
- Check completeness: All requirements covered?
- Security audit: Encryption, authentication, authorization
- Compliance check: GDPR (customer data), SOC2 (if required)
- Best practices: High availability, disaster recovery, monitoring

Output: {
    "validation_status": "APPROVED_WITH_RECOMMENDATIONS",
    "completeness_check": {
        "nlp_processing": "✓ AWS Lex",
        "crm_integration": "✓ AppFlow",
        "escalation": "✓ EventBridge + SNS",
        "conversation_history": "✓ DynamoDB",
        "analytics": "✓ CloudWatch + QuickSight",
        "multi_channel": "✓ API Gateway (web + mobile)"
    },
    "security_recommendations": [
        "CRITICAL: Enable DynamoDB encryption at rest",
        "CRITICAL: Implement API Gateway authentication (Cognito or API keys)",
        "HIGH: Enable CloudTrail for audit logging",
        "MEDIUM: Add WAF to API Gateway to prevent abuse",
        "MEDIUM: Implement rate limiting (prevent spam conversations)"
    ],
    "compliance_notes": {
        "gdpr": "REQUIRED - customer conversation data stored. Add data retention policy,
                deletion API, consent management",
        "data_residency": "Consider multi-region deployment if serving EU customers"
    },
    "best_practices": [
        "Add DynamoDB point-in-time recovery (backup)",
        "Implement conversation timeout (auto-end inactive sessions)",
        "Add sentiment analysis to improve escalation logic",
        "Create runbook for common operational tasks"
    ],
    "missing_components": [
        "Authentication/authorization not specified - add Cognito",
        "No disaster recovery plan - add multi-AZ deployment",
        "No conversation sentiment tracking - add Comprehend"
    ]
}

Final Output: Complete, validated, cost-optimized cloud architecture

---

ERROR HANDLING & FAILURE SCENARIOS:

1. Agent Failure Scenario: Architecture Designer fails to recommend services
   Handling:
   - Retry with relaxed constraints (e.g., allow higher cost services)
   - Fallback to template-based architecture for common patterns
   - Alert orchestrator to request human intervention
   - Log failure reason for system improvement

2. Unclear Output Scenario: Requirements Analyst produces ambiguous requirements
   Handling:
   - Validation Agent detects missing critical fields
   - Send feedback to Requirements Analyst: "Please clarify CRM system type"
   - If still unclear after 2 attempts, flag for human review
   - Provide best-guess assumptions with disclaimer

3. Conflicting Recommendations: Cost Optimizer suggests cheaper database but
   Validator flags performance issues
   Handling:
   - Conflict Resolution Agent (meta-agent) evaluates trade-offs
   - Present multiple options to user: "Option A (cheaper), Option B (faster)"
   - Use decision matrix: Performance > Cost for user-facing features
   - Document decision rationale

4. Ensuring Completeness:
   - Requirements Analyst creates checklist of all stated needs
   - Each agent must mark which requirements they addressed
   - Validator performs final gap analysis: requirements vs. architecture
   - If gaps exist, send back to Architecture Designer with specific missing items
   - Final approval only if 100% requirements coverage + no critical security issues

WORKFLOW COORDINATION MECHANISM:
- Shared context store (Redis or DynamoDB) where agents read/write state
- Event-driven handoffs using message queue (SQS or Kafka)
- Timeout handling: If agent doesn't respond in 60s, escalate to supervisor
- Audit trail: Log all agent decisions for explainability and debugging
"""

# ============================================================================
# QUESTION 3: CLOUD RESOURCE MAPPING (20 points)
# ============================================================================

CLOUD_RESOURCE_MAPPING_ANSWER = """
SCENARIO: Customer Support Chatbot

COMPLETE CLOUD SERVICES RECOMMENDATION:

1. COMPUTE LAYER

   A. Serverless Functions (AWS Lambda)
   Services: 3 Lambda functions
   - chatbot_handler: Process incoming messages, invoke Lex, store conversations
   - crm_sync: Synchronize customer data with CRM
   - escalation_router: Handle escalation logic and notifications

   Justification:
   - Event-driven workload (triggered by user messages)
   - Variable traffic (500 conversations/day = low steady load)
   - Auto-scaling without capacity planning
   - Cost-effective: Pay only for actual execution time (~4s total per conversation)
   - Estimated cost: 500 conv × 3 functions × 2s × $0.0000166667 = $0.05/day = $1.50/month

   Configuration:
   - Memory: 512MB (sufficient for API calls and logic)
   - Timeout: 30s (handle slow CRM API responses)
   - Concurrency: 50 (support 50 simultaneous conversations)

   B. Container Service (AWS ECS Fargate) - Optional
   Service: 1 Fargate task for webhook listener
   - crm_webhook_listener: Receive CRM events (when customer data changes)

   Justification:
   - Long-running process needed for webhook endpoint
   - Maintains persistent connections
   - Lightweight: 0.25 vCPU, 0.5GB RAM
   - Estimated cost: $5-10/month

2. STORAGE LAYER

   A. NoSQL Database (Amazon DynamoDB)
   Tables:
   - conversations: Store all conversation history
   - customer_context: Cache customer data from CRM
   - escalation_queue: Track escalated conversations

   Justification:
   - Flexible schema (conversations vary in length and structure)
   - Fast reads (<10ms) for conversation history retrieval
   - On-demand pricing matches variable load (cheaper than provisioned for 500/day)
   - Automatic scaling without management
   - Built-in streams for real-time analytics

   Configuration:
   - Pricing mode: On-demand (predictable low cost)
   - Encryption: Enabled (customer data protection)
   - Point-in-time recovery: Enabled (disaster recovery)
   - TTL: 90 days for old conversations (GDPR compliance)
   - Estimated cost: 2GB storage + 4000 read/write units = $3/month

   Schema example:
   conversations table: {PK: conversation_id, SK: timestamp, customer_id, messages[], status}

   B. Cache Layer (Amazon ElastiCache Redis)
   Purpose: Session management and CRM data caching

   Justification:
   - Sub-millisecond response for frequently accessed customer data
   - Reduce CRM API calls (avoid rate limits, improve speed)
   - Store active conversation state (50 concurrent sessions)
   - Pub/Sub for real-time updates to admin dashboard

   Configuration:
   - Instance: cache.t3.micro (500MB memory)
   - Replication: Single node (multi-AZ for production)
   - Estimated cost: $10-15/month

   C. Object Storage (Amazon S3)
   Buckets:
   - conversation-archives: Long-term conversation storage (move from DynamoDB after 90 days)
   - analytics-data: Store aggregated metrics and reports

   Justification:
   - Cheap long-term storage (GDPR requires 6-year retention for some industries)
   - S3 Intelligent-Tiering automatically moves to cheapest tier
   - Durability: 99.999999999% (11 nines)

   Configuration:
   - Storage class: Intelligent-Tiering
   - Lifecycle: Move to Glacier after 1 year, delete after 7 years
   - Encryption: S3-managed keys (SSE-S3)
   - Estimated cost: 10GB/year × $0.023 = $0.23/month

3. NETWORKING LAYER

   A. API Gateway (AWS API Gateway)
   APIs:
   - WebSocket API: Real-time bidirectional chat communication
   - REST API: CRM integration, admin dashboard backend

   Justification:
   - Managed service (no server maintenance)
   - Built-in authentication (Cognito integration)
   - Rate limiting and throttling (prevent abuse)
   - Request/response transformation
   - WebSocket support for real-time chat

   Configuration:
   - WebSocket API for chat: $1.00 per million messages
   - REST API for admin: $3.50 per million calls
   - Throttling: 100 requests/second per user
   - Estimated cost: 4000 messages × $0.001 = $0.004/day = $0.12/month

   B. Load Balancer - NOT NEEDED
   Justification: API Gateway already provides load balancing and auto-scaling

   C. Content Delivery Network (CloudFront) - Optional
   Purpose: Deliver chatbot widget JavaScript to global users

   Justification:
   - Reduce latency for international users
   - Cache static assets (chatbot UI, images)
   - DDoS protection (Shield Standard included)

   Configuration:
   - Origin: S3 bucket with chatbot widget code
   - Cache TTL: 1 hour for widget code
   - Estimated cost: 1GB transfer × $0.085 = $0.085/month

4. AI/ML SERVICES

   A. Natural Language Processing (AWS Lex)
   Purpose: Chatbot conversation engine

   Justification:
   - Managed NLP service (no ML expertise needed)
   - Pre-built conversation flows and slot filling
   - Integrates with Lambda for custom logic
   - Multi-language support
   - Voice + text input support

   Configuration:
   - Pricing: $0.004 per text request
   - 500 conversations × 8 messages × $0.004 = $16/day = $480/month
   - OPTIMIZATION 1: Use Lex automated chatbot ($0.001) = $120/month
   - OPTIMIZATION 2: Consider open-source alternatives (Rasa, Dialogflow) for further cost reduction
   - Estimated cost: $60/month (with budget-conscious approach using DialogFlow ES)
   - Alternative: Custom NLP with Lambda + pre-trained models = $10-15/month

   B. Sentiment Analysis (AWS Comprehend) - OPTIONAL
   Purpose: Detect frustrated customers for escalation

   Justification:
   - Improve escalation accuracy (detect anger/frustration)
   - Proactive escalation before customer explicitly asks
   - Can be replaced with rule-based keyword detection initially

   Configuration:
   - Pricing: $0.0001 per request (100 characters)
   - 500 conversations × 8 messages × $0.0001 = $0.40/day = $12/month
   - COST OPTIMIZATION: Skip for MVP, add later if needed
   - Estimated cost: $0/month (deferred to Phase 2)

5. INTEGRATION SERVICES

   A. CRM Integration (AWS AppFlow)
   Purpose: Bi-directional sync with Salesforce/HubSpot

   Justification:
   - No-code integration (faster than custom API development)
   - Pre-built connectors for major CRMs
   - Scheduled and event-driven flows
   - Data transformation included

   Configuration:
   - Flow: Sync customer data every 5 minutes
   - Pricing: $0.001 per flow run
   - 12 runs/hour × 24 hours × 30 days × $0.001 = $8.64/month
   - Estimated cost: $9/month

   B. Event Bus (Amazon EventBridge)
   Purpose: Route escalation events to human agents

   Justification:
   - Decouple services (chatbot doesn't need to know about notification systems)
   - Multiple targets (email, SMS, Slack, ticketing system)
   - Event filtering and transformation

   Configuration:
   - Rules: Route escalation events based on severity
   - Estimated escalations: 50/day (10% of conversations)
   - Pricing: First 1M events free
   - Estimated cost: $0/month (within free tier)

   C. Notification Service (Amazon SNS)
   Purpose: Send escalation alerts to human agents

   Justification:
   - Multi-channel notifications (email, SMS, mobile push)
   - Fan-out pattern (notify multiple agents)
   - Reliable delivery with retries

   Configuration:
   - Topics: escalation_high_priority, escalation_normal
   - Pricing: $0.50 per 1M requests + $0.0065 per SMS
   - 50 escalations/day × 30 days × $0.0065 = $9.75/month
   - Estimated cost: $10/month

6. SECURITY & IDENTITY

   A. Authentication (Amazon Cognito)
   Purpose: User authentication for admin dashboard and customer identity

   Justification:
   - Managed user directory (no custom auth code)
   - Social login (Google, Facebook) for customers
   - MFA support for admin users
   - JWT tokens for API authorization

   Configuration:
   - User pool: Admin users (10 users)
   - Identity pool: Customer authentication (500 MAU)
   - Pricing: First 50,000 MAU free, then $0.0055 per MAU
   - Estimated cost: $0/month (within free tier)

   B. Web Application Firewall (AWS WAF)
   Purpose: Protect API Gateway from attacks

   Justification:
   - SQL injection protection (even though using NoSQL)
   - Rate-based rules (prevent spam/DDoS)
   - Geo-blocking (if needed)
   - Bot detection

   Configuration:
   - Rules: Rate limiting (100 req/min per IP), SQL injection protection
   - Pricing: $5/month + $1 per rule
   - Estimated cost: $7/month

   C. Secrets Manager (AWS Secrets Manager)
   Purpose: Store CRM API keys, database credentials

   Justification:
   - Automatic rotation (security best practice)
   - Encryption at rest
   - Audit trail (CloudTrail integration)

   Configuration:
   - Secrets: 3 (CRM API key, Lex bot credentials, database password)
   - Pricing: $0.40 per secret per month
   - Estimated cost: $1.20/month

7. MONITORING & LOGGING

   A. CloudWatch Logs
   Purpose: Centralized logging for all services

   Justification:
   - Automatic log collection from Lambda, API Gateway, Lex
   - Searchable with CloudWatch Insights
   - Retention policies (compliance)

   Configuration:
   - Log groups: 5 (per Lambda function, API Gateway, Lex)
   - Retention: 7 days (reduce costs, GDPR compliance)
   - Pricing: $0.50 per GB ingested
   - Estimated logs: 1GB/month
   - Estimated cost: $0.50/month

   B. CloudWatch Metrics & Alarms
   Purpose: Monitor performance and set alerts

   Justification:
   - Track conversation volume, response time, escalation rate
   - Alert on anomalies (sudden spike, high error rate)
   - Custom dashboards for stakeholders

   Configuration:
   - Metrics: 10 custom metrics (conversation count, avg response time, etc.)
   - Alarms: 5 (high error rate, budget exceeded, escalation spike, etc.)
   - Pricing: $0.30 per metric + $0.10 per alarm
   - Estimated cost: $3.50/month

   C. Analytics Dashboard - CloudWatch Dashboards (NOT QuickSight)
   Purpose: Basic metrics visualization

   Justification:
   - CloudWatch dashboards sufficient for basic monitoring
   - QuickSight ($18/month) overkill for 500 conversations/day
   - Can upgrade to QuickSight later if advanced analytics needed

   Configuration:
   - CloudWatch custom dashboards: 3 dashboards
   - Pricing: First 3 dashboards free, then $3/dashboard/month
   - Estimated cost: $0/month (within free tier)

   Future upgrade path:
   - If need advanced BI: Add QuickSight at $18/month later
   - Alternative: Grafana on ECS ($10/month) for open-source BI

   D. Distributed Tracing (AWS X-Ray)
   Purpose: Debug performance issues across services

   Justification:
   - Trace request flow: API Gateway → Lambda → Lex → DynamoDB → CRM
   - Identify bottlenecks (slow CRM API calls)
   - Visualize service map

   Configuration:
   - Tracing: Sample 10% of requests
   - Pricing: $5 per 1M traces + $0.50 per 1M traces scanned
   - Estimated cost: $0.50/month

8. TOTAL COST SUMMARY

OPTION A: Budget-Optimized Architecture ($100-120/month)
| Service Category | Monthly Cost (USD) |
|------------------|-------------------|
| Compute (Lambda + Fargate) | $6.50 |
| Storage (DynamoDB + ElastiCache + S3) | $13.23 |
| Networking (API Gateway + CloudFront) | $0.21 |
| AI/ML (DialogFlow ES or custom NLP) | $60 |
| Integration (AppFlow + EventBridge + SNS) | $19 |
| Security (Cognito + WAF + Secrets Manager) | $8.20 |
| Monitoring (CloudWatch + X-Ray only) | $4.50 |
| **TOTAL** | **$111.64/month** |

OPTION B: Production Architecture ($150-180/month)
| Service Category | Monthly Cost (USD) |
|------------------|-------------------|
| Compute (Lambda + Fargate) | $6.50 |
| Storage (DynamoDB + ElastiCache + S3) | $13.23 |
| Networking (API Gateway + CloudFront) | $0.21 |
| AI/ML (Lex optimized + Comprehend) | $132 |
| Integration (AppFlow + EventBridge + SNS) | $19 |
| Security (Cognito + WAF + Secrets Manager) | $8.20 |
| Monitoring (CloudWatch + QuickSight + X-Ray) | $22.50 |
| **TOTAL** | **$201.64/month** |

RECOMMENDATION: Start with Option A ($112/month), upgrade to Option B as usage grows

COST OPTIMIZATION NOTES:
- Primary cost driver: NLP service (Lex $120/month vs DialogFlow $60/month vs Custom $15/month)
- QuickSight removed from MVP - use CloudWatch dashboards (saves $18/month)
- Comprehend deferred to Phase 2 - use keyword detection initially (saves $12/month)
- Total savings: $50/month (45% reduction) while maintaining core functionality
- Growth projection: At 5000 conversations/day, upgrade to Option B and cost increases to ~$350/month

ARCHITECTURE JUSTIFICATION SUMMARY:
✓ Serverless-first approach minimizes operational overhead
✓ Managed services reduce development time (DialogFlow, AppFlow, Cognito)
✓ Pay-per-use pricing aligns cost with usage (Lambda, DynamoDB)
✓ Scalable to 10x traffic without architecture changes
✓ High availability (multi-AZ databases, auto-scaling compute)
✓ Secure by default (encryption, WAF, Secrets Manager, Cognito)
✓ Observable (CloudWatch, X-Ray)
✓ Cost-effective for startup/small business (~$110/month MVP, ~$200/month full-featured)
✓ Clear upgrade path from budget to production architecture
"""

# ============================================================================
# QUESTION 4: REUSABILITY & IMPROVEMENT (15 points)
# ============================================================================

REUSABILITY_IMPROVEMENT_ANSWER = """
MAKING THE SYSTEM REUSABLE ACROSS PROJECTS:

1. STANDARDIZE VS. CUSTOMIZE

   A. STANDARDIZED COMPONENTS (Same across all projects)

   Agent Framework:
   - Base Agent class with standard interface:
     ```python
     class BaseAgent:
         def analyze(self, input_data: dict) -> dict
         def validate_input(self, input_data: dict) -> bool
         def handle_error(self, error: Exception) -> dict
     ```
   - All agents inherit from BaseAgent
   - Standard input/output format (JSON schema)
   - Common error handling and retry logic

   Orchestration Engine:
   - Pipeline definition: DAG (Directed Acyclic Graph) of agents
   - Handoff protocol: Message queue (SQS) or event bus (EventBridge)
   - State management: Shared context store (DynamoDB or Redis)
   - Timeout and failure handling

   Cloud Service Catalog:
   - Predefined service templates:
     ```json
     {
       "compute": {
         "serverless": ["Lambda", "Cloud Functions", "Azure Functions"],
         "containers": ["ECS", "GKE", "AKS"],
         "vms": ["EC2", "Compute Engine", "Azure VMs"]
       },
       "database": {
         "relational": ["RDS", "Cloud SQL", "Azure SQL"],
         "nosql": ["DynamoDB", "Firestore", "Cosmos DB"],
         "cache": ["ElastiCache", "Memorystore", "Azure Cache"]
       }
     }
     ```
   - Service selection rules (decision tree)
   - Cost models for each service

   Validation Rules:
   - Security checklist (encryption, authentication, least privilege)
   - Compliance templates (GDPR, HIPAA, PCI-DSS, SOC2)
   - Best practices catalog (backup, monitoring, disaster recovery)

   B. CUSTOMIZABLE COMPONENTS (Project-specific)

   Requirements Templates:
   - Industry-specific templates (e-commerce, healthcare, fintech)
   - Load patterns (steady, spiky, seasonal, unpredictable)
   - Integration types (CRM, ERP, payment gateway, analytics)

   Example:
   ```python
   E_COMMERCE_TEMPLATE = {
       "required_features": ["product_catalog", "shopping_cart", "payment", "inventory"],
       "integrations": ["payment_gateway", "shipping_api"],
       "compliance": ["PCI_DSS"],
       "load_pattern": "seasonal_spikes"
   }
   ```

   Architecture Patterns:
   - Pattern library (microservices, serverless, monolith, event-driven)
   - Pattern matching: Map requirements to appropriate pattern
   - Pattern customization: Adjust based on scale and constraints

   Cost Constraints:
   - Budget input: "Target $500/month" or "Minimize cost"
   - Cost-performance trade-off preferences
   - Reserved capacity decisions (upfront savings vs flexibility)

   Cloud Provider Selection:
   - Provider preference (AWS, Azure, GCP, multi-cloud)
   - Existing infrastructure (use same provider as current systems)
   - Regional requirements (data residency, latency)

2. LEARNING FROM PREVIOUS RECOMMENDATIONS

   A. Recommendation Database

   Structure:
   ```python
   recommendation_history = {
       "project_id": "chatbot_2024_01",
       "requirements": {...},
       "architecture": {...},
       "actual_performance": {
           "cost_monthly": 215,  # vs estimated 200
           "response_time_p95": 450ms,  # vs target 500ms
           "availability": 99.97%  # vs target 99.95%
       },
       "issues_encountered": [
           "DynamoDB hot partition (fixed by changing partition key)",
           "Lambda cold starts (fixed by provisioned concurrency)"
       ],
       "optimizations_applied": [
           "Switched from provisioned to on-demand DynamoDB",
           "Added ElastiCache to reduce CRM API calls"
       ],
       "user_satisfaction": 4.5,  # 1-5 scale
       "would_recommend_again": true
   }
   ```

   Learning Mechanisms:

   1. Pattern Recognition:
      - Cluster similar projects: "All chatbots with CRM integration"
      - Extract common architectures: "Most use Lambda + DynamoDB + Lex"
      - Identify success patterns: "Projects with ElastiCache had 30% better response time"

   2. Cost Prediction Improvement:
      - Compare estimated vs actual costs
      - Build regression model: actual_cost = f(traffic, features, services)
      - Update cost estimator with real-world data
      - Example: "Lambda costs were underestimated by 20% for bursty workloads"

   3. Performance Tuning:
      - Track which optimizations worked
      - Example: "Adding CloudFront reduced p95 latency by 200ms for global users"
      - Build optimization recommendation engine

   4. Failure Analysis:
      - Document architecture issues: "Single-AZ RDS caused outage"
      - Update validation rules: "Always recommend multi-AZ for production"
      - Create anti-patterns catalog: "Don't use t2.micro for production databases"

   B. Feedback Loop Integration

   Post-Deployment Monitoring:
   - Automatically collect metrics from deployed architectures
   - Compare actual performance vs predictions
   - Detect architecture issues early (cost overruns, performance problems)

   Implementation:
   ```python
   def learn_from_deployment(project_id, days_since_deployment=30):
       actual_metrics = cloudwatch.get_metrics(project_id, days=days_since_deployment)
       predicted_metrics = recommendation_db.get_predictions(project_id)

       accuracy = calculate_prediction_accuracy(actual_metrics, predicted_metrics)

       if accuracy < 0.8:  # 80% accuracy threshold
           update_cost_model(project_id, actual_metrics)
           retrain_load_estimator(project_id)

       # Store learnings
       knowledge_base.add_case_study(project_id, actual_metrics, lessons_learned)
   ```

   Human Expert Feedback:
   - Allow architects to rate recommendations: 1-5 stars
   - Capture why a recommendation was rejected
   - Use feedback to tune agent weights in multi-agent voting

   Example:
   ```python
   feedback = {
       "recommendation_id": "rec_2024_01_15",
       "rating": 2,  # Low rating
       "rejection_reason": "Recommended DynamoDB but project needed complex joins",
       "actual_choice": "RDS PostgreSQL",
       "outcome": "Better fit, good performance"
   }
   # System learns: For projects with complex queries, prefer relational DB
   ```

3. FEEDBACK MECHANISMS FOR IMPROVEMENT

   A. Real-Time Feedback (During Recommendation)

   Interactive Refinement:
   - Present initial recommendation to user
   - Ask clarifying questions:
     - "Is $200/month within budget?" → Adjust cost constraints
     - "Do you need multi-region deployment?" → Add CloudFront, Route53
     - "Any compliance requirements?" → Add encryption, audit logging

   Confidence Scoring:
   - Each agent outputs confidence score: 0-100%
   - If any agent has <70% confidence, flag for human review
   - Example: "Requirements Analyst 60% confident - problem statement vague"

   Alternative Recommendations:
   - Generate 2-3 architecture options:
     - Option A: Lowest cost ($150/month) - Basic features
     - Option B: Balanced ($250/month) - Recommended
     - Option C: High performance ($500/month) - Premium features
   - User selects preferred option
   - System learns user preferences for future recommendations

   B. Post-Deployment Feedback

   Automated Performance Tracking:
   - Deploy CloudWatch dashboard with recommendation
   - Set up cost anomaly detection
   - Weekly report: "Your chatbot cost $220 this month (vs predicted $200)"

   Issue Tracking Integration:
   - Connect to Jira/GitHub Issues
   - If architecture issue filed, link back to recommendation
   - Example: "Issue #123: DynamoDB throttling" → Update load estimator

   Quarterly Architecture Review:
   - Auto-generate review report after 90 days:
     - Cost efficiency: Actual vs predicted
     - Performance: SLA compliance
     - Scaling: Did architecture handle growth?
     - Issues: What broke? What was over-engineered?
   - Feed findings back into knowledge base

   C. Continuous Learning Pipeline

   Data Collection:
   ```
   Deployed Architectures → CloudWatch Metrics → Data Lake (S3)
   User Feedback → Feedback DB
   Architecture Issues → Issue Tracker → Knowledge Base
   ```

   ML Model Training:
   - Monthly retraining of cost prediction model
   - Weekly updates to load estimation (traffic patterns change seasonally)
   - Quarterly review of architecture patterns (new services launch)

   A/B Testing:
   - Test new agent versions: "New Cost Optimizer vs Old Cost Optimizer"
   - Randomly assign 10% of recommendations to new version
   - Compare user satisfaction and actual costs
   - Promote new version if 5% better

   Knowledge Base Updates:
   - Automated: New service launches (AWS re:Invent) → Update service catalog
   - Manual: Expert architects add new patterns → Review and approve
   - Crowdsourced: Community submissions (like Stack Overflow)

4. EXAMPLE LEARNING SCENARIO

   Initial State (Week 1):
   - System recommends Lambda + DynamoDB for chatbot
   - Estimated cost: $200/month

   Deployment Feedback (Week 4):
   - Actual cost: $280/month (40% higher)
   - Root cause: Underestimated Lambda invocations (users send more messages than predicted)

   System Learning:
   - Update load estimator: "Chatbot conversations average 12 messages (not 8)"
   - Update cost model: "Lambda costs 40% higher for chatbot workloads"
   - Add to knowledge base: "Chatbot case study: Users more engaged than expected"

   Next Recommendation (Week 8):
   - New chatbot project arrives
   - System applies learning: Estimates 12 messages per conversation
   - New cost estimate: $270/month (more accurate)
   - Actual deployment cost: $265/month (98% accuracy)

   Continuous Improvement:
   - After 10 chatbot projects, accuracy improves to 95%
   - System identifies: "Industry matters - healthcare chatbots have 15 messages, retail has 8"
   - Add industry-specific load profiles

SUMMARY:
- Standardize agent framework, orchestration, validation rules
- Customize requirements templates, architecture patterns, cost constraints
- Learn from deployment metrics, user feedback, issue tracking
- Feedback loops: Interactive refinement, post-deployment tracking, quarterly reviews
- Continuous improvement: ML model retraining, A/B testing, knowledge base updates
- Result: System becomes more accurate and valuable over time
"""

# ============================================================================
# QUESTION 5: PRACTICAL CONSIDERATIONS (20 points)
# ============================================================================

PRACTICAL_CONSIDERATIONS_ANSWER = """
HANDLING REAL-WORLD CHALLENGES:

1. CONFLICTING RECOMMENDATIONS BETWEEN AGENTS

   SCENARIO: Cost Optimizer says "Use t3.micro RDS ($15/month)" but
             Validator says "t3.micro insufficient for 1000 users, use t3.small ($30/month)"

   CHALLENGE:
   - Two agents have valid but opposing recommendations
   - Cost vs Performance trade-off
   - No single "correct" answer

   SOLUTION APPROACH:

   A. Multi-Criteria Decision Framework

   Create decision matrix with weighted criteria:
   ```python
   decision_matrix = {
       "criteria": {
           "cost": {"weight": 0.3, "t3.micro": 10, "t3.small": 6},
           "performance": {"weight": 0.4, "t3.micro": 4, "t3.small": 9},
           "reliability": {"weight": 0.2, "t3.micro": 5, "t3.small": 8},
           "scalability": {"weight": 0.1, "t3.micro": 3, "t3.small": 7}
       }
   }

   t3_micro_score = 0.3*10 + 0.4*4 + 0.2*5 + 0.1*3 = 6.3
   t3_small_score = 0.3*6 + 0.4*9 + 0.2*8 + 0.1*7 = 7.9

   Winner: t3.small (higher score)
   ```

   B. User-Configurable Priorities

   Ask user to set preferences at start:
   ```python
   user_priorities = {
       "cost_sensitivity": "medium",  # low, medium, high
       "performance_importance": "high",
       "risk_tolerance": "low"  # prefer proven solutions
   }

   # Adjust weights based on user priorities
   if user_priorities["cost_sensitivity"] == "high":
       weights["cost"] = 0.5  # Increase cost weight
       weights["performance"] = 0.2  # Decrease performance weight
   ```

   C. Escalation to Meta-Agent (Arbiter)

   Create Conflict Resolution Agent:
   ```python
   class ConflictResolutionAgent:
       def resolve(self, conflicting_recommendations, context):
           # Analyze conflict type
           if self.is_cost_vs_performance_conflict(conflicting_recommendations):
               # Apply heuristic: Performance wins for user-facing features
               if context["user_facing"]:
                   return conflicting_recommendations["validator"]
               else:
                   return conflicting_recommendations["cost_optimizer"]

           # Escalate to human if cannot resolve
           if self.confidence < 0.7:
               return self.request_human_decision(conflicting_recommendations)
   ```

   D. Present Multiple Options

   Instead of forcing a single recommendation, show trade-offs:
   ```
   RECOMMENDATION SUMMARY:

   Option A: Cost-Optimized ($180/month)
   - t3.micro RDS instance
   - Risk: May struggle at peak load
   - Best for: Tight budget, willing to upgrade if needed

   Option B: Balanced (Recommended) ($250/month) ⭐
   - t3.small RDS instance
   - Better performance headroom
   - Best for: Production workloads

   Option C: High-Performance ($400/month)
   - t3.medium RDS instance with read replica
   - Handles 5x growth without changes
   - Best for: Rapid growth expected

   Our recommendation: Option B (balanced cost and performance)
   Rationale: 1000 users exceed t3.micro capacity, t3.small provides headroom
   ```

2. INCOMPLETE OR VAGUE PROBLEM STATEMENTS

   SCENARIO: "Build a website for my business"

   CHALLENGE:
   - Missing critical details: What type of business? How many users? Features needed?
   - Cannot design architecture without requirements
   - Risk of wrong assumptions

   SOLUTION APPROACH:

   A. Structured Requirement Elicitation

   Requirements Analyst Agent asks targeted questions:
   ```python
   questions = [
       {
           "question": "What type of business is this? (e-commerce, blog, SaaS, etc.)",
           "required": True,
           "default": None
       },
       {
           "question": "How many users do you expect? (daily active users)",
           "required": True,
           "options": ["<100", "100-1000", "1000-10000", "10000+"],
           "default": "100-1000"
       },
       {
           "question": "What are the main features? (select all that apply)",
           "required": True,
           "options": ["User accounts", "Payment processing", "Content management",
                      "Search", "Analytics", "Mobile app"],
           "default": []
       },
       {
           "question": "Do you have a budget range?",
           "required": False,
           "default": "No preference"
       },
       {
           "question": "Any compliance requirements? (GDPR, HIPAA, PCI-DSS, etc.)",
           "required": False,
           "default": "None"
       }
   ]
   ```

   B. Intelligent Defaults Based on Patterns

   Use ML to infer missing details:
   ```python
   # If user says "e-commerce site"
   inferred_requirements = {
       "features": ["product_catalog", "shopping_cart", "payment", "inventory"],
       "expected_users": 1000,  # Small business average
       "compliance": ["PCI_DSS"],  # Required for payments
       "integrations": ["payment_gateway", "shipping_api"]
   }

   # Present to user for confirmation:
   "Based on 'e-commerce site', we assume you need payment processing,
    product catalog, and ~1000 daily users. Is this correct?"
   ```

   C. Progressive Refinement

   Start with minimal viable architecture, then refine:
   ```python
   iteration_1 = generate_basic_architecture(vague_requirements)
   # Output: "Static website on S3 + CloudFront ($5/month)"

   user_feedback = "I need user accounts and a database"

   iteration_2 = refine_architecture(iteration_1, user_feedback)
   # Output: "Add Cognito for auth, RDS for database ($50/month)"

   user_feedback_2 = "Also need to process payments"

   iteration_3 = refine_architecture(iteration_2, user_feedback_2)
   # Output: "Add Stripe integration, ensure PCI compliance ($50/month)"
   ```

   D. Confidence Scoring & Warnings

   Flag incomplete requirements:
   ```
   ⚠️ RECOMMENDATION CONFIDENCE: 40% (Low)

   Reason: Missing critical information:
   - Expected user load not specified
   - Feature list incomplete
   - Budget constraints unknown

   We've made the following assumptions:
   ✓ Small business (1000 users/day)
   ✓ Basic features (product catalog, shopping cart)
   ✓ Budget under $500/month

   ➡️ ACTION REQUIRED: Please review and confirm assumptions before deployment
   ```

3. BUDGET CONSTRAINTS NOT MENTIONED IN REQUIREMENTS

   SCENARIO: Design recommended architecture costs $800/month, but client can only afford $200/month

   CHALLENGE:
   - Discovered late in process (after design complete)
   - May require complete redesign
   - Balance cost cuts without compromising critical features

   SOLUTION APPROACH:

   A. Proactive Budget Discovery

   Always ask about budget early:
   ```python
   # In Requirements Analyst Agent
   def analyze_requirements(self, problem_statement):
       requirements = self.extract_requirements(problem_statement)

       # ALWAYS ask about budget
       if "budget" not in requirements:
           budget = self.ask_user("What is your monthly cloud budget range?",
                                 options=["<$100", "$100-500", "$500-2000", ">$2000", "No limit"])
           requirements["budget"] = budget

       return requirements
   ```

   B. Cost-Aware Architecture Design

   Cost Optimizer Agent runs DURING design (not just at end):
   ```python
   def design_architecture(self, requirements, budget_constraint):
       architecture = {}
       running_cost = 0

       # Start with essential services
       architecture["database"] = self.select_database(requirements)
       running_cost += architecture["database"]["cost"]

       # Check budget before adding each service
       if running_cost + self.estimate_cost("cache") < budget_constraint:
           architecture["cache"] = self.select_cache(requirements)
       else:
           architecture["cache"] = None  # Skip if over budget
           self.add_warning("Cache omitted due to budget constraints")

       return architecture, running_cost
   ```

   C. Budget Tiers with Feature Trade-offs

   Create tiered recommendations:
   ```
   BUDGET: $200/month (specified)

   TIER 1: Minimum Viable ($180/month) ✓ Within Budget
   - Lambda + DynamoDB (serverless, low fixed cost)
   - S3 for static assets
   - API Gateway
   - Missing: Cache, CDN, advanced monitoring
   - Trade-off: Slower performance, no global distribution

   TIER 2: Recommended ($450/month) ⚠️ Over Budget
   - Add ElastiCache (faster performance)
   - Add CloudFront (global CDN)
   - Add QuickSight (analytics)
   - Need additional $250/month

   RECOMMENDATION: Start with Tier 1, upgrade when budget allows
   ```

   D. Cost Reduction Strategies

   If over budget, automatically apply savings:
   ```python
   cost_reduction_strategies = [
       {"action": "Use Spot Instances for batch jobs", "savings": "70%"},
       {"action": "Switch RDS to Aurora Serverless", "savings": "$80/month"},
       {"action": "Enable S3 Intelligent-Tiering", "savings": "$20/month"},
       {"action": "Use Reserved Instances (1-year)", "savings": "40%"},
       {"action": "Remove non-essential services (QuickSight)", "savings": "$18/month"},
       {"action": "Reduce log retention (30 days → 7 days)", "savings": "$5/month"}
   ]

   # Apply strategies until under budget
   while estimated_cost > budget:
       strategy = select_highest_savings_strategy()
       apply_strategy(strategy)
       estimated_cost -= strategy["savings"]
   ```

   E. Phased Deployment Plan

   Spread costs over time:
   ```
   PHASE 1 (Months 1-3): MVP ($180/month)
   - Core features only
   - Single region
   - Basic monitoring

   PHASE 2 (Months 4-6): Enhanced ($320/month) - After revenue starts
   - Add caching for performance
   - Upgrade monitoring
   - Add analytics

   PHASE 3 (Months 7+): Full Production ($500/month) - At scale
   - Multi-region deployment
   - Advanced security (WAF)
   - Premium support
   ```

4. INTEGRATION WITH EXISTING LEGACY SYSTEMS

   SCENARIO: Need to integrate with 15-year-old on-premise Oracle database and SOAP web services

   CHALLENGE:
   - Legacy systems lack modern APIs (REST, GraphQL)
   - Network connectivity (VPN, Direct Connect)
   - Security (legacy systems may have vulnerabilities)
   - Data format incompatibilities
   - Performance (legacy systems may be slow)

   SOLUTION APPROACH:

   A. Legacy Integration Discovery Agent

   Add specialized agent to identify legacy integration needs:
   ```python
   class LegacyIntegrationAgent:
       def analyze(self, requirements):
           legacy_systems = requirements.get("existing_systems", [])

           integration_plan = []
           for system in legacy_systems:
               plan = {
                   "system": system["name"],
                   "type": self.identify_system_type(system),  # SOAP, REST, Database, etc.
                   "connectivity": self.assess_connectivity(system),  # On-premise, VPN, etc.
                   "integration_pattern": self.recommend_pattern(system),
                   "risks": self.identify_risks(system)
               }
               integration_plan.append(plan)

           return integration_plan
   ```

   B. Integration Patterns Catalog

   Maintain library of integration patterns:
   ```python
   integration_patterns = {
       "on_premise_database": {
           "pattern": "AWS Direct Connect + RDS Proxy + Database Migration Service",
           "components": ["Direct Connect", "VPN as backup", "DMS for replication"],
           "cost": "$150/month (Direct Connect) + $50/month (DMS)",
           "latency": "20-50ms",
           "use_case": "Real-time data sync from on-premise Oracle to RDS"
       },
       "soap_web_service": {
           "pattern": "API Gateway + Lambda SOAP-to-REST adapter",
           "components": ["Lambda function with SOAP client library", "API Gateway"],
           "cost": "$5/month (low traffic)",
           "latency": "100-200ms (SOAP overhead)",
           "use_case": "Wrap legacy SOAP service with modern REST API"
       },
       "mainframe_system": {
           "pattern": "AWS Mainframe Modernization + MQ integration",
           "components": ["MQ for messaging", "Transformation layer"],
           "cost": "$200/month (MQ broker)",
           "latency": "500ms-2s",
           "use_case": "Queue-based integration with mainframe"
       }
   }
   ```

   C. Integration Risk Assessment

   Identify and mitigate risks:
   ```python
   legacy_risks = {
       "Oracle_Database_v10": {
           "risks": [
               {"risk": "Unsupported version", "severity": "HIGH",
                "mitigation": "Upgrade to Oracle 19c or migrate to RDS PostgreSQL"},
               {"risk": "No encryption in transit", "severity": "CRITICAL",
                "mitigation": "Force SSL connection, use VPN"},
               {"risk": "Slow query performance", "severity": "MEDIUM",
                "mitigation": "Add caching layer (ElastiCache)"}
           ]
       }
   }
   ```

   D. Strangler Fig Pattern

   Gradually replace legacy systems:
   ```
   INTEGRATION STRATEGY: Strangler Fig Pattern

   Phase 1 (Months 1-3): Facade Layer
   - Build API Gateway facade in front of legacy SOAP service
   - New applications call modern REST API
   - API Gateway translates to SOAP behind the scenes

   Phase 2 (Months 4-6): Partial Migration
   - Migrate read-heavy operations to new cloud database
   - Writes still go to legacy system
   - Use DMS for real-time replication

   Phase 3 (Months 7-12): Full Migration
   - Migrate all operations to cloud
   - Legacy system becomes read-only archive
   - Eventually decommission legacy system

   Benefits:
   ✓ Low risk (incremental changes)
   ✓ Business continuity (legacy system still works)
   ✓ Gradual team learning curve
   ```

   E. Adapter/Wrapper Services

   Create integration microservices:
   ```python
   # Example: SOAP-to-REST adapter
   @app.route('/api/customers/<customer_id>', methods=['GET'])
   def get_customer(customer_id):
       # Call legacy SOAP service
       soap_response = legacy_soap_client.call('GetCustomer', customer_id)

       # Transform SOAP XML to JSON
       customer_json = xml_to_json_transformer(soap_response)

       # Cache result to reduce legacy system load
       cache.set(f'customer:{customer_id}', customer_json, ttl=3600)

       return jsonify(customer_json)
   ```

5. KEEPING UP WITH NEW CLOUD SERVICES AND PRICING

   CHALLENGE:
   - AWS launches 3000+ new features per year
   - Pricing changes constantly (new tiers, regions, discounts)
   - New services may obsolete current recommendations
   - Agents become outdated quickly

   SOLUTION APPROACH:

   A. Automated Service Catalog Updates

   Monitor cloud provider announcements:
   ```python
   class CloudServiceCatalogUpdater:
       def monitor_announcements(self):
           # RSS feed from AWS, Azure, GCP blogs
           new_services = self.fetch_announcements([
               "https://aws.amazon.com/new/feed/",
               "https://azure.microsoft.com/en-us/updates/feed/",
               "https://cloud.google.com/feeds/cloud-blog.xml"
           ])

           for service in new_services:
               if self.is_relevant(service):
                   self.add_to_catalog(service)
                   self.notify_review_team(service)

       def is_relevant(self, service):
           # Filter out minor updates
           keywords = ["new service", "general availability", "pricing update"]
           return any(keyword in service.title.lower() for keyword in keywords)
   ```

   B. Quarterly Architecture Review Process

   Scheduled updates every 3 months:
   ```
   Q1 2024 Review:
   - New service: AWS Bedrock (managed LLM service)
     Action: Update AI/ML agent to recommend Bedrock for chatbots
     Impact: May reduce costs vs SageMaker for some use cases

   - Pricing change: Lambda free tier increased to 1M requests/month
     Action: Update cost model
     Impact: Small projects now cheaper

   - New region: AWS Sydney availability zone expansion
     Action: Update region selection logic
     Impact: Better latency for Australia users
   ```

   C. Version Control for Agents

   Track agent versions:
   ```python
   agent_versions = {
       "CostOptimizerAgent": {
           "v1.0": "Initial release (Jan 2024)",
           "v1.1": "Added Lambda free tier update (Apr 2024)",
           "v1.2": "Added Bedrock pricing (Jul 2024)",
           "current": "v1.2"
       }
   }

   # Allow rollback if new version has issues
   if agent_v1_2.error_rate > 0.05:
       rollback_to_version("v1.1")
   ```

   D. Community-Driven Updates

   Leverage community knowledge:
   ```
   - GitHub repository for architecture patterns
   - Community contributions (pull requests)
   - Peer review process (2 reviewers required)
   - Changelog and release notes

   Example contribution:
   "Added pattern for IoT sensor data ingestion using AWS IoT Core + Kinesis"
   Review: Approved, merged to main branch
   Impact: System can now recommend architecture for IoT projects
   ```

   E. Pricing API Integration

   Use cloud provider pricing APIs:
   ```python
   import boto3

   pricing_client = boto3.client('pricing', region_name='us-east-1')

   def get_latest_lambda_pricing():
       response = pricing_client.get_products(
           ServiceCode='AWSLambda',
           Filters=[
               {'Type': 'TERM_MATCH', 'Field': 'location', 'Value': 'US East (N. Virginia)'}
           ]
       )
       return parse_pricing(response)

   # Update pricing daily
   schedule.every().day.at("02:00").do(update_all_pricing)
   ```

   F. Deprecation Handling

   Track and warn about deprecated services:
   ```python
   deprecated_services = {
       "EC2-Classic": {
           "deprecation_date": "2022-08-15",
           "replacement": "VPC",
           "action": "Migrate to VPC-based instances"
       },
       "RDS MySQL 5.5": {
           "deprecation_date": "2023-02-28",
           "replacement": "MySQL 8.0",
           "action": "Upgrade database version"
       }
   }

   def validate_architecture(architecture):
       warnings = []
       for service in architecture["services"]:
           if service in deprecated_services:
               warnings.append(f"⚠️ {service} is deprecated, use {deprecated_services[service]['replacement']}")
       return warnings
   ```

SUMMARY OF PRACTICAL SOLUTIONS:

1. Conflicts: Multi-criteria decision framework, user priorities, meta-agent arbitration
2. Vague requirements: Structured questions, intelligent defaults, progressive refinement
3. Budget constraints: Proactive budget discovery, cost-aware design, tiered recommendations
4. Legacy systems: Integration patterns catalog, strangler fig migration, adapter services
5. Service updates: Automated monitoring, quarterly reviews, community contributions, pricing APIs

These approaches make the system robust for real-world complexity and edge cases.
"""

print("=" * 80)
print("AGENT ORCHESTRATION CHALLENGE - COMPLETE")
print("=" * 80)
print()
print("All 5 questions answered with comprehensive responses:")
print("✓ Question 1: Agent Design (5 agents with roles and collaboration)")
print("✓ Question 2: Orchestration Workflow (Customer Support Chatbot scenario)")
print("✓ Question 3: Cloud Resource Mapping (Complete service recommendations)")
print("✓ Question 4: Reusability & Improvement (Learning mechanisms)")
print("✓ Question 5: Practical Considerations (5 real-world challenges)")
print()
print("=" * 80)