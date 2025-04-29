// App.js - Simplified version with proper syntax
import React from 'react';
import { NavigationContainer } from '@react-navigation/native';
import { createBottomTabNavigator } from '@react-navigation/bottom-tabs';
import { View, Text, StyleSheet } from 'react-native';
import { Ionicons } from '@expo/vector-icons';

// Simple placeholder components
const DashboardScreen = () => (
  <View style={styles.screen}>
    <Text style={styles.title}>Dashboard</Text>
  </View>
);

const WorkoutsScreen = () => (
  <View style={styles.screen}>
    <Text style={styles.title}>Workouts</Text>
  </View>
);

const NutritionScreen = () => (
  <View style={styles.screen}>
    <Text style={styles.title}>Nutrition</Text>
  </View>
);

const FastingScreen = () => (
  <View style={styles.screen}>
    <Text style={styles.title}>Fasting</Text>
  </View>
);

const ProfileScreen = () => (
  <View style={styles.screen}>
    <Text style={styles.title}>Profile</Text>
  </View>
);

const Tab = createBottomTabNavigator();

export default function App() {
  return (
    <NavigationContainer>
      <Tab.Navigator
        screenOptions={({ route }) => ({
          tabBarIcon: ({ focused, color, size }) => {
            let iconName;

            if (route.name === 'Dashboard') {
              iconName = focused ? 'home' : 'home-outline';
            } else if (route.name === 'Workouts') {
              iconName = focused ? 'fitness' : 'fitness-outline';
            } else if (route.name === 'Nutrition') {
              iconName = focused ? 'restaurant' : 'restaurant-outline';
            } else if (route.name === 'Fasting') {
              iconName = focused ? 'timer' : 'timer-outline';
            } else if (route.name === 'Profile') {
              iconName = focused ? 'person' : 'person-outline';
            }

            return <Ionicons name={iconName} size={size} color={color} />;
          },
          tabBarActiveTintColor: '#4CAF50',
          tabBarInactiveTintColor: 'gray',
          headerStyle: {
            backgroundColor: '#4CAF50',
          },
          headerTintColor: '#fff',
        })}
      >
        <Tab.Screen name="Dashboard" component={DashboardScreen} />
        <Tab.Screen name="Workouts" component={WorkoutsScreen} />
        <Tab.Screen name="Nutrition" component={NutritionScreen} />
        <Tab.Screen name="Fasting" component={FastingScreen} />
        <Tab.Screen name="Profile" component={ProfileScreen} />
      </Tab.Navigator>
    </NavigationContainer>
  );
}

const styles = StyleSheet.create({
  screen: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: '#f5f5f5',
  },
  title: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#4CAF50',
  }
});