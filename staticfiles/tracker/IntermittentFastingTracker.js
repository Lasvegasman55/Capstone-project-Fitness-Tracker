// IntermittentFastingTracker.js
import React, { useState, useEffect } from 'react';

const FASTING_PROTOCOLS = [
  { id: '16-8', name: '16:8 (Leangains)', fastHours: 16, eatHours: 8 },
  { id: '18-6', name: '18:6', fastHours: 18, eatHours: 6 },
  { id: '20-4', name: '20:4 (Warrior Diet)', fastHours: 20, eatHours: 4 },
  { id: '5-2', name: '5:2 (5 normal days, 2 fasting days)', type: 'weekly' },
  { id: 'custom', name: 'Custom', fastHours: 0, eatHours: 0 },
];

const IntermittentFastingTracker = () => {
  // State management
  const [selectedProtocol, setSelectedProtocol] = useState(FASTING_PROTOCOLS[0]);
  const [customFastHours, setCustomFastHours] = useState(16);
  const [customEatHours, setCustomEatHours] = useState(8);
  const [isFasting, setIsFasting] = useState(false);
  const [fastingStartTime, setFastingStartTime] = useState(null);
  const [fastingEndTime, setFastingEndTime] = useState(null);
  const [currentTime, setCurrentTime] = useState(new Date());
  const [fastingLogs, setFastingLogs] = useState([]);
  const [fastingStreak, setFastingStreak] = useState(0);
  const [notes, setNotes] = useState('');

  // Load data from local storage on component mount
  useEffect(() => {
    const savedProtocol = localStorage.getItem('selectedProtocol');
    const savedCustomFastHours = localStorage.getItem('customFastHours');
    const savedCustomEatHours = localStorage.getItem('customEatHours');
    const savedFastingStartTime = localStorage.getItem('fastingStartTime');
    const savedFastingEndTime = localStorage.getItem('fastingEndTime');
    const savedIsFasting = localStorage.getItem('isFasting');
    const savedFastingLogs = localStorage.getItem('fastingLogs');
    const savedFastingStreak = localStorage.getItem('fastingStreak');
    
    if (savedProtocol) {
      const protocol = FASTING_PROTOCOLS.find(p => p.id === savedProtocol);
      if (protocol) setSelectedProtocol(protocol);
    }
    
    if (savedCustomFastHours) setCustomFastHours(parseInt(savedCustomFastHours));
    if (savedCustomEatHours) setCustomEatHours(parseInt(savedCustomEatHours));
    if (savedFastingStartTime) setFastingStartTime(new Date(parseInt(savedFastingStartTime)));
    if (savedFastingEndTime) setFastingEndTime(new Date(parseInt(savedFastingEndTime)));
    if (savedIsFasting) setIsFasting(savedIsFasting === 'true');
    if (savedFastingLogs) setFastingLogs(JSON.parse(savedFastingLogs));
    if (savedFastingStreak) setFastingStreak(parseInt(savedFastingStreak));
  }, []);

  // Save data to local storage when state changes
  useEffect(() => {
    localStorage.setItem('selectedProtocol', selectedProtocol.id);
    localStorage.setItem('customFastHours', customFastHours.toString());
    localStorage.setItem('customEatHours', customEatHours.toString());
    localStorage.setItem('isFasting', isFasting.toString());
    
    if (fastingStartTime) {
      localStorage.setItem('fastingStartTime', fastingStartTime.getTime().toString());
    }
    
    if (fastingEndTime) {
      localStorage.setItem('fastingEndTime', fastingEndTime.getTime().toString());
    }
    
    localStorage.setItem('fastingLogs', JSON.stringify(fastingLogs));
    localStorage.setItem('fastingStreak', fastingStreak.toString());
  }, [
    selectedProtocol,
    customFastHours,
    customEatHours,
    isFasting,
    fastingStartTime,
    fastingEndTime,
    fastingLogs,
    fastingStreak
  ]);

  // Update current time every minute
  useEffect(() => {
    const timer = setInterval(() => {
      setCurrentTime(new Date());
    }, 60000);
    
    return () => clearInterval(timer);
  }, []);

  // Calculate fasting progress
  const calculateFastingProgress = () => {
    if (!isFasting || !fastingStartTime) return 0;
    
    const elapsedMs = currentTime.getTime() - fastingStartTime.getTime();
    const elapsedHours = elapsedMs / (1000 * 60 * 60);
    
    const targetHours = 
      selectedProtocol.id === 'custom' ? customFastHours : selectedProtocol.fastHours;
    
    return Math.min(100, (elapsedHours / targetHours) * 100);
  };

  // Calculate time remaining in fast
  const calculateTimeRemaining = () => {
    if (!isFasting || !fastingStartTime) return '0:00';
    
    const targetHours = 
      selectedProtocol.id === 'custom' ? customFastHours : selectedProtocol.fastHours;
    
    const targetMs = targetHours * 60 * 60 * 1000;
    const endTime = new Date(fastingStartTime.getTime() + targetMs);
    const remainingMs = endTime.getTime() - currentTime.getTime();
    
    if (remainingMs <= 0) return '0:00';
    
    const remainingHours = Math.floor(remainingMs / (1000 * 60 * 60));
    const remainingMinutes = Math.floor((remainingMs % (1000 * 60 * 60)) / (1000 * 60));
    
    return `${remainingHours}:${remainingMinutes.toString().padStart(2, '0')}`;
  };

  // Start fasting period
  const startFasting = () => {
    const startTime = new Date();
    setFastingStartTime(startTime);
    
    const targetHours = 
      selectedProtocol.id === 'custom' ? customFastHours : selectedProtocol.fastHours;
    
    const endTime = new Date(startTime.getTime() + targetHours * 60 * 60 * 1000);
    setFastingEndTime(endTime);
    setIsFasting(true);
  };

  // End fasting period
  const endFasting = (completed = true) => {
    if (completed) {
      const newLog = {
        id: Date.now(),
        protocol: selectedProtocol.id,
        startTime: fastingStartTime,
        endTime: currentTime,
        duration: (currentTime.getTime() - fastingStartTime.getTime()) / (1000 * 60 * 60),
        completed: true,
        notes: notes
      };
      
      setFastingLogs([newLog, ...fastingLogs]);
      setFastingStreak(fastingStreak + 1);
    } else {
      const newLog = {
        id: Date.now(),
        protocol: selectedProtocol.id,
        startTime: fastingStartTime,
        endTime: currentTime,
        duration: (currentTime.getTime() - fastingStartTime.getTime()) / (1000 * 60 * 60),
        completed: false,
        notes: notes
      };
      
      setFastingLogs([newLog, ...fastingLogs]);
      setFastingStreak(0);
    }
    
    setIsFasting(false);
    setFastingStartTime(null);
    setFastingEndTime(null);
    setNotes('');
  };

  // Handle protocol selection
  const handleProtocolChange = (e) => {
    const selected = FASTING_PROTOCOLS.find(p => p.id === e.target.value);
    setSelectedProtocol(selected);
  };

  return (
    <div className="intermittent-fasting-tracker">
      <h2>Intermittent Fasting Tracker</h2>
      
      {/* Protocol Selection */}
      <div className="protocol-selection">
        <h3>Select Fasting Protocol</h3>
        <select 
          value={selectedProtocol.id} 
          onChange={handleProtocolChange}
          disabled={isFasting}
        >
          {FASTING_PROTOCOLS.map(protocol => (
            <option key={protocol.id} value={protocol.id}>
              {protocol.name}
            </option>
          ))}
        </select>
        
        {selectedProtocol.id === 'custom' && (
          <div className="custom-protocol">
            <div>
              <label>Fast Hours:</label>
              <input 
                type="number" 
                min="1" 
                max="23" 
                value={customFastHours}
                onChange={(e) => setCustomFastHours(parseInt(e.target.value))}
                disabled={isFasting}
              />
            </div>
            <div>
              <label>Eating Window Hours:</label>
              <input 
                type="number" 
                min="1" 
                max="23" 
                value={customEatHours}
                onChange={(e) => setCustomEatHours(parseInt(e.target.value))}
                disabled={isFasting}
              />
            </div>
          </div>
        )}
      </div>
      
      {/* Current Fast Status */}
      <div className="fasting-status">
        <h3>Current Status</h3>
        {isFasting ? (
          <>
            <p><strong>Status:</strong> Fasting in progress</p>
            <p><strong>Started:</strong> {fastingStartTime.toLocaleString()}</p>
            <p><strong>Target End:</strong> {fastingEndTime.toLocaleString()}</p>
            <p><strong>Time Remaining:</strong> {calculateTimeRemaining()}</p>
            
            <div className="progress-bar">
              <div 
                className="progress" 
                style={{ width: `${calculateFastingProgress()}%` }}
              ></div>
            </div>
            <p>{Math.round(calculateFastingProgress())}% complete</p>
            
            <div className="fasting-notes">
              <h4>Notes (optional)</h4>
              <textarea
                value={notes}
                onChange={(e) => setNotes(e.target.value)}
                placeholder="How are you feeling? Any observations?"
              />
            </div>
            
            <div className="action-buttons">
              <button onClick={() => endFasting(true)}>Complete Fast</button>
              <button onClick={() => endFasting(false)}>End Fast Early</button>
            </div>
          </>
        ) : (
          <>
            <p><strong>Status:</strong> Not currently fasting</p>
            <p><strong>Current Streak:</strong> {fastingStreak} successful fasts</p>
            <button onClick={startFasting}>Start Fasting</button>
          </>
        )}
      </div>
      
      {/* Fasting History Log */}
      <div className="fasting-history">
        <h3>Fasting History</h3>
        {fastingLogs.length === 0 ? (
          <p>No fasting sessions recorded yet.</p>
        ) : (
          <div className="fasting-logs">
            {fastingLogs.slice(0, 5).map(log => (
              <div key={log.id} className={`log-entry ${log.completed ? 'completed' : 'incomplete'}`}>
                <div className="log-date">
                  {new Date(log.startTime).toLocaleDateString()}
                </div>
                <div className="log-protocol">
                  {FASTING_PROTOCOLS.find(p => p.id === log.protocol)?.name || log.protocol}
                </div>
                <div className="log-duration">
                  {log.duration.toFixed(1)} hours
                </div>
                <div className="log-status">
                  {log.completed ? 'Completed' : 'Incomplete'}
                </div>
                {log.notes && <div className="log-notes">{log.notes}</div>}
              </div>
            ))}
            {fastingLogs.length > 5 && (
              <p className="view-more">+ {fastingLogs.length - 5} more sessions</p>
            )}
          </div>
        )}
      </div>
    </div>
  );
};

export default IntermittentFastingTracker;