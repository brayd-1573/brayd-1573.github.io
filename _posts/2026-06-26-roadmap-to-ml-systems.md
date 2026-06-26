---
title: "My Roadmap for Summer 2026 Through Fall Semester"
date: 2026-06-26 09:00:00 -0500
categories: [Learning, ML Systems]
tags: [roadmap, deep-learning, ml-compilers, vanderbilt, career-pivot]
---

## The Journey So Far

Four months ago, I was convinced my future was in quantitative finance. I was grinding through graduate-level math—real analysis, topology, measure theory, and stochastic processes—with my sights set on becoming a quant trader or researcher. I had the green book and everything. But at some point, the path stopped feeling right. I no longer had any passion for what I was studying.

It wasn't just burnout from overloading my schedule (though that certainly didn't help). It was the realization that I couldn't see myself proving theorems for the next five years just to get positioned for the roles I thought I wanted. What I actually enjoy is building things—not regurgitating proofs—and understanding how they work under the hood. So I decided to lean back into that.

## My Foundation

To understand where I'm going, it helps to know where I've been. Here's the academic foundation I've built over my first two years at Vanderbilt:

### Freshman Year (2024-2025)

**Fall 2024**
- Calculus I (MATH 1300)
- General Physics I (PHYS 1601)
- Introduction to Engineering (ES 1401-3)
- CS Ethics (CS 1151)

**Spring 2025**
- Calculus II (MATH 1301)
- Physics II (PHYS 1602)
- Programming & Problem Solving (CS 1101)
- Biology Today (BSCI 1100)
- Principles of Macroeconomics (ECON 1010)

### Sophomore Year (2025-2026)

**Summer 2025**
- Multivariable Calculus (MATH 2300)
- Linear Algebra (MATH 2410)

**Fall 2025**
- Probability and Statistics + Lab (MATH 2820L)
- Discrete Structures (CS 2212)
- Data Structures (CS 2201)
- Math Reasoning (MATH 2100)
- Economic Statistics (ECON 1500)
- Quantitative Methods: Statistical Analysis (ECON 2400)

**Spring 2026**
- Probability (MATH 3640)
- Introduction to Analysis (MATH 3100)
- Introduction to Topology (MATH 3200)
- Ordinary Differential Equations (MATH 2610)
- Intermediate Software Design (CS 3251)

That spring semester—the one with topology and all that graduate-level math—was my breaking point. But it also clarified what I actually wanted to do. Luckily, I now have a solid mathematical foundation and decent programming fundamentals, so I can focus fully on ML Systems.

## The Roadmap: Summer 2026 - Fall 2026

### Phase 1: Deep Learning Systems (Now - Early August)

**Course:** [CMU 15-414: Deep Learning Systems](https://dlsyscourse.org/)

**Timeline:** June 26, 2026 → First week of August 2026

This is where I'm starting. CMU's Deep Learning Systems course teaches the complete DL technology stack—from automatic differentiation implementation to device-level efficient algorithms. The core project is building **Needle**, a deep learning library from scratch.

**Why this matters:** Most people who work with PyTorch or TensorFlow treat them as black boxes. This course tears that black box apart. I'll be implementing:
- Automatic differentiation from first principles
- Neural network modules (layers, activations, optimizers)
- CPU and CUDA backends for hardware acceleration
- Advanced operations (convolutions, transformers, etc.)

By the end, I'll understand how deep learning frameworks work at every layer of the stack. This is foundational knowledge for anyone serious about ML systems engineering.

**What I'm building:** Five homework assignments (HW0-HW4) incrementally building Needle, plus a substantial final project implementing new features.

**Course level:** This is an advanced course with serious prerequisites. You need prior experience with systems programming (CMU 15-213 or equivalent), linear algebra, calculus, probability, and machine learning fundamentals. The course also requires proficiency in both Python and C++. Homework 0 serves as a diagnostic—if you're not comfortable with all the concepts there, you'll struggle. This isn't a beginner-friendly introduction; it's designed for students who already have the foundations and want to understand how the systems actually work.

### Phase 2: ML Compilers (August - Late August)

**Course:** [MLC: Machine Learning Compilation](https://mlc.ai/summer22/)

**Timeline:** Early August → End of August (before Fall semester)

Once I understand how DL frameworks work internally, the next question is: how do we make them run efficiently across different hardware? That's where ML compilation comes in.

**Why this matters:** Deploying ML models to production isn't just about accuracy—it's about:
- Minimizing software dependencies
- Optimizing memory usage
- Leveraging specific hardware capabilities
- Scaling across diverse environments (GPUs, TPUs, edge devices)

This course covers the systematic techniques for handling these challenges: ML programming abstractions, automatic optimization through learning-driven search, and end-to-end deployment optimization.

**The timing:** This is a shorter course, designed to bridge my summer self-study into my fall semester coursework. It gives me the compiler perspective that will be crucial for understanding the systems-level optimizations in my fall classes.

### Phase 3: Fall 2026 - Going Deep on Systems

**Official Coursework at Vanderbilt:**

1. **Computer Architecture**
2. **Algorithms**
3. **Applied ML or Foundations of ML** (depending on waitlist)
4. **Systems for AI (Auditing)**

**Systems for AI (CS-3891-02)** deserves special attention. Here's the course description:

> *Systems for AI examines the design and operation of computing systems that enable modern artificial intelligence workloads. Topics include GPU/TPU architectures, distributed training and inference, data pipelines, storage systems, networking for AI clusters, performance optimization, scalability, and reliability. The course emphasizes system model co-design, resource management, and emerging infrastructure for large-scale foundation models.*

This course covers *exactly* what I want to specialize in. GPU/TPU architectures, distributed training, inference systems, performance optimization—this is the heart of ML systems engineering. It's taught by **Professor Aniruddha Gokhale**, who will also be supervising my independent study.

### Phase 4: Independent Study & Research (Fall 2026)

**Materials:** [CMU 15-442/642: Machine Learning Systems](https://mlsyscourse.org/)

**Supervisor:** Professor Aniruddha Gokhale

Professor Gokhale's research focuses heavily on deep learning workloads and systems. His [accomplishments](https://www.dre.vanderbilt.edu/~gokhale/WWW/CV/accomplishments.pdf) include extensive work on distributed systems, middleware, and real-time systems—all directly applicable to the challenges of deploying ML at scale.

**The Plan:** CMU 15-442/642 covers:
- ML framework design rationale (why systems like PyTorch/JAX are architected the way they are)
- System optimization techniques (scaling, memory reduction, heterogeneous compute)
- LLM systems (training and serving case studies from production systems)

I'll work through this material throughout the fall, culminating in a research project. My current plan is to focus on **LLM inference and serving**—one of the hottest areas in ML systems right now, with tons of open problems around:
- Efficient attention mechanisms
- KV-cache optimization
- Batching strategies
- Multi-GPU serving
- Quantization and compression

The combination of Systems for AI lectures + CMU 642 materials + research with Gokhale should give me a comprehensive foundation in modern ML systems.

**Course level:** CMU 15-442 is the undergraduate version, 15-642 is graduate level. Both cover similar content but 642 has more rigorous expectations. Since I'm doing this as an independent study rather than for official CMU credit, I'm treating it as the graduate version—working through the harder problem sets and aiming for that level of depth. The course is designed for students who want to pursue ML systems research or engineering roles, so it assumes you already have ML fundamentals down and focuses on the systems side.

## Visual Timeline

```
SUMMER 2026
═══════════════════════════════════════════════════════════════
June 26 ─────────────────────── August 7 ──────────── August 26
   │                                 │                     │
   │                                 │                     │
   ▼                                 ▼                     │
┌──────────────────────────────┐ ┌──────────────────┐      │
│  CMU 414: DL Systems         │ │ MLC: ML          │      │
│  • Building Needle framework │ │ Compilers        │      │
│  • Auto differentiation      │ │ • Optimization   │      │
│  • CUDA backends             │ │ • Deployment     │     /
│  • HW0-HW4 + Final Project   │ │                  │    │
└──────────────────────────────┘ └──────────────────┘    │
                                                         │
FALL 2026                                                │
═════════════════════════════════════════════════════════▼══════
                                              August 26 ─── December
                                                    │
                    ┌───────────────────────────────┴───────────────┐
                    │                                               │
                    ▼                                               ▼
         ┌─────────────────────────┐                   ┌──────────────────────┐
         │  OFFICIAL COURSES       │                   │  INDEPENDENT STUDY   │
         │  ───────────────        │                   │  ──────────────────  │
         │  • Computer Arch        │                   │  Materials:          │
         │  • Algorithms           │                   │  • CMU 642: ML Sys   │
         │  • Applied/Found ML     │                   │  • MLSysBook.ai      │
         │  • Systems for AI (Aud) │                   │                      │
         │                         │                   │  Supervisor:         │
         │  Focus: GPU/TPU arch,   │◄──────────────────┤  Prof. Gokhale       │
         │  distributed training,  │      Synergy      │                      │
         │  inference systems      │                   │  Goal: LLM inference │
         └─────────────────────────┘                   │  & serving project   │
                                                       └──────────────────────┘
```

## Why This Path?

Each piece builds on the previous:

1. **DL Systems** gives me framework internals—how do we represent and compute gradients?
2. **ML Compilers** adds the optimization layer—how do we make those computations efficient?
3. **Computer Architecture** provides the hardware context—what are we actually optimizing for?
4. **Systems for AI** brings it all together—how do production ML systems actually work?
5. **CMU 642 + Research** lets me go deep on a specific problem area with guidance

By December, the goal is to move past just using frameworks and really understand how the whole stack fits together—from mathematical operations to automatic differentiation to compilation to hardware execution to distributed systems.

One major goal for me this time is to avoid burning out—I’ve stretched myself too thin in the past, and I want to make sure I actually understand what I’m studying instead of just getting through it.

## Learning from the Market: Job Descriptions as a Roadmap

One habit I’ve developed is reading through job descriptions for roles I’m targeting. Here are a few positions I’ve saved:

### [NVIDIA - Senior Software Engineer, CUDA Deep Learning Systems](https://www.linkedin.com/jobs/view/4415138369/)
**What they want:** 8+ years of C++/Python, deep transformer knowledge, CUDA kernel optimization, distributed training at cluster scale. They’re building "novel systems optimizations for advanced deep learning models at the intersection of high-level DL frameworks and low-level CUDA."

**What I’m learning:** This is exactly why I’m doing CMU 414. They want people who can move between PyTorch-level abstractions and raw CUDA kernels. Building Needle forces me to understand both layers.

**Salary:** $184K–$356K depending on level

### [Meta - Software Engineer, SystemML (Scaling/Performance)](https://www.linkedin.com/jobs/view/4427304628/)
**What they want:** Experience with distributed ML training, GPU architecture, CUDA, PyTorch internals, NCCL, and parallelism strategies (FSDP, Tensor Parallel, Pipeline Parallel). The team works on "reliable and highly scalable distributed ML training on Meta’s large-scale GPU training infra with a focus on GenAI/LLM scaling."

**What I’m learning:** This is the distributed systems piece. My independent study on LLM inference/serving needs to cover these parallelism strategies. The Systems for AI course covers NCCL and cluster networking—exactly what they’re asking for.

**Salary:** $154K–$217K plus equity

### [NVIDIA - High-Performance LLM Training Engineer (New Grad)](https://www.linkedin.com/jobs/view/4427781384/)
**What they want:** MS in CS/EE/CE, deep learning expertise, GPU architecture knowledge, C++/Python/CUDA proficiency, performance analysis skills. They want people who can "analyze, profile, and optimize AI training workloads on innovative hardware."

**What I’m learning:** This is a new grad role (my target timeline), and they want exactly what I’m building toward. The course stack I’m taking—DL systems, compilers, architecture, Systems for AI—maps directly to their requirements.

**Salary:** $124K–$195K for new grads

### [Anthropic - Performance Engineer, GPU](https://www.linkedin.com/jobs/view/4322320290/)
**What they want:** CUDA/Triton/CUTLASS, PyTorch/JAX internals, kernel fusion, distributed communication (NCCL, NVLink), quantization (INT8/FP8). The role spans "custom kernel development to distributed system architectures" and orchestrating thousands of GPUs.

**What I’m learning:** Anthropic is pushing frontier models, so they need the full stack—from low-level kernel optimization to multi-node coordination. This validates why I need both the systems programming side (414) and the distributed systems side (642/Systems for AI).

**Salary:** $280K–$850K (wide range, likely based on experience/level)

### [NVIDIA - Senior Deep Learning Performance Architect](https://www.linkedin.com/jobs/view/4395475638/)
**What they want:** MS/PhD, 4+ years in parallel computing architectures, GPU/ASIC experience, understanding of transformer architectures, performance/power/area analysis. They’re "creating innovative hardware designs to advance parallel computing performance and energy efficiency."

**What I’m learning:** This is more hardware-focused but requires deep understanding of how software (transformers, distributed training) maps to hardware. Computer Architecture + Systems for AI should give me the foundation to understand these tradeoffs.

**Salary:** $184K–$287K

### [Oxmiq Labs - Compiler Engineer (GPU Backend)](https://www.linkedin.com/jobs/view/4427097485/)
**What they want:** 5+ years compiler engineering, LLVM/MLIR expertise, GPU execution models, Triton kernel frameworks. They’re "designing compiler infrastructure for GPU-accelerated workloads, including lowering pipelines and code generation backends."

**What I’m learning:** This is the ML compilers piece. The MLC course covers MLIR, lowering passes, and optimization. This is a more specialized path but shows there’s demand for people who understand the compilation stack.

### The Pattern

What do all these roles have in common?

1. **Deep understanding of the full stack** - You can’t just know PyTorch, you need to know what happens under the hood
2. **Systems programming skills** - C++, CUDA, low-level optimization
3. **Distributed systems knowledge** - Multi-GPU, multi-node, communication primitives
4. **Performance obsession** - Profiling, bottleneck analysis, hardware-software co-design
5. **Transformer/LLM expertise** - The market is all about generative AI now

## What Success Looks Like

By the end of Fall 2026, I want to:

- **Have built** a complete deep learning framework (Needle)
- **Understand** how modern ML compilers optimize code for different hardware targets
- **Complete** a research project on LLM inference/serving with tangible results
- **Contribute** to an open-source ML systems project (TVM, PyTorch, vLLM, etc.)
- **Publish** technical blog posts documenting key insights from each phase
- **Be ready** for summer 2027 ML systems internships at companies pushing the frontier

## Accountability

This blog is my commitment device. I'll be posting:

- **Weekly progress updates** during the summer courses
- **Technical deep-dives** on interesting problems I encounter
- **Project showcases** when I complete major milestones
- **Research notes** from my independent study

If you're on a similar journey or interested in ML systems, let's connect. You can find me on [GitHub](https://github.com/brayd-1573) or reach out via [email](mailto:brayden.cox2005@icloud.com).

---

*Last updated: June 26, 2026*
