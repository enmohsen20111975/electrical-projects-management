// Materials Tab Handlers
async function runSupplierComparison() {
    const form = document.getElementById('supplierCompareForm');
    const materialType = form.material_type.value;
    const quantity = parseInt(form.quantity.value);
    // Simulate supplier price comparison (replace with API call as needed)
    const suppliers = [
        { name: 'Graybar', price: quantity * 10 + 100, availability: 'In Stock', lead_time: 2 },
        { name: 'WESCO', price: quantity * 9.5 + 120, availability: 'Backorder', lead_time: 7 },
        { name: 'Schneider Electric', price: quantity * 11 + 90, availability: 'In Stock', lead_time: 3 }
    ];
    let html = '<table class="table"><thead><tr><th>Supplier</th><th>Price</th><th>Availability</th><th>Lead Time</th></tr></thead><tbody>';
    suppliers.forEach(s => {
        html += `<tr><td>${s.name}</td><td>$${s.price.toFixed(2)}</td><td>${s.availability}</td><td>${s.lead_time} days</td></tr>`;
    });
    html += '</tbody></table>';
    document.getElementById('supplierComparisonResults').innerHTML = html;
}

let inventory = [];
function addInventoryItem() {
    const form = document.getElementById('inventoryForm');
    const item = {
        name: form.material_name.value,
        stock: parseInt(form.stock_level.value),
        lead_time: parseInt(form.lead_time.value)
    };
    inventory.push(item);
    renderInventoryList();
    form.reset();
}

function renderInventoryList() {
    if (inventory.length === 0) {
        document.getElementById('inventoryList').innerHTML = '<p class="text-muted">No inventory items added.</p>';
        return;
    }
    let html = '<table class="table"><thead><tr><th>Material</th><th>Stock Level</th><th>Lead Time</th></tr></thead><tbody>';
    inventory.forEach(item => {
        html += `<tr><td>${item.name}</td><td>${item.stock}</td><td>${item.lead_time} days</td></tr>`;
    });
    html += '</tbody></table>';
    document.getElementById('inventoryList').innerHTML = html;
}
// Calculation Tab Handlers
async function runLoadFlowCalculation() {
    const form = document.getElementById('loadFlowForm');
    const data = {
        calculation_type: 'load_flow',
        voltage: parseFloat(form.voltage.value),
        current: parseFloat(form.current.value),
        power_factor: parseFloat(form.power_factor.value),
        distance: parseFloat(form.distance.value)
    };
    try {
        const response = await fetch('/api/projects/1/calculations', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });
        const result = await response.json();
        showCalculationResults('Load Flow Analysis', result);
    } catch (error) {
        dashboard.showAlert('Calculation failed', 'danger');
    }
}

async function runVoltageDropCalculation() {
    const form = document.getElementById('voltageDropForm');
    const data = {
        calculation_type: 'voltage_drop',
        voltage: parseFloat(form.voltage.value),
        current: parseFloat(form.current.value),
        distance: parseFloat(form.distance.value)
    };
    try {
        const response = await fetch('/api/projects/1/calculations', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });
        const result = await response.json();
        showCalculationResults('Voltage Drop Calculation', result);
    } catch (error) {
        dashboard.showAlert('Calculation failed', 'danger');
    }
}

async function runFaultCurrentCalculation() {
    const form = document.getElementById('faultCurrentForm');
    const data = {
        calculation_type: 'fault_current',
        voltage: parseFloat(form.voltage.value),
        impedance: parseFloat(form.impedance.value)
    };
    try {
        const response = await fetch('/api/projects/1/calculations', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });
        const result = await response.json();
        showCalculationResults('Fault Current Analysis', result);
    } catch (error) {
        dashboard.showAlert('Calculation failed', 'danger');
    }
}

async function runCableSizingCalculation() {
    const form = document.getElementById('cableSizingForm');
    const data = {
        calculation_type: 'cable_sizing',
        current: parseFloat(form.current.value),
        length: parseFloat(form.length.value),
        voltage: parseFloat(form.voltage.value)
    };
    try {
        const response = await fetch('/api/projects/1/calculations', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });
        const result = await response.json();
        showCalculationResults('Cable Sizing', result);
    } catch (error) {
        dashboard.showAlert('Calculation failed', 'danger');
    }
}

function showCalculationResults(title, result) {
    const resultsDiv = document.getElementById('calculationResults');
    resultsDiv.innerHTML = `
        <div class="card mt-3">
            <div class="card-header">${title} Results</div>
            <div class="card-body">
                <pre>${JSON.stringify(result, null, 2)}</pre>
            </div>
        </div>
    `;
}
// Dashboard JavaScript
class DashboardApp {
    constructor() {
        this.projects = [];
        this.init();
    }

    init() {
        this.loadProjects();
        this.loadRecentActivity();
        this.setupEventListeners();
        this.startAutoRefresh();
    }
    async loadRecentActivity() {
        try {
            // Simulate fetching recent activity from backend (replace with API call as needed)
            const activities = [
                { type: 'project', action: 'created', name: 'Industrial Complex - Phase 2', time: '2 hours ago' },
                { type: 'calculation', action: 'completed', name: 'Load flow analysis for Main Panel A', time: '5 hours ago' },
                { type: 'material', action: 'updated', name: 'Copper prices refreshed', time: '1 day ago' }
            ];
            this.renderRecentActivity(activities);
        } catch (error) {
            this.showAlert('Failed to load recent activity', 'danger');
        }
    }

    renderRecentActivity(activities) {
        const feed = document.querySelector('.activity-feed');
        if (!feed) return;
        feed.innerHTML = '';
        activities.forEach(act => {
            let icon, bg;
            if (act.type === 'project') { icon = 'fa-plus'; bg = 'bg-primary'; }
            else if (act.type === 'calculation') { icon = 'fa-calculator'; bg = 'bg-success'; }
            else if (act.type === 'material') { icon = 'fa-cogs'; bg = 'bg-info'; }
            else { icon = 'fa-info-circle'; bg = 'bg-secondary'; }
            feed.innerHTML += `
                <div class="activity-item">
                    <div class="activity-icon ${bg}"><i class="fas ${icon} text-white"></i></div>
                    <div class="activity-content">
                        <h6>${act.action.charAt(0).toUpperCase() + act.action.slice(1)} ${act.type.charAt(0).toUpperCase() + act.type.slice(1)}</h6>
                        <p class="text-muted">${act.name}</p>
                        <small class="text-muted">${act.time}</small>
                    </div>
                </div>
            `;
        });
    }

    setupEventListeners() {
        // Auto-refresh prices every hour
        setInterval(() => {
            this.updateMaterialPrices();
        }, 3600000);
    }

    async loadProjects() {
        try {
            const response = await fetch('/api/projects');
            if (response.ok) {
                this.projects = await response.json();
                this.renderProjects();
                this.updateKPIs();
            } else {
                console.error('Failed to load projects');
            }
        } catch (error) {
            console.error('Error loading projects:', error);
        }
    }

    renderProjects() {
        const tbody = document.getElementById('projects-tbody');
        if (!tbody) return;

        tbody.innerHTML = '';

        if (this.projects.length === 0) {
            tbody.innerHTML = `
                <tr>
                    <td colspan="7" class="text-center text-muted py-4">
                        <i class="fas fa-project-diagram fa-3x mb-3 d-block"></i>
                        No projects found. Create your first project to get started.
                    </td>
                </tr>
            `;
            return;
        }

        this.projects.forEach(project => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>
                    <div class="fw-bold">${project.name}</div>
                    <small class="text-muted">${project.description || 'No description'}</small>
                </td>
                <td>
                    <span class="badge bg-${this.getStatusColor(project.status)}">
                        ${this.formatStatus(project.status)}
                    </span>
                </td>
                <td>
                    <div class="progress" style="height: 6px;">
                        <div class="progress-bar bg-${this.getProgressColor(project.progress)}" 
                             style="width: ${project.progress}%"></div>
                    </div>
                    <small class="text-muted">${project.progress}%</small>
                </td>
                <td>${this.formatCurrency(project.budget)}</td>
                <td>${this.formatCurrency(project.actual_cost)}</td>
                <td>
                    <small>${this.formatDate(project.start_date)} - ${this.formatDate(project.end_date)}</small>
                </td>
                <td>
                    <div class="btn-group btn-group-sm">
                        <button class="btn btn-outline-primary" onclick="dashboard.viewProject(${project.id})" title="View">
                            <i class="fas fa-eye"></i>
                        </button>
                        <button class="btn btn-outline-success" onclick="dashboard.editProject(${project.id})" title="Edit">
                            <i class="fas fa-edit"></i>
                        </button>
                        <button class="btn btn-outline-info" onclick="dashboard.calculateProject(${project.id})" title="Calculate">
                            <i class="fas fa-calculator"></i>
                        </button>
                        <button class="btn btn-outline-warning" onclick="dashboard.estimateMaterials(${project.id})" title="Materials">
                            <i class="fas fa-cogs"></i>
                        </button>
                    </div>
                </td>
            `;
            tbody.appendChild(row);
        });
    }

    updateKPIs() {
        const activeProjects = this.projects.filter(p => p.status === 'in_progress');
        const totalBudget = this.projects.reduce((sum, p) => sum + (p.budget || 0), 0);
        const totalActualCost = this.projects.reduce((sum, p) => sum + (p.actual_cost || 0), 0);
        const avgProgress = this.projects.length > 0 ? 
            this.projects.reduce((sum, p) => sum + (p.progress || 0), 0) / this.projects.length : 0;
        const costVariance = totalBudget > 0 ? 
            ((totalActualCost - totalBudget) / totalBudget * 100) : 0;

        // Update KPI cards
        document.getElementById('active-projects-count').textContent = activeProjects.length;
        document.getElementById('total-budget').textContent = this.formatCurrency(totalBudget);
        document.getElementById('avg-progress').textContent = `${Math.round(avgProgress)}%`;
        document.getElementById('cost-variance').innerHTML = `
            <span class="${costVariance > 0 ? 'cost-negative' : 'cost-positive'}">
                ${Math.abs(costVariance).toFixed(1)}%
            </span>
        `;

        // Update progress bar
        document.getElementById('progress-bar').style.width = `${avgProgress}%`;

        // Render charts
        this.renderProgressChart();
        this.renderBudgetChart();
    }

    renderProgressChart() {
        const ctx = document.getElementById('progressChart').getContext('2d');
        const labels = this.projects.map(p => p.name);
        const data = this.projects.map(p => p.progress);
        if (window.progressChartInstance) window.progressChartInstance.destroy();
        window.progressChartInstance = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: labels,
                datasets: [{
                    label: 'Progress (%)',
                    data: data,
                    backgroundColor: '#36b9cc'
                }]
            },
            options: {
                responsive: true,
                plugins: { legend: { display: false } },
                scales: { y: { beginAtZero: true, max: 100 } }
            }
        });
    }

    renderBudgetChart() {
        const ctx = document.getElementById('budgetChart').getContext('2d');
        const labels = this.projects.map(p => p.name);
        const budgetData = this.projects.map(p => p.budget);
        const actualData = this.projects.map(p => p.actual_cost);
        if (window.budgetChartInstance) window.budgetChartInstance.destroy();
        window.budgetChartInstance = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: labels,
                datasets: [
                    {
                        label: 'Budget',
                        data: budgetData,
                        backgroundColor: '#1cc88a'
                    },
                    {
                        label: 'Actual Cost',
                        data: actualData,
                        backgroundColor: '#f6c23e'
                    }
                ]
            },
            options: {
                responsive: true,
                plugins: { legend: { display: true } },
                scales: { y: { beginAtZero: true } }
            }
        });
    }

    getStatusColor(status) {
        const colors = {
            'planning': 'info',
            'in_progress': 'warning',
            'completed': 'success',
            'on_hold': 'danger'
        };
        return colors[status] || 'secondary';
    }

    getProgressColor(progress) {
        if (progress < 30) return 'danger';
        if (progress < 70) return 'warning';
        return 'success';
    }

    formatStatus(status) {
        return status.replace('_', ' ').replace(/\b\w/g, l => l.toUpperCase());
    }

    formatCurrency(amount) {
        return new Intl.NumberFormat('en-US', {
            style: 'currency',
            currency: 'USD',
            minimumFractionDigits: 0,
            maximumFractionDigits: 0
        }).format(amount || 0);
    }

    formatDate(dateString) {
        if (!dateString) return 'N/A';
        return new Date(dateString).toLocaleDateString('en-US', {
            month: 'short',
            day: 'numeric',
            year: 'numeric'
        });
    }

    // Project Actions

    async viewProject(projectId) {
        // Fetch project details and show modal
        try {
            const response = await fetch(`/api/projects/${projectId}`);
            if (!response.ok) throw new Error('Failed to fetch project details');
            const project = await response.json();
            this.showProjectDetailModal(project);
        } catch (error) {
            this.showAlert('Could not load project details', 'danger');
        }
    }

    showProjectDetailModal(project) {
        const modalBody = document.getElementById('project-detail-body');
        modalBody.innerHTML = `
            <div><strong>Name:</strong> ${project.name}</div>
            <div><strong>Status:</strong> ${this.formatStatus(project.status)}</div>
            <div><strong>Progress:</strong> ${project.progress}%</div>
            <div><strong>Budget:</strong> ${this.formatCurrency(project.budget)}</div>
            <div><strong>Actual Cost:</strong> ${this.formatCurrency(project.actual_cost)}</div>
            <div><strong>Start Date:</strong> ${this.formatDate(project.start_date)}</div>
            <div><strong>End Date:</strong> ${this.formatDate(project.end_date)}</div>
            <div><strong>Description:</strong> ${project.description}</div>
        `;
        // Set up delete and edit buttons
        document.getElementById('delete-project-btn').onclick = () => this.deleteProject(project.id);
        document.getElementById('edit-project-btn').onclick = () => this.editProject(project.id);
        const modal = new bootstrap.Modal(document.getElementById('projectDetailModal'));
        modal.show();
    }

    async deleteProject(projectId) {
        if (!confirm('Are you sure you want to delete this project?')) return;
        try {
            const response = await fetch(`/api/projects/${projectId}`, { method: 'DELETE' });
            if (!response.ok) throw new Error('Failed to delete project');
            this.showAlert('Project deleted successfully!', 'success');
            // Close modal and reload projects
            const modal = bootstrap.Modal.getInstance(document.getElementById('projectDetailModal'));
            modal.hide();
            this.loadProjects();
        } catch (error) {
            this.showAlert('Failed to delete project', 'danger');
        }
    }

    editProject(projectId) {
        // TODO: Implement project editing
        console.log('Edit project:', projectId);
    }

    async calculateProject(projectId) {
        try {
            const calculationData = {
                calculation_type: 'load_flow',
                voltage: 480,
                current: 100,
                power_factor: 0.8,
                distance: 100
            };

            const response = await fetch(`/api/projects/${projectId}/calculations`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(calculationData)
            });

            if (response.ok) {
                const result = await response.json();
                this.showCalculationResult(result);
            } else {
                throw new Error('Calculation failed');
            }
        } catch (error) {
            console.error('Calculation error:', error);
            this.showAlert('Failed to perform calculation', 'danger');
        }
    }

    async estimateMaterials(projectId) {
        try {
            const materialsData = {
                materials: [
                    {
                        type: 'copper_thhn_12awg',
                        quantity: 1000,
                        specifications: { voltage_rating: '600V' }
                    },
                    {
                        type: 'breaker_20a_1p',
                        quantity: 20,
                        specifications: {}
                    }
                ]
            };

            const response = await fetch(`/api/projects/${projectId}/materials`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(materialsData)
            });

            if (response.ok) {
                const result = await response.json();
                this.showMaterialEstimate(result);
            } else {
                throw new Error('Material estimation failed');
            }
        } catch (error) {
            console.error('Material estimation error:', error);
            this.showAlert('Failed to estimate materials', 'danger');
        }
    }

    showCalculationResult(result) {
        // Create modal to show calculation results
        const modal = new bootstrap.Modal(document.createElement('div'));
        const modalHtml = `
            <div class="modal fade" tabindex="-1">
                <div class="modal-dialog modal-lg">
                    <div class="modal-content">
                        <div class="modal-header">
                            <h5 class="modal-title">Electrical Calculation Results</h5>
                            <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                        </div>
                        <div class="modal-body">
                            <div class="row">
                                <div class="col-md-6">
                                    <div class="calculation-card">
                                        <h5><i class="fas fa-bolt"></i> Power Analysis</h5>
                                        <div class="calculation-result">${result.load_analysis.real_power_kw} kW</div>
                                        <div class="calculation-unit">Real Power</div>
                                        <div class="mt-2">
                                            <small>Reactive: ${result.load_analysis.reactive_power_kvar} kVAR</small><br>
                                            <small>Apparent: ${result.load_analysis.apparent_power_kva} kVA</small>
                                        </div>
                                    </div>
                                </div>
                                <div class="col-md-6">
                                    <div class="calculation-card">
                                        <h5><i class="fas fa-chart-line"></i> System Performance</h5>
                                        <div class="calculation-result">${result.system_performance.voltage_drop_percent}%</div>
                                        <div class="calculation-unit">Voltage Drop</div>
                                        <div class="mt-2">
                                            <small>Efficiency: ${result.system_performance.efficiency_percent}%</small><br>
                                            <small>Losses: ${result.system_performance.copper_losses_watts} W</small>
                                        </div>
                                    </div>
                                </div>
                            </div>
                            ${result.recommendations ? this.renderRecommendations(result.recommendations) : ''}
                        </div>
                        <div class="modal-footer">
                            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                        </div>
                    </div>
                </div>
            </div>
        `;
        
        const modalElement = document.createElement('div');
        modalElement.innerHTML = modalHtml;
        document.body.appendChild(modalElement.querySelector('.modal'));
        
        const bsModal = new bootstrap.Modal(modalElement.querySelector('.modal'));
        bsModal.show();
        
        // Clean up modal when hidden
        modalElement.querySelector('.modal').addEventListener('hidden.bs.modal', () => {
            modalElement.remove();
        });
    }

    renderRecommendations(recommendations) {
        if (!recommendations.length) return '';
        
        const recHtml = recommendations.map(rec => `
            <div class="alert alert-${rec.severity === 'high' ? 'danger' : 'warning'} mt-3">
                <h6><i class="fas fa-exclamation-triangle"></i> ${rec.message}</h6>
                <p class="mb-0"><strong>Action:</strong> ${rec.action}</p>
            </div>
        `).join('');
        
        return `
            <div class="mt-4">
                <h6>Recommendations</h6>
                ${recHtml}
            </div>
        `;
    }

    showMaterialEstimate(result) {
        const modalHtml = `
            <div class="modal fade" tabindex="-1">
                <div class="modal-dialog modal-xl">
                    <div class="modal-content">
                        <div class="modal-header">
                            <h5 class="modal-title">Material Cost Estimate</h5>
                            <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                        </div>
                        <div class="modal-body">
                            <div class="row mb-4">
                                <div class="col-md-6">
                                    <div class="material-card">
                                        <div class="material-name">Total Estimated Cost</div>
                                        <div class="material-price">${this.formatCurrency(result.total_estimated_cost)}</div>
                                    </div>
                                </div>
                                <div class="col-md-6">
                                    <div class="material-card">
                                        <div class="material-name">Material Items</div>
                                        <div class="material-price">${result.materials.length}</div>
                                    </div>
                                </div>
                            </div>
                            <div class="table-responsive">
                                <table class="table table-striped">
                                    <thead>
                                        <tr>
                                            <th>Material</th>
                                            <th>Quantity</th>
                                            <th>Unit Cost</th>
                                            <th>Total Cost</th>
                                            <th>Supplier</th>
                                            <th>Lead Time</th>
                                        </tr>
                                    </thead>
                                    <tbody>
                                        ${result.materials.map(material => `
                                            <tr>
                                                <td>
                                                    <strong>${material.material_name}</strong><br>
                                                    <small class="text-muted">${material.description}</small>
                                                </td>
                                                <td>${material.quantity} ${material.unit}</td>
                                                <td>${this.formatCurrency(material.unit_cost)}</td>
                                                <td><strong>${this.formatCurrency(material.total_cost)}</strong></td>
                                                <td>${material.supplier}</td>
                                                <td>
                                                    ${material.lead_time_days} days
                                                    ${material.availability === 'In Stock' ? 
                                                        '<span class="badge bg-success">In Stock</span>' : 
                                                        '<span class="badge bg-warning">Backorder</span>'
                                                    }
                                                </td>
                                            </tr>
                                        `).join('')}
                                    </tbody>
                                </table>
                            </div>
                        </div>
                        <div class="modal-footer">
                            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                            <button type="button" class="btn btn-primary">Export to Excel</button>
                        </div>
                    </div>
                </div>
            </div>
        `;
        
        const modalElement = document.createElement('div');
        modalElement.innerHTML = modalHtml;
        document.body.appendChild(modalElement.querySelector('.modal'));
        
        const bsModal = new bootstrap.Modal(modalElement.querySelector('.modal'));
        bsModal.show();
        
        modalElement.querySelector('.modal').addEventListener('hidden.bs.modal', () => {
            modalElement.remove();
        });
    }

    showAlert(message, type = 'info') {
        const alertHtml = `
            <div class="alert alert-${type} alert-dismissible fade show" role="alert">
                ${message}
                <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
            </div>
        `;
        
        const alertContainer = document.getElementById('alert-container') || this.createAlertContainer();
        alertContainer.innerHTML = alertHtml;
        
        // Auto-dismiss after 5 seconds
        setTimeout(() => {
            const alert = alertContainer.querySelector('.alert');
            if (alert) {
                const bsAlert = new bootstrap.Alert(alert);
                bsAlert.close();
            }
        }, 5000);
    }

    createAlertContainer() {
        const container = document.createElement('div');
        container.id = 'alert-container';
        container.style.position = 'fixed';
        container.style.top = '20px';
        container.style.right = '20px';
        container.style.zIndex = '9999';
        document.body.appendChild(container);
        return container;
    }

    async updateMaterialPrices() {
        try {
            // Simulate real-time price updates
            console.log('Updating material prices...');
            // In a real implementation, this would call the material pricing API
        } catch (error) {
            console.error('Failed to update material prices:', error);
        }
    }

    startAutoRefresh() {
        // Refresh project data every 30 seconds
        setInterval(() => {
            this.loadProjects();
        }, 30000);
    }
}

// Global functions
function showTab(tabName) {
    // Hide all content
    document.getElementById('dashboard-content').style.display = 'none';
    document.getElementById('projects-content').style.display = 'none';
    document.getElementById('calculations-content').style.display = 'none';
    document.getElementById('materials-content').style.display = 'none';
    
    // Show selected tab
    const contentElement = document.getElementById(`${tabName}-content`);
    if (contentElement) {
        contentElement.style.display = 'block';
    }
    
    // Update navigation
    document.querySelectorAll('.navbar-nav .nav-link').forEach(link => {
        link.classList.remove('active');
    });
    document.querySelector(`[onclick="showTab('${tabName}')"]`).classList.add('active');
}

function openCreateProjectModal() {
    const modal = new bootstrap.Modal(document.getElementById('createProjectModal'));
    modal.show();
}

async function createProject() {
    const form = document.getElementById('createProjectForm');
    const formData = new FormData(form);
    
    const projectData = {
        name: formData.get('name'),
        type: formData.get('type'),
        description: formData.get('description'),
        start_date: formData.get('start_date'),
        end_date: formData.get('end_date'),
        budget: parseFloat(formData.get('budget') || 0),
        voltage_level: formData.get('voltage_level')
    };
    
    try {
        const response = await fetch('/api/projects', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(projectData)
        });
        
        if (response.ok) {
            const result = await response.json();
            dashboard.showAlert('Project created successfully!', 'success');
            
            // Close modal and reload projects
            const modal = bootstrap.Modal.getInstance(document.getElementById('createProjectModal'));
            modal.hide();
            form.reset();
            dashboard.loadProjects();
        } else {
            throw new Error('Failed to create project');
        }
    } catch (error) {
        console.error('Error creating project:', error);
        dashboard.showAlert('Failed to create project', 'danger');
    }
}

// Initialize dashboard when page loads
let dashboard;
document.addEventListener('DOMContentLoaded', function() {
    dashboard = new DashboardApp();
});