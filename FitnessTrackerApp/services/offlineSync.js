// services/offlineSync.js
import AsyncStorage from '@react-native-async-storage/async-storage';
import NetInfo from '@react-native-community/netinfo';

export const saveDataOffline = async (key, data) => {
  try {
    await AsyncStorage.setItem(key, JSON.stringify(data));
    return true;
  } catch (error) {
    console.error(`Error saving ${key}:`, error);
    return false;
  }
};

export const syncOfflineData = async () => {
  const isConnected = (await NetInfo.fetch()).isConnected;
  
  if (!isConnected) {
    console.log('No internet connection, sync skipped');
    return false;
  }
  
  // Example: sync workout data
  try {
    const offlineWorkouts = await AsyncStorage.getItem('offlineWorkouts');
    if (offlineWorkouts) {
      const workouts = JSON.parse(offlineWorkouts);
      // Send to server with your API service
      // ...
      // Clear offline data after successful sync
      await AsyncStorage.removeItem('offlineWorkouts');
    }
    return true;
  } catch (error) {
    console.error('Sync error:', error);
    return false;
  }
};