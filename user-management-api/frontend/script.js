// API Configuration
const API_BASE_URL = 'http://localhost:5000/api';

// Global State
let currentUser = null;
let authToken = null;

// DOM Elements
const elements = {
    // Sections
    loginSection: document.getElementById('loginSection'),
    registerSection: document.getElementById('registerSection'),
    dashboardSection: document.getElementById('dashboardSection'),
    
    // Navigation
    loginTab: document.getElementById('loginTab'),
    registerTab: document.getElementById('registerTab'),
    dashboardTab: document.getElementById('dashboardTab'),
    logoutBtn: document.getElementById('logoutBtn'),
    
    // Forms
    loginForm: document.getElementById('loginForm'),
    registerForm: document.getElementById('registerForm'),
    editForm: document.getElementById('editForm'),
    
    // Profile elements
    profileUsername: document.getElementById('profileUsername'),
    profileEmail: document.getElementById('profileEmail'),
    profileCreated: document.getElementById('profileCreated'),
    avatarImg: document.getElementById('avatarImg'),
    avatarUpload: document.getElementById('avatarUpload'),
    changeAvatarBtn: document.getElementById('changeAvatarBtn'),
    
    // Statistics
    totalUsers: document.getElementById('totalUsers'),
    todayUsers: document.getElementById('todayUsers'),
    totalLogs: document.getElementById('totalLogs'),
    
    // Logs
    logsContainer: document.getElementById('logsContainer'),
    logsLimit: document.getElementById('logsLimit'),
    
    // Modal
    editModal: document.getElementById('editModal'),
    modalTitle: document.getElementById('modalTitle'),
    editLabel: document.getElementById('editLabel'),
    editInput: document.getElementById('editInput'),
    
    // Alert container
    alertContainer: document.getElementById('alertContainer')
};

// Utility Functions
function showAlert(message, type = 'info') {
    const alert = document.createElement('div');
    alert.className = `alert alert-${type}`;
    alert.textContent = message;
    
    elements.alertContainer.appendChild(alert);
    
    // Auto remove after 5 seconds
    setTimeout(() => {
        if (alert.parentNode) {
            alert.parentNode.removeChild(alert);
        }
    }, 5000);
}

function setLoading(button, loading) {
    const btnText = button.querySelector('.btn-text');
    const btnLoading = button.querySelector('.btn-loading');
    
    if (loading) {
        btnText.classList.add('hidden');
        btnLoading.classList.remove('hidden');
        button.disabled = true;
    } else {
        btnText.classList.remove('hidden');
        btnLoading.classList.add('hidden');
        button.disabled = false;
    }
}

function formatDate(dateString) {
    try {
        const date = new Date(dateString);
        return date.toLocaleDateString('en-US', {
            year: 'numeric',
            month: 'long',
            day: 'numeric'
        });
    } catch {
        return 'Unknown';
    }
}

function formatDateTime(dateString) {
    try {
        const date = new Date(dateString);
        return date.toLocaleString('en-US', {
            month: 'short',
            day: 'numeric',
            hour: '2-digit',
            minute: '2-digit'
        });
    } catch {
        return 'Unknown';
    }
}

// API Functions
async function apiRequest(endpoint, options = {}) {
    const url = `${API_BASE_URL}${endpoint}`;
    const config = {
        headers: {
            'Content-Type': 'application/json',
            ...options.headers
        },
        ...options
    };

    // Add auth token if available
    if (authToken) {
        config.headers['Authorization'] = `Bearer ${authToken}`;
    }

    try {
        const response = await fetch(url, config);
        const data = await response.json();
        
        if (!response.ok) {
            throw new Error(data.error || 'Request failed');
        }
        
        return data;
    } catch (error) {
        console.error('API Request Error:', error);
        throw error;
    }
}

// Authentication Functions
async function login(username, password) {
    const data = await apiRequest('/login', {
        method: 'POST',
        body: JSON.stringify({ username, password })
    });
    
    if (data.success) {
        authToken = data.token;
        currentUser = data.user;
        localStorage.setItem('authToken', authToken);
        localStorage.setItem('currentUser', JSON.stringify(currentUser));
        return data;
    }
    
    throw new Error(data.error);
}

async function register(username, email, password) {
    const data = await apiRequest('/register', {
        method: 'POST',
        body: JSON.stringify({ username, email, password })
    });
    
    if (data.success) {
        return data;
    }
    
    throw new Error(data.error);
}

async function validateToken() {
    try {
        const data = await apiRequest('/validate-token');
        if (data.success) {
            currentUser = data.user;
            return true;
        }
    } catch (error) {
        console.error('Token validation failed:', error);
        logout();
    }
    return false;
}

function logout() {
    authToken = null;
    currentUser = null;
    localStorage.removeItem('authToken');
    localStorage.removeItem('currentUser');
    showAuthSection();
}

// UI Navigation Functions
function showSection(sectionName) {
    // Hide all sections
    elements.loginSection.classList.add('hidden');
    elements.registerSection.classList.add('hidden');
    elements.dashboardSection.classList.add('hidden');
    
    // Remove active class from all nav links
    document.querySelectorAll('.nav-link').forEach(link => {
        link.classList.remove('active');
    });
    
    // Show selected section and activate nav link
    switch(sectionName) {
        case 'login':
            elements.loginSection.classList.remove('hidden');
            elements.loginTab.classList.add('active');
            break;
        case 'register':
            elements.registerSection.classList.remove('hidden');
            elements.registerTab.classList.add('active');
            break;
        case 'dashboard':
            elements.dashboardSection.classList.remove('hidden');
            elements.dashboardTab.classList.add('active');
            break;
    }
}

function showAuthSection() {
    // Show auth navigation, hide dashboard navigation
    elements.loginTab.classList.remove('hidden');
    elements.registerTab.classList.remove('hidden');
    elements.dashboardTab.classList.add('hidden');
    elements.logoutBtn.classList.add('hidden');
    
    showSection('login');
}

function showDashboardSection() {
    // Hide auth navigation, show dashboard navigation
    elements.loginTab.classList.add('hidden');
    elements.registerTab.classList.add('hidden');
    elements.dashboardTab.classList.remove('hidden');
    elements.logoutBtn.classList.remove('hidden');
    
    showSection('dashboard');
    loadDashboardData();
}

// Dashboard Functions
async function loadDashboardData() {
    try {
        // Load profile
        await loadProfile();
        
        // Load statistics
        await loadStatistics();
        
        // Load logs
        await loadLogs();
        
    } catch (error) {
        console.error('Failed to load dashboard data:', error);
        showAlert('Failed to load dashboard data', 'error');
    }
}

async function loadProfile() {
    try {
        const data = await apiRequest('/profile');
        if (data.success) {
            const user = data.user;
            elements.profileUsername.textContent = user.username;
            elements.profileEmail.textContent = user.email;
            elements.profileCreated.textContent = formatDate(user.created_at);
            
            // Load avatar
            if (user.avatar_filename && user.avatar_filename !== 'default-avatar.png') {
                elements.avatarImg.src = `${API_BASE_URL}/avatar/${user.avatar_filename}`;
            } else {
                elements.avatarImg.src = `data:image/svg+xml,${encodeURIComponent('<svg xmlns="http://www.w3.org/2000/svg" width="100" height="100" viewBox="0 0 100 100"><rect width="100" height="100" fill="#e5e7eb"/><text x="50" y="55" font-size="30" text-anchor="middle" fill="#9ca3af">👤</text></svg>')}`;
            }
        }
    } catch (error) {
        console.error('Failed to load profile:', error);
    }
}

async function loadStatistics() {
    try {
        const data = await apiRequest('/stats');
        if (data.success) {
            const stats = data.stats;
            elements.totalUsers.textContent = stats.total_users;
            elements.todayUsers.textContent = stats.today_users;
            elements.totalLogs.textContent = stats.total_logs;
        }
    } catch (error) {
        console.error('Failed to load statistics:', error);
    }
}

async function loadLogs() {
    try {
        const limit = elements.logsLimit.value;
        const data = await apiRequest(`/logs?limit=${limit}`);
        
        if (data.success) {
            displayLogs(data.logs);
        }
    } catch (error) {
        console.error('Failed to load logs:', error);
        elements.logsContainer.innerHTML = '<div class="logs-loading">❌ Failed to load logs</div>';
    }
}

function displayLogs(logs) {
    if (logs.length === 0) {
        elements.logsContainer.innerHTML = '<div class="logs-loading">📭 No logs found</div>';
        return;
    }
    
    const logsHTML = logs.map(log => {
        const actionClass = log.action.toLowerCase().includes('error') ? 'error' :
                           log.action.toLowerCase().includes('login') ? 'login' :
                           log.action.toLowerCase().includes('register') ? 'register' : 'profile';
        
        return `
            <div class="log-entry">
                <div class="log-timestamp">${formatDateTime(log.timestamp)}</div>
                <div class="log-user">${log.username}</div>
                <div class="log-action ${actionClass}">${log.action}</div>
                <div class="log-details">${log.details || '-'}</div>
                <div class="log-ip">${log.ip_address || '-'}</div>
            </div>
        `;
    }).join('');
    
    elements.logsContainer.innerHTML = logsHTML;
}

// Profile Management
async function updateProfile(field, value) {
    try {
        const updateData = {};
        updateData[field] = value;
        
        const data = await apiRequest('/profile', {
            method: 'PUT',
            body: JSON.stringify(updateData)
        });
        
        if (data.success) {
            showAlert(`${field} updated successfully!`, 'success');
            await loadProfile(); // Reload profile
            return true;
        }
        
        throw new Error(data.error);
    } catch (error) {
        showAlert(`Failed to update ${field}: ${error.message}`, 'error');
        return false;
    }
}

async function uploadAvatar(file) {
    try {
        const formData = new FormData();
        formData.append('avatar', file);
        
        const response = await fetch(`${API_BASE_URL}/upload-avatar`, {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${authToken}`
            },
            body: formData
        });
        
        const data = await response.json();
        
        if (data.success) {
            showAlert('Avatar updated successfully!', 'success');
            await loadProfile(); // Reload profile to show new avatar
        } else {
            throw new Error(data.error);
        }
    } catch (error) {
        showAlert(`Failed to upload avatar: ${error.message}`, 'error');
    }
}

// Event Listeners
document.addEventListener('DOMContentLoaded', function() {
    // Check for existing token
    const savedToken = localStorage.getItem('authToken');
    const savedUser = localStorage.getItem('currentUser');
    
    if (savedToken && savedUser) {
        authToken = savedToken;
        currentUser = JSON.parse(savedUser);
        validateToken().then(isValid => {
            if (isValid) {
                showDashboardSection();
            } else {
                showAuthSection();
            }
        });
    } else {
        showAuthSection();
    }
    
    // Navigation event listeners
    elements.loginTab.addEventListener('click', (e) => {
        e.preventDefault();
        showSection('login');
    });
    
    elements.registerTab.addEventListener('click', (e) => {
        e.preventDefault();
        showSection('register');
    });
    
    elements.dashboardTab.addEventListener('click', (e) => {
        e.preventDefault();
        showSection('dashboard');
    });
    
    elements.logoutBtn.addEventListener('click', (e) => {
        e.preventDefault();
        logout();
        showAlert('Logged out successfully', 'info');
    });
    
    // Auth form switches
    document.getElementById('switchToRegister').addEventListener('click', (e) => {
        e.preventDefault();
        showSection('register');
    });
    
    document.getElementById('switchToLogin').addEventListener('click', (e) => {
        e.preventDefault();
        showSection('login');
    });
    
    // Form submissions
    elements.loginForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const username = document.getElementById('loginUsername').value.trim();
        const password = document.getElementById('loginPassword').value;
        const submitBtn = document.getElementById('loginSubmit');
        
        setLoading(submitBtn, true);
        
        try {
            await login(username, password);
            showAlert('Login successful!', 'success');
            showDashboardSection();
        } catch (error) {
            showAlert(error.message, 'error');
        } finally {
            setLoading(submitBtn, false);
        }
    });
    
    elements.registerForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const username = document.getElementById('registerUsername').value.trim();
        const email = document.getElementById('registerEmail').value.trim();
        const password = document.getElementById('registerPassword').value;
        const confirmPassword = document.getElementById('confirmPassword').value;
        const submitBtn = document.getElementById('registerSubmit');
        
        // Validation
        if (password !== confirmPassword) {
            showAlert('Passwords do not match', 'error');
            return;
        }
        
        setLoading(submitBtn, true);
        
        try {
            await register(username, email, password);
            showAlert('Registration successful! Please login.', 'success');
            showSection('login');
            elements.registerForm.reset();
        } catch (error) {
            showAlert(error.message, 'error');
        } finally {
            setLoading(submitBtn, false);
        }
    });
    
    // Profile edit buttons
    document.getElementById('editUsernameBtn').addEventListener('click', () => {
        showEditModal('username', 'Username', elements.profileUsername.textContent);
    });
    
    document.getElementById('editEmailBtn').addEventListener('click', () => {
        showEditModal('email', 'Email', elements.profileEmail.textContent);
    });
    
    // Avatar upload
    elements.changeAvatarBtn.addEventListener('click', () => {
        elements.avatarUpload.click();
    });
    
    elements.avatarUpload.addEventListener('change', (e) => {
        const file = e.target.files[0];
        if (file) {
            // Validate file
            if (!file.type.startsWith('image/')) {
                showAlert('Please select an image file', 'error');
                return;
            }
            
            if (file.size > 5 * 1024 * 1024) { // 5MB
                showAlert('File too large. Maximum 5MB allowed', 'error');
                return;
            }
            
            uploadAvatar(file);
        }
    });
    
    // Refresh buttons
    document.getElementById('refreshStatsBtn').addEventListener('click', loadStatistics);
    document.getElementById('refreshLogsBtn').addEventListener('click', loadLogs);
    
    // Logs limit change
    elements.logsLimit.addEventListener('change', loadLogs);
    
    // Modal event listeners
    document.getElementById('closeModal').addEventListener('click', hideEditModal);
    document.getElementById('cancelEdit').addEventListener('click', hideEditModal);
    
    elements.editForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const field = elements.editInput.dataset.field;
        const value = elements.editInput.value.trim();
        
        if (!value) {
            showAlert('Value cannot be empty', 'error');
            return;
        }
        
        const success = await updateProfile(field, value);
        if (success) {
            hideEditModal();
        }
    });
    
    // Close modal on background click
    elements.editModal.addEventListener('click', (e) => {
        if (e.target === elements.editModal) {
            hideEditModal();
        }
    });
});

// Modal Functions
function showEditModal(field, label, currentValue) {
    elements.modalTitle.textContent = `Edit ${label}`;
    elements.editLabel.textContent = `${label}:`;
    elements.editInput.value = currentValue;
    elements.editInput.dataset.field = field;
    
    elements.editModal.classList.remove('hidden');
    elements.editInput.focus();
}

function hideEditModal() {
    elements.editModal.classList.add('hidden');
    elements.editForm.reset();
}