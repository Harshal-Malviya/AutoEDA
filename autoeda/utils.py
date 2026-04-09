from jinja2 import Template

html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ title }}</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600&display=swap" rel="stylesheet">
    <style>
        :root {
            --primary: #2563eb;
            --bg-body: #f3f4f6;
            --bg-card: #ffffff;
            --text-main: #1f2937;
            --text-muted: #6b7280;
            --border: #e5e7eb;
            --stat-bg: #f8fafc;
            --table-th-bg: #f9fafb;
            --insight-bg: #eff6ff;
            --insight-text: #1e40af;
        }

        /* Dark Mode Variables */
        body.dark {
            --bg-body: #111827;
            --bg-card: #1f2937;
            --text-main: #f9fafb;
            --text-muted: #9ca3af;
            --border: #374151;
            --stat-bg: #374151;
            --table-th-bg: #374151;
            --insight-bg: #1e3a8a;
            --insight-text: #bfdbfe;
        }

        body {
            font-family: 'Inter', sans-serif;
            background-color: var(--bg-body);
            color: var(--text-main);
            margin: 0;
            padding: 0;
            line-height: 1.6;
            transition: background-color 0.3s, color 0.3s;
        }

        /* --- Navigation --- */
        .navbar {
            background: var(--bg-card);
            border-bottom: 1px solid var(--border);
            padding: 1rem 2rem;
            position: sticky;
            top: 0;
            z-index: 100;
            display: flex;
            justify-content: space-between;
            align-items: center;
            box-shadow: 0 1px 3px rgba(0,0,0,0.05);
            transition: background-color 0.3s, border-color 0.3s;
        }

        .navbar h1 { margin: 0; font-size: 1.25rem; font-weight: 600; }

        .nav-links {
            display: flex;
            align-items: center;
        }

        .nav-links a {
            text-decoration: none;
            color: var(--text-muted);
            margin-left: 20px;
            font-size: 0.9rem;
            transition: color 0.2s;
        }
        .nav-links a:hover { color: var(--primary); }

        .btn-action {
            padding: 8px 16px;
            border-radius: 6px;
            cursor: pointer;
            font-weight: 500;
            margin-left: 15px;
            transition: all 0.2s;
            font-size: 0.9rem;
        }

        .btn-toggle {
            background-color: transparent;
            color: var(--text-main);
            border: 1px solid var(--border);
        }
        .btn-toggle:hover {
            background-color: var(--border);
        }

        .btn-download {
            background-color: var(--primary);
            color: white;
            border: none;
        }
        .btn-download:hover { background-color: #1d4ed8; }

        /* --- Layout --- */
        .container {
            max-width: 1200px;
            margin: 2rem auto;
            padding: 0 1rem;
        }

        section {
            scroll-margin-top: 80px; 
            margin-bottom: 3rem;
        }

        .section-title {
            font-size: 1.5rem;
            font-weight: 600;
            margin-bottom: 1rem;
            color: var(--text-main);
            border-left: 4px solid var(--primary);
            padding-left: 12px;
            cursor: pointer;
            display: flex;
            justify-content: space-between;
            align-items: center;
            user-select: none;
        }
        
        .section-title::after {
            content: '▼';
            font-size: 1rem;
            color: var(--text-muted);
            transition: transform 0.2s;
        }
        
        .section-title.collapsed::after {
            transform: rotate(-90deg);
        }

        .card {
            background: var(--bg-card);
            border-radius: 12px;
            padding: 1.5rem;
            box-shadow: 0 1px 3px rgba(0,0,0,0.05);
            border: 1px solid var(--border);
            transition: background-color 0.3s, border-color 0.3s;
        }

        /* --- Statistics & Tables --- */
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 1rem;
        }
        
        .stat-box {
            background: var(--stat-bg);
            padding: 1rem;
            border-radius: 8px;
            text-align: center;
            transition: background-color 0.3s;
        }
        .stat-value { font-size: 1.5rem; font-weight: 600; color: var(--primary); }
        .stat-label { font-size: 0.875rem; color: var(--text-muted); text-transform: uppercase; letter-spacing: 0.05em;}

        .insights-list { list-style: none; padding: 0; margin: 0; }
        .insights-list li {
            background: var(--insight-bg);
            color: var(--insight-text);
            padding: 10px 14px;
            border-radius: 6px;
            margin-bottom: 8px;
            border-left: 3px solid var(--primary);
            transition: background-color 0.3s, color 0.3s;
        }

        table { width: 100%; border-collapse: collapse; font-size: 0.95rem; }
        th, td { padding: 12px; text-align: left; border-bottom: 1px solid var(--border); transition: border-color 0.3s;}
        th { background-color: var(--table-th-bg); font-weight: 600; color: var(--text-muted); transition: background-color 0.3s;}
        tr:hover { background-color: var(--table-th-bg); }

        /* --- Images & Expansion --- */
        .img-fluid { 
            max-width: 100%; 
            height: auto; 
            border-radius: 4px;
            cursor: zoom-in;
            transition: transform 0.2s;
            object-fit: contain;
            background-color: white; /* Ensures transparent charts remain visible in dark mode */
        }
        .img-fluid:hover {
            opacity: 0.9;
        }

        .dist-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 1.5rem;
        }

        /* --- Modal (Lightbox) Styles --- */
        .modal {
            display: none; 
            position: fixed; 
            z-index: 1000; 
            padding-top: 50px; 
            left: 0;
            top: 0;
            width: 100%; 
            height: 100%; 
            overflow: auto; 
            background-color: rgb(0,0,0); 
            background-color: rgba(0,0,0,0.9); 
        }

        .modal-content {
            margin: auto;
            display: block;
            width: 80%;
            max-width: 1200px;
            max-height: 85vh;
            object-fit: contain;
            animation-name: zoom;
            animation-duration: 0.3s;
            background-color: white; /* Visibility for dark mode */
        }

        @keyframes zoom {
            from {transform:scale(0)} 
            to {transform:scale(1)}
        }

        .close {
            position: absolute;
            top: 15px;
            right: 35px;
            color: #f1f1f1;
            font-size: 40px;
            font-weight: bold;
            transition: 0.3s;
            cursor: pointer;
        }

        .close:hover,
        .close:focus {
            color: #bbb;
            text-decoration: none;
            cursor: pointer;
        }
        
        #caption {
            margin: auto;
            display: block;
            width: 80%;
            max-width: 700px;
            text-align: center;
            color: #ccc;
            padding: 10px 0;
            height: 150px;
        }

        /* --- PDF / Print Styles --- */
        @media print {
            .navbar, .btn-action, .modal { display: none !important; } 
            body { background: white !important; color: black !important; -webkit-print-color-adjust: exact; }
            .container { width: 100%; max-width: 100%; margin: 0; }
            .card { box-shadow: none; border: 1px solid #ccc; break-inside: avoid; margin-bottom: 20px; background: white !important;}
            section { margin-bottom: 2rem; break-after: auto; }
            h2 { page-break-before: auto; color: black !important;}
            .dist-grid { display: block; } 
            .dist-grid .card { width: 45%; display: inline-block; margin: 1%; vertical-align: top; }
            /* Expand all sections for printing */
            .section-content { display: block !important; }
            .section-title::after { display: none; }
        }
    </style>
</head>
<body>

    <nav class="navbar">
        <h1>{{ title }}</h1>
        <div class="nav-links">
            <button class="btn-action btn-toggle" onclick="toggleTheme()">🌓 Theme</button>
            <button class="btn-action btn-download" onclick="downloadPDF()">Download PDF</button>
        </div>
    </nav>

    <div class="container">
        
        <section id="overview">
            <h2 class="section-title" onclick="toggleSection(this)">Dataset Overview</h2>
            <div class="card section-content">
                <div class="stats-grid">
                    <div class="stat-box">
                        <div class="stat-value">{{ report.summary.rows if report.summary else '' }}</div>
                        <div class="stat-label">Rows</div>
                    </div>

                    <div class="stat-box">
                        <div class="stat-value">{{ report.summary.columns if report.summary else '' }}</div>
                        <div class="stat-label">Columns</div>
                    </div>

                    <div class="stat-box">
                        <div class="stat-value">{{ report.summary.missing_percent if report.summary else '' }}%</div>
                        <div class="stat-label">Missing Data</div>
                    </div>

                    <div class="stat-box">
                        <div class="stat-value">{{ report.summary.duplicates if report.summary else '' }}</div>
                        <div class="stat-label">Duplicates</div>
                    </div>

                    <div class="stat-box">
                        <div class="stat-value">{{ report.summary.memory if report.summary else '' }} MB</div>
                        <div class="stat-label">Memory Usage</div>
                    </div>
                </div>
                
                <h3 style="margin-top: 1.5rem; margin-bottom: 1rem;">Key Insights</h3>
                {% if report.insights %}
                <ul class="insights-list">
                    {% for i in report.insights %}
                    <li>{{ i }}</li>
                    {% endfor %}
                </ul>
                {% else %}
                <p style="color: var(--text-muted)">No critical alerts found.</p>
                {% endif %}
            </div>
        </section>

        <section id="missing">
            <h2 class="section-title" onclick="toggleSection(this)">Missing Values Analysis</h2>
            <div class="card section-content">
                {% if report.missing %}
                <table>
                    <thead>
                        <tr>
                            <th>Column Name</th>
                            <th>Missing Count</th>
                            <th>Missing Percentage</th>
                        </tr>
                    </thead>
                    <tbody>
                        {% for col, info in report.missing.items() %}
                        <tr>
                            <td style="font-weight: 500;">{{ col }}</td>
                            <td>{{ info.n_missing }}</td>
                            <td>
                                <div style="display: flex; align-items: center; gap: 10px;">
                                    <div style="flex-grow:1; background:#e5e7eb; height:6px; border-radius:3px; max-width:100px;">
                                        <div style="width:{{ info.percent_missing }}%; background:var(--primary); height:6px; border-radius:3px;"></div>
                                    </div>
                                    {{ "%.2f"|format(info.percent_missing) }}%
                                </div>
                            </td>
                        </tr>
                        {% endfor %}
                    </tbody>
                </table>
                {% else %}
                <p style="text-align:center; color: var(--text-muted); padding: 20px;">No missing data found.</p>
                {% endif %}
            </div>
        </section>

        {% if report.correlations %}
        <section id="correlations">
            <h2 class="section-title" onclick="toggleSection(this)">Correlation Matrix</h2>
            <div class="card section-content" style="text-align: center;">
                <p style="font-size:0.8rem; color:var(--text-muted); margin-bottom:10px;"></p>
                <img class="img-fluid clickable-img" 
                     src="data:image/png;base64,{{ report.correlations }}" 
                     alt="Correlation Matrix" 
                     onclick="openModal(this)" />
            </div>
        </section>
        
        <section id="spread">
            <h2 class="section-title" onclick="toggleSection(this)">Data Spread Summary</h2>
            <div class="card section-content">
                <table>
                    <thead>
                        <tr>
                            <th>Column</th>
                            <th>Min</th>
                            <th>25%</th>
                            <th>Median</th>
                            <th>75%</th>
                            <th>Max</th>
                            <th>Mean</th>
                            <th>Std</th>
                        </tr>
                    </thead>
                    <tbody>
                        {% for col, s in report.spread.items() %}
                        <tr>
                            <td style="font-weight:600;">{{ col }}</td>
                            <td>{{ "%.2f"|format(s.min) }}</td>
                            <td>{{ "%.2f"|format(s.p25) }}</td>
                            <td>{{ "%.2f"|format(s.p50) }}</td>
                            <td>{{ "%.2f"|format(s.p75) }}</td>
                            <td>{{ "%.2f"|format(s.max) }}</td>
                            <td>{{ "%.2f"|format(s.mean) }}</td>
                            <td>{{ "%.2f"|format(s.std) }}</td>
                        </tr>
                        {% endfor %}
                    </tbody>
                </table>
            </div>
        </section>
        
        <section id="boxplots">
            <h2 class="section-title" onclick="toggleSection(this)">Boxplots</h2>
            <div class="dist-grid section-content">
                {% for col, b64 in report.boxplots.items() %}
                <div class="card">
                    <h4 style="margin-top:0;">{{ col }}</h4>
                    <img class="img-fluid clickable-img" 
                         src="data:image/png;base64,{{ b64 }}" 
                         onclick="openModal(this)"
                         alt="Boxplot - {{ col }}" />
                </div>
                {% endfor %}
            </div>
        </section>
        
        <section id="scatterplots">
            <h2 class="section-title" onclick="toggleSection(this)">Scatterplots</h2>
            <div class="dist-grid section-content">
                {% for name, b64 in report.scatterplots.items() %}
                <div class="card">
                    <h4 style="margin-top:0;">{{ name.replace('_vs_', ' vs ') }}</h4>
                    <img class="img-fluid clickable-img" 
                         src="data:image/png;base64,{{ b64 }}" 
                         alt="{{ name }}" 
                         onclick="openModal(this)" />
                </div>
                {% endfor %}
            </div>
        </section>
        {% endif %}

        <section id="distributions">
            <h2 class="section-title" onclick="toggleSection(this)">Variable Distributions</h2>
            <div class="dist-grid section-content">
                {% for col, b64 in report.distributions.items() %}
                <div class="card">
                    <h4 style="margin-top:0; border-bottom:1px solid var(--border); padding-bottom:10px;">{{ col }}</h4>
                    <img class="img-fluid clickable-img" 
                         src="data:image/png;base64,{{ b64 }}" 
                         alt="Distribution of {{ col }}" 
                         onclick="openModal(this)" />
                </div>
                {% endfor %}
            </div>
        </section>

    </div>

    <div id="imgModal" class="modal">
        <span class="close" onclick="closeModal()">&times;</span>
        <img class="modal-content" id="img01">
        <div id="caption"></div>
    </div>

    <script>
        // --- Theme Logic ---
        function toggleTheme() {
            document.body.classList.toggle("dark");
            // Optional: Store the user's preference if needed later
            // const isDark = document.body.classList.contains("dark");
            // localStorage.setItem("theme", isDark ? "dark" : "light");
        }

        // Detect system preference on load
        if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
            document.body.classList.add("dark");
        }

        function downloadPDF() {
            window.print();
        }

        // --- Collapse Logic ---
        function toggleSection(el){
            let content = el.nextElementSibling;
            if(content.style.display === "none"){
                content.style.display = "";
                el.classList.remove("collapsed");
            } else {
                content.style.display = "none";
                el.classList.add("collapsed");
            }
        }

        // --- Modal Logic ---
        var modal = document.getElementById("imgModal");
        var modalImg = document.getElementById("img01");
        var captionText = document.getElementById("caption");

        function openModal(element) {
            modal.style.display = "block";
            modalImg.src = element.src;
            captionText.innerHTML = element.alt;
            
            document.body.style.overflow = "hidden";
        }

        function closeModal() {
            modal.style.display = "none";
            document.body.style.overflow = "auto";
        }

        window.onclick = function(event) {
            if (event.target == modal) {
                closeModal();
            }
        }
        
        document.addEventListener('keydown', function(event) {
            if (event.key === "Escape") {
                closeModal();
            }
        });
    </script>
</body>
</html>
"""

def render_html_report(report, title="Auto EDA Report"):
    tmpl = Template(html_template)
    return tmpl.render(report=report, title=title)