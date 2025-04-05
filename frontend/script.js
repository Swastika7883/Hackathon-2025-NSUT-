// Doctor data - would come from backend in real app
const doctorsByDepartment = {
    cardiology: [
        { id: 'card1', name: 'Dr. Sarah Johnson' },
        { id: 'card2', name: 'Dr. Michael Chen' }
    ],
    neurology: [
        { id: 'neuro1', name: 'Dr. Robert Williams' },
        { id: 'neuro2', name: 'Dr. Emily Davis' }
    ],
    orthopedics: [
        { id: 'ortho1', name: 'Dr. James Wilson' },
        { id: 'ortho2', name: 'Dr. Lisa Martinez' }
    ],
    general: [
        { id: 'gen1', name: 'Dr. David Thompson' },
        { id: 'gen2', name: 'Dr. Patricia Brown' }
    ]
};

// DOM Elements
const recordButton = document.getElementById('recordButton');
const statusIndicator = document.getElementById('statusIndicator');
const statusText = document.getElementById('statusText');
const transcriptContainer = document.getElementById('transcriptContainer');
const transcript = document.getElementById('transcript');
const sendButton = document.getElementById('sendButton');
const cancelButton = document.getElementById('cancelButton');
const confirmation = document.getElementById('confirmation');
const newRequestButton = document.getElementById('newRequestButton');
const departmentSelect = document.getElementById('department');
const doctorSelect = document.getElementById('doctor');

// State variables
let mediaRecorder;
let audioChunks = [];
let isRecording = false;
let recordedAudio = null;

// Update doctors dropdown based on department selection
function updateDoctors() {
    const department = departmentSelect.value;
    doctorSelect.innerHTML = '';
    
    if (!department) {
        doctorSelect.disabled = true;
        doctorSelect.innerHTML = '<option value="">Select Department First</option>';
        return;
    }
    
    doctorSelect.disabled = false;
    doctorSelect.innerHTML = '<option value="">Select Doctor</option>';
    
    doctorsByDepartment[department].forEach(doctor => {
        const option = document.createElement('option');
        option.value = doctor.id;
        option.textContent = doctor.name;
        doctorSelect.appendChild(option);
    });
}

// Start recording
async function startRecording() {
    try {
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
        mediaRecorder = new MediaRecorder(stream);
        audioChunks = [];
        
        mediaRecorder.ondataavailable = event => {
            audioChunks.push(event.data);
        };
        
        mediaRecorder.onstop = () => {
            recordedAudio = new Blob(audioChunks, { type: 'audio/wav' });
            simulateTranscription(); // In real app, this would call your backend
        };
        
        mediaRecorder.start();
        isRecording = true;
        updateRecordingUI();
    } catch (error) {
        console.error('Error accessing microphone:', error);
        statusText.textContent = "Microphone access denied";
    }
}

// Stop recording
function stopRecording() {
    if (mediaRecorder && isRecording) {
        mediaRecorder.stop();
        isRecording = false;
        updateRecordingUI();
        
        // Stop all tracks in the stream
        mediaRecorder.stream.getTracks().forEach(track => track.stop());
    }
}

// Update UI during recording
function updateRecordingUI() {
    if (isRecording) {
        recordButton.classList.add('recording');
        statusIndicator.classList.add('recording');
        statusText.textContent = "Recording... Speak now";
    } else {
        recordButton.classList.remove('recording');
        statusIndicator.classList.remove('recording');
        statusText.textContent = "Recording stopped";
    }
}

// Simulate transcription - in real app this would call your backend
function simulateTranscription() {
    statusText.textContent = "Processing your message...";
    
    // Simulate API delay
    setTimeout(() => {
        // This is a simulated transcription - real app would use actual speech recognition
        const sampleResponses = [
            "I'm feeling severe chest pain and difficulty breathing.",
            "My headache has gotten worse and I'm feeling dizzy.",
            "I think I have a fever and my joints are aching.",
            "The pain in my abdomen hasn't improved since yesterday."
        ];
        
        const randomResponse = sampleResponses[Math.floor(Math.random() * sampleResponses.length)];
        transcript.textContent = randomResponse;
        transcriptContainer.classList.remove('hidden');
        sendButton.disabled = false;
        statusText.textContent = "Message ready to send";
    }, 2000);
}

// Send message to doctor
function sendMessage() {
    const patientName = document.getElementById('patient-name').value;
    const patientAge = document.getElementById('patient-age').value;
    const roomNumber = document.getElementById('room-number').value;
    const doctorId = doctorSelect.value;
    
    if (!patientName || !patientAge || !roomNumber || !doctorId) {
        alert('Please fill in all patient information and select a doctor');
        return;
    }
    
    // In real app, this would send to your backend
    console.log('Sending message to doctor:', {
        patientName,
        patientAge,
        roomNumber,
        doctorId,
        message: transcript.textContent
    });
    
    // Show confirmation
    transcriptContainer.classList.add('hidden');
    confirmation.classList.remove('hidden');
}

// Reset form for new request
function resetForm() {
    transcript.textContent = '';
    transcriptContainer.classList.add('hidden');
    confirmation.classList.add('hidden');
    statusText.textContent = "Ready to record";
}

// Event Listeners
recordButton.addEventListener('mousedown', startRecording);
recordButton.addEventListener('mouseup', stopRecording);
recordButton.addEventListener('mouseleave', stopRecording); // In case mouse leaves button while recording

sendButton.addEventListener('click', sendMessage);
cancelButton.addEventListener('click', resetForm);
newRequestButton.addEventListener('click', resetForm);

// Prevent right-click on record button (can interfere with hold-to-record)
recordButton.addEventListener('contextmenu', (e) => {
    e.preventDefault();
});

// Initialize department/doctor selection
departmentSelect.addEventListener('change', updateDoctors);