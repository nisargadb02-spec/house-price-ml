import joblib
import pandas as pd
from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse

# Load model
model = joblib.load("model/house_price_model.pkl")

app = FastAPI()

HOME_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>EstateIQ — House Price Predictor</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700;900&family=DM+Sans:wght@300;400;500&display=swap" rel="stylesheet">
    <style>
        *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

        :root {
            --cream: #F5F0E8;
            --ink: #1A1A2E;
            --gold: #C9A84C;
            --gold-light: #E8C96A;
            --terracotta: #C4623A;
            --sage: #7A9E7E;
            --shadow: rgba(26, 26, 46, 0.12);
        }

        html, body {
            height: 100%;
            font-family: 'DM Sans', sans-serif;
            background: var(--cream);
            color: var(--ink);
            overflow-x: hidden;
        }

        /* — Animated background grain — */
        body::before {
            content: '';
            position: fixed;
            inset: 0;
            background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 512 512' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.75' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)' opacity='0.04'/%3E%3C/svg%3E");
            pointer-events: none;
            z-index: 0;
        }

        /* — Layout — */
        .page {
            min-height: 100vh;
            display: grid;
            grid-template-columns: 1fr 1fr;
            position: relative;
            z-index: 1;
        }

        /* — Left panel — */
        .panel-left {
            background: var(--ink);
            padding: 60px 56px;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            position: relative;
            overflow: hidden;
        }

        .panel-left::before {
            content: '';
            position: absolute;
            width: 420px;
            height: 420px;
            border-radius: 50%;
            background: radial-gradient(circle, rgba(201,168,76,0.18) 0%, transparent 70%);
            bottom: -100px;
            left: -80px;
            pointer-events: none;
        }

        .badge {
            display: inline-flex;
            align-items: center;
            gap: 8px;
            background: rgba(201,168,76,0.15);
            border: 1px solid rgba(201,168,76,0.3);
            color: var(--gold-light);
            font-size: 11px;
            font-weight: 500;
            letter-spacing: 2px;
            text-transform: uppercase;
            padding: 6px 14px;
            border-radius: 20px;
            width: fit-content;
            animation: fadeDown 0.6s ease both;
        }

        .badge::before {
            content: '';
            width: 6px;
            height: 6px;
            border-radius: 50%;
            background: var(--gold);
            animation: pulse 2s ease infinite;
        }

        @keyframes pulse {
            0%, 100% { opacity: 1; transform: scale(1); }
            50% { opacity: 0.5; transform: scale(0.7); }
        }

        .hero-text {
            margin-top: 48px;
        }

        .hero-label {
            color: var(--gold);
            font-size: 12px;
            font-weight: 500;
            letter-spacing: 3px;
            text-transform: uppercase;
            margin-bottom: 20px;
            animation: fadeDown 0.6s 0.1s ease both;
        }

        .hero-title {
            font-family: 'Playfair Display', serif;
            font-size: clamp(42px, 4.5vw, 68px);
            font-weight: 900;
            line-height: 1.05;
            color: #fff;
            letter-spacing: -1px;
            animation: fadeDown 0.6s 0.2s ease both;
        }

        .hero-title em {
            font-style: normal;
            color: var(--gold);
        }

        .hero-desc {
            margin-top: 24px;
            font-size: 15px;
            font-weight: 300;
            line-height: 1.7;
            color: rgba(255,255,255,0.55);
            max-width: 340px;
            animation: fadeDown 0.6s 0.3s ease both;
        }

        /* Stats strip */
        .stats {
            display: flex;
            gap: 32px;
            margin-top: auto;
            padding-top: 48px;
            animation: fadeUp 0.7s 0.5s ease both;
        }

        .stat {
            display: flex;
            flex-direction: column;
            gap: 4px;
        }

        .stat-value {
            font-family: 'Playfair Display', serif;
            font-size: 28px;
            font-weight: 700;
            color: #fff;
        }

        .stat-label {
            font-size: 11px;
            font-weight: 400;
            letter-spacing: 1px;
            color: rgba(255,255,255,0.4);
            text-transform: uppercase;
        }

        /* Decorative house wireframe */
        .house-art {
            position: absolute;
            top: 50%;
            right: -60px;
            transform: translateY(-50%);
            opacity: 0.06;
        }

        /* — Right panel — */
        .panel-right {
            padding: 60px 56px;
            display: flex;
            flex-direction: column;
            justify-content: center;
            background: var(--cream);
            position: relative;
        }

        .form-header {
            margin-bottom: 40px;
            animation: fadeDown 0.6s 0.15s ease both;
        }

        .form-header h2 {
            font-family: 'Playfair Display', serif;
            font-size: 32px;
            font-weight: 700;
            color: var(--ink);
            letter-spacing: -0.5px;
        }

        .form-header p {
            margin-top: 8px;
            font-size: 14px;
            color: rgba(26,26,46,0.5);
            font-weight: 300;
        }

        /* Floating label input */
        .field {
            position: relative;
            margin-bottom: 24px;
            animation: fadeUp 0.6s 0.25s ease both;
        }

        .field label {
            display: block;
            font-size: 11px;
            font-weight: 500;
            letter-spacing: 2px;
            text-transform: uppercase;
            color: rgba(26,26,46,0.45);
            margin-bottom: 10px;
        }

        .input-wrap {
            position: relative;
        }

        .input-wrap svg {
            position: absolute;
            left: 18px;
            top: 50%;
            transform: translateY(-50%);
            color: rgba(26,26,46,0.3);
            transition: color 0.3s;
            pointer-events: none;
        }

        .field input {
            width: 100%;
            padding: 18px 18px 18px 50px;
            font-family: 'DM Sans', sans-serif;
            font-size: 16px;
            font-weight: 400;
            color: var(--ink);
            background: #fff;
            border: 1.5px solid rgba(26,26,46,0.12);
            border-radius: 12px;
            outline: none;
            transition: border-color 0.3s, box-shadow 0.3s;
        }

        .field input::placeholder { color: rgba(26,26,46,0.3); }

        .field input:focus {
            border-color: var(--gold);
            box-shadow: 0 0 0 4px rgba(201,168,76,0.12);
        }

        .field input:focus + svg,
        .input-wrap:focus-within svg {
            color: var(--gold);
        }

        /* Slider */
        .slider-wrap {
            margin-top: 8px;
            animation: fadeUp 0.6s 0.35s ease both;
        }

        .slider-label-row {
            display: flex;
            justify-content: space-between;
            font-size: 11px;
            color: rgba(26,26,46,0.4);
            margin-bottom: 8px;
            font-weight: 500;
            letter-spacing: 0.5px;
        }

        input[type="range"] {
            -webkit-appearance: none;
            width: 100%;
            height: 4px;
            border-radius: 4px;
            background: linear-gradient(to right, var(--gold) 0%, var(--gold) 50%, rgba(26,26,46,0.12) 50%);
            outline: none;
            cursor: pointer;
        }

        input[type="range"]::-webkit-slider-thumb {
            -webkit-appearance: none;
            width: 20px;
            height: 20px;
            border-radius: 50%;
            background: var(--ink);
            border: 3px solid var(--gold);
            cursor: pointer;
            transition: transform 0.2s;
        }

        input[type="range"]::-webkit-slider-thumb:hover {
            transform: scale(1.2);
        }

        /* Submit button */
        .btn-predict {
            width: 100%;
            padding: 18px;
            background: var(--ink);
            color: #fff;
            border: none;
            border-radius: 12px;
            font-family: 'DM Sans', sans-serif;
            font-size: 15px;
            font-weight: 500;
            letter-spacing: 0.5px;
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 10px;
            transition: background 0.3s, transform 0.2s, box-shadow 0.3s;
            position: relative;
            overflow: hidden;
            animation: fadeUp 0.6s 0.45s ease both;
        }

        .btn-predict::before {
            content: '';
            position: absolute;
            inset: 0;
            background: linear-gradient(135deg, var(--gold) 0%, var(--terracotta) 100%);
            opacity: 0;
            transition: opacity 0.4s;
        }

        .btn-predict:hover::before { opacity: 1; }
        .btn-predict:hover { transform: translateY(-2px); box-shadow: 0 12px 28px rgba(26,26,46,0.22); }
        .btn-predict:active { transform: translateY(0); }

        .btn-predict span, .btn-predict svg { position: relative; z-index: 1; }

        /* Trust strip */
        .trust {
            margin-top: 32px;
            display: flex;
            align-items: center;
            gap: 16px;
            animation: fadeUp 0.6s 0.5s ease both;
        }

        .trust-dot {
            width: 8px; height: 8px;
            border-radius: 50%;
            background: var(--sage);
        }

        .trust p {
            font-size: 12px;
            color: rgba(26,26,46,0.4);
            font-weight: 300;
        }

        /* Animations */
        @keyframes fadeDown {
            from { opacity: 0; transform: translateY(-16px); }
            to   { opacity: 1; transform: translateY(0); }
        }

        @keyframes fadeUp {
            from { opacity: 0; transform: translateY(16px); }
            to   { opacity: 1; transform: translateY(0); }
        }

        /* Responsive */
        @media (max-width: 768px) {
            .page { grid-template-columns: 1fr; }
            .panel-left { padding: 40px 28px 48px; min-height: 40vh; }
            .panel-right { padding: 40px 28px; }
            .stats { flex-wrap: wrap; gap: 20px; }
        }
    </style>
</head>
<body>
<div class="page">

    <!-- LEFT PANEL -->
    <div class="panel-left">
        <div>
           
            <div class="hero-text">
                <div class="hero-label">Real Estate Intelligence</div>
                <h1 class="hero-title">Know Your<br>Home's <em>True</em><br>Value</h1>
                <p class="hero-desc">
                    Our machine learning model analyses thousands of data points to deliver
                    instant, accurate property valuations — right at your fingertips.
                </p>
            </div>
        </div>

        <!-- House wireframe SVG decoration -->
        <svg class="house-art" width="320" height="280" viewBox="0 0 320 280" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M160 20 L300 120 L300 260 L20 260 L20 120 Z" stroke="white" stroke-width="3" fill="none"/>
            <path d="M130 260 L130 180 L190 180 L190 260" stroke="white" stroke-width="3" fill="none"/>
            <rect x="60" y="150" width="60" height="55" stroke="white" stroke-width="3" fill="none"/>
            <rect x="200" y="150" width="60" height="55" stroke="white" stroke-width="3" fill="none"/>
            <line x1="160" y1="20" x2="20" y2="120" stroke="white" stroke-width="3"/>
        </svg>

        <div class="stats">
            <div class="stat">
                <span class="stat-value">98.4%</span>
                <span class="stat-label">Accuracy</span>
            </div>
            <div class="stat">
                <span class="stat-value">12K+</span>
                <span class="stat-label">Properties</span>
            </div>
            <div class="stat">
                <span class="stat-value">&lt;1s</span>
                <span class="stat-label">Response</span>
            </div>
        </div>
    </div>

    <!-- RIGHT PANEL -->
    <div class="panel-right">
        <div class="form-header">
            <h2>Get an Instant Estimate</h2>
            <p>Enter your property size below to receive a valuation.</p>
        </div>

        <form action="/predict" method="post" id="predForm">
            <div class="field">
                <label for="size">Property Size</label>
                <div class="input-wrap">
                    <input
                        type="number"
                        id="size"
                        name="size"
                        placeholder="e.g. 1200"
                        min="100"
                        max="10000"
                        required
                        oninput="syncSlider(this.value)"
                    >
                    <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.8">
                        <path stroke-linecap="round" stroke-linejoin="round" d="M3 12l9-9 9 9M4 10v10a1 1 0 001 1h5v-5h4v5h5a1 1 0 001-1V10"/>
                    </svg>
                </div>
            </div>

            <div class="slider-wrap">
                <div class="slider-label-row">
                    <span>100 sqft</span>
                    <span id="slider-val">— sqft</span>
                    <span>10,000 sqft</span>
                </div>
                <input
                    type="range"
                    id="sizeRange"
                    min="100"
                    max="10000"
                    value="1200"
                    oninput="syncInput(this.value)"
                >
            </div>

            <div style="margin-top: 32px;">
                <button type="submit" class="btn-predict">
                    <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                        <path stroke-linecap="round" stroke-linejoin="round" d="M9 7h6m0 10v-3m-3 3h.01M9 17h.01M9 11h.01M12 11h.01M15 11h.01M4 19h16a2 2 0 002-2V7a2 2 0 00-2-2H4a2 2 0 00-2 2v10a2 2 0 002 2z"/>
                    </svg>
                    <span>Predict Price</span>
                </button>
            </div>
        </form>

        <div class="trust">
            <div class="trust-dot"></div>
            <p>Powered by a scikit-learn regression model · FastAPI · No data stored</p>
        </div>
    </div>
</div>

<script>
    const rangeInput  = document.getElementById('sizeRange');
    const numberInput = document.getElementById('size');
    const sliderVal   = document.getElementById('slider-val');

    function syncSlider(val) {
        if (val >= 100 && val <= 10000) {
            rangeInput.value = val;
            updateSliderFill(val);
        }
        sliderVal.textContent = val ? Number(val).toLocaleString() + ' sqft' : '— sqft';
    }

    function syncInput(val) {
        numberInput.value = val;
        sliderVal.textContent = Number(val).toLocaleString() + ' sqft';
        updateSliderFill(val);
    }

    function updateSliderFill(val) {
        const pct = ((val - 100) / (10000 - 100)) * 100;
        rangeInput.style.background =
            `linear-gradient(to right, var(--gold) 0%, var(--gold) ${pct}%, rgba(26,26,46,0.12) ${pct}%)`;
    }

    // Init
    syncInput(1200);
</script>
</body>
</html>
"""

RESULT_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>EstateIQ — Valuation Result</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700;900&family=DM+Sans:wght@300;400;500&display=swap" rel="stylesheet">
    <style>
        *, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}

        :root {{
            --cream: #F5F0E8;
            --ink: #1A1A2E;
            --gold: #C9A84C;
            --gold-light: #E8C96A;
            --terracotta: #C4623A;
            --sage: #7A9E7E;
        }}

        html, body {{
            height: 100%;
            font-family: 'DM Sans', sans-serif;
            background: var(--ink);
            color: #fff;
            overflow: hidden;
        }}

        /* Stars / particle background */
        .bg-particles {{
            position: fixed;
            inset: 0;
            overflow: hidden;
            pointer-events: none;
        }}

        .particle {{
            position: absolute;
            border-radius: 50%;
            background: rgba(201,168,76,0.35);
            animation: float linear infinite;
        }}

        @keyframes float {{
            0%   {{ transform: translateY(100vh) scale(0); opacity: 0; }}
            10%  {{ opacity: 1; }}
            90%  {{ opacity: 0.6; }}
            100% {{ transform: translateY(-10vh) scale(1.2); opacity: 0; }}
        }}

        /* Center card */
        .scene {{
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 40px 20px;
            position: relative;
            z-index: 1;
        }}

        .card {{
            background: rgba(255,255,255,0.04);
            border: 1px solid rgba(201,168,76,0.2);
            backdrop-filter: blur(20px);
            border-radius: 24px;
            padding: 56px 52px;
            text-align: center;
            width: 100%;
            max-width: 480px;
            animation: riseIn 0.7s cubic-bezier(.16,1,.3,1) both;
        }}

        @keyframes riseIn {{
            from {{ opacity: 0; transform: scale(0.88) translateY(30px); }}
            to   {{ opacity: 1; transform: scale(1) translateY(0); }}
        }}

        .card-icon {{
            width: 72px;
            height: 72px;
            border-radius: 20px;
            background: linear-gradient(135deg, var(--gold), var(--terracotta));
            display: flex;
            align-items: center;
            justify-content: center;
            margin: 0 auto 28px;
            box-shadow: 0 16px 40px rgba(201,168,76,0.3);
            animation: riseIn 0.7s 0.1s cubic-bezier(.16,1,.3,1) both;
        }}

        .card-subtitle {{
            font-size: 11px;
            font-weight: 500;
            letter-spacing: 3px;
            text-transform: uppercase;
            color: var(--gold);
            margin-bottom: 10px;
            animation: riseIn 0.7s 0.15s cubic-bezier(.16,1,.3,1) both;
        }}

        .card-title {{
            font-family: 'Playfair Display', serif;
            font-size: 26px;
            font-weight: 700;
            color: rgba(255,255,255,0.9);
            animation: riseIn 0.7s 0.2s cubic-bezier(.16,1,.3,1) both;
        }}

        .divider {{
            width: 48px;
            height: 2px;
            background: linear-gradient(to right, var(--gold), var(--terracotta));
            margin: 24px auto;
            border-radius: 2px;
            animation: riseIn 0.7s 0.25s cubic-bezier(.16,1,.3,1) both;
        }}

        /* Detail row */
        .detail-row {{
            display: flex;
            align-items: center;
            justify-content: space-between;
            background: rgba(255,255,255,0.05);
            border: 1px solid rgba(255,255,255,0.07);
            border-radius: 12px;
            padding: 16px 20px;
            margin-bottom: 12px;
            animation: riseIn 0.7s 0.3s cubic-bezier(.16,1,.3,1) both;
        }}

        .detail-key {{
            font-size: 12px;
            font-weight: 500;
            letter-spacing: 1px;
            text-transform: uppercase;
            color: rgba(255,255,255,0.4);
        }}

        .detail-val {{
            font-size: 15px;
            font-weight: 500;
            color: rgba(255,255,255,0.85);
        }}

        /* Big price */
        .price-block {{
            background: linear-gradient(135deg, rgba(201,168,76,0.12), rgba(196,98,58,0.08));
            border: 1px solid rgba(201,168,76,0.25);
            border-radius: 16px;
            padding: 28px 24px;
            margin: 8px 0 28px;
            animation: riseIn 0.7s 0.38s cubic-bezier(.16,1,.3,1) both;
        }}

        .price-label {{
            font-size: 11px;
            letter-spacing: 2px;
            text-transform: uppercase;
            color: var(--gold);
            margin-bottom: 8px;
            font-weight: 500;
        }}

        .price-value {{
            font-family: 'Playfair Display', serif;
            font-size: clamp(36px, 7vw, 52px);
            font-weight: 900;
            background: linear-gradient(135deg, var(--gold-light), var(--terracotta));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            line-height: 1.1;
            counter-reset: price;
        }}

        .price-note {{
            font-size: 12px;
            color: rgba(255,255,255,0.3);
            margin-top: 6px;
            font-weight: 300;
        }}

        /* Actions */
        .actions {{
            display: flex;
            gap: 12px;
            animation: riseIn 0.7s 0.45s cubic-bezier(.16,1,.3,1) both;
        }}

        .btn {{
            flex: 1;
            padding: 16px;
            border-radius: 12px;
            font-family: 'DM Sans', sans-serif;
            font-size: 14px;
            font-weight: 500;
            cursor: pointer;
            text-decoration: none;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 8px;
            transition: transform 0.2s, box-shadow 0.3s, opacity 0.3s;
        }}

        .btn:hover {{ transform: translateY(-2px); }}
        .btn:active {{ transform: translateY(0); }}

        .btn-primary {{
            background: linear-gradient(135deg, var(--gold), var(--terracotta));
            color: #fff;
            border: none;
            box-shadow: 0 8px 24px rgba(201,168,76,0.25);
        }}

        .btn-primary:hover {{ box-shadow: 0 12px 32px rgba(201,168,76,0.4); }}

        .btn-secondary {{
            background: transparent;
            color: rgba(255,255,255,0.6);
            border: 1px solid rgba(255,255,255,0.12);
        }}

        .btn-secondary:hover {{ border-color: rgba(255,255,255,0.3); color: #fff; }}

        @media (max-width: 520px) {{
            .card {{ padding: 36px 24px; }}
            .actions {{ flex-direction: column; }}
        }}
    </style>
</head>
<body>

<!-- Floating particles -->
<div class="bg-particles" id="particles"></div>

<div class="scene">
    <div class="card">
        <div class="card-icon">
            <svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" fill="none" viewBox="0 0 24 24" stroke="white" stroke-width="1.8">
                <path stroke-linecap="round" stroke-linejoin="round" d="M3 12l9-9 9 9M4 10v10a1 1 0 001 1h5v-5h4v5h5a1 1 0 001-1V10"/>
            </svg>
        </div>

        <div class="card-subtitle">Valuation Complete</div>
        <div class="card-title">Your Estimate is Ready</div>
        <div class="divider"></div>

        <div class="detail-row">
            <span class="detail-key">Property Size</span>
            <span class="detail-val">{size:,.0f} sqft</span>
        </div>

        <div class="price-block">
            <div class="price-label">Estimated Market Value</div>
            <div class="price-value" id="priceDisplay">₹ 0</div>
            <div class="price-note">Based on current market regression model</div>
        </div>

        <div class="actions">
            <a href="/" class="btn btn-primary">
                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"/>
                </svg>
                New Estimate
            </a>
            <button class="btn btn-secondary" onclick="window.print()">
                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M17 17h2a2 2 0 002-2v-4a2 2 0 00-2-2H5a2 2 0 00-2 2v4a2 2 0 002 2h2m2 4h6a2 2 0 002-2v-4a2 2 0 00-2-2H9a2 2 0 00-2 2v4a2 2 0 002 2zm8-12V5a2 2 0 00-2-2H9a2 2 0 00-2 2v4h10z"/>
                </svg>
                Save
            </button>
        </div>
    </div>
</div>

<script>
    // Animated price counter
    const target = {price};
    const el = document.getElementById('priceDisplay');
    const duration = 1400;
    const start = performance.now();

    function easeOut(t) {{ return 1 - Math.pow(1 - t, 3); }}

    function tick(now) {{
        const elapsed = now - start;
        const progress = Math.min(elapsed / duration, 1);
        const current = Math.round(easeOut(progress) * target);
        el.textContent = '€ ' + current.toLocaleString('en-US',{{ maximumFractionDigits: 0 }});
        if (progress < 1) requestAnimationFrame(tick);
    }}

    setTimeout(() => requestAnimationFrame(tick), 400);

    // Generate floating particles
    const container = document.getElementById('particles');
    for (let i = 0; i < 18; i++) {{
        const p = document.createElement('div');
        p.className = 'particle';
        const size = Math.random() * 5 + 2;
        p.style.cssText = `
            width: ${{size}}px; height: ${{size}}px;
            left: ${{Math.random() * 100}}%;
            animation-duration: ${{Math.random() * 12 + 8}}s;
            animation-delay: ${{Math.random() * 10}}s;
            opacity: ${{Math.random() * 0.6 + 0.1}};
        `;
        container.appendChild(p);
    }}
</script>
</body>
</html>
"""


@app.get("/", response_class=HTMLResponse)
def home():
    return HOME_HTML


@app.post("/predict")
def predict(size: float = Form(...)):
    input_data = pd.DataFrame({"size_sqft": [size]})
    prediction = model.predict(input_data)
    price = float(prediction[0])

    return HTMLResponse(RESULT_HTML.format(size=size, price=price))