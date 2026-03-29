---
title: Drug Side Effect AI
emoji: 💊
colorFrom: blue
colorTo: green
sdk: docker
app_port: 7860
app_file: app.py
pinned: false
---

# 💊 Drug Side Effect Balancer AI

## Problem
Balancing drug effectiveness and side effects in healthcare.

## Environment

### State
- health
- side_effect
- drug

### Actions
0: decrease dose  
1: increase dose  
2: switch drug  
3: maintain  

## Reward Function
reward = (health * 1.2) - side_effect

## Tasks

### Easy
Maintain stable health with low side effects

### Medium
Optimize drug switching for better outcomes

### Hard
Achieve health > 90 and side_effect < 20

## Grader

Score between 0–1:
score = (health/100) - (side_effect/100)

## Baseline Agent

Random action agent implemented in inference.py

## Reproducibility

Random seed is fixed for consistent results.

## Usage

docker build -t drug-env  
docker run drug-env
# final update
# graph fix final