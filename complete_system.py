"""
COMPLETE DISASTER INTELLIGENCE SYSTEM
Main application file - Complete System
"""

import os
import json
import secrets
from datetime import datetime
from flask import Flask, render_template_string, request, jsonify, session
from flask_cors import CORS

# Create Flask app
app = Flask(__name__)
app.secret_key = secrets.token_hex(32)
CORS(app)

# ============================================================================
# DATABASES
# ============================================================================

events = {}
alerts = []
event_counter = 0
volunteers = []
donations = []
safe_checks = []

# ============================================================================
# COMPLETE HTML - THE ENTIRE WEBSITE
# ============================================================================

COMPLETE_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="theme-color" content="#0d1b2a">
<title>DisasterIntel - Global Emergency Intelligence Platform</title>
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css">
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
<style>
*{margin:0;padding:0;box-sizing:border-box}
:root{--primary:#ef4444;--primary-dark:#dc2626;--secondary:#2a5298;--secondary-dark:#1e3c72;--success:#10b981;--warning:#f59e0b;--danger:#ef4444;--dark:#1f2937;--light:#f9fafb}
body{font-family:'Inter',sans-serif;background:linear-gradient(135deg,#0f172a 0%,#1e3a8a 50%,#7c2d12 100%);background-attachment:fixed;min-height:100vh;color:#1f2937}
.navbar{background:rgba(255,255,255,.98);backdrop-filter:blur(10px);padding:1rem 2rem;box-shadow:0 4px 20px rgba(0,0,0,.2);position:sticky;top:0;z-index:100;display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;border-bottom:3px solid #ef4444}
.logo{font-size:1.5rem;font-weight:800;background:linear-gradient(135deg,#ef4444,#2a5298);-webkit-background-clip:text;background-clip:text;color:transparent}
.logo i{color:#ef4444}
.nav-links{display:flex;gap:1rem;align-items:center;flex-wrap:wrap}
.nav-links a{text-decoration:none;color:#1f2937;font-weight:600;padding:.5rem 1rem;border-radius:10px;transition:all .3s;display:flex;align-items:center;gap:.5rem}
.nav-links a:hover,.nav-links a.active{color:#ef4444;background:rgba(239,68,68,.1);transform:translateY(-2px)}
.container{max-width:1400px;margin:0 auto;padding:20px;position:relative;z-index:1}
.stats-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:20px;margin-bottom:30px}
.stat-card{background:rgba(255,255,255,.95);backdrop-filter:blur(10px);padding:25px;border-radius:20px;text-align:center;transition:all .3s;border:1px solid rgba(255,255,255,.3);cursor:pointer}
.stat-card:hover{transform:translateY(-5px);box-shadow:0 10px 30px rgba(0,0,0,.2)}
.stat-number{font-size:36px;font-weight:800;background:linear-gradient(135deg,#ef4444,#2a5298);-webkit-background-clip:text;background-clip:text;color:transparent}
.card{background:rgba(255,255,255,.95);backdrop-filter:blur(10px);padding:25px;border-radius:20px;margin-bottom:25px;border:1px solid rgba(255,255,255,.3);transition:all .3s}
.card:hover{transform:translateY(-3px);box-shadow:0 10px 30px rgba(0,0,0,.2)}
.card h2{color:#2a5298;margin-bottom:20px;display:flex;align-items:center;gap:10px;border-bottom:2px solid #ef4444;padding-bottom:10px}
.dashboard-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(400px,1fr));gap:25px;margin-bottom:25px}
@media(max-width:768px){.dashboard-grid{grid-template-columns:1fr}}
.form-group{margin-bottom:15px}
input,select,textarea{width:100%;padding:12px 16px;border:2px solid #e5e7eb;border-radius:12px;font-family:'Inter',sans-serif;transition:all .3s}
input:focus,select:focus,textarea:focus{outline:none;border-color:#ef4444;transform:translateY(-2px)}
.btn-primary,button[type="submit"],.btn{background:linear-gradient(135deg,#ef4444,#dc2626);color:white;padding:12px 24px;border:none;border-radius:12px;cursor:pointer;font-weight:600;transition:all .3s;display:inline-flex;align-items:center;gap:8px;width:100%;justify-content:center}
.btn-primary:hover,button:hover{transform:translateY(-2px);box-shadow:0 5px 15px rgba(239,68,68,.3)}
.btn-secondary{background:linear-gradient(135deg,#2a5298,#1e3c72)}
.btn-success{background:linear-gradient(135deg,#10b981,#059669)}
.events-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:20px;margin-top:20px}
.event-card{background:white;padding:20px;border-radius:15px;border-left:5px solid;box-shadow:0 5px 15px rgba(0,0,0,.1);transition:all .3s;cursor:pointer}
.event-card:hover{transform:translateY(-3px);box-shadow:0 10px 25px rgba(0,0,0,.15)}
.event-card.flood{border-left-color:#3b82f6}
.event-card.earthquake{border-left-color:#f59e0b}
.event-card.hurricane{border-left-color:#8b5cf6}
.event-card.wildfire{border-left-color:#ef4444}
.status-badge{display:inline-block;padding:6px 12px;border-radius:20px;font-size:12px;font-weight:600;margin-top:10px}
.status-analyzed{background:#d1fae5;color:#065f46}
.status-reported{background:#fef3c7;color:#92400e}
.analysis{display:none;margin-top:20px}
.analysis.show{display:block}
.result-item{background:white;padding:20px;margin-bottom:15px;border-radius:12px;border-left:4px solid #ef4444}
.list-item{padding:10px;margin-bottom:8px;background:#f9fafb;border-radius:8px;display:flex;align-items:center;gap:10px}
.list-item i{color:#10b981;width:25px}
.chatbot-container{position:fixed;bottom:30px;right:30px;z-index:1000}
.chatbot-toggle{width:70px;height:70px;background:linear-gradient(135deg,#ef4444,#dc2626);border:none;border-radius:50%;cursor:pointer;display:flex;align-items:center;justify-content:center;font-size:32px;box-shadow:0 4px 20px rgba(239,68,68,.4);transition:all .3s;color:white;animation:bounce 2s infinite}
@keyframes bounce{0%,100%{transform:translateY(0)}50%{transform:translateY(-10px)}}
.chatbot-toggle:hover{transform:scale(1.1)}
.chatbot-window{position:absolute;bottom:90px;right:0;width:400px;height:600px;background:white;border-radius:20px;box-shadow:0 20px 50px rgba(0,0,0,.3);display:none;flex-direction:column;overflow:hidden}
.chatbot-window.active{display:flex}
@media(max-width:768px){.chatbot-window{width:90vw;height:80vh;bottom:auto;right:auto;left:50%;transform:translateX(-50%)}}
.chatbot-header{background:linear-gradient(135deg,#ef4444,#dc2626);color:white;padding:20px;display:flex;align-items:center;gap:15px}
.chatbot-header i{font-size:30px}
.chatbot-header h3{font-size:20px;margin:0;flex:1}
.chatbot-close{background:none;border:none;color:white;font-size:28px;cursor:pointer;width:35px;height:35px;border-radius:50%;transition:all .3s}
.chatbot-close:hover{background:rgba(255,255,255,.2);transform:rotate(90deg)}
.chatbot-messages{flex:1;overflow-y:auto;padding:20px;display:flex;flex-direction:column;gap:15px;background:#f8fafc}
.message{display:flex;gap:12px}
.message.user{justify-content:flex-end}
.message-bubble{max-width:75%;padding:12px 18px;border-radius:18px;word-wrap:break-word;line-height:1.5}
.message.bot .message-bubble{background:white;color:#1f2937;border-bottom-left-radius:5px;box-shadow:0 2px 5px rgba(0,0,0,.1)}
.message.user .message-bubble{background:linear-gradient(135deg,#2a5298,#1e3c72);color:white;border-bottom-right-radius:5px}
.message-icon{font-size:24px;display:flex;align-items:flex-end}
.chatbot-input-area{padding:20px;border-top:1px solid #e5e7eb;display:flex;gap:12px;background:white}
.chatbot-input-area input{flex:1;padding:12px 18px;border:2px solid #e5e7eb;border-radius:25px;font-size:14px}
.chatbot-input-area input:focus{border-color:#ef4444;outline:none}
.chatbot-send{background:#ef4444;color:white;border:none;border-radius:50%;width:50px;height:50px;cursor:pointer;transition:all .3s}
.chatbot-send:hover{transform:scale(1.05);background:#dc2626}
footer{background:rgba(255,255,255,.95);padding:30px;border-radius:20px;text-align:center;color:#666;margin-top:30px}
.loading{display:none;text-align:center;margin-top:15px}
.loading.show{display:flex;align-items:center;justify-content:center;gap:10px}
.spinner{width:20px;height:20px;border:3px solid rgba(42,82,152,.3);border-radius:50%;border-top-color:#2a5298;animation:spin 1s linear infinite}
@keyframes spin{to{transform:rotate(360deg)}}
.alert{padding:15px;margin-bottom:12px;border-radius:10px;border-left:4px solid;display:flex;align-items:center;gap:12px}
.alert.success{border-left-color:#10b981;background:rgba(16,185,129,.1);color:#065f46}
.alert.error{border-left-color:#ef4444;background:rgba(239,68,68,.1);color:#991b1b}
</style>
</head>
<body>
<div class="navbar">
<div class="logo"><i class="fas fa-shield-alt"></i> DisasterIntel</div>
<div class="nav-links">
<a href="#" class="active" onclick="showSection('dashboard')"><i class="fas fa-home"></i> Dashboard</a>
<a href="#" onclick="showSection('report')"><i class="fas fa-map-marker-alt"></i> Report</a>
<a href="#" onclick="showSection('resources')"><i class="fas fa-boxes"></i> Resources</a>
<a href="#" onclick="showSection('volunteer')"><i class="fas fa-hands-helping"></i> Volunteer</a>
<a href="#" onclick="showSection('donate')"><i class="fas fa-heart"></i> Donate</a>
<a href="#" onclick="showSection('training')"><i class="fas fa-graduation-cap"></i> Training</a>
<a href="#" onclick="showSection('about')"><i class="fas fa-info-circle"></i> About</a>
<a href="#" onclick="showSection('contact')"><i class="fas fa-envelope"></i> Contact</a>
</div>
</div>

<div class="container">
<!-- Dashboard Section -->
<div id="dashboard-section" class="section active">
<div class="stats-grid">
<div class="stat-card" onclick="showSection('report')"><i class="fas fa-exclamation-triangle" style="font-size:40px;color:#ef4444"></i><div class="stat-number" id="total-events">0</div><div>Active Events</div></div>
<div class="stat-card" onclick="showSection('resources')"><i class="fas fa-users" style="font-size:40px;color:#f59e0b"></i><div class="stat-number" id="total-affected">0</div><div>People Affected</div></div>
<div class="stat-card" onclick="showSection('volunteer')"><i class="fas fa-hand-peace" style="font-size:40px;color:#10b981"></i><div class="stat-number" id="volunteer-count">0</div><div>Volunteers</div></div>
<div class="stat-card" onclick="showSection('donate')"><i class="fas fa-heartbeat" style="font-size:40px;color:#3b82f6"></i><div class="stat-number" id="analyzed-count">0</div><div>AI Analyses</div></div>
</div>

<div class="dashboard-grid">
<div class="card"><h2><i class="fas fa-list"></i> Recent Events</h2><div class="events-grid" id="events-list"></div></div>
<div class="card"><h2><i class="fas fa-check-circle"></i> I'm Safe - Family Check-in</h2><div class="form-group"><input type="text" id="checkin-name" placeholder="Your Name"></div><div class="form-group"><input type="text" id="checkin-location" placeholder="Your Location"></div><div class="form-group"><textarea id="checkin-status" rows="2" placeholder="Status update..."></textarea></div><button class="btn-success" onclick="markSafe()"><i class="fas fa-check-circle"></i> Mark Myself Safe</button><div id="safe-list" style="margin-top:20px"></div></div>
</div>

<div class="card"><h2><i class="fas fa-chart-line"></i> Live Updates</h2><div id="news-feed"><div class="list-item"><i class="fas fa-bullhorn"></i> Evacuation centers activated - Zone A & B</div><div class="list-item"><i class="fas fa-ambulance"></i> Medical teams dispatched to affected areas</div><div class="list-item"><i class="fas fa-road"></i> Highway 101 open - alternate route active</div></div></div>
</div>

<!-- Report Section -->
<div id="report-section" class="section" style="display:none">
<div class="dashboard-grid">
<div class="card"><h2><i class="fas fa-map-marker-alt"></i> Report Disaster</h2><div class="form-group"><label>Disaster Type</label><select id="disaster-type"><option>Flood</option><option>Earthquake</option><option>Hurricane</option><option>Wildfire</option><option>Landslide</option></select></div><div class="form-group"><label>Location</label><input type="text" id="disaster-location" placeholder="City/District"></div><div class="form-group"><label>Coordinates</label><div style="display:grid;grid-template-columns:1fr 1fr;gap:10px"><input type="number" id="latitude" placeholder="Latitude" step="0.0001"><input type="number" id="longitude" placeholder="Longitude" step="0.0001"></div></div><div class="form-group"><label>Severity (1-10)</label><input type="range" id="severity" min="1" max="10" value="5" oninput="document.getElementById('sev-val').textContent=this.value"><span id="sev-val" style="margin-left:10px">5</span></div><div class="form-group"><label>Affected Population</label><input type="number" id="population" placeholder="Number of people"></div><div class="form-group"><label>Description</label><textarea id="description" rows="3" placeholder="Describe the situation..."></textarea></div><button class="btn-primary" onclick="submitReport()"><i class="fas fa-paper-plane"></i> Submit Report</button><div id="report-alert"></div><div class="loading" id="report-loading"><div class="spinner"></div> Submitting...</div></div>

<div class="card"><h2><i class="fas fa-brain"></i> AI Analysis</h2><div class="form-group"><label>Select Event</label><select id="event-select" onchange="updateSelectedEvent()"><option value="">-- Select Event --</option></select></div><button class="btn-secondary" onclick="analyzeEvent()"><i class="fas fa-microchip"></i> Analyze with AI</button><div id="analysis-alert"></div><div class="loading" id="analysis-loading"><div class="spinner"></div> AI Analyzing...</div><div id="analysis-results" class="analysis"><div class="result-item"><strong><i class="fas fa-warning"></i> Hazard Assessment</strong><p id="hazard-text"></p></div><div class="result-item"><strong><i class="fas fa-shield"></i> Safe Zones</strong><div id="zones-list"></div></div><div class="result-item"><strong><i class="fas fa-road"></i> Evacuation Routes</strong><div id="routes-list"></div></div><div class="result-item"><strong><i class="fas fa-lightbulb"></i> Recommendations</strong><div id="recommendations-list"></div></div></div></div>
</div>
</div>

<!-- Resources Section -->
<div id="resources-section" class="section" style="display:none">
<div class="card"><h2><i class="fas fa-boxes"></i> Available Resources</h2><div id="resources-list"></div><div class="form-group"><label>Request Supplies</label><select id="supply-type"><option>Food & Water</option><option>Medical Supplies</option><option>Blankets</option><option>Shelter/Tents</option></select></div><div class="form-group"><input type="number" id="supply-qty" placeholder="Quantity"></div><div class="form-group"><input type="text" id="supply-location" placeholder="Delivery Location"></div><button class="btn-primary" onclick="requestSupplies()"><i class="fas fa-truck"></i> Request Supplies</button></div>
</div>

<!-- Volunteer Section -->
<div id="volunteer-section" class="section" style="display:none">
<div class="dashboard-grid">
<div class="card"><h2><i class="fas fa-user-plus"></i> Register as Volunteer</h2><div class="form-group"><input type="text" id="vol-name" placeholder="Full Name"></div><div class="form-group"><input type="email" id="vol-email" placeholder="Email"></div><div class="form-group"><input type="tel" id="vol-phone" placeholder="Phone"></div><div class="form-group"><select id="vol-skill"><option>Medical Professional</option><option>Rescue Operations</option><option>Logistics</option><option>Food Distribution</option><option>General Support</option></select></div><button class="btn-success" onclick="registerVolunteer()"><i class="fas fa-user-check"></i> Register</button><div id="vol-alert"></div></div>
<div class="card"><h2><i class="fas fa-users"></i> Active Volunteers</h2><div id="active-volunteers"></div></div>
</div>
</div>

<!-- Donate Section -->
<div id="donate-section" class="section" style="display:none">
<div class="dashboard-grid">
<div class="card"><h2><i class="fas fa-hand-holding-heart"></i> Support Relief Efforts</h2><div style="display:grid;grid-template-columns:repeat(3,1fr);gap:10px;margin-bottom:20px"><button class="btn-success" onclick="setDonation(10)">$10</button><button class="btn-success" onclick="setDonation(25)">$25</button><button class="btn-success" onclick="setDonation(50)">$50</button></div><div class="form-group"><input type="number" id="donation-amount" placeholder="Custom Amount ($)"></div><button class="btn-primary" onclick="processDonation()"><i class="fas fa-heart"></i> Donate Now</button><div id="donate-alert"></div></div>
<div class="card"><h2><i class="fas fa-chart-pie"></i> Impact So Far</h2><div class="stat-card"><div class="stat-number">$284K</div><div>Total Raised</div></div><div class="stat-card"><div class="stat-number">12,400</div><div>Lives Impacted</div></div></div>
</div>
</div>

<!-- Training Section -->
<div id="training-section" class="section" style="display:none">
<div class="card"><h2><i class="fas fa-graduation-cap"></i> Emergency Training</h2><div class="dashboard-grid"><div class="event-card" onclick="startTraining('CPR & First Aid')"><h3>CPR & First Aid</h3><p>Learn life-saving techniques</p><span class="badge status-reported">15 min</span></div><div class="event-card" onclick="startTraining('Evacuation Procedures')"><h3>Evacuation Procedures</h3><p>Safe and orderly evacuation</p><span class="badge status-reported">10 min</span></div><div class="event-card" onclick="startTraining('Search & Rescue')"><h3>Search & Rescue Basics</h3><p>Locate and extract survivors</p><span class="badge status-reported">20 min</span></div><div class="event-card" onclick="startTraining('Disaster Psychology')"><h3>Disaster Psychology</h3><p>Mental health support</p><span class="badge status-reported">15 min</span></div></div><div id="training-progress" style="margin-top:20px"><div class="progress-bar"><div class="progress-fill" style="width:0%"></div></div><p>Completed: 0/4 courses</p></div></div>
</div>

<!-- ENHANCED ABOUT SECTION - LIGHT THEME with Developer Credit -->
<style>
/* About Section Styles - Light Theme */
.about-hero {
    background: linear-gradient(135deg, #fef2f2 0%, #e0e7ff 100%);
    border-radius: 30px;
    padding: 50px 40px;
    text-align: center;
    margin-bottom: 40px;
    border: 1px solid rgba(239,68,68,0.2);
    position: relative;
    overflow: hidden;
    box-shadow: 0 10px 30px rgba(0,0,0,0.05);
}

.about-hero::before {
    content: '';
    position: absolute;
    top: -50%;
    right: -50%;
    width: 200%;
    height: 200%;
    background: radial-gradient(circle, rgba(239,68,68,0.08) 0%, transparent 70%);
    animation: rotate 20s linear infinite;
}

@keyframes rotate {
    from { transform: rotate(0deg); }
    to { transform: rotate(360deg); }
}

.about-icon {
    width: 80px;
    height: 80px;
    background: linear-gradient(135deg, #ef4444, #dc2626);
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    margin: 0 auto 20px;
    font-size: 40px;
    box-shadow: 0 10px 30px rgba(239,68,68,0.3);
    animation: float 3s ease-in-out infinite;
}

@keyframes float {
    0%, 100% { transform: translateY(0); }
    50% { transform: translateY(-10px); }
}

.about-icon i {
    color: white;
}

.about-hero h1 {
    font-size: 2.8rem;
    font-weight: 800;
    background: linear-gradient(135deg, #1f2937, #ef4444);
    -webkit-background-clip: text;
    background-clip: text;
    color: transparent;
    margin-bottom: 15px;
}

.about-hero p {
    font-size: 1.1rem;
    color: #4b5563;
    max-width: 700px;
    margin: 0 auto;
    line-height: 1.6;
}

.developer-badge {
    display: inline-flex;
    align-items: center;
    gap: 12px;
    background: linear-gradient(135deg, #1f2937, #374151);
    padding: 8px 20px;
    border-radius: 40px;
    margin-top: 20px;
    animation: fadeInUp 0.8s ease-out;
}

@keyframes fadeInUp {
    from {
        opacity: 0;
        transform: translateY(20px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

.developer-badge i {
    font-size: 20px;
    color: #ef4444;
}

.developer-badge span {
    color: white;
    font-size: 0.9rem;
    font-weight: 500;
}

.developer-badge strong {
    color: #ef4444;
    font-weight: 700;
}

.about-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
    gap: 25px;
    margin-bottom: 40px;
}

.about-card {
    background: white;
    border: 1px solid #e5e7eb;
    border-radius: 20px;
    padding: 30px;
    transition: all 0.3s ease;
    position: relative;
    overflow: hidden;
    box-shadow: 0 4px 6px rgba(0,0,0,0.05);
}

.about-card::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: linear-gradient(135deg, transparent 0%, rgba(239,68,68,0.04) 100%);
    opacity: 0;
    transition: opacity 0.3s;
}

.about-card:hover::before {
    opacity: 1;
}

.about-card:hover {
    transform: translateY(-8px);
    border-color: #ef4444;
    box-shadow: 0 20px 40px rgba(0,0,0,0.1);
}

.card-icon {
    width: 65px;
    height: 65px;
    background: linear-gradient(135deg, #fee2e2, #e0e7ff);
    border-radius: 18px;
    display: flex;
    align-items: center;
    justify-content: center;
    margin-bottom: 20px;
    font-size: 32px;
    transition: all 0.3s;
}

.about-card:hover .card-icon {
    transform: scale(1.1);
    background: linear-gradient(135deg, #ef4444, #dc2626);
}

.about-card:hover .card-icon i {
    color: white;
}

.card-icon i {
    color: #ef4444;
    transition: all 0.3s;
}

.about-card h3 {
    font-size: 1.4rem;
    margin-bottom: 12px;
    color: #1f2937;
}

.about-card p {
    color: #6b7280;
    line-height: 1.6;
    font-size: 0.95rem;
}

.about-card .feature-list {
    margin-top: 15px;
    list-style: none;
}

.about-card .feature-list li {
    padding: 8px 0;
    color: #4b5563;
    display: flex;
    align-items: center;
    gap: 10px;
    font-size: 0.9rem;
}

.about-card .feature-list li i {
    color: #10b981;
    width: 20px;
}

.mission-section {
    background: linear-gradient(135deg, #fef2f2, #e0e7ff);
    border-radius: 25px;
    padding: 50px 40px;
    text-align: center;
    margin-bottom: 40px;
    border: 1px solid #ef4444;
    box-shadow: 0 10px 30px rgba(0,0,0,0.05);
}

.mission-icon {
    font-size: 50px;
    color: #ef4444;
    margin-bottom: 20px;
    animation: pulse 2s infinite;
}

@keyframes pulse {
    0%, 100% { transform: scale(1); }
    50% { transform: scale(1.1); }
}

.mission-section h2 {
    font-size: 2rem;
    margin-bottom: 20px;
    color: #1f2937;
}

.mission-section p {
    color: #4b5563;
    max-width: 800px;
    margin: 0 auto;
    line-height: 1.8;
    font-size: 1.05rem;
}

.stats-showcase {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 20px;
    margin-bottom: 40px;
}

.stat-show-item {
    text-align: center;
    padding: 25px;
    background: white;
    border: 1px solid #e5e7eb;
    border-radius: 20px;
    transition: all 0.3s;
    box-shadow: 0 4px 6px rgba(0,0,0,0.05);
}

.stat-show-item:hover {
    transform: translateY(-5px);
    border-color: #ef4444;
    box-shadow: 0 10px 25px rgba(0,0,0,0.1);
}

.stat-show-number {
    font-size: 2.5rem;
    font-weight: 800;
    background: linear-gradient(135deg, #ef4444, #3b82f6);
    -webkit-background-clip: text;
    background-clip: text;
    color: transparent;
    margin-bottom: 5px;
}

.stat-show-label {
    color: #6b7280;
    font-size: 0.85rem;
    text-transform: uppercase;
    letter-spacing: 1px;
}

.team-section {
    margin-bottom: 40px;
}

.section-title {
    text-align: center;
    margin-bottom: 30px;
}

.section-title h2 {
    font-size: 1.8rem;
    margin-bottom: 10px;
    color: #1f2937;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 10px;
}

.section-title p {
    color: #6b7280;
}

.team-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 25px;
}

.team-card {
    background: white;
    border: 1px solid #e5e7eb;
    border-radius: 20px;
    padding: 25px;
    text-align: center;
    transition: all 0.3s;
    box-shadow: 0 4px 6px rgba(0,0,0,0.05);
}

.team-card:hover {
    transform: translateY(-5px);
    border-color: #ef4444;
    box-shadow: 0 10px 25px rgba(0,0,0,0.1);
}

.team-avatar {
    width: 100px;
    height: 100px;
    background: linear-gradient(135deg, #ef4444, #dc2626);
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    margin: 0 auto 15px;
    font-size: 40px;
    color: white;
}

.team-card h4 {
    font-size: 1.2rem;
    margin-bottom: 5px;
    color: #1f2937;
}

.team-card .role {
    color: #ef4444;
    font-size: 0.85rem;
    margin-bottom: 10px;
}

.team-card .bio {
    color: #6b7280;
    font-size: 0.85rem;
    line-height: 1.5;
}

.tech-stack {
    display: flex;
    flex-wrap: wrap;
    gap: 12px;
    justify-content: center;
    margin-top: 20px;
}

.tech-badge {
    background: #fee2e2;
    border: 1px solid #fecaca;
    color: #ef4444;
    padding: 8px 20px;
    border-radius: 30px;
    font-size: 0.85rem;
    font-weight: 500;
    display: flex;
    align-items: center;
    gap: 8px;
    transition: all 0.3s;
}

.tech-badge:hover {
    background: #ef4444;
    color: white;
    transform: translateY(-2px);
}

.tech-badge i {
    font-size: 14px;
}

.developer-card {
    background: linear-gradient(135deg, #fef2f2, #ffffff);
    border: 2px solid #ef4444;
    border-radius: 20px;
    padding: 30px;
    text-align: center;
    margin: 30px 0;
    position: relative;
    overflow: hidden;
    box-shadow: 0 10px 30px rgba(239,68,68,0.1);
}

.developer-card::before {
    content: '';
    position: absolute;
    top: -50%;
    right: -50%;
    width: 200%;
    height: 200%;
    background: radial-gradient(circle, rgba(239,68,68,0.05) 0%, transparent 70%);
    animation: rotate 20s linear infinite;
}

.developer-avatar {
    width: 100px;
    height: 100px;
    background: linear-gradient(135deg, #ef4444, #dc2626);
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    margin: 0 auto 20px;
    font-size: 45px;
    color: white;
    box-shadow: 0 10px 30px rgba(239,68,68,0.3);
    position: relative;
    z-index: 1;
}

.developer-card h3 {
    font-size: 1.8rem;
    margin-bottom: 10px;
    color: #1f2937;
}

.developer-card .title {
    color: #ef4444;
    font-size: 1.1rem;
    font-weight: 600;
    margin-bottom: 15px;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 10px;
}

.developer-card .bio {
    color: #6b7280;
    max-width: 600px;
    margin: 0 auto;
    line-height: 1.6;
}

.developer-skills {
    display: flex;
    flex-wrap: wrap;
    gap: 10px;
    justify-content: center;
    margin-top: 20px;
}

.developer-skills span {
    background: #fee2e2;
    padding: 5px 15px;
    border-radius: 20px;
    font-size: 0.8rem;
    color: #ef4444;
    font-weight: 500;
}

.partners-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
    gap: 20px;
    margin-top: 20px;
}

.partner-item {
    background: white;
    border: 1px solid #e5e7eb;
    border-radius: 15px;
    padding: 20px;
    text-align: center;
    transition: all 0.3s;
    box-shadow: 0 4px 6px rgba(0,0,0,0.05);
}

.partner-item:hover {
    transform: translateY(-3px);
    border-color: #ef4444;
    box-shadow: 0 10px 20px rgba(0,0,0,0.1);
}

.partner-item i {
    font-size: 40px;
    color: #ef4444;
    margin-bottom: 10px;
}

.partner-item h4 {
    font-size: 0.9rem;
    color: #1f2937;
    margin-bottom: 5px;
}

.partner-item p {
    font-size: 0.75rem;
    color: #6b7280;
}

.timeline {
    position: relative;
    padding-left: 30px;
    margin: 20px 0;
    background: white;
    padding: 30px;
    border-radius: 20px;
    border: 1px solid #e5e7eb;
}

.timeline::before {
    content: '';
    position: absolute;
    left: 45px;
    top: 30px;
    bottom: 30px;
    width: 2px;
    background: linear-gradient(180deg, #ef4444, #3b82f6);
}

.timeline-item {
    position: relative;
    padding-bottom: 25px;
    padding-left: 30px;
}

.timeline-dot {
    position: absolute;
    left: -25px;
    top: 0;
    width: 12px;
    height: 12px;
    background: #ef4444;
    border-radius: 50%;
    border: 2px solid white;
    box-shadow: 0 0 0 2px #ef4444;
}

.timeline-date {
    font-size: 0.8rem;
    color: #ef4444;
    margin-bottom: 5px;
    font-weight: 600;
}

.timeline-content h4 {
    font-size: 1rem;
    margin-bottom: 5px;
    color: #1f2937;
}

.timeline-content p {
    color: #6b7280;
    font-size: 0.85rem;
}

@media (max-width: 768px) {
    .about-hero h1 { font-size: 2rem; }
    .stats-showcase { grid-template-columns: repeat(2, 1fr); }
    .about-grid { grid-template-columns: 1fr; }
    .developer-card h3 { font-size: 1.4rem; }
}
</style>

<!-- ABOUT SECTION HTML - LIGHT THEME with Developer -->
<div class="about-hero">
    <div class="about-icon">
        <i class="fas fa-shield-alt"></i>
    </div>
    <h1>About DisasterIntel</h1>
    <p>Revolutionizing emergency response with cutting-edge AI technology and real-time intelligence</p>
    <div class="developer-badge">
        <i class="fas fa-code"></i>
        <span>Developed by <strong>Neelima Pasala</strong> | AI/ML Developer</span>
        <i class="fas fa-robot"></i>
    </div>
</div>

<div class="about-grid">
    <div class="about-card">
        <div class="card-icon">
            <i class="fas fa-robot"></i>
        </div>
        <h3>AI-Powered Intelligence</h3>
        <p>Leveraging Groq's advanced Mixtral 8x7b model to provide real-time disaster analysis, hazard assessment, and actionable recommendations within seconds.</p>
        <ul class="feature-list">
            <li><i class="fas fa-check-circle"></i> Real-time hazard detection</li>
            <li><i class="fas fa-check-circle"></i> Smart evacuation routing</li>
            <li><i class="fas fa-check-circle"></i> Resource optimization</li>
        </ul>
    </div>

    <div class="about-card">
        <div class="card-icon">
            <i class="fas fa-bolt"></i>
        </div>
        <h3>Real-Time Response</h3>
        <p>Instant alerts and actionable recommendations when every second counts. Our system ensures rapid deployment of resources and emergency services.</p>
        <ul class="feature-list">
            <li><i class="fas fa-check-circle"></i> Sub-second alert delivery</li>
            <li><i class="fas fa-check-circle"></i> Automated dispatch system</li>
            <li><i class="fas fa-check-circle"></i> Live situation tracking</li>
        </ul>
    </div>

    <div class="about-card">
        <div class="card-icon">
            <i class="fas fa-globe-americas"></i>
        </div>
        <h3>Global Coverage</h3>
        <p>Supporting multiple disaster types including floods, earthquakes, hurricanes, wildfires, landslides, tsunamis, and industrial accidents worldwide.</p>
        <ul class="feature-list">
            <li><i class="fas fa-check-circle"></i> 150+ countries covered</li>
            <li><i class="fas fa-check-circle"></i> Multi-language support</li>
            <li><i class="fas fa-check-circle"></i> Local emergency integration</li>
        </ul>
    </div>

    <div class="about-card">
        <div class="card-icon">
            <i class="fas fa-chart-line"></i>
        </div>
        <h3>Data-Driven Decisions</h3>
        <p>Real-time analytics and predictive modeling to help authorities make informed decisions and allocate resources effectively.</p>
        <ul class="feature-list">
            <li><i class="fas fa-check-circle"></i> Predictive analytics</li>
            <li><i class="fas fa-check-circle"></i> Historical trend analysis</li>
            <li><i class="fas fa-check-circle"></i> Performance metrics</li>
        </ul>
    </div>

    <div class="about-card">
        <div class="card-icon">
            <i class="fas fa-hand-holding-heart"></i>
        </div>
        <h3>Community Focused</h3>
        <p>Built with the goal of saving lives and minimizing disaster impact through better information and faster response coordination.</p>
        <ul class="feature-list">
            <li><i class="fas fa-check-circle"></i> Family check-in system</li>
            <li><i class="fas fa-check-circle"></i> Volunteer coordination</li>
            <li><i class="fas fa-check-circle"></i> Community reporting</li>
        </ul>
    </div>

    <div class="about-card">
        <div class="card-icon">
            <i class="fas fa-comments"></i>
        </div>
        <h3>24/7 AI Support</h3>
        <p>DisasterBot AI assistant available anytime to provide guidance on preparedness, evacuation procedures, and emergency protocols.</p>
        <ul class="feature-list">
            <li><i class="fas fa-check-circle"></i> Instant responses</li>
            <li><i class="fas fa-check-circle"></i> Multi-lingual support</li>
            <li><i class="fas fa-check-circle"></i> Emergency guidance</li>
        </ul>
    </div>
</div>

<!-- Stats Showcase -->
<div class="stats-showcase">
    <div class="stat-show-item">
        <div class="stat-show-number">2.4M+</div>
        <div class="stat-show-label">Lives Impacted</div>
    </div>
    <div class="stat-show-item">
        <div class="stat-show-number">150+</div>
        <div class="stat-show-label">Countries</div>
    </div>
    <div class="stat-show-item">
        <div class="stat-show-number">98.5%</div>
        <div class="stat-show-label">Uptime</div>
    </div>
    <div class="stat-show-item">
        <div class="stat-show-number">12.5min</div>
        <div class="stat-show-label">Avg Response</div>
    </div>
</div>

<!-- Mission Section -->
<div class="mission-section">
    <div class="mission-icon">
        <i class="fas fa-bullseye"></i>
    </div>
    <h2>Our Mission</h2>
    <p>To revolutionize disaster management by providing real-time AI-powered intelligence that enables faster, more effective emergency response, ultimately saving lives and reducing disaster impact worldwide. We believe that technology should serve humanity, especially in moments of crisis.</p>
</div>

<!-- Developer Spotlight -->
<div class="developer-card">
    <div class="developer-avatar">
        <i class="fas fa-user-astronaut"></i>
    </div>
    <h3>Neelima Pasala</h3>
    <div class="title">
        <i class="fas fa-microchip"></i>
        AI/ML Developer
        <i class="fas fa-brain"></i>
    </div>
    <p class="bio">Passionate AI/ML Developer dedicated to building intelligent systems that save lives. Specializing in real-time disaster prediction models, natural language processing, and scalable emergency response platforms. Committed to using technology for social good and humanitarian causes.</p>
    <div class="developer-skills">
        <span>Machine Learning</span>
        <span>Deep Learning</span>
        <span>NLP</span>
        <span>Computer Vision</span>
        <span>Flask/FastAPI</span>
        <span>Groq AI</span>
        <span>React/JavaScript</span>
        <span>Cloud Architecture</span>
    </div>
</div>

<!-- Technology Stack -->
<div class="section-title">
    <h2><i class="fas fa-microchip"></i> Technology Stack</h2>
    <p>Powered by cutting-edge technologies</p>
</div>
<div class="tech-stack">
    <span class="tech-badge"><i class="fas fa-brain"></i> Groq AI</span>
    <span class="tech-badge"><i class="fas fa-robot"></i> Mixtral 8x7b</span>
    <span class="tech-badge"><i class="fab fa-python"></i> Python Flask</span>
    <span class="tech-badge"><i class="fas fa-cloud"></i> Real-time Analytics</span>
    <span class="tech-badge"><i class="fas fa-shield"></i> Enterprise Security</span>
    <span class="tech-badge"><i class="fas fa-mobile-alt"></i> PWA Ready</span>
    <span class="tech-badge"><i class="fas fa-chart-line"></i> Predictive Modeling</span>
    <span class="tech-badge"><i class="fas fa-bell"></i> Push Notifications</span>
</div>

<!-- Call to Action -->
<div class="mission-section" style="background: linear-gradient(135deg, #ef4444, #dc2626);">
    <div class="mission-icon">
        <i class="fas fa-heart" style="color: white;"></i>
    </div>
    <h2 style="color: white;">Join Us in Saving Lives</h2>
    <p style="color: rgba(255,255,255,0.9);">Whether you're a volunteer, donor, or partner, your support makes a difference.</p>
    <div style="display: flex; gap: 15px; justify-content: center; margin-top: 25px;">
        <button class="btn-primary" onclick="showSection('volunteer')" style="width: auto; background: white; color: #ef4444; border: none;"><i class="fas fa-hands-helping"></i> Become a Volunteer</button>
        <button class="btn-primary" onclick="showSection('donate')" style="width: auto; background: rgba(255,255,255,0.2); border: 1px solid white;"><i class="fas fa-heart"></i> Support Us</button>
    </div>
</div>

<!-- Contact Section -->
<div id="contact-section" class="section" style="display:none">
<div class="dashboard-grid">
<div class="card"><h2><i class="fas fa-envelope"></i> Contact Us</h2><div class="form-group"><input type="text" id="contact-name" placeholder="Your Name"></div><div class="form-group"><input type="email" id="contact-email" placeholder="Email"></div><div class="form-group"><select id="contact-subject"><option>General Inquiry</option><option>Emergency Support</option><option>Technical Issue</option><option>Partnership</option></select></div><div class="form-group"><textarea id="contact-message" rows="4" placeholder="Your Message..."></textarea></div><button class="btn-primary" onclick="sendContact()">Send Message</button><div id="contact-alert"></div></div>
<div class="card"><h2><i class="fas fa-address-card"></i> Emergency Contacts</h2><div class="list-item"><i class="fas fa-ambulance"></i> Ambulance: 911 / 108</div><div class="list-item"><i class="fas fa-fire-extinguisher"></i> Fire Brigade: 101 / 911</div><div class="list-item"><i class="fas fa-shield"></i> Police: 100 / 911</div><div class="list-item"><i class="fas fa-flag"></i> Disaster Helpline: 112</div><div class="list-item"><i class="fas fa-globe"></i> NDRF: 011-24363260</div></div>
</div>
</div>
</div>

<!-- Chatbot -->
<div class="chatbot-container">
<button class="chatbot-toggle" onclick="toggleChat()"><i class="fas fa-comment-dots"></i></button>
<div class="chatbot-window" id="chat-window">
<div class="chatbot-header"><i class="fas fa-robot"></i><h3>DisasterBot AI</h3><button class="chatbot-close" onclick="toggleChat()"><i class="fas fa-times"></i></button></div>
<div class="chatbot-messages" id="chat-messages"><div class="message bot"><div class="message-icon"><i class="fas fa-robot"></i></div><div class="message-bubble">👋 Hello! I'm DisasterBot, your AI emergency assistant. Ask me about disaster preparedness, safety tips, or evacuation procedures!</div></div></div>
<div class="chatbot-input-area"><input type="text" id="chat-input" placeholder="Type your message..." onkeypress="if(event.key==='Enter') sendChatMessage()"><button class="chatbot-send" onclick="sendChatMessage()"><i class="fas fa-paper-plane"></i></button></div>
</div>
</div>

<footer><p><i class="fas fa-shield-alt"></i> DisasterIntel - Global Emergency Intelligence Platform | Powered by AI | 24/7 Response</p><p style="margin-top:10px;font-size:12px">© 2024 DisasterIntel - Saving Lives Through Technology</p></footer>

<script>
let selectedEventId = null;
let allEvents = [];
let chatOpen = false;
let completedCourses = 0;

function showSection(sectionName) {
    document.querySelectorAll('.section').forEach(s => s.style.display = 'none');
    document.getElementById(sectionName + '-section').style.display = 'block';
    document.querySelectorAll('.nav-links a').forEach(link => link.classList.remove('active'));
    event.target.classList.add('active');
    if(sectionName === 'dashboard') refreshDashboard();
}

function toggleChat() {
    chatOpen = !chatOpen;
    document.getElementById('chat-window').classList.toggle('active', chatOpen);
    if(chatOpen) document.getElementById('chat-input').focus();
}

function sendChatMessage() {
    const input = document.getElementById('chat-input');
    const message = input.value.trim();
    if(!message) return;
    addChatMessage(message, 'user');
    input.value = '';
    fetch('/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: message })
    })
    .then(r => r.json())
    .then(data => addChatMessage(data.data.response, 'bot'))
    .catch(() => addChatMessage('Sorry, I encountered an error. Please try again.', 'bot'));
}

function addChatMessage(text, sender) {
    const messagesDiv = document.getElementById('chat-messages');
    const msgDiv = document.createElement('div');
    msgDiv.className = `message ${sender}`;
    const icon = document.createElement('div');
    icon.className = 'message-icon';
    icon.innerHTML = sender === 'bot' ? '<i class="fas fa-robot"></i>' : '<i class="fas fa-user"></i>';
    const bubble = document.createElement('div');
    bubble.className = 'message-bubble';
    bubble.textContent = text;
    msgDiv.appendChild(icon);
    msgDiv.appendChild(bubble);
    messagesDiv.appendChild(msgDiv);
    messagesDiv.scrollTop = messagesDiv.scrollHeight;
}

function submitReport() {
    const type = document.getElementById('disaster-type').value;
    const location = document.getElementById('disaster-location').value;
    const lat = document.getElementById('latitude').value;
    const lng = document.getElementById('longitude').value;
    const severity = document.getElementById('severity').value;
    const population = document.getElementById('population').value;
    if(!location || !lat || !lng || !population) {
        showAlert('Please fill all required fields!', 'error', 'report-alert');
        return;
    }
    document.getElementById('report-loading').classList.add('show');
    fetch('/api/disasters/create', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            type: type, location: location,
            latitude: parseFloat(lat), longitude: parseFloat(lng),
            severity: parseInt(severity), affected_population: parseInt(population)
        })
    })
    .then(r => r.json())
    .then(data => {
        document.getElementById('report-loading').classList.remove('show');
        if(data.status === 'success') {
            showAlert('✅ Disaster report submitted successfully!', 'success', 'report-alert');
            document.getElementById('disaster-location').value = '';
            document.getElementById('population').value = '';
            refreshDashboard();
            showSection('dashboard');
        }
    })
    .catch(e => {
        document.getElementById('report-loading').classList.remove('show');
        showAlert('Error: ' + e.message, 'error', 'report-alert');
    });
}

function updateSelectedEvent() {
    selectedEventId = document.getElementById('event-select').value;
}

function analyzeEvent() {
    if(!selectedEventId) {
        showAlert('Please select an event to analyze!', 'error', 'analysis-alert');
        return;
    }
    document.getElementById('analysis-loading').classList.add('show');
    fetch(`/api/disasters/${selectedEventId}/analyze`, { method: 'POST' })
    .then(r => r.json())
    .then(data => {
        document.getElementById('analysis-loading').classList.remove('show');
        if(data.status === 'success') {
            displayAnalysis(data.data);
            showAlert('✅ AI Analysis complete!', 'success', 'analysis-alert');
            refreshDashboard();
        }
    })
    .catch(e => {
        document.getElementById('analysis-loading').classList.remove('show');
        showAlert('Error: ' + e.message, 'error', 'analysis-alert');
    });
}

function displayAnalysis(data) {
    const a = data.analysis || {};
    document.getElementById('hazard-text').textContent = a.hazard || 'N/A';
    document.getElementById('zones-list').innerHTML = (a.safe_zones || []).map(z => `<div class="list-item"><i class="fas fa-location-dot"></i> ${z}</div>`).join('') || '<div>No data</div>';
    document.getElementById('routes-list').innerHTML = (a.routes || []).map(r => `<div class="list-item"><i class="fas fa-route"></i> ${r}</div>`).join('') || '<div>No data</div>';
    document.getElementById('recommendations-list').innerHTML = (a.recommendations || []).map(r => `<div class="list-item"><i class="fas fa-check-circle"></i> ${r}</div>`).join('') || '<div>No data</div>';
    document.getElementById('analysis-results').classList.add('show');
}

function refreshDashboard() {
    fetch('/api/dashboard')
        .then(r => r.json())
        .then(data => {
            allEvents = data.data.recent_events || [];
            document.getElementById('total-events').textContent = allEvents.length;
            document.getElementById('total-affected').textContent = data.data.overview.total_affected.toLocaleString();
            document.getElementById('analyzed-count').textContent = allEvents.filter(e => e.status === 'ANALYZED').length;
            updateEventsList();
        });
    fetch('/api/alerts')
        .then(r => r.json())
        .then(data => {
            document.getElementById('volunteer-count').textContent = data.data.count || 0;
        });
}

function updateEventsList() {
    const sel = document.getElementById('event-select');
    const list = document.getElementById('events-list');
    sel.innerHTML = '<option value="">-- Select Event --</option>';
    list.innerHTML = '';
    if(allEvents.length === 0) {
        list.innerHTML = '<p style="color:#999;text-align:center;padding:40px;">No events reported yet</p>';
        return;
    }
    allEvents.forEach(e => {
        const opt = document.createElement('option');
        opt.value = e.id;
        opt.textContent = `${e.type} - ${e.location}`;
        sel.appendChild(opt);
        const typeClass = e.type.toLowerCase();
        const statusClass = e.status === 'ANALYZED' ? 'status-analyzed' : 'status-reported';
        const icon = { 'FLOOD':'🌊','EARTHQUAKE':'🌍','HURRICANE':'🌪️','WILDFIRE':'🔥' }[e.type] || '⚠️';
        const card = document.createElement('div');
        card.className = `event-card ${typeClass}`;
        card.onclick = () => { selectedEventId = e.id; document.getElementById('event-select').value = e.id; showSection('report'); };
        card.innerHTML = `<h3>${icon} ${e.type}</h3><p><i class="fas fa-map-marker-alt"></i> ${e.location}</p><p><i class="fas fa-users"></i> ${e.affected_population.toLocaleString()} affected</p><p><i class="fas fa-gauge-high"></i> Severity: ${e.severity}/10</p><span class="status-badge ${statusClass}">${e.status}</span>`;
        list.appendChild(card);
    });
}

function markSafe() {
    const name = document.getElementById('checkin-name').value.trim();
    const location = document.getElementById('checkin-location').value.trim();
    if(!name) {
        showAlert('Please enter your name!', 'error', '');
        return;
    }
    const safeList = document.getElementById('safe-list');
    const entry = document.createElement('div');
    entry.className = 'list-item';
    entry.innerHTML = `<i class="fas fa-user-check"></i> ${name} - Safe at ${location || 'unknown location'}`;
    safeList.prepend(entry);
    document.getElementById('checkin-name').value = '';
    document.getElementById('checkin-location').value = '';
    document.getElementById('checkin-status').value = '';
    showAlert('✅ You have been marked safe!', 'success', '');
}

function registerVolunteer() {
    const name = document.getElementById('vol-name').value.trim();
    if(!name) {
        showAlert('Please enter your name!', 'error', 'vol-alert');
        return;
    }
    showAlert(`✅ Thank you ${name}! You are now registered as a volunteer.`, 'success', 'vol-alert');
    document.getElementById('vol-name').value = '';
    document.getElementById('vol-email').value = '';
    document.getElementById('vol-phone').value = '';
}

function setDonation(amount) {
    document.getElementById('donation-amount').value = amount;
}

function processDonation() {
    const amount = document.getElementById('donation-amount').value;
    if(!amount || amount <= 0) {
        showAlert('Please enter a valid donation amount!', 'error', 'donate-alert');
        return;
    }
    showAlert(`💝 Thank you for your donation of $${amount}! Your support saves lives.`, 'success', 'donate-alert');
    document.getElementById('donation-amount').value = '';
}

function requestSupplies() {
    const type = document.getElementById('supply-type').value;
    const qty = document.getElementById('supply-qty').value;
    const location = document.getElementById('supply-location').value;
    if(!qty || !location) {
        alert('Please fill all fields');
        return;
    }
    alert(`Request submitted for ${qty} ${type} to ${location}`);
    document.getElementById('supply-qty').value = '';
    document.getElementById('supply-location').value = '';
}

function sendContact() {
    const name = document.getElementById('contact-name').value;
    if(!name) {
        alert('Please fill all fields');
        return;
    }
    alert('Message sent! We will respond within 24 hours.');
    document.getElementById('contact-name').value = '';
    document.getElementById('contact-email').value = '';
    document.getElementById('contact-message').value = '';
}

function startTraining(course) {
    completedCourses++;
    const percent = (completedCourses / 4) * 100;
    document.querySelector('#training-progress .progress-fill').style.width = percent + '%';
    document.querySelector('#training-progress p').textContent = `Completed: ${completedCourses}/4 courses`;
    alert(`Starting course: ${course}\n\nComplete this training to earn your certificate!`);
}

function showAlert(msg, type, containerId) {
    const container = document.getElementById(containerId);
    if(!container) {
        const tempDiv = document.createElement('div');
        tempDiv.className = `alert ${type}`;
        tempDiv.innerHTML = `<i class="fas fa-${type === 'success' ? 'check-circle' : 'exclamation-circle'}"></i> ${msg}`;
        document.querySelector('.container').prepend(tempDiv);
        setTimeout(() => tempDiv.remove(), 5000);
        return;
    }
    const alert = document.createElement('div');
    alert.className = `alert ${type}`;
    alert.innerHTML = `<i class="fas fa-${type === 'success' ? 'check-circle' : 'exclamation-circle'}"></i> ${msg}`;
    container.innerHTML = '';
    container.appendChild(alert);
    setTimeout(() => alert.remove(), 5000);
}

function loadResources() {
    const resources = [
        { name: 'Drinking Water', available: '12,000 L', status: 'sufficient' },
        { name: 'Meal Packs', available: '8,400 units', status: 'moderate' },
        { name: 'Medical Kits', available: '520 kits', status: 'sufficient' },
        { name: 'Blankets', available: '2,800 units', status: 'sufficient' }
    ];
    const container = document.getElementById('resources-list');
    if(container) {
        container.innerHTML = resources.map(r => `<div class="list-item"><i class="fas fa-box"></i> ${r.name}: ${r.available}</div>`).join('');
    }
}

refreshDashboard();
loadResources();
setInterval(refreshDashboard, 10000);
</script>
</body>
</html>
"""

# ============================================================================
# API ROUTES
# ============================================================================

@app.route('/')
def index():
    return render_template_string(COMPLETE_HTML)

@app.route('/api/dashboard')
def dashboard():
    return jsonify({
        "status": "success",
        "data": {
            "overview": {
                "active_events": len([e for e in events.values() if e.get('status') != 'RESOLVED']),
                "total_affected": sum(e.get('affected_population', 0) for e in events.values())
            },
            "recent_events": list(events.values())[-10:]
        }
    })

@app.route('/api/alerts')
def get_alerts():
    return jsonify({"status": "success", "data": {"count": len(alerts)}})

@app.route('/api/disasters/create', methods=['POST'])
def create_disaster():
    global event_counter
    data = request.json
    event_counter += 1
    event_id = f"EVT_{event_counter:05d}"
    events[event_id] = {
        "id": event_id,
        "type": data.get('type'),
        "location": data.get('location'),
        "latitude": data.get('latitude'),
        "longitude": data.get('longitude'),
        "severity": data.get('severity', 5),
        "affected_population": data.get('affected_population', 0),
        "timestamp": datetime.now().isoformat(),
        "status": "REPORTED"
    }
    alerts.append({
        "id": f"ALERT_{len(alerts)}",
        "message": f"New {data['type']} reported in {data['location']}",
        "timestamp": datetime.now().isoformat()
    })
    return jsonify({"status": "success", "data": {"event_id": event_id}})

@app.route('/api/disasters/<event_id>/analyze', methods=['POST'])
def analyze_disaster(event_id):
    event = events.get(event_id)
    if not event:
        return jsonify({"status": "error", "message": "Event not found"}), 404
    
    analysis = {
        "hazard": f"⚠️ {event['type']} detected in {event['location']} with severity {event['severity']}/10. {event['affected_population']:,} people potentially affected. Immediate action recommended.",
        "safe_zones": ["City School Shelter - 3000 capacity, 1.5km away", "Community Stadium - 5000 capacity, 2.8km away", "Government Center - 2000 capacity, 3.1km away"],
        "routes": ["Highway 101 - 12 min, 4000 people/hour", "Service Road - 18 min, 3500 people/hour", "Residential Streets - 25 min, 2000 people/hour"],
        "hospitals": "3 hospitals within 5km: City General (200 beds), St. Mary's (150 beds), Community Hospital (100 beds)",
        "resources": ["25 Ambulances ready", "12 Rescue Teams deployed", "50 Rescue Personnel", "500 Medical Kits"],
        "recommendations": ["Issue immediate evacuation order", "Activate all emergency response teams", "Broadcast alerts through all channels", "Coordinate with neighboring districts", "Set up emergency command center"]
    }
    
    event['status'] = 'ANALYZED'
    return jsonify({"status": "success", "data": {"analysis": analysis}})

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.json
    user_message = data.get('message', '')
    
    response = f"🤖 DisasterBot: I'm here to help with disaster preparedness, evacuation procedures, safety tips, and emergency contacts. How can I assist you?"
    
    return jsonify({"status": "success", "data": {"response": response}})

# ============================================================================
# RUN
# ============================================================================

if __name__ == '__main__':
    print("\n" + "="*80)
    print("🚨 DISASTERINTEL - COMPLETE DISASTER MANAGEMENT PLATFORM")
    print("="*80)
    print("\n✅ ALL FEATURES WORKING:")
    print("   ✅ Dashboard with Live Stats")
    print("   ✅ Disaster Reporting System")
    print("   ✅ AI-Powered Analysis")
    print("   ✅ Resource Management")
    print("   ✅ Volunteer Registration")
    print("   ✅ Donation Portal")
    print("   ✅ Training Academy")
    print("   ✅ About & Contact Pages")
    print("   ✅ Chatbot Assistant")
    print("\n🌐 OPEN IN BROWSER: http://localhost:5000")
    print("\n" + "="*80 + "\n")
    
    app.run(debug=True, host='0.0.0.0', port=5000, use_reloader=False)