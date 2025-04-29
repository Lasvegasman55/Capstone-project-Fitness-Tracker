// screens/DashboardScreen.js
import React from 'react';
import { View, Text, StyleSheet, ScrollView, TouchableOpacity } from 'react-native';
import { Ionicons } from '@expo/vector-icons';

const DashboardScreen = () => {
  return (
    <ScrollView style={styles.container}>
      <View style={styles.header}>
        <Text style={styles.headerText}>Dashboard</Text>
      </View>
      
      {/* Today's Stats Section */}
      <View style={styles.card}>
        <Text style={styles.cardTitle}>Today's Stats</Text>
        <View style={styles.statRow}>
          <Ionicons name="flame-outline" size={20} color="#333" />
          <Text style={styles.statLabel}>Calories</Text>
          <Text style={styles.statValue}>0 kcal</Text>
        </View>
        <View style={styles.statRow}>
          <Ionicons name="water-outline" size={20} color="#333" />
          <Text style={styles.statLabel}>Water</Text>
          <Text style={styles.statValue}>0 ml</Text>
        </View>
        <View style={styles.statRow}>
          <Ionicons name="barbell-outline" size={20} color="#333" />
          <Text style={styles.statLabel}>This week's workouts</Text>
          <Text style={styles.statValue}>0</Text>
        </View>
        <View style={styles.buttonRow}>
          <TouchableOpacity style={styles.button}>
            <Text style={styles.buttonText}>Log Food</Text>
          </TouchableOpacity>
          <TouchableOpacity style={styles.button}>
            <Text style={styles.buttonText}>Log Water</Text>
          </TouchableOpacity>
          <TouchableOpacity style={styles.button}>
            <Text style={styles.buttonText}>Log Workout</Text>
          </TouchableOpacity>
        </View>
      </View>
      
      {/* Recent Workouts Section */}
      <View style={[styles.card, styles.greenCard]}>
        <Text style={styles.cardTitle}>Recent Workouts</Text>
        <Text style={styles.emptyState}>No workouts recorded yet.</Text>
        <TouchableOpacity style={styles.viewAllButton}>
          <Text style={styles.viewAllButtonText}>View All Workouts</Text>
        </TouchableOpacity>
      </View>
      
      {/* Active Goals Section */}
      <View style={[styles.card, styles.yellowCard]}>
        <Text style={styles.cardTitle}>Active Goals</Text>
        <Text style={styles.emptyState}>No active goals found.</Text>
        <TouchableOpacity style={styles.viewAllButton}>
          <Text style={styles.viewAllButtonText}>View All Goals</Text>
        </TouchableOpacity>
      </View>
      
      {/* Body Measurements Section */}
      <View style={[styles.card, styles.blueCard]}>
        <Text style={styles.cardTitle}>Body Measurements</Text>
        <Text style={styles.emptyState}>No measurements recorded yet.</Text>
        <TouchableOpacity style={styles.recordButton}>
          <Text style={styles.buttonText}>Record Measurements</Text>
        </TouchableOpacity>
      </View>
    </ScrollView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f5f5f5',
  },
  header: {
    padding: 15,
    backgroundColor: '#4CAF50',
  },
  headerText: {
    fontSize: 24,
    color: 'white',
    fontWeight: 'bold',
  },
  card: {
    backgroundColor: 'white',
    borderRadius: 10,
    padding: 15,
    margin: 10,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 2,
  },
  greenCard: {
    borderLeftWidth: 5,
    borderLeftColor: '#4CAF50',
  },
  yellowCard: {
    borderLeftWidth: 5,
    borderLeftColor: '#FFC107',
  },
  blueCard: {
    borderLeftWidth: 5,
    borderLeftColor: '#03A9F4',
  },
  cardTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    marginBottom: 15,
  },
  statRow: {
    flexDirection: 'row',
    alignItems: 'center',
    paddingVertical: 8,
    borderBottomWidth: 1,
    borderBottomColor: '#f0f0f0',
  },
  statLabel: {
    flex: 1,
    marginLeft: 10,
    fontSize: 16,
  },
  statValue: {
    fontSize: 16,
    fontWeight: 'bold',
  },
  buttonRow: {
    flexDirection: 'row',
    justifyContent: 'space-around',
    marginTop: 15,
  },
  button: {
    backgroundColor: '#e0e0e0',
    paddingVertical: 8,
    paddingHorizontal: 12,
    borderRadius: 5,
  },
  buttonText: {
    fontSize: 14,
    color: '#333',
  },
  emptyState: {
    color: '#666',
    fontStyle: 'italic',
    marginBottom: 15,
  },
  viewAllButton: {
    alignSelf: 'center',
    paddingVertical: 8,
    paddingHorizontal: 15,
    borderWidth: 1,
    borderColor: '#ddd',
    borderRadius: 5,
  },
  viewAllButtonText: {
    color: '#666',
    fontSize: 14,
  },
  recordButton: {
    alignSelf: 'center',
    backgroundColor: '#e0e0e0',
    paddingVertical: 8,
    paddingHorizontal: 15,
    borderRadius: 5,
  },
});

export default DashboardScreen;