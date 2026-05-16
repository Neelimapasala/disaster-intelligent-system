
        function createParticles() {
            const particlesContainer = document.getElementById('particles');
            if (!particlesContainer) return;
            particlesContainer.innerHTML = '';
            for (let i = 0; i < 50; i++) {
                const particle = document.createElement('div');
                particle.className = 'particle';
                const size = Math.random() * 5 + 4;
                particle.style.width = size + 'px';
                particle.style.height = size + 'px';
                particle.style.left = Math.random() * 100 + '%';
                particle.style.animationDelay = Math.random() * 20 + 's';
                particle.style.animationDuration = 15 + Math.random() * 10 + 's';
                particlesContainer.appendChild(particle);
            }
        }

        createParticles();

        let selectedEventId = null;
        let allEvents = [];
        let chatOpen = false;
        let currentStep = 1;
        let uploadedFiles = [];

        function updateSeverity(value) {
            const severityValue = document.getElementById('severityValue');
            if (severityValue) {
                severityValue.textContent = value + '/10';
            }
        }

        function toggleSection(id) {
            const element = document.getElementById(id);
            if (!element) return;
            element.style.display = element.style.display === 'block' ? 'none' : 'block';
        }

        function toggleChat() {
            chatOpen = !chatOpen;
            const chatbotWindow = document.getElementById('chatbotWindow');
            const chatbotToggle = document.getElementById('chatbotToggle');
            const chatNotification = document.getElementById('chatNotification');
            if (chatbotWindow) {
                if (chatOpen) {
                    chatbotWindow.classList.add('active');
                } else {
                    chatbotWindow.classList.remove('active');
                }
            }
            if (chatbotToggle) {
                if (chatOpen) {
                    chatbotToggle.classList.add('active');
                } else {
                    chatbotToggle.classList.remove('active');
                }
            }
            if (chatNotification) {
                chatNotification.style.display = 'none';
            }
            if (chatOpen) {
                const chatInput = document.getElementById('chatInput');
                if (chatInput) chatInput.focus();
            }
        }

        function handleChatKeyPress(e) {
            if (e.key === 'Enter') {
                sendChat();
            }
        }

        function sendChat() {
            const input = document.getElementById('chatInput');
            if (!input) return;
            const message = input.value.trim();
            if (!message) return;
            addChatMessage(message, 'user');
            input.value = '';
            fetch('/api/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ message: message })
            })
            .then(function(response) {
                return response.json();
            })
            .then(function(data) {
                if (data.status === 'success') {
                    addChatMessage(data.data.response, 'bot');
                } else {
                    addChatMessage('The chatbot did not respond. Please try again.', 'bot');
                }
            })
            .catch(function() {
                addChatMessage('Sorry, there was an error sending your chat message.', 'bot');
            });
        }

        function addChatMessage(text, sender) {
            const messagesDiv = document.getElementById('chatMessages');
            if (!messagesDiv) return;
            const messageDiv = document.createElement('div');
            messageDiv.className = 'message ' + sender;
            const icon = document.createElement('div');
            icon.className = 'message-icon';
            icon.innerHTML = sender === 'bot' ? '<i class="fas fa-robot"></i>' : '<i class="fas fa-user"></i>';
            const bubble = document.createElement('div');
            bubble.className = 'message-bubble';
            bubble.textContent = text;
            messageDiv.appendChild(icon);
            messageDiv.appendChild(bubble);
            messagesDiv.appendChild(messageDiv);
            messagesDiv.scrollTop = messagesDiv.scrollHeight;
        }

        function createDisaster() {
            const type = document.getElementById('type') ? document.getElementById('type').value : '';
            const location = document.getElementById('location') ? document.getElementById('location').value : '';
            const lat = document.getElementById('latitude') ? document.getElementById('latitude').value : '';
            const lon = document.getElementById('longitude') ? document.getElementById('longitude').value : '';
            const sev = document.getElementById('severity') ? document.getElementById('severity').value : 0;
            const pop = document.getElementById('population') ? document.getElementById('population').value : 0;
            if (!location || !lat || !lon || !pop) {
                showAlert('Please fill all required fields.', 'error', 'createAlerts');
                return;
            }
            const loading = document.getElementById('createLoading');
            if (loading) loading.classList.add('show');
            fetch('/api/disasters/create', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ type: type, location: location, latitude: parseFloat(lat), longitude: parseFloat(lon), severity: parseFloat(sev), affected_population: parseInt(pop, 10) })
            })
            .then(function(response) { return response.json(); })
            .then(function(data) {
                if (loading) loading.classList.remove('show');
                if (data.status === 'success') {
                    showAlert('Disaster reported successfully.', 'success', 'createAlerts');
                    if (document.getElementById('location')) document.getElementById('location').value = '';
                    if (document.getElementById('population')) document.getElementById('population').value = '';
                    if (document.getElementById('latitude')) document.getElementById('latitude').value = '';
                    if (document.getElementById('longitude')) document.getElementById('longitude').value = '';
                    refreshEvents();
                    var chatNotification = document.getElementById('chatNotification');
                    if (chatNotification) chatNotification.style.display = 'flex';
                }
            })
            .catch(function(error) {
                if (loading) loading.classList.remove('show');
                showAlert('Error: ' + error.message, 'error', 'createAlerts');
            });
        }

        function analyzeDisaster() {
            if (!selectedEventId) {
                showAlert('Please select an event first.', 'error', 'analyzeAlerts');
                return;
            }
            const loading = document.getElementById('analyzeLoading');
            if (loading) loading.classList.add('show');
            fetch('/api/disasters/' + selectedEventId + '/analyze', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' }
            })
            .then(function(response) { return response.json(); })
            .then(function(data) {
                if (loading) loading.classList.remove('show');
                if (data.status === 'success') {
                    displayAnalysis(data.data);
                    showAlert('AI analysis is complete.', 'success', 'analyzeAlerts');
                    refreshEvents();
                }
            })
            .catch(function(error) {
                if (loading) loading.classList.remove('show');
                showAlert('Error: ' + error.message, 'error', 'analyzeAlerts');
            });
        }

        function displayAnalysis(data) {
            const a = data.analysis || {};
            const hazard = document.getElementById('hazard');
            const zones = document.getElementById('zones');
            const routes = document.getElementById('routes');
            const hospitals = document.getElementById('hospitals');
            const resourcesList = document.getElementById('resourcesList');
            const recommendations = document.getElementById('recommendations');
            if (hazard) hazard.innerHTML = '<i class="fas fa-exclamation-triangle"></i> ' + (a.hazard || 'N/A');
            if (zones) zones.innerHTML = (a.safe_zones || []).map(function(item) { return '<div class="list-item"><i class="fas fa-location-dot"></i> ' + item + '</div>'; }).join('') || '<div>No data</div>';
            if (routes) routes.innerHTML = (a.routes || []).map(function(item) { return '<div class="list-item"><i class="fas fa-route"></i> ' + item + '</div>'; }).join('') || '<div>No data</div>';
            if (hospitals) hospitals.innerHTML = '<i class="fas fa-hospital"></i> ' + (a.hospitals || 'N/A');
            if (resourcesList) resourcesList.innerHTML = (a.resources || []).map(function(item) { return '<div class="list-item"><i class="fas fa-box"></i> ' + item + '</div>'; }).join('') || '<div>No data</div>';
            if (recommendations) recommendations.innerHTML = (a.recommendations || []).map(function(item) { return '<div class="list-item"><i class="fas fa-check-circle"></i> ' + item + '</div>'; }).join('') || '<div>No data</div>';
            const analysisResults = document.getElementById('analysisResults');
            if (analysisResults) analysisResults.classList.add('show');
            window.scrollTo({ top: 0, behavior: 'smooth' });
        }

        function refreshEvents() {
            fetch('/api/dashboard').then(function(response) {
                return response.json();
            }).then(function(data) {
                allEvents = data.data.recent_events || [];
                updateEventsList();
                updateStats();
            }).catch(function() {
                // ignore refresh failures
            });
        }

        function updateEventsList() {
            const sel = document.getElementById('eventSelect');
            const list = document.getElementById('eventsList');
            if (sel) sel.innerHTML = '<option value="">-- Select Event --</option>';
            if (list) list.innerHTML = '';
            if (!allEvents || allEvents.length === 0) {
                if (list) list.innerHTML = '<p style="color:#999; text-align:center; padding:40px;"><i class="fas fa-inbox"></i><br>No events reported yet</p>';
                return;
            }
            allEvents.forEach(function(event) {
                const opt = document.createElement('option');
                opt.value = event.id;
                opt.textContent = event.type + ' - ' + event.location;
                if (sel) sel.appendChild(opt);
                if (!list) return;
                const card = document.createElement('div');
                card.className = 'event-card ' + (event.type ? event.type.toLowerCase() : 'event');
                card.innerHTML = '<h3>' + (event.type || '') + '</h3>' +
                    '<p><i class="fas fa-map-marker-alt"></i> ' + (event.location || '') + '</p>' +
                    '<p><i class="fas fa-users"></i> ' + (event.affected_population || 0) + ' affected</p>' +
                    '<p><i class="fas fa-gauge-high"></i> Severity: ' + (event.severity || 0) + '/10</p>' +
                    '<span class="status-badge ' + (event.status === 'ANALYZED' ? 'status-analyzed' : 'status-reported') + '">' + (event.status || '') + '</span>';
                list.appendChild(card);
            });
        }

        function updateStats() {
            const totalEvents = document.getElementById('total-events');
            const totalAffected = document.getElementById('total-affected');
            const analyzedCount = document.getElementById('analyzed-count');
            if (totalEvents) totalEvents.textContent = (allEvents ? allEvents.length : 0);
            if (totalAffected) totalAffected.textContent = (allEvents ? allEvents.reduce(function(sum, event) { return sum + (event.affected_population || 0); }, 0) : 0).toLocaleString();
            if (analyzedCount) analyzedCount.textContent = (allEvents ? allEvents.filter(function(event) { return event.status === 'ANALYZED'; }).length : 0);
            fetch('/api/alerts').then(function(response) { return response.json(); }).then(function(data) {
                const activeAlerts = document.getElementById('active-alerts');
                if (activeAlerts) activeAlerts.textContent = (data.data && data.data.count) ? data.data.count : 0;
            }).catch(function() {
                // ignore
            });
        }

        function updateEvent() {
            const select = document.getElementById('eventSelect');
            if (select) selectedEventId = select.value;
        }

        function showAlert(message, type, containerId) {
            const container = document.getElementById(containerId);
            if (!container) return;
            const alert = document.createElement('div');
            alert.className = 'alert ' + type;
            alert.innerHTML = '<i class="fas fa-' + (type === 'success' ? 'check-circle' : 'exclamation-circle') + '"></i><span>' + message + '</span>';
            container.innerHTML = '';
            container.appendChild(alert);
            setTimeout(function() { if (alert.parentElement) alert.parentElement.removeChild(alert); }, 5000);
        }

        function updateStepVisibility() {
            var stepIds = ['step1Content', 'step2Content', 'step3Content'];
            stepIds.forEach(function(id) {
                var el = document.getElementById(id);
                if (el) {
                    el.style.display = 'none';
                }
            });
            var current = document.getElementById('step' + currentStep + 'Content');
            if (current) current.style.display = 'block';
            for (var i = 1; i <= 4; i++) {
                var stepEl = document.getElementById('step' + i);
                if (!stepEl) continue;
                if (i < currentStep) {
                    stepEl.className = 'step completed';
                } else if (i === currentStep) {
                    stepEl.className = 'step active';
                } else {
                    stepEl.className = 'step';
                }
            }
            var progressEl = document.getElementById('progress');
            if (progressEl) progressEl.style.width = (currentStep / 4 * 100) + '%';
        }

        function nextStep(step) {
            currentStep = step;
            updateStepVisibility();
        }

        function prevStep(step) {
            currentStep = step;
            updateStepVisibility();
        }

        function getCurrentLocation() {
            var statusDiv = document.getElementById('locationStatus');
            if (statusDiv) {
                statusDiv.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Fetching your location...';
            }
            if (!navigator.geolocation) {
                if (statusDiv) statusDiv.innerHTML = '<i class="fas fa-exclamation-circle"></i> Geolocation not available.';
                return;
            }
            navigator.geolocation.getCurrentPosition(function(position) {
                var lat = position.coords.latitude.toFixed(4);
                var lon = position.coords.longitude.toFixed(4);
                var latInput = document.getElementById('latitude');
                var lonInput = document.getElementById('longitude');
                if (latInput) latInput.value = lat;
                if (lonInput) lonInput.value = lon;
                fetch('https://nominatim.openstreetmap.org/reverse?format=json&lat=' + lat + '&lon=' + lon + '&zoom=18&addressdetails=1')
                .then(function(response) { return response.json(); })
                .then(function(data) {
                    var locationName = (data.address && (data.address.city || data.address.town || data.address.village)) || 'Unknown location';
                    var locationInput = document.getElementById('location');
                    if (locationInput) locationInput.value = locationName;
                    if (statusDiv) statusDiv.innerHTML = '<i class="fas fa-check-circle"></i> Location captured.';
                    setTimeout(function() { if (statusDiv) statusDiv.innerHTML = ''; }, 3000);
                }).catch(function() {
                    if (statusDiv) statusDiv.innerHTML = '<i class="fas fa-check-circle"></i> Coordinates captured.';
                    setTimeout(function() { if (statusDiv) statusDiv.innerHTML = ''; }, 3000);
                });
            }, function() {
                if (statusDiv) statusDiv.innerHTML = '<i class="fas fa-exclamation-circle"></i> Location permission denied or unavailable.';
            });
        }

        function previewMedia(input) {
            var preview = document.getElementById('preview');
            if (!preview || !input.files) return;
            preview.innerHTML = '';
            uploadedFiles = Array.prototype.slice.call(input.files);
            uploadedFiles.forEach(function(file) {
                var reader = new FileReader();
                reader.onload = function(event) {
                    var wrapper = document.createElement('div');
                    if (file.type.indexOf('image/') === 0) {
                        wrapper.innerHTML = '<img src="' + event.target.result + '" style="width:100%;height:100px;object-fit:cover;border-radius:8px;">';
                    } else {
                        wrapper.innerHTML = '<video style="width:100%;height:100px;object-fit:cover;border-radius:8px;" controls><source src="' + event.target.result + '"></video>';
                    }
                    preview.appendChild(wrapper);
                };
                reader.readAsDataURL(file);
            });
        }

        function submitEnhancedReport() {
            var reportData = {
                type: document.getElementById('type') ? document.getElementById('type').value : '',
                location: document.getElementById('location') ? document.getElementById('location').value : '',
                latitude: parseFloat(document.getElementById('latitude') ? document.getElementById('latitude').value : 0),
                longitude: parseFloat(document.getElementById('longitude') ? document.getElementById('longitude').value : 0),
                severity: parseInt(document.getElementById('severity') ? document.getElementById('severity').value : '5', 10),
                affected_population: parseInt(document.getElementById('population') ? document.getElementById('population').value : '0', 10) || 0,
                incidentDateTime: document.getElementById('incidentDateTime') ? document.getElementById('incidentDateTime').value : '',
                description: document.getElementById('description') ? document.getElementById('description').value : '',
                weather: document.getElementById('weather') ? document.getElementById('weather').value : '',
                deaths: parseInt(document.getElementById('deaths') ? document.getElementById('deaths').value : '0', 10) || 0,
                injured: parseInt(document.getElementById('injured') ? document.getElementById('injured').value : '0', 10) || 0,
                missing: parseInt(document.getElementById('missing') ? document.getElementById('missing').value : '0', 10) || 0,
                displaced: parseInt(document.getElementById('displaced') ? document.getElementById('displaced').value : '0', 10) || 0,
                buildingsDamaged: parseInt(document.getElementById('buildingsDamaged') ? document.getElementById('buildingsDamaged').value : '0', 10) || 0,
                buildingsDestroyed: parseInt(document.getElementById('buildingsDestroyed') ? document.getElementById('buildingsDestroyed').value : '0', 10) || 0,
                roadsBlocked: parseInt(document.getElementById('roadsBlocked') ? document.getElementById('roadsBlocked').value : '0', 10) || 0,
                bridgesDamaged: parseInt(document.getElementById('bridgesDamaged') ? document.getElementById('bridgesDamaged').value : '0', 10) || 0,
                resources: Array.prototype.slice.call(document.querySelectorAll('.resource-need:checked')).map(function(cb) { return cb.value; }),
                reportType: document.getElementById('reportType') ? document.getElementById('reportType').value : '',
                urgency: document.querySelector('input[name="urgency"]:checked') ? document.querySelector('input[name="urgency"]:checked').value : 'medium',
                contactName: document.getElementById('contactName') ? document.getElementById('contactName').value : '',
                contactPhone: document.getElementById('contactPhone') ? document.getElementById('contactPhone').value : ''
            };

            if (!reportData.location || !reportData.latitude || !reportData.longitude) {
                showAlert('Please provide valid location information.', 'error', 'createAlerts');
                currentStep = 1;
                updateStepVisibility();
                return;
            }
            if (!reportData.type) {
                showAlert('Please select a disaster type.', 'error', 'createAlerts');
                currentStep = 2;
                updateStepVisibility();
                return;
            }
            var loading = document.getElementById('createLoading');
            if (loading) loading.classList.add('show');
            fetch('/api/disasters/create', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(reportData)
            })
            .then(function(response) { return response.json(); })
            .then(function(data) {
                if (loading) loading.classList.remove('show');
                if (data.status === 'success') {
                    showAlert('Disaster report submitted successfully.', 'success', 'createAlerts');
                    if (document.getElementById('location')) document.getElementById('location').value = '';
                    if (document.getElementById('population')) document.getElementById('population').value = '';
                    if (document.getElementById('description')) document.getElementById('description').value = '';
                    refreshEvents();
                    var chatNotification = document.getElementById('chatNotification');
                    if (chatNotification) chatNotification.style.display = 'flex';
                    currentStep = 1;
                    updateStepVisibility();
                }
            })
            .catch(function(error) {
                if (loading) loading.classList.remove('show');
                showAlert('Error: ' + error.message, 'error', 'createAlerts');
            });
        }

        function registerVolunteer() {
            var name = document.getElementById('volunteerName') ? document.getElementById('volunteerName').value : '';
            if (name) {
                showAlert('Thank you ' + name + '! You are now registered as a volunteer.', 'success', 'createAlerts');
                if (document.getElementById('volunteerName')) document.getElementById('volunteerName').value = '';
                if (document.getElementById('volunteerEmail')) document.getElementById('volunteerEmail').value = '';
                if (document.getElementById('volunteerPhone')) document.getElementById('volunteerPhone').value = '';
            } else {
                showAlert('Please enter your name to register.', 'error', 'createAlerts');
            }
        }

        function processDonation() {
            var amountEl = document.getElementById('customAmount');
            if (!amountEl) return;
            var amount = amountEl.value.trim();
            if (amount && Number(amount) > 0) {
                showAlert('Thank you for your donation of $' + amount + '.', 'success', 'createAlerts');
                amountEl.value = '';
            } else {
                showAlert('Please enter a valid donation amount.', 'error', 'createAlerts');
            }
        }

        function markSafe() {
            var name = document.getElementById('checkinName') ? document.getElementById('checkinName').value : '';
            var location = document.getElementById('checkinLocation') ? document.getElementById('checkinLocation').value : '';
            if (!name) {
                showAlert('Please enter your name to mark yourself safe.', 'error', 'createAlerts');
                return;
            }
            var safeList = document.getElementById('safeList');
            if (safeList) {
                var entry = document.createElement('div');
                entry.className = 'safe-entry';
                entry.style.cssText = 'padding: 10px; background: #d1fae5; border-radius: 10px; margin-top: 10px;';
                entry.innerHTML = '<i class="fas fa-user-check"></i> ' + name + ' - Safe at ' + (location || 'unknown location');
                safeList.appendChild(entry);
            }
            showAlert('You have been marked safe.', 'success', 'createAlerts');
            if (document.getElementById('checkinName')) document.getElementById('checkinName').value = '';
            if (document.getElementById('checkinLocation')) document.getElementById('checkinLocation').value = '';
        }

        function changeLanguage(lang) {
            var messages = {
                es: 'Idioma cambiado a Español.',
                hi: 'भाषा हिंदी में बदल गई।',
                fr: 'Langue changée en français.',
                en: 'Language changed to English.'
            };
            alert(messages[lang] || 'Language changed.');
        }

        var highContrastEnabled = false;
        function highContrast() {
            highContrastEnabled = !highContrastEnabled;
            document.body.style.filter = highContrastEnabled ? 'invert(1) hue-rotate(180deg)' : 'none';
        }

        function increaseFont() {
            var currentSize = parseFloat(window.getComputedStyle(document.body).fontSize) || 16;
            document.body.style.fontSize = (currentSize + 2) + 'px';
        }

        function readAloud() {
            if (!window.speechSynthesis) return;
            var text = document.body.innerText || '';
            var utterance = new SpeechSynthesisUtterance(text);
            utterance.lang = 'en-US';
            window.speechSynthesis.speak(utterance);
        }

        function toggleAccessibility() {
            var options = document.getElementById('accessibilityOptions');
            if (!options) return;
            options.style.display = options.style.display === 'block' ? 'none' : 'block';
        }

        function playVideo(topic) {
            alert('Training video will play: ' + topic);
        }

        function showWeatherDetails() {
            alert('Weather Alert Details:\n\nHeavy rainfall expected in coastal regions. Stay safe and avoid low areas.');
        }

        function selectDonation(amount) {
            var customAmount = document.getElementById('customAmount');
            if (customAmount) customAmount.value = amount;
        }

        refreshEvents();
        setInterval(refreshEvents, 10000);
    