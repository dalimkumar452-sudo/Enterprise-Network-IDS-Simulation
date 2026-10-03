const API_BASE = "http://127.0.0.1:8000/api";

// --- Tab Switching Logic (Sidebar ti kaj koranor jonno) ---
function switchTab(tabId) {
    // Hide all views
    document.querySelectorAll('.view-section').forEach(el => {
        el.classList.add('hidden');
        el.classList.remove('block');
    });
    
    // Show selected view
    document.getElementById(tabId).classList.remove('hidden');
    document.getElementById(tabId).classList.add('block');

    // Update Sidebar styling
    const buttons = ['dashboard', 'network', 'reports'];
    buttons.forEach(btn => {
        let el = document.getElementById('btn-' + btn);
        el.className = "w-full flex items-center px-6 py-3 text-gray-400 hover:text-white hover:bg-gray-800/50 transition border-r-4 border-transparent";
        if(btn === tabId) {
            el.className = "w-full flex items-center px-6 py-3 bg-blue-600/10 text-blue-400 border-r-4 border-blue-500 transition";
            document.getElementById('header-title').innerText = el.innerText.trim();
        }
    });
}

// --- Chart.js Setup (Updated Pie Chart & Bar Chart) ---
let pieChart, barChart;

function initCharts() {
    // Pie Chart (Doughnut with thinner ring)
    const ctxPie = document.getElementById('severityPieChart').getContext('2d');
    pieChart = new Chart(ctxPie, {
        type: 'doughnut',
        data: {
            labels: ['Critical', 'High', 'Medium', 'Low'],
            datasets: [{
                data: [0, 0, 0, 0],
                backgroundColor: ['#ef4444', '#f97316', '#eab308', '#3b82f6'],
                borderWidth: 0,
                hoverOffset: 4
            }]
        },
        options: { 
            responsive: true, 
            maintainAspectRatio: false,
            cutout: '85%', // Ring ke sundor chikon korbe
            plugins: { 
                legend: { 
                    position: 'bottom', 
                    labels: { color: '#cbd5e1', padding: 15, boxWidth: 10, font: { size: 11 } } 
                } 
            } 
        }
    });

    // Bar Chart (Thinner bars for professional look)
    const ctxBar = document.getElementById('statusBarChart').getContext('2d');
    barChart = new Chart(ctxBar, {
        type: 'bar',
        data: {
            labels: ['NEW', 'INVESTIGATING', 'RESOLVED', 'FALSE POSITIVE'],
            datasets: [{
                label: 'Alert Count',
                data: [0, 0, 0, 0],
                backgroundColor: ['#3b82f6', '#a855f7', '#10b981', '#64748b'],
                borderRadius: 4,
                maxBarThickness: 40 // Bar guloke slim korar jonno
            }]
        },
        options: { 
            responsive: true, maintainAspectRatio: false, 
            scales: { 
                y: { beginAtZero: true, grid: { color: 'rgba(255,255,255,0.05)' }, ticks: { color: '#94a3b8', stepSize: 1 } },
                x: { grid: { display: false }, ticks: { color: '#94a3b8', font: { size: 10 } } }
            },
            plugins: { legend: { display: false } }
        }
    });
}

// Update Graphs dynamically with API Data
function updateCharts(alertsData) {
    // Presentation er jonno kichu dummy data add kora holo jate sob rong show kore
    let counts = { CRITICAL: 1, HIGH: 0, MEDIUM: 2, LOW: 1 }; 
    let statuses = { NEW: 0, INVESTIGATING: 1, RESOLVED: 2, FALSE_POSITIVE: 1 }; 

    alertsData.forEach(a => {
        if(counts[a.severity] !== undefined) counts[a.severity]++;
        if(statuses[a.status] !== undefined) statuses[a.status]++;
    });

    pieChart.data.datasets[0].data = [counts.CRITICAL, counts.HIGH, counts.MEDIUM, counts.LOW];
    pieChart.update();

    barChart.data.datasets[0].data = [statuses.NEW, statuses.INVESTIGATING, statuses.RESOLVED, statuses.FALSE_POSITIVE];
    barChart.update();
}

// --- Data Fetching (Stats & Alerts) ---
async function fetchStats() {
    try {
        const res = await fetch(`${API_BASE}/dashboard/stats`);
        const data = await res.json();
        document.getElementById("total_alerts").innerText = data.total_alerts;
        document.getElementById("open_alerts").innerText = data.open_alerts;
    } catch (e) { console.error("Stats API error:", e); }
}

function getSeverityBadge(sev) {
    if (sev === 'CRITICAL') return '<span class="text-red-500 font-bold"><i class="fa-solid fa-fire mr-1"></i>CRITICAL</span>';
    if (sev === 'HIGH') return '<span class="text-orange-400 font-bold">HIGH</span>';
    return `<span class="text-yellow-400 font-bold">${sev}</span>`;
}

function getStatusBadge(st) {
    if (st === 'NEW') return '<span class="text-blue-400"><i class="fa-solid fa-circle text-[8px] animate-pulse mr-1"></i>NEW</span>';
    if (st === 'INVESTIGATING') return '<span class="text-purple-400"><i class="fa-solid fa-spinner animate-spin mr-1"></i>INV</span>';
    if (st === 'RESOLVED') return '<span class="text-emerald-500">RESOLVED</span>';
    return '<span class="text-gray-500">FP</span>';
}

async function fetchAlerts() {
    try {
        const res = await fetch(`${API_BASE}/alerts`);
        const data = await res.json();
        
        const tbody = document.getElementById("alerts_body");
        tbody.innerHTML = "";
        
        data.forEach(a => {
            let date = new Date(a.ts * 1000).toLocaleTimeString([], {hour: '2-digit', minute:'2-digit', second:'2-digit'});
            tbody.innerHTML += `
                <tr class="hover:bg-slate-800/50 group">
                    <td class="p-4 text-gray-400 font-mono text-xs">${date}</td>
                    <td class="p-4 text-gray-300 font-mono text-xs">${a.src}</td>
                    <td class="p-4 text-gray-300 font-mono text-xs">${a.dst}</td>
                    <td class="p-4 text-gray-200 text-xs">${a.rule}</td>
                    <td class="p-4 text-center text-xs">${getSeverityBadge(a.severity)}</td>
                    <td class="p-4 text-center font-bold ${a.risk >= 60 ? 'text-orange-400' : 'text-emerald-400'}">${a.risk}</td>
                    <td class="p-4 text-xs font-semibold">${getStatusBadge(a.status)}</td>
                    <td class="p-4">
                        <div class="flex justify-center space-x-3 opacity-50 group-hover:opacity-100 transition">
                            <button onclick="updateStatus(${a.id}, 'INVESTIGATING')" class="hover:text-purple-400"><i class="fa-solid fa-magnifying-glass"></i></button>
                            <button onclick="updateStatus(${a.id}, 'FALSE_POSITIVE')" class="hover:text-gray-400"><i class="fa-solid fa-ban"></i></button>
                            <button onclick="updateStatus(${a.id}, 'RESOLVED')" class="hover:text-emerald-400"><i class="fa-solid fa-check-double"></i></button>
                        </div>
                    </td>
                </tr>`;
        });

        // Update Graphs dynamically
        updateCharts(data);
    } catch (e) { console.error("Alerts API error:", e); }
}

async function updateStatus(id, status) {
    await fetch(`${API_BASE}/alerts/${id}/status?status=${status}`, { method: 'PUT' });
    fetchAlerts(); fetchStats();
}

// --- Live Network Terminal Simulation ---
function generateLiveTraffic() {
    const term = document.getElementById('terminal-logs');
    if(!term) return;
    
    const protocols = ['TCP', 'UDP', 'ICMP', 'DNS', 'TLSv1.3', 'HTTP'];
    const ports = [443, 80, 53, 22, 3389, 8080];
    
    setInterval(() => {
        // Random fake IP and stats generation
        const src = `192.168.1.${Math.floor(Math.random()*255)}`;
        const dst = `10.0.0.${Math.floor(Math.random()*255)}`;
        const proto = protocols[Math.floor(Math.random()*protocols.length)];
        const port = ports[Math.floor(Math.random()*ports.length)];
        const time = new Date().toISOString().split('T')[1].substring(0,8);
        const len = Math.floor(Math.random()*1500) + 40;
        
        let colorClass = proto === 'TCP' ? 'text-blue-300' : (proto === 'UDP' ? 'text-purple-300' : 'text-green-300');
        
        const log = `<div class="mb-1 border-b border-gray-800/50 pb-1 hover:bg-gray-800/30">
            <span class="text-gray-500">[${time}]</span> 
            <span class="text-emerald-400 font-bold">${src}</span> 
            <i class="fa-solid fa-arrow-right-arrow-left text-gray-600 px-2 text-[10px]"></i> 
            <span class="text-yellow-400">${dst}:${port}</span> 
            <span class="${colorClass} pl-4 pr-2 font-bold">[${proto}]</span> 
            <span class="text-gray-400">Len=${len}</span>
        </div>`;
        
        term.insertAdjacentHTML('afterbegin', log);
        
        // Keep terminal clean (max 40 lines) to prevent lag
        if(term.children.length > 40) term.lastElementChild.remove();
    }, 600); // Prottek 0.6 second e notun log asbe
}

// --- Initialize System ---
window.onload = () => {
    initCharts();
    fetchStats();
    fetchAlerts();
    generateLiveTraffic(); // Start Live Terminal
    setInterval(() => { fetchStats(); fetchAlerts(); }, 2000);
};