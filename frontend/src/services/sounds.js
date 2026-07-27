let audioCtx = null;
let isEnabled = false;

function initAudio() {
  if (!audioCtx) {
    audioCtx = new (window.AudioContext || window.webkitAudioContext)();
  }
}

export function toggleSound() {
  isEnabled = !isEnabled;
  if (isEnabled) {
    initAudio();
    if (audioCtx.state === 'suspended') {
      audioCtx.resume();
    }
  }
  return isEnabled;
}

export function setSoundEnabled(val) {
  isEnabled = val;
  if (isEnabled) {
    initAudio();
    if (audioCtx.state === 'suspended') {
      audioCtx.resume();
    }
  }
}

export function isSoundEnabled() {
  return isEnabled;
}

// Hover: Soft tiny tick
export function playHover() {
  if (!isEnabled) return;
  initAudio();
  if (audioCtx.state === 'suspended') audioCtx.resume();

  const osc = audioCtx.createOscillator();
  const gain = audioCtx.createGain();
  
  osc.type = 'sine';
  osc.frequency.setValueAtTime(600, audioCtx.currentTime);
  
  gain.gain.setValueAtTime(0.015, audioCtx.currentTime);
  gain.gain.exponentialRampToValueAtTime(0.0001, audioCtx.currentTime + 0.05);
  
  osc.connect(gain);
  gain.connect(audioCtx.destination);
  
  osc.start();
  osc.stop(audioCtx.currentTime + 0.05);
}

// Click: slightly louder soft pop
export function playClick() {
  if (!isEnabled) return;
  initAudio();
  if (audioCtx.state === 'suspended') audioCtx.resume();

  const osc = audioCtx.createOscillator();
  const gain = audioCtx.createGain();
  
  osc.type = 'triangle';
  osc.frequency.setValueAtTime(400, audioCtx.currentTime);
  osc.frequency.exponentialRampToValueAtTime(100, audioCtx.currentTime + 0.1);
  
  gain.gain.setValueAtTime(0.04, audioCtx.currentTime);
  gain.gain.exponentialRampToValueAtTime(0.0001, audioCtx.currentTime + 0.1);
  
  osc.connect(gain);
  gain.connect(audioCtx.destination);
  
  osc.start();
  osc.stop(audioCtx.currentTime + 0.1);
}
