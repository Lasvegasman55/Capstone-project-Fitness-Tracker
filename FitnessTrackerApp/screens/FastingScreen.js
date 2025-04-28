// screens/FastingScreen.js
import React, { useState } from 'react';
import { View, Text, StyleSheet, TouchableOpacity } from 'react-native';
import { Ionicons } from '@expo/vector-icons';

const FastingScreen = () => {
  const [isFasting, setIsFasting] = useState(false);
  const [progress, setProgress] = useState(0);
  
  // This would be replaced with actual API calls in a real app
  const toggleFasting = () => {
    setIsFasting(!isFasting);
    setProgress(0);
  };
  
  return (
    <View style={styles.container}>
      <View style={styles.card}>
        <Text style={styles.cardTitle}>Intermittent Fasting</Text>
        
        {isFasting ? (
          <>
            <View style={styles.statusContainer}>
              <Text style={styles.statusText}>Fasting in progress</Text>
              <Text style={styles.protocolText}>16:8 Protocol</Text>
            </View>
            
            <View style={styles.progressContainer}>
              <View style={styles.progressBar}>
                <View style={[styles.progressFill, { width: `${progress}%` }]} />
              </View>
              <Text style={styles.progressText}>{progress}% Complete</Text>
            </View>
            
            <TouchableOpacity style={styles.button} onPress={toggleFasting}>
              <Text style={styles.buttonText}>End Fast</Text>
            </TouchableOpacity>
          </>
        ) : (
          <>
            <View style={styles.statusContainer}>
              <Text style={styles.statusText}>Not currently fasting</Text>
              <Text style={styles.infoText}>
                Start a new fasting session to track your progress
              </Text>
            </View>
            
            <TouchableOpacity style={styles.button} onPress={toggleFasting}>
              <Text style={styles.buttonText}>Start Fasting</Text>
            </TouchableOpacity>
          </>
        )}
      </View>
      
      <View style={styles.card}>
        <Text style={styles.cardTitle}>Fasting History</Text>
        <View style={styles.emptyHistory}>
          <Ionicons name="time-outline" size={48} color="#ccc" />
          <Text style={styles.emptyText}>No fasting sessions yet</Text>
        </View>
      </View>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f5f5f5',
    padding: 10,
  },
  card: {
    backgroundColor: 'white',
    borderRadius: 10,
    padding: 15,
    marginBottom: 15,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 2,
  },
  cardTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    marginBottom: 15,
  },
  statusContainer: {
    alignItems: 'center',
    marginBottom: 20,
  },
  statusText: {
    fontSize: 16,
    fontWeight: 'bold',
    marginBottom: 5,
  },
  protocolText: {
    fontSize: 14,
    color: '#666',
  },
  infoText: {
    fontSize: 14,
    color: '#666',
    textAlign: 'center',
  },
  progressContainer: {
    marginBottom: 20,
  },
  progressBar: {
    height: 20,
    backgroundColor: '#e0e0e0',
    borderRadius: 10,
    overflow: 'hidden',
    marginBottom: 5,
  },
  progressFill: {
    height: '100%',
    backgroundColor: '#4CAF50',
  },
  progressText: {
    textAlign: 'center',
    color: '#666',
  },
  button: {
    backgroundColor: '#4CAF50',
    borderRadius: 8,
    padding: 15,
    alignItems: 'center',
  },
  buttonText: {
    color: 'white',
    fontSize: 16,
    fontWeight: 'bold',
  },
  emptyHistory: {
    alignItems: 'center',
    padding: 20,
  },
  emptyText: {
    fontSize: 16,
    color: '#666',
    marginTop: 10,
  },
});

export default FastingScreen;